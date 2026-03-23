.PHONY: setup reset dev install test test-cov test-v lint format typecheck quality migrate migration migrate-down up down logs

COMPOSE := docker compose

setup:
	$(COMPOSE) up -d
	uv sync
	uv run alembic upgrade head

reset:
	$(COMPOSE) down -v
	$(MAKE) setup

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

install:
	uv sync

test:
	uv run pytest -v

test-cov:
	uv run pytest --cov=app --cov-report=term-missing

test-v:
	uv run pytest -v

lint:
	uv run ruff check app tests
	uv run ruff format --check app tests

format:
	uv run ruff format app tests

typecheck:
	uv run mypy app

quality: lint typecheck

migrate:
	uv run alembic upgrade head

migration:
	uv run alembic revision --autogenerate -m "$(msg)"

migrate-down:
	uv run alembic downgrade -1

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f
