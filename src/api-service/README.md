# Data Collector Service

Standalone service for collecting data from various sources (APIs, web scraping, databases, files).

## Purpose

This service is responsible for:
- Fetching data from external sources
- Initial data validation
- Storing raw data in PostgreSQL or GCS
- Can be triggered by API or run as scheduled job

## Implementation Tasks

Students should implement:

1. **Data Sources**
   - API clients for external data sources
   - Web scraping logic
   - File reading capabilities
   - Database connectors

2. **Data Storage**
   - Save raw data to PostgreSQL
   - Upload files to GCS buckets
   - Track collection metadata

3. **Error Handling**
   - Retry logic for failed requests
   - Validation of collected data
   - Logging and monitoring

## Usage

### As a CLI tool:
```bash
python main.py --source <source_name> --output <path>
```

### As a scheduled job:
```bash
# Using cron or Kubernetes CronJob
```

### Via API:
The api-service can trigger this service through HTTP calls or message queues.

## Environment Variables

- `DATA_SOURCE_API_KEY`: API key for data sources
- `DATABASE_URL`: PostgreSQL connection string
- `GCS_BUCKET_DATA`: GCS bucket for raw data
- `COLLECTION_SCHEDULE`: Cron expression for scheduled runs

## Docker

Build:
```bash
docker build -t mlops-data-collector .
```

Run:
```bash
docker run mlops-data-collector
```
