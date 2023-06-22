PROJECT_ID=$(gcloud config get project)

gcloud workflows deploy WorfklowPOC --source=workflow.yaml \
    --service-account=workflow-poc@${PROJECT_ID}.iam.gserviceaccount.com

# gcloud eventarc triggers create worfklow-poc-trigger \
#     --location=us-central1 \
#     --destination-workflow=WorfklowPOC  \
#     --destination-workflow-location=us-central1 \
#     --event-filters="type=google.cloud.storage.object.v1.finalized" \
#     --event-filters="bucket=${PROJECT_ID}_worfklow_poc" \
#     --service-account="workflow-poc@${PROJECT_ID}.iam.gserviceaccount.com"
