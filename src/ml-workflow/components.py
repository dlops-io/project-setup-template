"""The steps a pipeline is made of. Two kinds:

Container components run one of our own images, pushed with scripts/build-push.sh. With command=[]
the image keeps its ENTRYPOINT (docker-entrypoint.sh), which gets `args`: so the data-processor step
runs `python cli.py --process`, exactly as `./docker-shell.sh cli.py --process` does on the laptop.
Each argument is its own list item: ["--bucket", name], never "--bucket name".

Lightweight components are Python functions that kfp runs in a stock Python image. Ours call the
Vertex AI SDK, to start a training job and to deploy a model, so they import it inside the function:
only the function's own code goes to the cloud.
"""

from kfp import dsl

import settings

PYTHON_IMAGE = "python:3.13-slim"
AIPLATFORM = "google-cloud-aiplatform==2.7.0"  # the version in uv.lock


@dsl.container_component
def data_processor():
    return dsl.ContainerSpec(
        image=settings.step_image("data-processor"),
        command=[],  # empty: keep the image's ENTRYPOINT
        args=["cli.py", "--process"],
    )


# Copy data_processor() for each new step image, for example data-collector:
#
# @dsl.container_component
# def data_collector():
#     return dsl.ContainerSpec(
#         image=settings.step_image("data-collector"),
#         command=[],
#         args=["cli.py", "--collect", "--bucket", settings.require("GCS_BUCKET_NAME")],
#     )


@dsl.component(base_image=PYTHON_IMAGE, packages_to_install=[AIPLATFORM])
def model_training(
    project: str,
    location: str,
    staging_bucket: str,
    python_package_gcs_uri: str,
    base_output_dir: str,
    epochs: int = 3,
    batch_size: int = 16,
):
    """Runs the trainer package (src/model-training) as a Vertex AI training job, and waits for it"""
    import google.cloud.aiplatform as aip

    aip.init(project=project, location=location, staging_bucket=staging_bucket)

    job = aip.CustomPythonPackageTrainingJob(
        display_name="mlops-app-training",
        python_package_gcs_uri=python_package_gcs_uri,
        python_module_name="trainer.task",
        # A prebuilt training image with the framework the trainer needs:
        # https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
        container_uri="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-17.py310:latest",
    )
    job.run(
        args=[f"--epochs={epochs}", f"--batch_size={batch_size}"],
        # The trainer saves the model to $AIP_MODEL_DIR, which is <base_output_dir>/model
        base_output_dir=base_output_dir,
        replica_count=1,
        machine_type="n1-standard-4",
        # With a GPU (needs GPU quota in your project, and a GPU image in container_uri):
        # accelerator_type="NVIDIA_TESLA_T4",
        # accelerator_count=1,
        sync=True,
    )


@dsl.component(base_image=PYTHON_IMAGE, packages_to_install=[AIPLATFORM])
def model_deploy(
    project: str,
    location: str,
    artifact_uri: str,
    deploy_endpoint: bool = False,
):
    """Uploads the trained model to the Model Registry, and deploys it to an endpoint if asked.

    An endpoint keeps a machine running, and billed, until you undeploy it: deploy_endpoint is
    False unless you set it. src/model-deploy does the same by hand (--upload, --deploy), and
    --predict and --cleanup the endpoint this makes: keep the names here and there the same.
    """
    import google.cloud.aiplatform as aip

    model_name = "mlops-app-model"
    endpoint_name = "mlops-app-endpoint"
    aip.init(project=project, location=location)

    # A model with this name already registered gets a new version, not a second model
    existing = aip.Model.list(filter=f'display_name="{model_name}"', order_by="create_time desc")
    model = aip.Model.upload(
        display_name=model_name,
        artifact_uri=artifact_uri,
        # A prebuilt serving image for the model's framework. Vertex AI only accepts images on its list:
        # https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-15:latest",
        parent_model=existing[0].resource_name if existing else None,
    )
    print(f"Registered {model.resource_name} (version {model.version_id})")

    if not deploy_endpoint:
        print("Not deployed to an endpoint (deploy_endpoint=False).")
        return

    # Reuse our endpoint, so deploying again never starts a second machine
    endpoints = aip.Endpoint.list(filter=f'display_name="{endpoint_name}"')
    endpoint = endpoints[0] if endpoints else aip.Endpoint.create(display_name=endpoint_name)
    previously_deployed = endpoint.list_models()
    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=model_name,
        traffic_percentage=100,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )
    # Older versions get no traffic now, but would keep their machines running
    for deployed_model in previously_deployed:
        endpoint.undeploy(deployed_model_id=deployed_model.id)
    print("Endpoint:", endpoint.resource_name)


# The sample pipeline's steps: plain Python, no images of our own


@dsl.component(base_image=PYTHON_IMAGE)
def square(x: float) -> float:
    return x**2


@dsl.component(base_image=PYTHON_IMAGE)
def add(x: float, y: float) -> float:
    return x + y


@dsl.component(base_image=PYTHON_IMAGE)
def square_root(x: float) -> float:
    return x**0.5
