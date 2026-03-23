# api/

FastAPI backend with DDD 4-layer architecture.

## Quick Reference

```bash
make setup    # Docker + deps + migrate
make dev      # uvicorn :8000 --reload
make test     # pytest (requires make up)
make quality  # ruff + mypy
```

## Code Style

- ruff: `line-length = 120`, B008 ignored (FastAPI Depends)
- mypy: `strict = true`, tests exempt from `disallow_untyped_defs`
- pytest: `asyncio_mode = "auto"`, fixtures in `tests/conftest.py`

## Layer Rules

- `domain/` → zero framework imports (pure Python)
- `application/` → abstract interfaces only (no SQLAlchemy/Redis)
- `infra/` → concrete implementations
- `interfaces/api/deps.py` → wires infra into abstractions via Depends()
