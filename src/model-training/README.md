# Model Training Service

Service for training machine learning models locally or on Google Cloud Vertex AI.

## Purpose

This service handles:

- Model training with various frameworks (scikit-learn, TensorFlow, PyTorch)
- Hyperparameter tuning
- Model evaluation and validation
- Experiment tracking with MLflow
- Training on Vertex AI

## Usage

### Local training:

```bash
python train.py --data <data_path> --model-type <model_type>
```

### Vertex AI training:

```bash
python train.py --mode vertex-ai --config <config.yaml>
```

### Hyperparameter tuning:

```bash
python train.py --tune --search-space <search_space.json>
```

## Environment Variables

- `GCP_PROJECT_ID`: Google Cloud project
- `VERTEX_AI_LOCATION`: Vertex AI region
- `GCS_BUCKET_MODELS`: Model storage bucket
- `MLFLOW_TRACKING_URI`: MLflow server URL

## Model Formats

Support for:

- Scikit-learn (.pkl, .joblib)
- TensorFlow (.h5, SavedModel)
- PyTorch (.pt, .pth)
- ONNX (.onnx)

## Docker

Build:

```bash
docker build -t mlops-model-training .
```

Run:

```bash
docker run -v $(pwd)/data:/app/data mlops-model-training
```
