Nextflow tower
================
June 25, 2024

-   [Deployment](#deployment)
    -   [AWS](#aws)
-   [Usage](#usage)
-   [References](#references)

## Deployment

### AWS

To deploy Nextflow tower to AWS, one need to follow the following 3
steps,

1.  Prepare AWS to have all the required elements, such as IAM roles,
    SMTP server, MySQL database, etc. [Check
    here](https://install.tower.nf/22.3/prerequisites/aws/).

2.  With that, one need to change the configuration files of tower.env,
    tower.yml, and docker-compose.yml to reflect the settings, including
    those set in step 1. [Check
    here](https://install.tower.nf/22.3/configuration/overview/).

3.  Finally, one can deploy the Nextflow tower enterprise, which
    includes download the tower docker images from Seqeralabs’ ECR and
    run docker to start these images. [Check
    here](https://install.tower.nf/22.3/docker-compose/).

## Usage

Regarding how to use nextflow tower to run pipelines, one can find more
information [here](https://help.tower.nf/).

## References

1.  AWS prerequisites for tower deployment:
    <https://install.tower.nf/22.3/prerequisites/aws/>

2.  Tower configurations in tower.env and tower.yml:
    <https://install.tower.nf/22.3/configuration/overview/>

3.  Deploy tower using docker-compose:
    <https://install.tower.nf/22.3/docker-compose/>

4.  Deploy tower using Kubernetes:
    <https://install.tower.nf/22.3/kubernetes/>
