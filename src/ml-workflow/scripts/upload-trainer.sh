#!/bin/bash
# Package the trainer (src/model-training/package) and upload it where the Model Training step finds
# it: $GCS_PACKAGE_URI/mlops-app-trainer.tar.gz. Rerun it after every change to the trainer.

set -e

ARCHIVE=/tmp/mlops-app-trainer.tar.gz
tar czf "$ARCHIVE" -C /src/model-training package
gcloud storage cp "$ARCHIVE" "$GCS_PACKAGE_URI/mlops-app-trainer.tar.gz"
echo "Uploaded $GCS_PACKAGE_URI/mlops-app-trainer.tar.gz"
