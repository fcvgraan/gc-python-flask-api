#!/bin/bash


#gcloud config set project recomed-294109
#gcloud functions deploy calculate-business-seconds-new-v8 --entry-point http_trigger2 --region europe-west1 --runtime python37 --trigger-http --allow-unauthenticated

GCF_NAME="calculate-business-seconds-new-v19"
GCF_ENTRY="http_trigger2"
GCF_REGION="europe-west1"

gcloud functions deploy $GCF_NAME \
  --entry-point $GCF_ENTRY \
  --region $GCF_REGION \
  --runtime python37 \
  --trigger-http \
  --allow-unauthenticated