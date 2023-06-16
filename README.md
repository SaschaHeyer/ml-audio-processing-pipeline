# ML Audio Processing Pipeline

## Setup

### Deploy services
Each service has it's own subfolder containing a `deploy.sh` that runs a Cloud Build step. 

### Deploy model
The model is a multi step process run in this order `build.sh`, `upload.sh`, `deploy.sh`

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