#!/bin/bash

set -e

export IMAGE_NAME="mlops-app-model-deploy"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="your-gcp-project" # CHANGE TO YOUR PROJECT ID
export GCP_REGION="us-central1"
export GCS_BUCKET_NAME="your-gcp-project-ml-workflow" # CHANGE: the bucket the pipeline trains into

# Build the image based on the Dockerfile
docker build -t "$IMAGE_NAME" -f Dockerfile .

# Run the container. Any arguments run as a command instead of opening a shell:
#   ./docker-shell.sh cli.py --predict
docker run --rm -ti \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets:ro \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
    -e GCP_PROJECT="$GCP_PROJECT" \
    -e GCP_REGION="$GCP_REGION" \
    -e GCS_BUCKET_NAME="$GCS_BUCKET_NAME" \
    "$IMAGE_NAME" "$@"
