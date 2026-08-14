# Environment Variables Are Scrubbed in Shiny Server

## The Issue

**Symptom:** After deploying the LeafViz Shiny app into a Docker container, the
**dataset dropdown menu was empty**, even though an environment variable pointing
at the correct manifest had been set in the `Dockerfile`:

```dockerfile
ENV LEAFVIZ_MANIFEST=/srv/shiny-server/apps/leafviz/config/manifest.prod.json
```

**When it triggered:** On every launch of the app under Shiny Server (i.e. served
from `/srv/shiny-server/...`). It did **not** trigger when running the app
directly from the CLI (e.g. `Rscript run_leafviz.R`), because that path does not
go through Shiny Server's process spawning.

**What the logs showed** (`/var/log/shiny-server/`):

```
su: ignoring --preserve-environment, it's mutually exclusive with --login
...
Manifest entry 'Example Dataset A' path does not exist:
  /srv/shiny-server/apps/leafviz/config/../example/dataset_a_results.Rdata
```

## Why It Happened

There were two cooperating causes:

### 1. Shiny Server scrubs the environment when spawning R workers

Shiny Server does not run the R worker in the same environment as the container.
It re-executes R as the `shiny` user using a `su` call that combines two
mutually-exclusive flags:

```
su shiny --login --preserve-environment -c "... R ..."
```

- `--login` (`-l`) starts a **login shell**, which **resets** the environment to
  a small whitelist (`HOME`, `PATH`, `USER`, `TERM`, ...) and sources
  `/etc/profile` and `~/.profile`.
- `--preserve-environment` (`-p`) asks to **keep** the current environment.

`su` cannot honor both, so it prints the warning and keeps `--login`:

```
su: ignoring --preserve-environment, it's mutually exclusive with --login
```

The login shell wins, so any variable set via `ENV` in the `Dockerfile`
(including `LEAFVIZ_MANIFEST`) is **wiped before R starts**. This warning is
emitted by Shiny Server itself, not by the app, and cannot be suppressed without
patching and rebuilding Shiny Server — which is not worth it.

### 2. The app silently fell back, then failed on a missing file

With `LEAFVIZ_MANIFEST` unset, the app's manifest-path resolver fell back to its
default of `<app-dir>/config/manifest.json`. That default manifest listed a
demo/example dataset with a relative path:

```json
{ "label": "Example Dataset A", "path": "../example/dataset_a_results.Rdata" }
```

The `example/` directory was **not copied into the container image**, so the file
genuinely did not exist. The manifest reader is all-or-nothing: a single missing
file makes it error out, the app catches the error and treats the manifest as
empty, and therefore the dropdown is left with no choices — the observed symptom.

## The Solution

Use Shiny Server's intended extension point: because the login shell sources
`~/.profile`, set the variable there for the `shiny` user. This is the same
mechanism already used for `PATH` and other custom variables.

```dockerfile
RUN printf "\nexport LEAFVIZ_MANIFEST=/srv/shiny-server/apps/leafviz/config/manifest.prod.json\n" \
    >> /home/shiny/.profile
```

### Alternative: `.Renviron` (R-only, more targeted)

R reads `~/.Renviron` on startup, after the shell environment. It is
purpose-built for this and is scoped to R only (no shell `export`, no `$`
expansion — plain `KEY=value` lines):

```dockerfile
RUN printf 'LEAFVIZ_MANIFEST=/srv/shiny-server/apps/leafviz/config/manifest.prod.json\n' \
    >> /home/shiny/.Renviron
```

### Notes

- The `su: ignoring --preserve-environment ...` warning is **expected and
  harmless**. Do not try to keep `--preserve-environment`; the flags come from
  Shiny Server and `--login` is what sources `~/.profile` in the first place.
- Setting the variable with `ENV` in the `Dockerfile` alone is **not enough** for
  processes that Shiny Server spawns via a login shell.
- Independently, make sure any file referenced by the active manifest actually
  exists in the image (e.g. copy the `example/` directory, or point the manifest
  only at datasets that are present).
