#!/bin/bash

set -e

export IMAGE_NAME="mlops-app-data-processor"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="your-gcp-project" # CHANGE TO YOUR PROJECT ID

# Create the network if we don't have it yet
docker network inspect mlops-app-network >/dev/null 2>&1 || docker network create mlops-app-network

# Build the image based on the Dockerfile
docker build -t "$IMAGE_NAME" -f Dockerfile .

# Run the container. Any arguments run as a job instead of opening a shell:
#   ./docker-shell.sh cli.py --check
docker run --rm -ti \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets:ro \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
    -e GCP_PROJECT="$GCP_PROJECT" \
    -e CHROMADB_HOST=vector-db \
    -e CHROMADB_PORT=8000 \
    -e POSTGRES_HOST=postgres \
    -e POSTGRES_PORT=5432 \
    --network mlops-app-network \
    "$IMAGE_NAME" "$@"
