# Model Deploy

Serves the trained model from a **Vertex AI endpoint**: registers it in the Model Registry, deploys it,
asks it for predictions, and takes it down again.

The pipeline's Model Deploy step registers each trained model by itself
(`model_deploy` in `../ml-workflow/components.py`). This folder is for the endpoint: you choose when to
start one, because it is billed every hour until you delete it.

## Run it

```bash
./docker-shell.sh
```

| Command | What it does |
|---|---|
| `python cli.py --upload` | Register the trained model (`gs://<GCS_BUCKET_NAME>/training/model`) as a new version |
| `python cli.py --deploy` | Deploy the newest version to `mlops-app-endpoint` (often 10-20 minutes). Deploying again replaces the old version, on the same machine |
| `python cli.py --predict` | Send `SAMPLE_INSTANCES` to the endpoint and print the predictions |
| `python cli.py --cleanup` | Undeploy and delete the endpoint, so it stops billing. The Model Registry versions and GCS files stay |

A command can also run without opening a shell: `./docker-shell.sh cli.py --predict`.

It uses the same key, project and bucket as `../ml-workflow`: set the `CHANGE` lines in
`docker-shell.sh` to the same values.

## Files

| File | What it does |
|---|---|
| `cli.py` | The four commands; the model and endpoint names, machine type and serving image at the top |
| `Dockerfile` | Python and the Vertex AI SDK. The image runs as a job too |
| `docker-entrypoint.sh` | With arguments, runs `python <args>` and stops; otherwise opens a shell |
| `docker-shell.sh` | Builds the image and starts a container, with the code and `../secrets` mounted |

## With your own model

- `SAMPLE_INSTANCES` in `cli.py`: one input per item, keyed by the argument name of the serving
  function the trainer saves (`serve(features)` in `../model-training/package/trainer/task.py`).
- `SERVING_IMAGE`: a prebuilt serving image for your framework, from the list Vertex AI accepts:
  https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers. Keep `model_deploy` in
  `../ml-workflow/components.py` on the same image.
