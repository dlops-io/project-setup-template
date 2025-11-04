# ML Workflow Service

Service for orchestrating end-to-end ML pipelines using Google Cloud Vertex AI Pipelines.

## Purpose

This service handles:

- Pipeline definition using Kubeflow Pipelines (KFP)
- Orchestrating data collection → processing → training → deployment
- Scheduling automated retraining
- Managing pipeline runs on Vertex AI

## Pipeline Structure

```
Data Collection → Data Processing → Model Training → Evaluation → Deployment
                                         ↓
                                  Hyperparameter Tuning
```

## Usage

### Define a pipeline:

```python
from kfp import dsl

@dsl.pipeline(
    name="ml-training-pipeline",
    description="End-to-end ML training pipeline"
)
def training_pipeline():
    # Define pipeline steps
    ...
```

### Submit pipeline to Vertex AI:

```bash
python pipeline.py --submit --config pipeline_config.yaml
```

### Schedule pipeline:

```bash
python pipeline.py --schedule "0 2 * * *"  # Daily at 2 AM
```

## Environment Variables

- `GCP_PROJECT_ID`: Google Cloud project
- `VERTEX_AI_LOCATION`: Vertex AI region
- `PIPELINE_ROOT`: GCS path for pipeline artifacts
- `SERVICE_ACCOUNT`: Service account for pipeline execution

## Pipeline Components

Each component is a containerized step:

- Uses Docker images from GCR
- Receives inputs from previous steps
- Produces outputs for next steps
- Logs metrics and artifacts

## Monitoring

- View pipeline runs in Vertex AI console
- Track metrics in pipeline UI
- Set up alerts for failures
- Export logs to Cloud Logging

## Docker

Build:

```bash
docker build -t mlops-ml-workflow .
```

Run:

```bash
docker run mlops-ml-workflow
```

## Resources

- [Vertex AI Pipelines Documentation](https://cloud.google.com/vertex-ai/docs/pipelines)
- [Kubeflow Pipelines SDK](https://www.kubeflow.org/docs/components/pipelines/)
