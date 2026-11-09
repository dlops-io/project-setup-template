#!/bin/bash
# Create the Artifact Registry repository the step images go to. Once per project.
# Needs permission to create repositories (roles/artifactregistry.admin); otherwise create it in the
# console: Artifact Registry > Create repository, format Docker, region $GCP_REGION.

set -e

if gcloud artifacts repositories describe "$ARTIFACT_REGISTRY_REPO" --location "$GCP_REGION" >/dev/null 2>&1; then
    echo "Repository $ARTIFACT_REGISTRY_REPO already exists in $GCP_REGION"
else
    gcloud artifacts repositories create "$ARTIFACT_REGISTRY_REPO" \
        --repository-format docker --location "$GCP_REGION" \
        --description "Step images for the ML workflow"
fi
echo "Images: ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${ARTIFACT_REGISTRY_REPO}/"
