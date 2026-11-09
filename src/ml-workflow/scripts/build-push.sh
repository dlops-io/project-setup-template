#!/bin/bash
# Build a step image for Vertex AI and push it to Artifact Registry, from the workflow container:
#   ./scripts/build-push.sh data-processor
# Rerun it after every change you want the pipeline to use: Vertex AI pulls the image by name.

set -e

SERVICE=${1:?"Usage: $0 <folder in src/>, for example: $0 data-processor"}
[[ -f "/src/$SERVICE/Dockerfile" ]] || { echo "No /src/$SERVICE/Dockerfile" >&2; exit 1; }
cd "$(dirname "$0")/.."  # where settings.py is
IMAGE=$(python settings.py "$SERVICE")

# linux/amd64: the machines Vertex AI runs on. On Apple silicon this build is emulated, so it is
# slower than the one docker-shell.sh makes.
docker build --platform linux/amd64 -t "$IMAGE" --push "/src/$SERVICE"

echo "Pushed $IMAGE"
