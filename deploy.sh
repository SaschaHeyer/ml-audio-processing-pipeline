PROJECT_ID=$(gcloud config get project)

gcloud workflows deploy WorkflowPOC --source=workflow.yaml \
    --service-account=workflow-poc@${PROJECT_ID}.iam.gserviceaccount.com

gcloud eventarc triggers create workflow-poc-trigger \
    --location=us-central1 \
    --destination-workflow=WorkflowPOC  \
    --destination-workflow-location=us-central1 \
    --event-filters="type=google.cloud.storage.object.v1.finalized" \
    --event-filters="bucket=${PROJECT_ID}_workflow_poc" \
    --service-account="workflow-poc@${PROJECT_ID}.iam.gserviceaccount.com"