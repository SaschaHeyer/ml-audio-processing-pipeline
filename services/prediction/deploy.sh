PROJECT_ID=$(gcloud config get project)

ENDPOINT_ID=$(gcloud ai endpoints list --project=$PROJECT_ID --region=us-central1 | grep 'workflow-poc-endpoint' | awk '{print $1}')

gcloud builds submit --config cloudbuild.yaml --substitutions=_ENDPOINT_ID=$ENDPOINT_ID