# Data Collector

Ingests raw data from external sources (APIs, files, databases) and stores it in PostgreSQL or GCS.

A job: copy the [`data-processor`](../data-processor/README.md) folder, which runs one command and stops, and replace its `cli.py` with your steps.
