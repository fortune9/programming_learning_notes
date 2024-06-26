nf-core tools
================
Zhenguo Zhang
25 June, 2024

-   [Configuration](#configuration)
    -   [config file .nf-core.yml](#config-file-nf-coreyml)
    -   [Other configurations](#other-configurations)
-   [Modules](#modules)
    -   [List modules](#list-modules)
    -   [Show info of a module](#show-info-of-a-module)
    -   [Install a module](#install-a-module)
    -   [Update a module](#update-a-module)
    -   [Patch a module](#patch-a-module)
    -   [Lint modules](#lint-modules)
    -   [Create a module](#create-a-module)
    -   [Bump software versions](#bump-software-versions)
-   [Workflows](#workflows)
-   [Pipelines](#pipelines)
    -   [Create a pipeline](#create-a-pipeline)
    -   [Launch a pipeline](#launch-a-pipeline)
    -   [Bump versions](#bump-versions)
    -   [Schema](#schema)
-   [Private repositories](#private-repositories)
-   [Lint](#lint)

[nf-core tools](https://nf-co.re/docs/nf-core-tools) is a set of tools
written in python for managing nextflow modules, workflows and
pipelines. With it, the writing and updating nextflow modules/workflows
are simplified. In this document, we are going to summarize some key
features of the tools.

## Configuration

### config file .nf-core.yml

There is a config file .nf-core.yml in nf-core pipeline or
modules/workflow repository, which guides the behaviors of nf-core
tools. For example, when it is a pipeline repo, `nf-core modules create`
will create a local module instead of a shared/remote module.

Here are some common settings in the .nf-core.yml file:

-   repository type

    -   set `repository_type` modules or pipeline, and the latter is for
        a pipeline repo.

-   organization path

    -   org\_path: in a modules repo, set this to value, say ‘my\_org’,
        then it will create a subfolder ‘my\_org’ in the folders
        ‘modules’ and ‘subworkflows’, and all new modules/subworkflows
        will be created under these new folders.

-   Ignore a file in linting

    ``` yaml
    repository_type: pipeline
    lint:
        files_unchanged:
            - file_to_ignore
    ```

### Other configurations

-   modules and subworkflows from the nf-core repository are tracked
    using hashes in the modules.json file. This file is updated when a
    module/subworkflow is installed or updated. It is organized in the
    hierarchy git repo -&gt; modules or subworkflows -&gt; individual
    module/subworkflow.

-   Each nf-core module also has a meta.yml file which describes the
    inputs and outputs. This meta file is rendered on the nf-core
    website, or can be viewed using the `nf-core modules info` command.
    One can find the allowed entries in the schema file at
    <https://raw.githubusercontent.com/nf-core/modules/master/modules/meta-schema.json>

-   If you have added parameters and they have not been documented in
    the nextflow\_schema.json file then pipeline tests will fail during
    linting. The nf-core schema build command is designed to support
    developers write, check, validate, and propose additions to your
    nextflow\_schema.json file. It will enable you to launch a web
    builder to edit this file in your web browser rather than trying to
    edit this file manually.

-   The nf-core modules patch command allows you keep using the nf-core
    component without needing to make it into a local module for tests
    to pass. Instead, nf-core modules patch command creates a diff file
    that will keep track of the changes you made. If you subsequently
    update the module using the nf-core tooling, the diff file will be
    retained.

-   To set the minimum version of nextflow for a pipeline, run like

        nf-core bump-version 23.10.0 --nextflow

-   To update templates, run the following

        nf-core sync # update TEMPLATE branch
        git merge TEMPLATE # update current branch

## Modules

### List modules

To list remote modules,

    nf-core modules list remote

To list installed modules in a pipeline

    nf-core modules list local

### Show info of a module

    nf-core modules info <module-name>

### Install a module

``` bash
nf-core modules install <module-name>
```

To install a module from a private repo (instead of nf-core) and a
certain branch, use

``` bash
nf-core modules --git-remote <my-git-repo> --branch <target-branch> install <module-name>
```

Note that a custom remote must follow a similar directory structure to
that of nf-core/modules for the nf-core commands to work properly.

In order to browse private repositories you have to configure the GitHub
CLI auth and provide your credentials with the command below.

``` bash
gh auth login
```

One can use `org_path: install-folder` in *.nf-core.yml* to change where
to install modules.

### Update a module

    nf-core modules update <module-name> 

To skip updating a module or wants to update to a specific version, set
the following in the file *.nf-core.yml*:

    update:
      https://github.com/nf-core/modules.git:
        nf-core:
          star/align: False
          agat/spstatistics: "bc6c61dadb7967b613d46fe6316aacbafbbf1c35"

### Patch a module

If one modifies an installed nf-core module, and the linting process
will fail because it doesn’t match the version at nf-core. To resolve
this issue, one can patch a module locally, which will generate a `diff`
file and its path is added to modules.json

    nf-core modules patch <module-name>

### Lint modules

To lint all modules,

    nf-core modules lint --all

To also lint local modules,

    nf-core modules lint --all --local

To lint modules in a different directory:

    nf-core modules lint --dir path/to/modules

### Create a module

    nf-core modules create

This will prompt questions and create a module in the local folder
`modules/local` in a pipeline folder.

If the repository type is *modules*, this command will however create a
module in `modules/nf-core`. So the effect of this command depends on
the repository type.

If you run this command in a folder without .nf-core.yml file, it will
ask you multiple questions to set proper variables such as
repository\_type, org\_path, etc.

### Bump software versions

To bump bioconda and container versions of certain modules, you can use:

    nf-core modules bump-versions

This will bump the bioconda version of a single or all modules to the
latest version and also fetch the correct Docker and Singularity
container tags.

## Workflows

-   Create a subworkflow

        nf-core subworkflows create

This command can be used both when writing a subworkflow for the shared
nf-core/modules repository, and also when creating local subworkflows
for a pipeline.

Which type of repository you are working in is detected by the
repository\_type flag in a .nf-core.yml file in the root directory, set
to either pipeline or modules.

-   Test a subworkflow

<!-- -->

    nf-core subworkflows test <subworkflow-name>

-   Check the format of subworkflow against the nf-core guidelines

-   Install a workflow into a pipeline

        nf-core subworkflows install <subworkflow-name>

    when installing a workflow, and it will look for included modules if
    the module is included in the subworkflow in the following format

        include { my_module } from './path/to/modules'

    and will try to install the module if not installed yet.

    Note that when putting the path to separate line, the module check
    will not be triggered, like below:

        include { my_module } from \
            './path/to/modules'

    Also note that when searching the module, it will replace underline
    `_` with ‘/’ to construct a path (here
    ‘./path/to/modules/my/module’) to find the module, so it is
    important to avoid ’\_’ in the module names unless it is consistent
    with the predicted path.

## Pipelines

### Create a pipeline

    nf-core create --name <pipeline-name> \
                   --description <pipeline-description> \
                   --version <initial version number> \
                   --outdir <directory for new pipeline; default is pipeline name> \

This will create a pipeline backbone in the folder specified with
`--outdir`. The backbone contains many useful functions/workflows, such
as paramter validation.

### Launch a pipeline

One can use the following command to launch a webpage to input
parameters which can saved in a file and then feed nextflow with the
option `-params-file` to run a pipeline.

    nf-core launch

### Bump versions

    nf-core bump-version <new-version>

The command uses results from the linting process, so will only work
with workflows that pass these tests.

### Schema

The file nextflow\_schema.json contains the input parameters and
descriptions for a pipeline. One can find more description of schema at
<https://nextflow-io.github.io/nf-schema/latest/nextflow_schema/>.

To understand the general format of json-schema, one can check this page
<https://json-schema.org/understanding-json-schema>.

-   Two types of schema

    -   pipeline schema:
        <https://nextflow-io.github.io/nf-schema/latest/nextflow_schema/nextflow_schema_specification/>
    -   samplesheet schema:
        <https://nextflow-io.github.io/nf-schema/latest/nextflow_schema/sample_sheet_schema_specification/>

-   Update schema

    After adding some parameters in any config files such as
    nextflow.config, run the following to open an interactive interface
    to update pipeline schema

        nf-core schema build

    The tool will run the nextflow config command to extract your
    pipeline’s configuration and compare the output to your
    nextflow\_schema.json file (if it exists). It will prompt you to
    update the schema file with any changes, then it will ask if you
    wish to edit the schema using the web interface.

    You can run the nf-core schema build command again and again, as
    many times as you like. It’s designed both for initial creation but
    also future updates of the schema file.

-   Display schema

    One can display a pipeline schema in markdown or html format using
    the command

        nf-core schema docs <pipeline>

-   Parameter validation

    One can use a json schema to define the required fields in an input
    file, which will be tested later during validation.

    In the file nextflow\_schema.json, parameters can be grouped, and
    each of them be further defined in the *properties* section. This
    file can also use `schema` to refer to other json file which defines
    the fields of an input file, so that the input file can be checked.

    Some special fields used to check input file:

    -   meta: this field will be added into the meta map
    -   unique: the field needs to be unique; deprecated in nf-schema
    -   deprecated: throw a deprecation message
    -   dependentRequired: useful when specifying fields when other
        conditions are needed.

    To validate the parameters in a file, say, params.json, one can run
    the command

        nf-core schema validate <pipeline> params.json

## Private repositories

One can use private github or gitlab repositories to host
modules/subworkflows, to do so, one just need to setup a repository as
normally do, then use the following commands to add new modules and
workflows:

    nf-core modules create # for modules
    nf-core subworkflows create  # for subworkflows

When one wants to install modules/workflows from this repository, one
needs to feed the option *–git-remote* with the private git repo
address.

One can find more info at
<https://nf-co.re/docs/nf-core-tools/custom_remotes>.

## Lint

-   Executing the `nf-core lint` command from within your pipeline
    repository will print a list of ignored tests, warnings, failed
    tests, and a summary.
