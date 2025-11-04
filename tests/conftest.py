"""
Pytest configuration and shared fixtures for integration tests.

Students can add common fixtures here that are used across multiple test files.
"""

import pytest
import os


@pytest.fixture(scope="session")
def test_env():
    """
    Set up test environment variables.

    Students should add environment variables needed for testing.
    """
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DATABASE_URL"] = "postgresql://test_user:test_password@localhost:5432/test_db"
    os.environ["CHROMA_HOST"] = "localhost"
    os.environ["CHROMA_PORT"] = "8001"
    yield
    # Cleanup if needed


# Example: Database fixture
# @pytest.fixture(scope="session")
# def test_db():
#     """
#     Create a test database session.
#     """
#     from sqlalchemy import create_engine
#     from sqlalchemy.orm import sessionmaker
#
#     engine = create_engine(os.environ["DATABASE_URL"])
#     TestingSessionLocal = sessionmaker(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()


# Example: API client fixture
# @pytest.fixture
# def test_client():
#     """
#     Create a test client for the API.
#     """
#     from fastapi.testclient import TestClient
#     from api_service.main import app
#
#     client = TestClient(app)
#     return client


# Example: Test data fixture
# @pytest.fixture
# def sample_data():
#     """
#     Provide sample data for tests.
#     """
#     return {
#         "text": "Sample text for testing",
#         "features": {"feature1": 1.0, "feature2": 2.0},
#         "label": "test_label"
#     }
