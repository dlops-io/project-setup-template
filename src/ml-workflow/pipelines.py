"""The pipelines: which steps run, with what, in what order. cli.py compiles and submits them."""

from kfp import dsl

import components
import settings


@dsl.pipeline(name="mlops-app-sample")
def sample(a: float = 3.0, b: float = 4.0) -> float:
    """sqrt(a^2 + b^2): checks your project, bucket and service account before any of your own images"""
    a_squared = components.square(x=a)
    b_squared = components.square(x=b)
    total = components.add(x=a_squared.output, y=b_squared.output)
    return components.square_root(x=total.output).output


def data_processor_step():
    # Limits, for steps that need more than the default machine:
    #   .set_cpu_limit("4").set_memory_limit("16G")
    return components.data_processor().set_display_name("Data Processor")


def model_training_step():
    return components.model_training(
        project=settings.require("GCP_PROJECT"),
        location=settings.GCP_REGION,
        staging_bucket=settings.bucket_uri(),
        python_package_gcs_uri=f"{settings.require('GCS_PACKAGE_URI')}/mlops-app-trainer.tar.gz",
        base_output_dir=settings.training_output_dir(),
    ).set_display_name("Model Training")


def model_deploy_step():
    return components.model_deploy(
        project=settings.require("GCP_PROJECT"),
        location=settings.GCP_REGION,
        artifact_uri=f"{settings.training_output_dir()}/model",
    ).set_display_name("Model Deploy")


@dsl.pipeline(name="mlops-app-data-processor")
def data_processor():
    data_processor_step()


@dsl.pipeline(name="mlops-app-model-training")
def model_training():
    model_training_step()


@dsl.pipeline(name="mlops-app-model-deploy")
def model_deploy():
    model_deploy_step()


@dsl.pipeline(name="mlops-app-pipeline")
def ml_pipeline():
    processing = data_processor_step()
    training = model_training_step().after(processing)
    model_deploy_step().after(training)
