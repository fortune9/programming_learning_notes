Singularity reference
================
Zhenguo Zhang
11 January, 2026

- [Installation](#installation)
- [Images](#images)
  - [Build images from difference
    sources](#build-images-from-difference-sources)
  - [Types](#types)
- [Configurations](#configurations)
- [References](#references)

Singularity is an open source container platform designed to be simple,
fast, and secure. Unlike Docker which requires root privileges to run
containers, singularity is designed for ease-of-use and in HPC
environments. Singularity is compatible with all docker images and can
also be used with GPU and MPI applications.

## Installation

To install singularity, one can follow the instructions here
<https://docs.sylabs.io/guides/4.1/admin-guide/installation.html>.

Basically, it includes 3 steps:

- install system dependencies

- install Go: <https://go.dev/doc/install>

- install Singularity: download source code, compile, and install.

## Images

### Build images from difference sources

Singularity can build images from the following sources, and the sources
need to be prepended correct prefix. Here is a summary

| Source                         | Prefix        | Example                     |
|--------------------------------|---------------|-----------------------------|
| local docker images            | docker-daemon | docker-deamon://ubuntu      |
| singularity image library      | library       | default to cloud.syslabs.io |
| docker registry                | docker        | default to docker hub       |
| singularity registry           | shub          | default to singularty hub   |
| OCI registry holding SIF files | oras          | oras://oci-registry/ubuntu  |

### Types

- default: compressed read-only image format

- sandbox: can read-and-write in a directory structure; turned on with
  option `--sandbox` in `singularity build`.

## Configurations

- SINGULARITY_CACHEDIR: the folder to store the cached files, including
  pulled containers. The default is ~/.singularity

- singularity.conf: main file specifying the dependencies of running
  singularity. check
  <https://docs.sylabs.io/guides/4.1/admin-guide/installation.html#installation-on-linux>

## References
