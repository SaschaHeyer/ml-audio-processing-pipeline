PROJECT_ID=$(gcloud config get project)

ENDPOINT_ID=$(gcloud ai endpoints list --project=$PROJECT_ID --region=us-central1 | grep 'workflow-poc-endpoint' | awk '{print $1}')

if [ -z "$ENDPOINT_ID" ]
then
	
	echo "Creating endpoint"
	
	gcloud ai endpoints create --project=$PROJECT_ID --region=us-central1 --display-name=workflow-poc-endpoint
	
	ENDPOINT_ID=$(gcloud ai endpoints list --project=$PROJECT_ID --region=us-central1 | grep 'workflow-poc-endpoint' | awk '{print $1}')

	echo "Endpoint $ENDPOINT_ID created"
else
	echo "Endpoint already exists, deploying model"
fi

MODEL_ID=$(gcloud ai models list --project=$PROJECT_ID --region=us-central1 | grep 'audio-classification' | awk '{print $1}')

echo "Deploying model $MODEL_ID"

if [ -z "$ENDPOINT_ID" ] || [ -z "$MODEL_ID" ]
then
      echo "ERROR: Endpoint or model ID is empty"
else
      gcloud ai endpoints deploy-model $ENDPOINT_ID \
	  --project=$PROJECT_ID \
	  --region=us-central1 \
	  --model=$MODEL_ID \
	  --machine-type="n1-standard-16" \
	  --accelerator=type="nvidia-tesla-t4,count=1" \
	  --display-name=image-audio-classification\
	  --service-account="workflow-poc@$PROJECT_ID.iam.gserviceaccount.com"
fi

