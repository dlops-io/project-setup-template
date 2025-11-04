# MCP Server Usage Examples

This document provides examples of how to use the MCP Server in your MLOps project.

## Starting the Server

### Using Docker Compose (Recommended)

```bash
# From the project root directory
docker-compose up mcp-server
```

### Using Docker

```bash
# Build the image
cd src/mcp-server
docker build -t mcp-server .

# Run the container
docker run -p 8080:8080 mcp-server
```

### Local Development

```bash
# Install dependencies
cd src/mcp-server
uv sync --all-extras

# Run the server
uv run python src/server.py
```

## Available Tools

### 1. Get Model Information

Retrieve detailed information about a specific model.

```python
# Tool: get_model_info
# Parameters:
#   - model_name: string (required)

# Example response:
{
    "model_name": "sentiment-classifier",
    "status": "active",
    "version": "1.0.0",
    "accuracy": 0.95,
    "last_updated": "2024-11-04",
    "description": "Model information for sentiment-classifier"
}
```

### 2. List Available Models

Get a list of all models in the system.

```python
# Tool: list_available_models
# Parameters: none

# Example response:
[
    {
        "model_name": "sentiment-classifier",
        "type": "classification",
        "status": "active",
        "accuracy": 0.95
    },
    {
        "model_name": "text-generator",
        "type": "generation",
        "status": "active",
        "accuracy": 0.88
    }
]
```

### 3. Get System Health

Check the health status of the MLOps platform.

```python
# Tool: get_system_health
# Parameters: none

# Example response:
{
    "status": "healthy",
    "services": {
        "api": "running",
        "database": "running",
        "vector_db": "running",
        "mcp_server": "running"
    },
    "uptime": "99.9%",
    "active_models": 3
}
```

### 4. Trigger Model Training

Start a new model training job.

```python
# Tool: trigger_model_training
# Parameters:
#   - model_name: string (required)
#   - dataset_path: string (required)
#   - epochs: integer (default: 10)

# Example response:
{
    "job_id": "train-12345",
    "model_name": "sentiment-classifier",
    "dataset_path": "/data/training.csv",
    "epochs": 10,
    "status": "queued",
    "estimated_duration": "50 minutes",
    "message": "Training job for sentiment-classifier has been queued"
}
```

### 5. Get Model Metrics

Retrieve performance metrics for a model.

```python
# Tool: get_model_metrics
# Parameters:
#   - model_name: string (required)
#   - metric_type: string (default: "accuracy")
#     Options: "accuracy", "precision", "recall", "f1"

# Example response:
{
    "model_name": "sentiment-classifier",
    "metric_type": "accuracy",
    "value": 0.95,
    "all_metrics": {
        "accuracy": 0.95,
        "precision": 0.93,
        "recall": 0.94,
        "f1": 0.935
    },
    "timestamp": "2024-11-04T12:00:00Z"
}
```

## Available Resources

### 1. MLOps Configuration

```python
# Resource URI: config://mlops
# Returns: Configuration information as formatted text
```

### 2. Models List

```python
# Resource URI: models://list
# Returns: Formatted list of all available models
```

## Using with Claude Desktop

To connect Claude Desktop to this MCP server, add the following to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "mlops": {
      "command": "docker",
      "args": ["exec", "-i", "mlops-mcp-server", "python", "src/server.py"],
      "env": {}
    }
  }
}
```

Or if running locally:

```json
{
  "mcpServers": {
    "mlops": {
      "command": "uv",
      "args": ["run", "python", "src/server.py"],
      "cwd": "/path/to/project/src/mcp-server",
      "env": {}
    }
  }
}
```

## Testing

Run the test suite to verify everything is working:

```bash
cd src/mcp-server
uv run pytest
```

With coverage:

```bash
uv run pytest --cov --cov-report=term
```

## Environment Variables

Configure the MCP server using these environment variables:

- `MCP_PORT` - Port to run the server on (default: 8080)
- `API_SERVICE_URL` - URL of the API service for backend integration

Set these in your `.env` file:

```env
MCP_PORT=8080
API_SERVICE_URL=http://api-service:8000
```

## Troubleshooting

### Server won't start

1. Check if the port is already in use:
   ```bash
   lsof -i :8080
   ```

2. Verify dependencies are installed:
   ```bash
   cd src/mcp-server
   uv sync --all-extras
   ```

3. Check the logs:
   ```bash
   docker-compose logs mcp-server
   ```

### Can't connect to API service

Make sure the API service is running and accessible:

```bash
docker-compose ps
curl http://localhost:8000/health
```

## Next Steps

1. **Extend the tools**: Add more tools in [src/server.py](src/server.py) to expose additional functionality
2. **Add authentication**: Implement authentication for secure access
3. **Integrate with API**: Connect the MCP server to the actual API service for real data
4. **Add more resources**: Create additional resources for documentation and configuration
