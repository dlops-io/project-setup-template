"""Every setting the workflow reads, in one place: the environment variables docker-shell.sh sets.

A missing setting stops the command that needs it, so `python cli.py --help` works without any.
"""

import os
import sys

GCP_PROJECT = os.getenv("GCP_PROJECT")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")  # pipeline runs, data and the trained model
GCS_SERVICE_ACCOUNT = os.getenv("GCS_SERVICE_ACCOUNT")  # the pipelines run as this account
GCS_PACKAGE_URI = os.getenv("GCS_PACKAGE_URI")  # where the trainer package is uploaded
ARTIFACT_REGISTRY_REPO = os.getenv("ARTIFACT_REGISTRY_REPO", "mlops-app")
IMAGE_TAG = os.getenv("IMAGE_TAG", "latest")


def require(name: str) -> str:
    value = globals().get(name)
    if not value:
        sys.exit(f"{name} is not set: set it in docker-shell.sh")
    return value


def step_image(service: str) -> str:
    """The Artifact Registry address of one of our step images, e.g. step_image("data-processor")"""
    registry = f"{GCP_REGION}-docker.pkg.dev/{require('GCP_PROJECT')}/{ARTIFACT_REGISTRY_REPO}"
    return f"{registry}/mlops-app-{service}:{IMAGE_TAG}"


def bucket_uri() -> str:
    return f"gs://{require('GCS_BUCKET_NAME')}"


def pipeline_root() -> str:
    return f"{bucket_uri()}/pipeline_root"


def training_output_dir() -> str:
    """Vertex AI training writes here; the trainer saves the model to $AIP_MODEL_DIR = <this>/model"""
    return f"{bucket_uri()}/training"


if __name__ == "__main__":
    # scripts/build-push.sh asks here, so the image name has one definition
    print(step_image(sys.argv[1]))
