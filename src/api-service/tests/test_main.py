"""
Tests for main API application.

Students should add tests for:
- Health check endpoint
- Router registration
- Middleware configuration
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "api-service"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"


# TODO: Add more tests for each router
# Example:
# def test_data_collection():
#     response = client.post("/api/v1/data/collect", json={"source": "test"})
#     assert response.status_code == 200
