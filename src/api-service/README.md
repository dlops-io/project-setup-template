# API Service

FastAPI gateway for the app: exposes HTTP endpoints for data, RAG (vector search over ChromaDB), and
model inference. Everything the browser calls is under `/api`.

## Run it

With the whole stack, from `src`: `docker compose up --build`, then http://localhost:9000/api/docs.

In a shell, from this folder:

```bash
./docker-shell.sh
```

| Command | What it does |
|---|---|
| `api_server` | Run the API, reloading when you save: http://localhost:9000/api/docs |
| `pytest` | Run the tests |
| `uv add <package>` | Add a dependency (then rebuild the image) |

## Files

| File | What it does |
|---|---|
| `api/service.py` | The FastAPI app: add your routers here |
| `tests/` | Tests, run with `pytest` |
| `Dockerfile` | Production image: the virtualenv and `api/` only, as user 1000 |
| `Dockerfile.dev` | Development image: the dependencies; the code is mounted |
| `docker-entrypoint.dev.sh` | Defines `api_server`; with arguments runs them, otherwise opens a shell |
| `docker-shell.sh` | Shell in the running container, or builds and starts one |

## Settings

Environment variables, set in `src/docker-compose.yml` and `docker-shell.sh`:

| Variable | Value in development |
|---|---|
| `GCP_PROJECT` | Your GCP project ID |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/secrets/ml-workflow.json` |
| `CHROMADB_HOST`, `CHROMADB_PORT` | `vector-db`, `8000` |
| `DATABASE_URL` | `postgresql://mlops_user:mlops_password@postgres:5432/mlops_db` |
