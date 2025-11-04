# MLOps Project Template

A comprehensive template for building production-ready MLOps projects with modern best practices, containerization, and cloud deployment.

## Overview

This template provides a complete structure for building end-to-end machine learning operations (MLOps) projects, featuring:

- **Modern Python tooling** with `uv` for fast dependency management
- **Microservices architecture** with FastAPI and containerized services
- **Database integrations** with PostgreSQL and ChromaDB vector database
- **Cloud-native deployment** to Google Cloud Platform (GCP) with Kubernetes
- **Infrastructure as Code** using Pulumi
- **CI/CD pipeline** with GitHub Actions
- **Best practices** for secrets management, testing, and code quality

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (React Application)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Service                             │
│            (FastAPI with Modular Routers)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   Data   │  │   RAG    │  │  Model   │                  │
│  │  Router  │  │  Router  │  │  Router  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└───┬─────────────────┬─────────────────┬────────────────────┘
    │                 │                 │
    ▼                 ▼                 ▼
┌────────┐      ┌──────────┐     ┌──────────┐
│PostgreSQL│    │ ChromaDB │     │  GCS     │
│   DB    │    │ Vector DB│     │ Buckets  │
└────────┘      └──────────┘     └──────────┘
    │                                   │
    ▼                                   ▼
┌─────────────────────────────────────────────┐
│         Standalone Services                 │
│  ┌──────────────┐  ┌──────────────┐        │
│  │     Data     │  │     Data     │        │
│  │  Collector   │  │  Processor   │        │
│  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐  ┌──────────────┐        │
│  │    Model     │  │    Model     │        │
│  │   Training   │  │    Deploy    │        │
│  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐                          │
│  │ ML Workflow  │                          │
│  │ (Vertex AI)  │                          │
│  └──────────────┘                          │
└─────────────────────────────────────────────┘
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD pipeline
├── src/
│   ├── api-service/                  # Main FastAPI application
│   │   ├── routers/                  # API route handlers
│   │   │   ├── data.py              # Data operations endpoints
│   │   │   ├── rag.py               # RAG and vector search
│   │   │   └── model.py             # Model inference endpoints
│   │   ├── services/                # Business logic layer
│   │   ├── models/                  # Pydantic models
│   │   ├── migrations/              # Database migrations
│   │   ├── tests/                   # Unit tests
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── Dockerfile               # Container configuration
│   │   └── pyproject.toml           # Dependencies
│   ├── data-collector/              # Data ingestion service
│   ├── data-processor/              # Data preprocessing service
│   ├── model-training/              # ML training service
│   ├── model-deploy/                # Model serving service
│   ├── ml-workflow/                 # Vertex AI orchestration
│   └── frontend-react/              # React frontend
├── infrastructure/                   # Pulumi IaC for GCP
│   ├── __main__.py                  # Infrastructure definition
│   ├── Pulumi.yaml                  # Pulumi configuration
│   └── requirements.txt             # Pulumi dependencies
├── tests/                           # Integration tests
├── docker-compose.yml               # Local development (PostgreSQL, ChromaDB, API)
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── pyproject.toml                   # Root Python configuration
├── Makefile                         # Helper commands
└── README.md                        # This file
```

## Quick Start

### Prerequisites

- **Python 3.11+**
- **uv** - Fast Python package installer ([Install](https://github.com/astral-sh/uv))
- **Docker & Docker Compose** - For containerization
- **Node.js 20+** - For React frontend (optional)
- **Google Cloud SDK** - For GCP deployment (optional)
- **Pulumi CLI** - For infrastructure management (optional)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd project-setup-template

# Copy environment variables template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Install Dependencies

```bash
# Install Python dependencies with uv
make install

# Or manually
uv sync
```

### 3. Start Local Development Environment

```bash
# Start PostgreSQL, ChromaDB, and API service
make up

# Verify services are running
make ps
```

This will start:
- **PostgreSQL** on port 5432
- **ChromaDB** on port 8001
- **API Service** on port 8000

Access the API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4. Run Tests

```bash
# From project root
make test

# With coverage
make test-cov
```

## Development Workflow

### Local Development

1. **Start all services**:
   ```bash
   make up
   ```
   This starts PostgreSQL, ChromaDB, and the API service.

2. **View logs**:
   ```bash
   make logs              # All services
   make logs-postgres     # PostgreSQL only
   make logs-chroma       # ChromaDB only
   ```

3. **Run tests**:
   ```bash
   make test
   ```

4. **Code formatting**:
   ```bash
   make format
   make lint
   ```

### Building Docker Images

```bash
# Build API service
make build-api

# Build all services
make build-all
```

## Services

### API Service
**FastAPI-based REST API** serving as the main HTTP gateway.

- **Routers**: Modular endpoints for data, RAG, and models
- **Port**: 8000
- **Documentation**: `/docs` (Swagger UI)
- See: [src/api-service/README.md](src/api-service/README.md)

### Data Collector
**Standalone service** for collecting data from various sources.

- Fetch data from APIs, databases, or files
- Can be triggered via API or scheduled
- See: [src/data-collector/README.md](src/data-collector/README.md)

### Data Processor
**Data preprocessing and feature engineering** service.

- Clean and transform data
- Generate embeddings for vector search
- Prepare data for model training
- See: [src/data-processor/README.md](src/data-processor/README.md)

### Model Training
**ML model training** service with support for multiple frameworks.

- Train models locally or on Vertex AI
- Hyperparameter tuning
- Experiment tracking with MLflow
- See: [src/model-training/README.md](src/model-training/README.md)

### Model Deploy
**Model serving** for inference.

- Load models from GCS
- Single and batch predictions
- Model versioning and A/B testing
- See: [src/model-deploy/README.md](src/model-deploy/README.md)

### ML Workflow
**Pipeline orchestration** using Vertex AI Pipelines.

- Define end-to-end ML pipelines
- Schedule automated retraining
- Manage pipeline runs on GCP
- See: [src/ml-workflow/README.md](src/ml-workflow/README.md)

### Frontend React
**React-based UI** for interacting with the ML system.

- Data upload and visualization
- Model predictions interface
- RAG query interface
- See: [src/frontend-react/README.md](src/frontend-react/README.md)

## Databases

### PostgreSQL
**Relational database** for structured data.

- **Port**: 5432
- **Default credentials**: See `.env.example`
- **Migrations**: Use Alembic in `api-service/migrations/`

### ChromaDB
**Vector database** for embeddings and similarity search.

- **Port**: 8001
- **API**: http://localhost:8001
- **Collections**: Defined in application code

## Deployment

### Google Cloud Platform (GCP)

This template is designed for deployment to GCP using:
- **GKE** (Google Kubernetes Engine) for container orchestration
- **GCR** (Google Container Registry) for Docker images
- **GCS** (Google Cloud Storage) for data and models
- **Vertex AI** for ML workflows

### Infrastructure Setup

1. **Install Pulumi**:
   ```bash
   curl -fsSL https://get.pulumi.com | sh
   ```

2. **Configure GCP**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Deploy infrastructure**:
   ```bash
   cd infrastructure
   pip install -r requirements.txt
   pulumi stack init dev
   pulumi config set gcp:project YOUR_PROJECT_ID
   pulumi up
   ```

See [infrastructure/README.md](infrastructure/README.md) for detailed instructions.

### CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`) handles:

1. **Linting**: Ruff and Black checks
2. **Testing**: Pytest with coverage
3. **Building**: Docker image builds
4. **Deployment**: Push to GCR (when configured)

**Required Secrets**:
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_SA_KEY`: Service account key JSON

## Environment Variables

All configuration is managed through environment variables. Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `CHROMA_HOST`: ChromaDB host
- `GCP_PROJECT_ID`: Google Cloud project
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key

**Important**: Never commit `.env` or service account keys to Git!

## Secrets Management

### Local Development
- Use `.env` file (gitignored)
- Place GCP service account keys **outside** this repository

### Production
- Use Docker secrets (see `docker-compose.prod.yml`)
- Use GCP Secret Manager
- Use Kubernetes Secrets

## Testing

### Unit Tests
Located in each service's `tests/` directory:
```bash
cd src/api-service
uv run pytest
```

### Integration Tests
Located in `tests/` at project root:
```bash
pytest tests/
```

### Coverage
```bash
make test-cov
open htmlcov/index.html
```

## Code Quality

### Linting
```bash
make lint          # Check for issues
make lint-fix      # Auto-fix issues
```

### Formatting
```bash
make format        # Format code
make format-check  # Check formatting
```

## Common Commands

The `Makefile` provides helpful shortcuts:

```bash
make help          # Show all available commands
make install       # Install dependencies
make up            # Start databases
make down          # Stop databases
make logs          # View logs
make test          # Run tests
make lint          # Lint code
make format        # Format code
make clean         # Clean temporary files
make build-all     # Build all Docker images
```

## Best Practices

### Code Organization
- One service per directory in `src/`
- Each service is independently containerized
- Shared code goes in common packages

### API Design
- Use modular routers for different domains
- Implement proper error handling
- Document all endpoints with docstrings
- Use Pydantic models for validation

### Database
- Use migrations for schema changes
- Never commit database credentials
- Use connection pooling for performance

### Security
- Use environment variables for secrets
- Never commit `.env` or credentials
- Use non-root users in Docker containers
- Enable HTTPS in production
- Implement authentication/authorization

### Docker
- Multi-stage builds for smaller images
- Use `.dockerignore` to exclude files
- Non-root user for security
- Health checks for monitoring

### Testing
- Write tests for all critical functionality
- Use fixtures for common setup
- Mock external services
- Aim for high coverage

## Troubleshooting

### Database Connection Issues
```bash
# Check if databases are running
make ps

# View logs
make logs-postgres
make logs-chroma

# Restart services
make restart
```

### Docker Build Failures
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t service-name .
```

### Import Errors
```bash
# Reinstall dependencies
make clean
make install
```

## Contributing

### Adding a New Service

1. Create service directory in `src/`
2. Add `Dockerfile` and `pyproject.toml`
3. Update `docker-compose.yml` if needed
4. Add tests in service `tests/` directory
5. Document in service README
6. Update CI/CD workflow

### Making Changes

1. Create a feature branch
2. Make your changes
3. Run tests: `make test`
4. Format code: `make format`
5. Lint code: `make lint`
6. Commit with descriptive message
7. Push and create pull request

## Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pulumi GCP Guide](https://www.pulumi.com/registry/packages/gcp/)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### Tools
- [uv Documentation](https://github.com/astral-sh/uv)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Black Formatter](https://black.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

## License

[Add your license here]

## Support

For questions or issues:
1. Check the service-specific READMEs
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Contact the maintainers

---

**Happy Building!** 🚀
