.PHONY: help install dev test lint format clean run bootstrap migrate

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Install dev dependencies"
	@echo "  make run          - Run application"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code"
	@echo "  make bootstrap    - Initialize database"
	@echo "  make migrate      - Run migrations"
	@echo "  make clean        - Clean up temporary files"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt

run:
	python -m app.main

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=html
	lint:
	flake8 app/ tests/
	pylint app/
	bandit -r app/

format:
	black app/ tests/
	isort app/ tests/

bootstrap:
	python scripts/bootstrap.py

migrate:
	python scripts/migrate.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .tox
