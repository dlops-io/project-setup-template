"""
Model Router

Handles endpoints for model inference, management, and deployment.
Students will implement model serving and prediction endpoints here.
"""

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

router = APIRouter()


# Example request/response models
class PredictionRequest(BaseModel):
    """Request model for model prediction."""

    features: dict
    model_version: str | None = "latest"


class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions."""

    items: list[dict]
    model_version: str | None = "latest"


class ModelInfo(BaseModel):
    """Model information response."""

    name: str
    version: str
    status: str
    metrics: dict | None = None


@router.get("/")
async def list_models():
    """
    List available models.

    Students should implement:
    - Query model registry
    - Return model metadata (version, metrics, status)
    """
    # TODO: Implement model listing
    return {"message": "Model listing endpoint - to be implemented"}


@router.get("/{model_name}")
async def get_model_info(model_name: str, version: str | None = None):
    """
    Get information about a specific model.

    Students should implement:
    - Fetch model metadata from registry
    - Return model details and metrics
    """
    # TODO: Implement model info retrieval
    return {
        "message": "Model info endpoint - to be implemented",
        "model_name": model_name,
        "version": version or "latest",
    }


@router.post("/predict")
async def predict(request: PredictionRequest):
    """
    Make a single prediction.

    Students should implement:
    - Load model from registry
    - Validate input features
    - Run inference
    - Return prediction with confidence
    """
    # TODO: Implement prediction
    return {"message": "Prediction endpoint - to be implemented", "request": request.dict()}


@router.post("/predict/batch")
async def batch_predict(request: BatchPredictionRequest):
    """
    Make batch predictions.

    Students should implement:
    - Load model
    - Process batch efficiently
    - Return predictions for all items
    """
    # TODO: Implement batch prediction
    return {
        "message": "Batch prediction endpoint - to be implemented",
        "batch_size": len(request.items),
    }


@router.post("/upload")
async def upload_model(file: UploadFile = File(...)):
    """
    Upload a new model.

    Students should implement:
    - Validate model file
    - Store in model registry (GCS)
    - Update model metadata
    - Optionally trigger deployment
    """
    # TODO: Implement model upload
    return {
        "message": "Model upload endpoint - to be implemented",
        "filename": file.filename,
    }
