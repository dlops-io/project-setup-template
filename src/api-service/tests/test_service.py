import pytest
from fastapi.testclient import TestClient

from api import service


@pytest.fixture
def client():
    return TestClient(service.app)


def test_docs_are_served_under_api(client):
    assert client.get("/api/docs").status_code == 200


def test_status(client, monkeypatch):
    monkeypatch.setenv("GCP_PROJECT", "test-project")
    assert client.get("/api/status").json()["gcp_project"] == "test-project"


def test_liveness_needs_nothing(client):
    assert client.get("/healthz").json() == {"ok": True}
