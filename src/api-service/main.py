"""
FastAPI Application Entry Point

This is the main application file that initializes the FastAPI app
and registers all routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers (these will be implemented by students)
# from routers import data, rag, model

app = FastAPI(
    title="MLOps API Service",
    description="API service for MLOps project with data processing, RAG, and model inference",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for container orchestration."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "api-service",
            "version": "0.1.0",
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "MLOps API Service",
        "docs": "/docs",
        "health": "/health",
    }


# Register routers (uncomment as you implement them)
# app.include_router(data.router, prefix="/api/v1/data", tags=["Data"])
# app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
# app.include_router(model.router, prefix="/api/v1/model", tags=["Model"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
