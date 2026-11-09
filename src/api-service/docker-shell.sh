#!/bin/bash

set -e

export IMAGE_NAME="mlops-app-api-service"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="your-gcp-project" # CHANGE TO YOUR PROJECT ID

# Create the network if we don't have it yet
docker network inspect mlops-app-network >/dev/null 2>&1 || docker network create mlops-app-network

if docker ps --format "{{.Names}}" | grep -qx "${IMAGE_NAME}"; then
    echo "Container '${IMAGE_NAME}' is already running. Shelling into it..."
    docker exec -it "$IMAGE_NAME" /bin/bash docker-entrypoint.dev.sh
else
    echo "Building ${IMAGE_NAME} (Dockerfile.dev)..."
    docker build -t "$IMAGE_NAME" -f Dockerfile.dev .

    # Run the container
    # --network-alias: the frontend and the other services find it as api-service, as in docker compose
    docker run --rm --name "$IMAGE_NAME" -ti \
        -v "$BASE_DIR":/app \
        -v "$SECRETS_DIR":/secrets:ro \
        -v mlops-app-uv-cache:/home/app/.cache/uv \
        -p 9000:9000 \
        -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
        -e GCP_PROJECT="$GCP_PROJECT" \
        -e CHROMADB_HOST=vector-db \
        -e CHROMADB_PORT=8000 \
        -e DATABASE_URL=postgresql://mlops_user:mlops_password@postgres:5432/mlops_db \
        --network mlops-app-network \
        --network-alias api-service \
        "$IMAGE_NAME"
fi
