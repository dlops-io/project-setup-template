# MLOps Project Template

A starter template for ML and agent apps: a FastAPI gateway, an MCP server, PostgreSQL and ChromaDB, plus scaffolds for data, training, and deployment services. Every service has its own `Dockerfile` and `pyproject.toml` (managed with [uv](https://docs.astral.sh/uv/)), and local development runs through Docker Compose.

## Project Structure

```
.
├── docker-compose.yml        # Local stack: PostgreSQL, ChromaDB, API, MCP
├── .env.example              # Environment variables template
└── src/
    ├── api-service/          # FastAPI gateway (routers: data, rag, model)
    ├── mcp-service/          # FastMCP server exposing tools to AI agents
    ├── data-collector/       # Data ingestion (scaffold)
    ├── data-processor/       # Cleaning, features, embeddings (scaffold)
    ├── model-training/       # Training jobs (scaffold)
    ├── model-deploy/         # Model serving (scaffold)
    ├── ml-workflow/          # Vertex AI pipelines (scaffold)
    ├── frontend-app/         # Frontend (scaffold)
    └── deployment/           # Pulumi IaC for GCP (GKE, GCS, IAM)
```

Services marked *scaffold* contain only a `Dockerfile`, `pyproject.toml`, and `README.md`. Add your code there.

## Quick Start

Prerequisites: Docker with Compose v2.

```bash
cp .env.example .env        # then edit values
docker compose up -d --build
docker compose ps
```

| Service      | URL                                |
|--------------|------------------------------------|
| API (Swagger)| http://localhost:8000/docs         |
| API health   | http://localhost:8000/health       |
| MCP server   | localhost:8080                     |
| ChromaDB     | http://localhost:8001              |
| PostgreSQL   | localhost:5432                     |

Common commands:

```bash
docker compose logs -f api-service   # follow logs for one service
docker compose restart api-service   # restart a service
docker compose down                  # stop everything
docker compose down -v               # stop and delete database volumes
```

## Development

- **API routes** live in `src/api-service/routers/`. Uncomment the `include_router` lines in `main.py` as you implement them.
- **Business logic** goes in `src/api-service/services/`; database migrations go in `migrations/`.
- **MCP tools** are defined in `src/mcp-service/src/server.py`.
- **Tests** live in each service's `tests/` folder.

## Configuration

All configuration comes from environment variables. Copy `.env.example` to `.env`; Compose loads it into the API and MCP containers. Never commit `.env` or service account keys. Keep GCP keys outside the repository.

## Deployment

Infrastructure for GCP is defined with Pulumi in `src/deployment/`. See [src/deployment/README.md](src/deployment/README.md) for setup and `pulumi up` instructions.

## Adding a Service

1. Create `src/<service-name>/` with a `Dockerfile`, `pyproject.toml`, and `README.md`.
2. Add it to `docker-compose.yml` if it should run locally.
3. Put its tests in `src/<service-name>/tests/`.
