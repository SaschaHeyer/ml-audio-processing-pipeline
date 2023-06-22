PROJECT_ID=$(gcloud config get project)

gcloud ai models upload \
  --container-ports=8080 \
  --container-predict-route="/predict" \
  --container-health-route="/health" \
  --region=us-central1 \
  --display-name=audio-classification \
  --container-image-uri=gcr.io/$PROJECT_ID/audio-classification