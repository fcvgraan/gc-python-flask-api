#!/bin/bash

PROJECT_ID="gc-python-api-v1"
PROJECT_NAME="gc-python-api"

gcloud projects create $PROJECT_ID \
  --name="$PROJECT_NAME" \
  --set-as-default

BILLING_ACCOUNT=$(gcloud beta billing accounts list --format 'value(name)' --filter=open=true)
gcloud beta billing projects link $PROJECT_ID \
  --billing-account $BILLING_ACCOUNT

gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com  

GCF_NAME="calculate-business-seconds"
GCF_ENTRY="http_trigger"
GCF_REGION="europe-west1"

gcloud functions deploy $GCF_NAME \
  --entry-point $GCF_ENTRY \
  --region $GCF_REGION \
  --runtime python37 \
  --trigger-http \
  --allow-unauthenticated