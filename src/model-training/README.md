# Model Training

Trains and evaluates models on Vertex AI, and saves the trained model to GCS.

Training runs as a **Vertex AI training job**: a prebuilt framework image (TensorFlow, PyTorch,
scikit-learn) runs your trainer package on a machine you choose, with a GPU if you need one. The
pipeline's Model Training step starts the job (`model_training` in `../ml-workflow/components.py`).

## What the pipeline expects

A Python package with a `trainer.task` module:

```
src/model-training/
└── package/
    ├── setup.py          # name, version, install_requires (the packages the prebuilt image lacks)
    └── trainer/
        ├── __init__.py
        └── task.py       # parses --epochs and --batch_size, trains, saves the model
```

- `task.py` gets `--epochs=<n>` and `--batch_size=<n>` (set in `../ml-workflow/components.py`).
- It saves the model to the folder in the `AIP_MODEL_DIR` environment variable. Vertex AI sets it to
  `gs://<GCS_BUCKET_NAME>/training/model`, which is where the Model Deploy step looks.
- The prebuilt image is `container_uri` in `model_training()`: pick one with your framework and version
  from https://cloud.google.com/vertex-ai/docs/training/pre-built-containers.

## Upload the package

From the workflow shell (`../ml-workflow/docker-shell.sh`), which has gcloud and sees this folder at
`/src/model-training`:

```bash
tar czf /tmp/mlops-app-trainer.tar.gz -C /src/model-training package
```

```bash
gcloud storage cp /tmp/mlops-app-trainer.tar.gz "$GCS_PACKAGE_URI/mlops-app-trainer.tar.gz"
```

Then `python cli.py --model-training` runs it on its own, or `python cli.py --pipeline` after the data
step. Upload again after every change you want the pipeline to use.
