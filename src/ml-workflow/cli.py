"""ML workflow: compiles a pipeline to compiled/<name>.yaml and submits it to Vertex AI Pipelines.

    python cli.py --sample                  the sample pipeline: no images of our own
    python cli.py --data-processor          one step as its own pipeline
    python cli.py --pipeline                data-processor -> model-training -> model-deploy
    python cli.py --pipeline --compile-only write the YAML, submit nothing (no GCP needed)
"""

import argparse
from datetime import datetime
from pathlib import Path

PIPELINES = {
    "sample": "The sample pipeline: checks your project, bucket and service account",
    "data-processor": "The data-processor image, on its own",
    "model-training": "A Vertex AI training job with the trainer package, on its own",
    "model-deploy": "Upload the trained model to the Model Registry, on its own",
    "pipeline": "The whole pipeline: data-processor -> model-training -> model-deploy",
}


def compile_pipeline(name: str) -> Path:
    # Imported here, so --help works without any settings
    from kfp import compiler

    import pipelines

    pipeline_func = {
        "sample": pipelines.sample,
        "data-processor": pipelines.data_processor,
        "model-training": pipelines.model_training,
        "model-deploy": pipelines.model_deploy,
        "pipeline": pipelines.ml_pipeline,
    }[name]

    path = Path("compiled") / f"{name}.yaml"
    path.parent.mkdir(exist_ok=True)
    compiler.Compiler().compile(pipeline_func, package_path=str(path))
    print(f"Compiled {path}")
    return path


def submit(name: str, path: Path):
    import google.cloud.aiplatform as aip

    import settings

    aip.init(
        project=settings.require("GCP_PROJECT"),
        location=settings.GCP_REGION,
        staging_bucket=settings.bucket_uri(),
    )
    job = aip.PipelineJob(
        display_name=f"mlops-app-{name}-{datetime.now():%Y%m%d-%H%M%S}",
        template_path=str(path),
        pipeline_root=settings.pipeline_root(),
        enable_caching=False,
    )
    # Returns once the run starts; follow it with the console link printed above
    job.submit(service_account=settings.require("GCS_SERVICE_ACCOUNT"))


def main():
    parser = argparse.ArgumentParser(description="ML workflow on Vertex AI Pipelines")
    choice = parser.add_mutually_exclusive_group(required=True)
    for name, help_text in PIPELINES.items():
        choice.add_argument(f"--{name}", action="store_const", const=name, dest="name", help=help_text)
    parser.add_argument(
        "--compile-only", action="store_true", help="Write compiled/<name>.yaml, submit nothing"
    )
    args = parser.parse_args()

    path = compile_pipeline(args.name)
    if not args.compile_only:
        submit(args.name, path)


if __name__ == "__main__":
    main()
