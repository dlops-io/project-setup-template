"""
Data Router

Handles endpoints for data collection, processing, and management.
Students will implement data ingestion and transformation endpoints here.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# Example request/response models
class DataCollectRequest(BaseModel):
    """Request model for data collection."""

    source: str
    parameters: dict = {}


class DataProcessRequest(BaseModel):
    """Request model for data processing."""

    data_id: str
    process_type: str
    parameters: dict = {}


@router.get("/")
async def list_data():
    """
    List available datasets.

    Students should implement:
    - Query database for available datasets
    - Return metadata (size, created_at, etc.)
    """
    # TODO: Implement dataset listing
    return {"message": "Data listing endpoint - to be implemented"}


@router.post("/collect")
async def collect_data(request: DataCollectRequest):
    """
    Trigger data collection from specified source.

    Students should implement:
    - Validate source
    - Trigger data-collector service
    - Return job ID for tracking
    """
    # TODO: Implement data collection
    return {"message": "Data collection endpoint - to be implemented", "request": request.dict()}


@router.post("/process")
async def process_data(request: DataProcessRequest):
    """
    Process collected data.

    Students should implement:
    - Validate data exists
    - Trigger data-processor service
    - Return processing job ID
    """
    # TODO: Implement data processing
    return {"message": "Data processing endpoint - to be implemented", "request": request.dict()}
