"""API service. Everything the browser calls is under /api; the probes stay at the root.

/api/status   the version, and the settings the container was started with
/api/docs     FastAPI's interactive docs
/healthz      liveness: the process is up

Routes live under /api because the dev proxy (vite.config.js) and nginx forward the full path.
Add your own routers here, for example: app.include_router(data.router, prefix="/api/data")
"""

import os

from fastapi import FastAPI

app = FastAPI(title="MLOps App API", docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.get("/api/status")
def get_status():
    return {
        "version": "0.1.0",
        "gcp_project": os.getenv("GCP_PROJECT"),
        "chromadb_host": os.getenv("CHROMADB_HOST"),
    }


@app.get("/healthz")
def healthz():
    return {"ok": True}
