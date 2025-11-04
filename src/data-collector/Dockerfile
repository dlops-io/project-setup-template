# Dockerfile for Data Collector Service
# Using Python 3.12 with uv for fast dependency management

# Use the official Debian-hosted Python image
FROM python:3.12-slim-bookworm

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell Python to disable buffering so we don't lose any logs
ENV PYTHONUNBUFFERED=1

# Ensure we have an up to date baseline, install dependencies
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv

# Set working directory
WORKDIR /app

# Copy the source code
COPY . .

# Install dependencies with uv
RUN uv sync

# Default command (students can modify)
CMD ["uv", "run", "python", "main.py"]
