.PHONY: help install install-dev install-docs test test-cov test-browser test-headed lint format clean docs pre-commit setup

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

install-docs: ## Documentation dependencies are not currently configured
	@echo "No docs extras configured; documentation is maintained in markdown under docs/."

install-all: install install-dev ## Install all dependencies

setup: ## Setup development environment
	pre-commit install
	playwright install

test: ## Run all tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=tests --cov-report=html --cov-report=term-missing

test-browser: ## Run tests in specific browser (usage: make test-browser BROWSER=firefox)
	pytest --browser $(BROWSER)

test-headed: ## Run tests in headed mode (visible browser)
	pytest --headed

test-slow: ## Run only slow tests
	pytest -m slow

test-integration: ## Run integration tests
	pytest -m integration

lint: ## Run linting tools
	pre-commit run --all-files

format: ## Format code with black and isort
	black .
	isort .

type-check: ## Run mypy type checking
	mypy tests/

clean: ## Clean up generated files
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -rf test-results/ playwright-report/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs: ## Documentation build is not currently configured
	@echo "Documentation is maintained in markdown files under docs/."

docs-serve: ## Documentation serve is not currently configured
	@echo "Documentation is maintained in markdown files under docs/."

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	pre-commit autoupdate

update-deps: ## Update dependencies
	pip install --upgrade -r requirements.txt
	pip install --upgrade -e ".[dev,docs]"

build: ## Build distribution packages
	python -m build

release: clean test lint build ## Prepare for release
	@echo "Ready for release!"

# Default target
.DEFAULT_GOAL := help