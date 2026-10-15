# MLOps Project Template

A starter layout for ML and agent apps. It defines the folder structure and shared local infrastructure (PostgreSQL and ChromaDB). Each service folder is a placeholder for you to build out, and every service runs in its own container.

## Project Structure

```
.
├── docker-compose.yml        # Local stack: PostgreSQL, ChromaDB, and app services
├── .env.example              # Environment variables template
└── src/
    ├── api-service/          # FastAPI gateway (data, RAG, model endpoints)
    ├── mcp-service/          # MCP server exposing tools to AI agents
    ├── data-collector/       # Data ingestion from APIs, files, databases
    ├── data-processor/       # Cleaning, feature engineering, embeddings
    ├── model-training/       # Training jobs (local or Vertex AI)
    ├── model-deploy/         # Model serving / inference
    ├── ml-workflow/          # Pipeline orchestration (Vertex AI Pipelines)
    ├── frontend-app/         # Web UI
    └── deployment/           # Infrastructure as code for GCP
```

## Service Layout

Each service is self-contained and should follow this layout:

```
src/<service-name>/
├── Dockerfile
├── pyproject.toml            # Dependencies, managed with uv
├── README.md
├── <source code>
└── tests/
```

## Quick Start

Prerequisites: Docker with Compose v2.

```bash
cp .env.example .env                    # then edit values
docker compose up -d postgres chromadb  # start the databases
docker compose ps
```

| Service    | Address               |
|------------|-----------------------|
| PostgreSQL | localhost:5432        |
| ChromaDB   | http://localhost:8001 |

`docker-compose.yml` also defines `api-service` (port 8000) and `mcp-server` (port 8080). They will start once their folders contain a `Dockerfile`.

Common commands:

```bash
docker compose logs -f <service>   # follow logs
docker compose down                # stop everything
docker compose down -v             # stop and delete database volumes
```

## Configuration

All configuration comes from environment variables. Copy `.env.example` to `.env`; Compose loads it into the app containers. Never commit `.env` or service account keys. Keep GCP keys outside the repository.

## Adding a Service

1. Create `src/<service-name>/` following the layout above.
2. Add it to `docker-compose.yml` if it should run locally.
