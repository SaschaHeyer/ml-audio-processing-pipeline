gcloud ai endpoints deploy-model 3960172602411974656 \
  --project=sascha-playground-doit \
  --region=us-central1 \
  --model=6378392297054142464 \
  --traffic-split=0=100 \
  --machine-type="n1-standard-16" \
  --accelerator=type="nvidia-tesla-t4,count=1" \
  --display-name=image-audio-classification\
  --service-account='workflow-poc@sascha-playground-doit.iam.gserviceaccount.com'