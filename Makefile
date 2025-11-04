.PHONY: help install install-dev up down restart logs lint format test clean build

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)MLOps Project Template - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	@echo "$(BLUE)Installing dependencies with uv...$(NC)"
	uv sync

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	uv sync --dev

up: ## Start all services (databases)
	@echo "$(BLUE)Starting services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "PostgreSQL: localhost:5432"
	@echo "ChromaDB: localhost:8001"

down: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker-compose down

restart: ## Restart all services
	@echo "$(YELLOW)Restarting services...$(NC)"
	docker-compose restart

logs: ## Show logs from all services
	docker-compose logs -f

logs-postgres: ## Show PostgreSQL logs
	docker-compose logs -f postgres

logs-chroma: ## Show ChromaDB logs
	docker-compose logs -f chromadb

ps: ## Show running containers
	docker-compose ps

lint: ## Run linting with ruff
	@echo "$(BLUE)Running ruff linter...$(NC)"
	uv run ruff check .

lint-fix: ## Run linting and auto-fix issues
	@echo "$(BLUE)Running ruff with auto-fix...$(NC)"
	uv run ruff check --fix .

format: ## Format code with black
	@echo "$(BLUE)Formatting code with black...$(NC)"
	uv run black .

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code formatting...$(NC)"
	uv run black --check .

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	uv run pytest

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	uv run pytest --cov --cov-report=html --cov-report=term

clean: ## Clean up temporary files and caches
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-volumes: ## Remove all Docker volumes (WARNING: deletes data!)
	@echo "$(YELLOW)Removing Docker volumes...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)Volumes removed!$(NC)"

build-api: ## Build API service Docker image
	@echo "$(BLUE)Building API service...$(NC)"
	docker build -t mlops-api-service:latest ./src/api-service

build-all: ## Build all service Docker images
	@echo "$(BLUE)Building all services...$(NC)"
	docker build -t mlops-api-service:latest ./src/api-service
	docker build -t mlops-data-collector:latest ./src/data-collector
	docker build -t mlops-data-processor:latest ./src/data-processor
	docker build -t mlops-model-training:latest ./src/model-training
	docker build -t mlops-model-deploy:latest ./src/model-deploy
	@echo "$(GREEN)All services built!$(NC)"

shell-postgres: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U mlops_user -d mlops_db

check-env: ## Check if .env file exists
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Warning: .env file not found!$(NC)"; \
		echo "$(BLUE)Copy .env.example to .env and fill in your values:$(NC)"; \
		echo "  cp .env.example .env"; \
		exit 1; \
	else \
		echo "$(GREEN).env file found!$(NC)"; \
	fi

init: check-env install up ## Initialize project (check env, install deps, start services)
	@echo "$(GREEN)Project initialized!$(NC)"
	@echo "Next steps:"
	@echo "  1. Review and update .env file"
	@echo "  2. Run 'make test' to verify setup"
	@echo "  3. Start developing!"
