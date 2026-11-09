# ML Workflow

Orchestrates end-to-end pipelines (process → train → deploy) with Vertex AI Pipelines. This container
holds the tools: it compiles pipelines written in Python (`kfp`), submits them to Vertex AI, and builds
and pushes the step images. It never runs as a pipeline step itself.

## How a pipeline runs

| Step | Kind | What runs on Vertex AI |
|---|---|---|
| Data Processor | Container component | Our `data-processor` image from Artifact Registry, with `args: ["cli.py", "--process"]` |
| Model Training | Lightweight component | A Vertex AI training job running the trainer package from `GCS_PACKAGE_URI` (see `../model-training`) |
| Model Deploy | Lightweight component | Uploads the trained model to the Model Registry; to an endpoint only with `deploy_endpoint=True` |

A container component runs one of our images, so Vertex AI must be able to pull it: build it for
`linux/amd64` and push it to Artifact Registry with `scripts/build-push.sh` after every change. Its
entrypoint gets the arguments, exactly as `./docker-shell.sh cli.py --process` does on the laptop.

## Setup, once

1. A service account key at `../../../secrets/ml-workflow.json` (the `secrets` folder next to the
   repository). The account needs:
   - `roles/aiplatform.user`: run pipelines, training jobs and endpoints
   - `roles/storage.admin` on your buckets: pipeline runs, data, the trainer package, the model
   - `roles/artifactregistry.writer`: push the step images (Vertex AI pulls them as this account)
   - `roles/iam.serviceAccountUser` on itself: pipelines run as this account
2. Two buckets: one for the pipeline (`GCS_BUCKET_NAME`), one for the trainer package (`GCS_PACKAGE_URI`).
3. Your values in `docker-shell.sh`: every line marked `CHANGE`.

## Run it

```bash
./docker-shell.sh
```

| Command | What it does |
|---|---|
| `python cli.py --sample` | Submit the sample pipeline. It uses no images of our own, so it checks the project, bucket and service account first |
| `./scripts/create-registry.sh` | Create the Artifact Registry repository (once) |
| `./scripts/build-push.sh data-processor` | Build a step image for `linux/amd64` and push it |
| `python cli.py --data-processor` | Submit one step as its own pipeline (also `--model-training`, `--model-deploy`) |
| `python cli.py --pipeline` | Submit the whole pipeline |
| `... --compile-only` | Write `compiled/<name>.yaml` and submit nothing. Needs no GCP: use it to check a pipeline |

Each submit prints a console link to follow the run. A command can also run without opening a shell:

```bash
./docker-shell.sh cli.py --pipeline --compile-only
```

## Files

| File | What it does |
|---|---|
| `components.py` | The steps: container components for our images, lightweight components for training and deploy |
| `pipelines.py` | Which steps run, with what, in what order |
| `cli.py` | Compiles a pipeline to `compiled/<name>.yaml`, and submits it |
| `settings.py` | Every setting, from the environment; also the image names `build-push.sh` uses |
| `scripts/build-push.sh` | Builds `src/<service>` for Vertex AI and pushes it to Artifact Registry |
| `scripts/create-registry.sh` | Creates the Artifact Registry repository |
| `Dockerfile` | Python, `kfp` and the Vertex AI SDK, the gcloud CLI and the Docker CLI |
| `docker-entrypoint.sh` | Logs gcloud in with the key; with arguments runs `python <args>`, otherwise opens a shell |
| `docker-shell.sh` | Builds and starts the container, with the code, `../secrets`, the other services and Docker |

The container builds images through your laptop's Docker: `docker-shell.sh` mounts
`/var/run/docker.sock`. Anything with that socket controls your Docker, so only run code you trust in
this container.

## Adding a step

1. Make the step's image: copy `../data-processor`, and give `cli.py` a flag for the step.
2. In `components.py`, copy `data_processor()` and change the image and `args`.
3. In `pipelines.py`, add it to `ml_pipeline()`, with `.after(...)` for its place in the order.
4. `./scripts/build-push.sh <service>`, then `python cli.py --pipeline`.

## Costs

Pipeline steps and training jobs are billed while they run. An endpoint is billed until you undeploy
it: delete endpoints in the console (Vertex AI > Online prediction > Endpoints) when you are done.
