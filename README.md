# MLOps Project Template

A starter layout for ML and agent apps. Every service runs in its own container, and Docker is the only
thing your laptop needs: no Python or Node.

Three services are ready to run and copy from:

| Service | Pattern | Runs |
|---|---|---|
| `api-service` | Web service (FastAPI) | Always, reloads when you save |
| `frontend-app` | Web frontend (React + Vite, nginx in production) | Always, reloads when you save |
| `data-processor` | Job: runs a command and stops | When you ask for it |

The other folders are placeholders: build them out by copying the pattern that fits.

## Project Structure

```
.
└── src/
    ├── docker-compose.yml    # Local stack: PostgreSQL, ChromaDB, API, frontend, jobs
    ├── api-service/          # FastAPI gateway (data, RAG, model endpoints)
    ├── frontend-app/         # Web UI
    ├── data-processor/       # Cleaning, feature engineering, embeddings (the job example)
    ├── data-collector/       # Data ingestion from APIs, files, databases
    ├── model-training/       # Training jobs (local or Vertex AI)
    ├── model-deploy/         # Model serving / inference
    ├── ml-workflow/          # Pipeline orchestration (Vertex AI Pipelines)
    ├── mcp-service/          # MCP server exposing tools to AI agents
    └── deployment/           # Infrastructure as code for GCP
```

## Prerequisites

- Docker with Compose v2, and ports 3000, 9000, 8000 and 5432 free.
- A `secrets` folder **next to** this repository (not inside it) for GCP service account keys:

```
Academics/
├── secrets/
│   └── ml-workflow.json        # your GCP service account key
└── <this-repo>/
```

The containers mount it read-only at `/secrets`. Nothing needs a key until your code calls GCP.

- Your GCP project ID: search for `CHANGE TO YOUR PROJECT ID` in `src/docker-compose.yml` and the
  `docker-shell.sh` scripts, and replace `your-gcp-project`.

## Quick Start

```bash
cd src
```

```bash
docker compose up --build
```

The first run takes a few minutes to build the images. Then:

| What | Address |
|---|---|
| Frontend | http://localhost:3000 |
| API docs | http://localhost:9000/api/docs |
| ChromaDB | http://localhost:8000 |
| PostgreSQL | localhost:5432 (user `mlops_user`, password `mlops_password`, database `mlops_db`) |

The frontend calls `/api/status` and shows the answer, so a page that says "The API is up" means the
browser, the frontend and the API are all connected.

Run a job:

```bash
docker compose run --rm data-processor cli.py --check
```

Stop everything with Ctrl-C, then `docker compose down`. Add `-v` to delete the database volumes too.

## Working in a container

Each service folder has a `docker-shell.sh`. It gives you a bash shell in that service's container, with
your code mounted and a list of the commands you can run:

```bash
cd src/api-service
```

```bash
./docker-shell.sh
```

If `docker compose up` is already running the service, the script opens a shell in that container.
Otherwise it builds the image and starts one on its own, on the same `mlops-app-network`.

## Service Layout

Each service is self-contained and follows the files of the pattern it uses:

| File | Web service (`api-service`, `frontend-app`) | Job (`data-processor`) |
|---|---|---|
| `Dockerfile` | Production image: multi-stage, only what runs | The one image, for development and as a job |
| `Dockerfile.dev` | Development image: tools and dependencies; the code is mounted | — |
| `docker-entrypoint.dev.sh` / `docker-entrypoint.sh` | Starts the container: with arguments it runs them (that is how docker compose starts the server), without them it opens a shell | With arguments it runs `python <args>` and stops (a Kubernetes Job or pipeline step), without them it opens a shell |
| `docker-shell.sh` | Shell in the running container, or builds and starts one | Builds and starts a container |
| `.dockerignore` | What stays out of the image | What stays out of the image |
| `pyproject.toml` + `uv.lock` / `package.json` + `package-lock.json` | Dependencies. Commit the lockfile. | Dependencies. Commit the lockfile. |
| `tests/` | Tests | Tests, when you add them |

### Dependencies

Add Python packages from inside the container, so `uv.lock` is resolved for Linux:

```bash
uv add <package>
```

Then rebuild the image (`docker compose up --build`, or run `docker-shell.sh` again). For the frontend,
`npm install <package>` in its shell.

### Development and production images

The browser always calls `/api/...` on the page's own origin. In development, Vite forwards it to
`api-service` (`frontend-app/vite.config.js`); in production, nginx does (`nginx.conf.template`, which
reads `API_URL`). So there are no API addresses in the frontend code and no CORS.

To build and try a production image:

```bash
docker build -t mlops-app-api-service-prod src/api-service
```

## Adding a Service

1. Create `src/<service-name>/` by copying the folder whose pattern fits: `api-service` for a web
   service, `data-processor` for a job.
2. Rename the image and container names (`mlops-app-...`) in its scripts.
3. Add it to `src/docker-compose.yml` if it should run locally. Give a job `profiles: ["jobs"]` so
   `docker compose up` does not run it.
