PROJECT_ID=$(gcloud config get project)

gcloud storage buckets list gs://${PROJECT_ID}_workflow_poc > /dev/null 2>&1

if [ $? -gt 0 ]
then
    
    gcloud storage buckets create gs://${PROJECT_ID}_workflow_poc

    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:workflow-poc@${PROJECT_ID}.iam.gserviceaccount.com" --role="roles/storage.objectCreator" --condition=None --quiet

fi

gcloud builds submit --config cloudbuild.yaml