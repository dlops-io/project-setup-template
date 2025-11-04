# MCP Server

FastMCP-based Model Context Protocol server for the MLOps platform.

## Overview

This MCP server provides tools and resources for AI agents to interact with the MLOps platform. It exposes functionality for model management, training, metrics, and system health monitoring.

## Features

### Tools

- `get_model_info` - Retrieve information about a specific model
- `list_available_models` - List all available models in the system
- `get_system_health` - Get health status of the MLOps system
- `trigger_model_training` - Trigger a model training job
- `get_model_metrics` - Get performance metrics for a model

### Resources

- `config://mlops` - MLOps system configuration
- `models://list` - Formatted list of all available models

## Development

### Local Setup

```bash
cd src/mcp-server
uv sync --all-extras
uv run python src/server.py
```

### Running with Docker

```bash
docker build -t mcp-server .
docker run -p 8080:8080 mcp-server
```

### Running with Docker Compose

From the project root:

```bash
docker-compose up mcp-server
```

## Testing

```bash
cd src/mcp-server
uv run pytest
```

## Configuration

The MCP server can be configured using environment variables:

- `MCP_PORT` - Port to run the server on (default: 8080)
- `API_SERVICE_URL` - URL of the API service for backend integration

## Integration

### Connecting from an MCP Client

The server runs on port 8080 and uses the standard MCP protocol. Configure your MCP client to connect to:

```
http://localhost:8080
```

Or when running in Docker Compose:

```
http://mcp-server:8080
```

## Architecture

```
src/mcp-server/
├── src/
│   ├── __init__.py
│   └── server.py          # Main FastMCP server implementation
├── Dockerfile             # Docker container configuration
├── pyproject.toml         # Python dependencies
└── README.md             # This file
```

## Technologies

- **FastMCP** - Fast Model Context Protocol implementation
- **Python 3.11** - Runtime environment
- **Pydantic** - Data validation
- **uvicorn** - ASGI server
