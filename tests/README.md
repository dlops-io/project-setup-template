# Integration Tests

This directory contains integration tests that test the interaction between different services and components.

## Purpose

Integration tests verify that:
- Services work together correctly
- Database connections are properly configured
- API endpoints interact correctly with databases
- Data flows correctly through the pipeline
- External services are integrated properly

## Test Structure

### Unit Tests
Located in each service directory:
- `src/api-service/tests/` - API unit tests
- `src/data-collector/tests/` - Data collector tests
- etc.

### Integration Tests
Located here (`tests/`):
- Cross-service interactions
- Database integration
- API + Database tests
- End-to-end workflows

## Running Tests

### All Tests
From project root:
```bash
make test
```

Or with pytest directly:
```bash
pytest
```

### Integration Tests Only
```bash
pytest tests/
```

### With Coverage
```bash
pytest --cov --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## Writing Integration Tests

### Example: API + Database Test

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    # Create test database
    engine = create_engine("postgresql://test:test@localhost/test_db")
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_and_retrieve_data(test_db):
    client = TestClient(app)

    # Create data via API
    response = client.post("/api/v1/data/collect", json={
        "source": "test",
        "parameters": {}
    })
    assert response.status_code == 200

    # Verify in database
    data = test_db.query(DataModel).filter_by(source="test").first()
    assert data is not None
```

### Example: RAG Pipeline Test

```python
def test_rag_pipeline():
    # 1. Ingest documents
    docs = ["Document 1", "Document 2"]
    response = client.post("/api/v1/rag/ingest", json={"documents": docs})
    assert response.status_code == 200

    # 2. Query RAG
    response = client.post("/api/v1/rag/query", json={
        "question": "What is in document 1?"
    })
    assert response.status_code == 200
    assert "Document 1" in response.json()["answer"]
```

## Test Fixtures

Create reusable fixtures in `conftest.py`:

```python
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.compose import DockerCompose

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def docker_compose():
    with DockerCompose(".", compose_file_name="docker-compose.test.yml") as compose:
        yield compose
```

## Test Database

For integration tests, use:
1. **Test containers** (recommended): Spin up temporary containers
2. **Test database**: Dedicated test database
3. **SQLite in-memory**: For simple tests

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Always clean up test data
3. **Fixtures**: Use fixtures for common setup
4. **Mocking**: Mock external services (APIs, etc.)
5. **Speed**: Keep tests fast by using appropriate scope
6. **Coverage**: Aim for high coverage of critical paths

## CI/CD Integration

Integration tests run in GitHub Actions:
- PostgreSQL service container for database tests
- ChromaDB service for vector search tests
- All tests must pass before merging

## Common Issues

### Database Connection Errors
Ensure test database is running:
```bash
docker-compose up -d postgres
```

### Async Tests
Use `pytest-asyncio`:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Cleanup
Add teardown to fixtures:
```python
@pytest.fixture
def test_data():
    # Setup
    data = create_test_data()
    yield data
    # Teardown
    cleanup_test_data()
```
