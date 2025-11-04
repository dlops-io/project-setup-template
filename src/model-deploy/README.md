# Model Deploy Service

Dedicated service for model serving and inference (alternative to using api-service for model endpoints).

## Purpose

This service provides:

- Optimized model serving
- Fast inference endpoints
- Model version management
- A/B testing capabilities
- Model monitoring

## Usage

### Start the server:

```bash
uvicorn serve:app --host 0.0.0.0 --port 8080
```

### Make predictions:

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {...}}'
```

## Environment Variables

- `MODEL_NAME`: Name of the model to serve
- `MODEL_VERSION`: Model version (default: latest)
- `GCS_BUCKET_MODELS`: GCS bucket with models
- `BATCH_SIZE`: Batch size for inference
- `MAX_WORKERS`: Number of workers

## Deployment Options

### Local:

```bash
docker run -p 8080:8080 mlops-model-deploy
```

### GKE:

Deployed using Pulumi configuration in infrastructure/

### Vertex AI Endpoints:

Can also deploy to Vertex AI for managed serving

## Performance Optimization

- Model caching
- Batch processing
- GPU support (if available)
- Async inference for large batches
- Response streaming

## Docker

Build:

```bash
docker build -t mlops-model-deploy .
```

Run:

```bash
docker run -p 8080:8080 mlops-model-deploy
```
