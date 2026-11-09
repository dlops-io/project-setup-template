#!/bin/bash

set -e

export IMAGE_NAME="mlops-app-ml-workflow"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="your-gcp-project" # CHANGE TO YOUR PROJECT ID
export GCP_REGION="us-central1"
export GCS_BUCKET_NAME="your-gcp-project-ml-workflow"                                  # CHANGE: pipeline root and data
export GCS_SERVICE_ACCOUNT="ml-workflow@your-gcp-project.iam.gserviceaccount.com"     # CHANGE: runs the pipelines
export GCS_PACKAGE_URI="gs://your-gcp-project-trainer-code"                            # CHANGE: the trainer package
export ARTIFACT_REGISTRY_REPO="mlops-app"                                              # the step images go here

if docker ps --format "{{.Names}}" | grep -qx "${IMAGE_NAME}"; then
    echo "Container '${IMAGE_NAME}' is already running. Shelling into it..."
    docker exec -it "$IMAGE_NAME" /bin/bash docker-entrypoint.sh
    exit
fi

# Build the image based on the Dockerfile, for this machine's architecture
docker build -t "$IMAGE_NAME" -f Dockerfile .

# The container builds images through the laptop's Docker, so it needs the socket's group:
# root's (0) on Docker Desktop, the docker group's on Linux
DOCKER_SOCKET_GROUP=$(docker run --rm --entrypoint stat -v /var/run/docker.sock:/var/run/docker.sock "$IMAGE_NAME" -c %g /var/run/docker.sock)

# Run the container. Any arguments run as a command instead of opening a shell:
#   ./docker-shell.sh cli.py --pipeline --compile-only
# /src: the other services, read-only, so build-push.sh can build their images
docker run --rm --name "$IMAGE_NAME" -ti \
    -v "$BASE_DIR":/app \
    -v "$BASE_DIR/..":/src:ro \
    -v "$SECRETS_DIR":/secrets:ro \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --group-add "$DOCKER_SOCKET_GROUP" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
    -e GCP_PROJECT="$GCP_PROJECT" \
    -e GCP_REGION="$GCP_REGION" \
    -e GCS_BUCKET_NAME="$GCS_BUCKET_NAME" \
    -e GCS_SERVICE_ACCOUNT="$GCS_SERVICE_ACCOUNT" \
    -e GCS_PACKAGE_URI="$GCS_PACKAGE_URI" \
    -e ARTIFACT_REGISTRY_REPO="$ARTIFACT_REGISTRY_REPO" \
    "$IMAGE_NAME" "$@"
