# ML Audio Processing Pipeline

## Prerequisites
1. Authenticate and configure gcloud CLI:

   `gcloud auth login`

   `gcloud config set project <your_project_name>`

2. Enable the following APIs: Artifact Registry, Cloud Build, Cloud Run.
3. Make sure the gcr.io repository in your Artifact Registry (https://cloud.google.com/artifact-registry/docs/transition/setup-gcr-repo#create-repo)
4. Authenticate Cloud Build with Coud Run (https://cloud.google.com/build/docs/securing-builds/configure-access-for-cloud-build-service-account#service-account-permissions-settings)
5. Grant the Service Account User role to Cloud Build SA on your Cloud Run Service Account (https://cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts#permissions)

## Setup

### Deploy model
The model is a multi step process run in this order `build.sh`, `upload.sh`, `deploy.sh`

### Deploy services
Each service has it's own subfolder containing a `deploy.sh` that runs a Cloud Build step. 

### BigQuery
The pipeline result is stored in BigQuery. 

Create table with schema:

````
bq mk ml_audio_processing_workflow

!bq mk --table \
--description "Table contains the outpt of the ml audio processing workflow" \
--schema "audio_file:STRING,spectogram_image:STRING,prediction:STRING" \
ml_audio_processing_workflow.processed
````

### UI
The demo ui can be deployed with `deploy.sh`
