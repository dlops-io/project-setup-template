# API Service

FastAPI-based API service that serves as the main HTTP gateway for the MLOps project.

## Architecture

This service uses a **modular router architecture**:
- **Routers**: Handle HTTP endpoints for different domains (data, RAG, model)
- **Services**: Business logic layer (to be implemented)
- **Models**: Pydantic schemas for request/response validation
- **Migrations**: Database migration scripts using Alembic

## Project Structure

```
api-service/
├── routers/           # API route handlers
│   ├── data.py       # Data collection/processing endpoints
│   ├── rag.py        # RAG and vector search endpoints
│   └── model.py      # Model inference endpoints
├── services/         # Business logic (to be implemented)
├── models/           # Pydantic models (to be implemented)
├── migrations/       # Database migrations (to be implemented)
├── tests/            # Unit tests
├── main.py           # FastAPI application entry point
├── Dockerfile        # Container configuration
└── pyproject.toml    # Python dependencies
```

## Local Development

### Prerequisites
- Python 3.11+
- uv (for dependency management)
- Docker & Docker Compose (for databases)

### Setup

1. Install dependencies:
```bash
cd src/api-service
uv sync
```

2. Start databases (from project root):
```bash
make up
```

3. Run the API service:
```bash
uvicorn main:app --reload
```

4. Access the API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Testing

Run tests:
```bash
uv run pytest
```

With coverage:
```bash
uv run pytest --cov
```

## Docker

Build the image:
```bash
docker build -t mlops-api-service .
```

Run the container:
```bash
docker run -p 8000:8000 mlops-api-service
```

## API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /` - API information

### Data Endpoints (to be implemented)
- `GET /api/v1/data` - List datasets
- `POST /api/v1/data/collect` - Trigger data collection
- `POST /api/v1/data/process` - Process data

### RAG Endpoints (to be implemented)
- `POST /api/v1/rag/embed` - Generate embeddings
- `POST /api/v1/rag/search` - Vector similarity search
- `POST /api/v1/rag/query` - RAG query
- `POST /api/v1/rag/ingest` - Ingest documents

### Model Endpoints (to be implemented)
- `GET /api/v1/model` - List models
- `GET /api/v1/model/{name}` - Get model info
- `POST /api/v1/model/predict` - Single prediction
- `POST /api/v1/model/predict/batch` - Batch predictions
- `POST /api/v1/model/upload` - Upload model

## Implementation Tasks

Students should implement:

1. **Database Integration**
   - SQLAlchemy models in `models/`
   - Database connection setup
   - Alembic migrations in `migrations/`

2. **Business Logic**
   - Service layer in `services/`
   - Data processing logic
   - Model loading and inference
   - Vector database operations

3. **Router Implementation**
   - Complete TODOs in router files
   - Add proper error handling
   - Implement authentication if needed

4. **Testing**
   - Add tests for all endpoints
   - Integration tests with databases
   - Mock external services

## Environment Variables

See `.env.example` in project root for all configuration options.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `CHROMA_HOST`: ChromaDB host
- `GCP_PROJECT_ID`: Google Cloud project
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key

## Deployment

This service is deployed to GKE using Pulumi. See `infrastructure/` directory for deployment configuration.

## Best Practices

- Use dependency injection for database sessions
- Implement proper error handling and logging
- Validate all inputs with Pydantic models
- Use async/await for I/O operations
- Add comprehensive tests
- Document all endpoints with docstrings
