# Model Training

Trains and evaluates models on Vertex AI, and saves the trained model to GCS.

Training runs as a **Vertex AI training job**: a prebuilt framework image (here TensorFlow 2.17) runs
the trainer package in `package/` on a machine you choose, with a GPU if you need one. The pipeline's
Model Training step starts the job (`model_training` in `../ml-workflow/components.py`).

## The trainer package

```
package/
├── setup.py          # the packages the prebuilt image lacks (TensorFlow is already in it)
└── trainer/
    ├── __init__.py
    └── task.py       # parses --epochs and --batch_size, trains, saves the model
```

The skeleton in `task.py` trains a tiny model on made-up data, so the whole path works before you have
your own model: train, upload to the Model Registry, deploy, predict. Replace `load_data()` and
`build_model()` with yours. Keep these, which the other steps rely on:

- It saves the model to the folder in the `AIP_MODEL_DIR` environment variable. Vertex AI sets it to
  `gs://<GCS_BUCKET_NAME>/training/model`, which is where Model Deploy looks.
- It saves a SavedModel with a `serving_default` signature (`export()`), which the prebuilt serving
  image needs. The argument name of `serve()` is the key in each prediction request:
  `{"features": [...]}` here, and `SAMPLE_INSTANCES` in `../model-deploy/cli.py` sends that.
- It gets `--epochs=<n>` and `--batch_size=<n>`, set in `../ml-workflow/components.py`.
- Another framework or version: change `container_uri` in `model_training()` to a prebuilt training
  image for it, and the serving image in `../model-deploy/cli.py` to match:
  https://cloud.google.com/vertex-ai/docs/training/pre-built-containers

## Upload and run it

From the workflow shell (`../ml-workflow/docker-shell.sh`):

```bash
./scripts/upload-trainer.sh
```

```bash
python cli.py --model-training
```

Upload again after every change you want the pipeline to use. Make the archive with the script, not
with `tar` on a Mac: macOS adds hidden `._*` files to it, and then pip cannot find `setup.py`.
