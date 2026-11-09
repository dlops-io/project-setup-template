"""Model deploy: puts the trained model behind a Vertex AI endpoint, and asks it for predictions.

    python cli.py --upload     register the trained model in the Model Registry, as a new version
    python cli.py --deploy     deploy the newest version to the endpoint (created the first time)
    python cli.py --predict    send a sample request to the endpoint
    python cli.py --cleanup    undeploy the model and delete the endpoint, so it stops billing

The pipeline's Model Deploy step does --upload by itself (src/ml-workflow/components.py). An endpoint
keeps a machine running, and billed, until --cleanup.
"""

import argparse
import os
import sys

MODEL_NAME = "mlops-app-model"
ENDPOINT_NAME = "mlops-app-endpoint"
MACHINE_TYPE = "n1-standard-2"  # the smallest general-purpose machine; billed every hour it is deployed
# A prebuilt serving image for the model's framework. Vertex AI only accepts images on its list:
# https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
SERVING_IMAGE = "us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-15:latest"

# What the trainer skeleton's model expects (src/model-training/package/trainer/task.py). Change it
# with your model: each instance is one input, keyed by the serving function's argument name.
SAMPLE_INSTANCES = [{"features": [0.1, 0.2, 0.3, 0.4]}, {"features": [1.0, 1.0, 1.0, 1.0]}]


def setting(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        sys.exit(f"{name} is not set: set it in docker-shell.sh")
    return value


def model_artifact_uri() -> str:
    # Where training saves the model: $AIP_MODEL_DIR of the training job
    return os.getenv("MODEL_ARTIFACT_URI") or f"gs://{setting('GCS_BUCKET_NAME')}/training/model"


def find_endpoint(aiplatform):
    endpoints = aiplatform.Endpoint.list(filter=f'display_name="{ENDPOINT_NAME}"')
    return endpoints[0] if endpoints else None


def upload(aiplatform):
    # A model with this name already registered gets a new version, not a second model
    existing = aiplatform.Model.list(filter=f'display_name="{MODEL_NAME}"', order_by="create_time desc")
    model = aiplatform.Model.upload(
        display_name=MODEL_NAME,
        artifact_uri=model_artifact_uri(),
        serving_container_image_uri=SERVING_IMAGE,
        parent_model=existing[0].resource_name if existing else None,
    )
    print(f"Registered {model.resource_name} (version {model.version_id})")


def deploy(aiplatform):
    models = aiplatform.Model.list(filter=f'display_name="{MODEL_NAME}"', order_by="create_time desc")
    if not models:
        sys.exit(f"No model named {MODEL_NAME} in the Model Registry. Run: python cli.py --upload")
    model = models[0]  # its default version, which is the newest upload

    # Reuse our endpoint, so deploying again never starts a second machine
    endpoint = find_endpoint(aiplatform) or aiplatform.Endpoint.create(display_name=ENDPOINT_NAME)
    previously_deployed = endpoint.list_models()

    print(f"Deploying version {model.version_id} on a {MACHINE_TYPE} machine (often 10-20 minutes)...")
    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=MODEL_NAME,
        traffic_percentage=100,
        machine_type=MACHINE_TYPE,
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )

    # Older versions get no traffic now, but would keep their machines running
    for deployed_model in previously_deployed:
        print("Undeploying the previous version:", deployed_model.id)
        endpoint.undeploy(deployed_model_id=deployed_model.id)
    print("Endpoint ready:", endpoint.resource_name)


def predict(aiplatform):
    endpoint = find_endpoint(aiplatform)
    if not endpoint or not endpoint.list_models():
        sys.exit("Nothing is deployed. Run: python cli.py --deploy")
    result = endpoint.predict(instances=SAMPLE_INSTANCES)
    for instance, prediction in zip(SAMPLE_INSTANCES, result.predictions):
        print(instance, "->", prediction)


def cleanup(aiplatform):
    # The Model Registry versions and the files in GCS stay
    endpoint = find_endpoint(aiplatform)
    if not endpoint:
        print(f"No endpoint named {ENDPOINT_NAME}: nothing to clean up.")
        return
    endpoint.undeploy_all()
    endpoint.delete()
    print("Deleted", endpoint.resource_name)


def main():
    parser = argparse.ArgumentParser(description="Model deploy on Vertex AI")
    command = parser.add_mutually_exclusive_group(required=True)
    command.add_argument("--upload", action="store_true", help="Register the trained model, as a new version")
    command.add_argument("--deploy", action="store_true", help="Deploy the newest version to the endpoint")
    command.add_argument("--predict", action="store_true", help="Send a sample request to the endpoint")
    command.add_argument("--cleanup", action="store_true", help="Undeploy and delete the endpoint")
    args = parser.parse_args()

    key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if key and not os.path.exists(key):
        sys.exit(f"No service account key at {key}: put it in the secrets folder next to the repository")

    # Imported here, so --help is quick and needs no settings
    from google.cloud import aiplatform

    aiplatform.init(project=setting("GCP_PROJECT"), location=setting("GCP_REGION", "us-central1"))

    if args.upload:
        upload(aiplatform)
    elif args.deploy:
        deploy(aiplatform)
    elif args.predict:
        predict(aiplatform)
    elif args.cleanup:
        cleanup(aiplatform)


if __name__ == "__main__":
    main()
