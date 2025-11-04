# Data Processor Service

Service for data preprocessing, cleaning, feature engineering, and transformation.

## Purpose

This service handles:
- Data cleaning and validation
- Feature engineering
- Data transformation and normalization
- Preparing data for model training
- Generating embeddings for vector database

## Implementation Tasks

Students should implement:

1. **Data Cleaning**
   - Handle missing values
   - Remove duplicates
   - Data type conversions
   - Outlier detection

2. **Feature Engineering**
   - Create derived features
   - Encoding categorical variables
   - Feature scaling and normalization
   - Feature selection

3. **Transformations**
   - Text preprocessing for NLP
   - Image preprocessing for vision models
   - Time series transformations
   - Generate embeddings

4. **Pipeline Management**
   - Save preprocessing pipelines
   - Version control for transformations
   - Reproducible processing

## Usage

### Process raw data:
```bash
python main.py --input <raw_data_path> --output <processed_data_path>
```

### Generate embeddings:
```bash
python main.py --mode embeddings --input <text_data> --output <embeddings>
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `GCS_BUCKET_DATA`: Input data bucket
- `GCS_BUCKET_PROCESSED`: Processed data bucket
- `EMBEDDING_MODEL`: Model for generating embeddings

## Docker

Build:
```bash
docker build -t mlops-data-processor .
```

Run:
```bash
docker run mlops-data-processor
```
