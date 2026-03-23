# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Get CRM Kit is an open-source CRM for international trade (外贸) SOHO sellers. It's a monorepo with three main components: a FastAPI backend, a TanStack Start admin console, and a Next.js marketing website.

**Current state**: v0.1.0 scaffold complete — DDD backend skeleton, frontend apps scaffolded, Docker Compose + CI configured.

## Monorepo Structure

```
getcrmkit.com/
├── api/                    # FastAPI backend (Python 3.14, uv)
│   ├── docker-compose.yml  # PG18 (15432) + Redis8 (16379)
│   ├── docker-compose.override.yml  # Dev overrides
│   ├── docker-compose.prod.yml      # Production with app service
│   ├── Makefile
│   └── .env.example
├── web/                    # Frontend monorepo (Bun + Biome)
│   ├── apps/
│   │   ├── console/        # TanStack Start (SPA, shadcn b0)
│   │   └── website/        # Next.js 16 (SSG, shadcn b0)
│   ├── packages/
│   │   ├── ui/             # Shared shadcn/ui (@workspace/ui)
│   │   └── typescript-config/
│   ├── biome.json
│   └── package.json
├── .env.example
├── .mcp.json               # shadcn MCP
├── Makefile                # Root: dev (overmind), setup
├── Procfile.dev            # Overmind
├── README.md / README.zh-CN.md / README.zh-TW.md
└── docs/
```

- **Package manager**: Bun (workspace for `web/apps/*` + `web/packages/*`), uv (for `api/`)
- **Database**: PostgreSQL 18 (15432) via asyncpg + SQLAlchemy 2.0
- **Cache/Queue**: Redis 8 (16379), arq (async task queue)
- **Process manager**: Overmind (Procfile.dev)
- **Linting/Formatting**: Biome (replaces ESLint + Prettier for frontend)
- **docker-compose.yml** is in `api/`; `api/Makefile` uses `docker compose` directly (no -f flag)

## Tech Stack

### Backend (`api/`)
- FastAPI 0.135+, Python 3.14 (stdlib first — e.g. `uuid.uuid7()` over third-party), SQLAlchemy 2.0 (async), Alembic
- PyJWT + bcrypt for auth, boto3 for file storage (S3/MinIO)
- Linting: ruff | Type checking: mypy | Testing: pytest (against Docker Compose services)

### Console (`web/apps/console/`)
- TanStack Start (SPA mode) + TanStack Router
- shadcn/ui (preset b0), TailwindCSS 4, @workspace/ui shared components
- lucide-react
- Routes: `src/routes/` (TanStack Router file-based routing)

### Website (`web/apps/website/`)
- Next.js 16 (App Router), static export (SSG)
- shadcn/ui (preset b0), TailwindCSS 4, @workspace/ui shared components
- next-themes, lucide-react
- Routes: `app/` (Next.js App Router)

## Common Commands

**Prerequisites:** Python 3.14+, Bun 1.2+, uv 0.6+, Docker Compose v2, Overmind 2.5+

```bash
# Root
make dev                          # Overmind: start all services
make setup                        # cd api && make setup && cd web && bun install

# API (api/)
make setup                        # docker compose up + uv sync + alembic migrate
make reset                        # down -v + fresh setup
make dev                          # uvicorn --reload :8000
make test                         # pytest
make test-v                       # pytest -v
make quality                      # ruff + mypy
make format                       # ruff format
make migrate                      # alembic upgrade head
make migration msg="add users"    # alembic autogenerate
make up / make down               # docker compose up/down

# Frontend (web/)
bun run dev:console               # Console :3100
bun run dev:website               # Website :3000
bun run check                     # Biome check
bun run check:fix                 # Biome autofix
bun run typecheck                 # TypeScript check
```

## Architecture

### Backend: Domain-Driven Design (DDD) + CQRS

```
api/app/
├── domain/          # Entities, value objects, domain events, repository interfaces
├── application/     # Commands/Queries (CQRS), UnitOfWork, EventBus
├── infra/           # SQLAlchemy models, Redis, email (IMAP/SMTP), S3, arq workers
├── interfaces/      # REST API (v1), Pydantic schemas, WebSocket
└── config/          # Settings, logging
```

Domain modules: auth, customer, sea_pool, follow_up, email, product, quotation, order, shared.

### Frontend: Feature-Based Architecture

```
src/
├── features/        # Self-contained domains (auth, customer, quotation, etc.)
│   └── <feature>/   # components/, hooks/, api/, types/
├── shared/          # Cross-feature: components, hooks, lib, stores, types
├── routes/          # TanStack Router file-based routes (console) / app/ (website)
└── styles/          # TailwindCSS globals
```

**Critical rule**: Features must NOT import from each other. Cross-feature utilities go in `shared/`.

### Dependency Injection (FastAPI)

`interfaces/api/deps.py` is the composition root — wires infrastructure into application abstractions:

```python
# Endpoints depend on abstractions, not concrete implementations
@router.post("/customers")
async def create(uow: AbstractUnitOfWork = Depends(get_uow)):
    ...
```

| Dependency | Provider | Use case |
|------------|----------|----------|
| `get_uow()` | `AbstractUnitOfWork` | Business transactions |
| `get_db()` | `AsyncSession` | Direct queries |
| `get_engine()` | `AsyncEngine` | Health checks |
| `get_redis()` | `Redis` | Cache/queue |

**Layer rule**: `application/` defines abstract interfaces, `infra/` provides implementations, `interfaces/api/deps.py` wires them together.

## Database Conventions

- **Primary keys**: UUID v7 — PG18 native `uuidv7()` + Python 3.14 native `uuid.uuid7()`
- **Soft deletes**: `deleted_at` field (NULL = active) on all business entities
- **Audit fields**: `created_by`, `updated_by`, `created_at`, `updated_at`
- **Multi-currency**: store `amount` + `currency` + `exchange_rate` + `amount_base` (RMB base)
- **Timestamps**: All `TIMESTAMPTZ` in UTC; frontend converts to user timezone
- **Custom fields**: JSONB columns for extensibility
- **Sort fields**: `position: int` for entity ordering (not `sort_order`); `sort: Literal["asc", "desc"]` for query direction (not `sort_order`)
- **Full-text search**: pg_trgm extension + GIN indexes

## Domain-Specific Concepts

- **Trade terms**: FOB, CIF, EXW (international shipping terms)
- **Profit calculation**: RMB as base currency, customer grade-based pricing tiers
- **Follow-up stages**: new → contacted → quoted → sample_sent → negotiating → ordered → lost
- **Quotation lifecycle**: draft → sent → following → confirmed → converted/expired/rejected
- **Sea pool (公海池)**: Shared customer pool with auto-recycle rules
- **5-document export**: PI / SC / CI / PL / B/L (standard trade documents)

## Key Documentation

> **Note:** `docs/` is gitignored (private). These files exist locally only.

| File | Purpose |
|------|---------|
| `docs/prd.md` | Product requirements, EspoCRM competitive analysis |
| `docs/structure.md` | Full technical architecture (500+ lines) |
| `docs/database.md` | Complete PostgreSQL DDL (35 tables) |
| `docs/v1.0.0-roadmap.md` | MVP development phases |
| `docs/pricing.md` | User personas, pricing tiers |
| `docs/seo.md` | SEO strategy for marketing site |
| `docs/domain.md` | Brand and deployment strategy |

## Git Branching Rules

- **main must be a straight line** — never use `git merge --no-ff`. Always rebase feature branches onto main, then fast-forward merge:
  ```bash
  git checkout -b temp <feature-tip>
  git rebase main
  git checkout main && git merge --ff-only temp
  git branch -D temp
  ```

## Commit Convention

Format: `<gitmoji> <description>`

Uses [gitmoji](https://gitmoji.dev/) convention. Most used:

| Emoji | When to Use |
|-------|---------------------------------------------|
| ✨    | New features |
| 🐛    | Bug fix |
| ♻️    | Refactor |
| ✅    | Tests |
| 📝    | Documentation |
| 🔧    | Configuration |
| 🔥    | Remove code/files |
| ⬆️    | Upgrade dependencies |
| 🎉    | Initial commit |

Full reference: https://gitmoji.dev/

Rules:
- Every commit must start with a gitmoji emoji.
- Keep subject line under 72 characters.
- **No AI attribution** — never include `Co-Authored-By` or any AI-related metadata in commits.

## Development Principles

- Prefer Python standard library over third-party unless the third-party option is clearly superior
- Frontend types are auto-generated from OpenAPI spec — do not manually duplicate API types
- Biome replaces ESLint + Prettier for all frontend linting and formatting
- Tests run against Docker Compose services (`make up` required before `make test`)
- No RBAC, sea pool, email integration, or audit logs in v1.0.0 MVP — those are v2.0.0+
- Website deploys as static export (SSG) for zero-cost CDN hosting
- Dual deployment: SaaS cloud and self-hosted Docker Compose from the same codebase

## Gotchas

- **PG18 Docker volume**: Mount at `/var/lib/postgresql` (not `/var/lib/postgresql/data`) — PG18 changed the data directory layout
- **`ruff` B008 ignored**: `Depends()` in FastAPI default args triggers B008; suppressed in `pyproject.toml`
- **`get_settings()` is cached**: Uses `@lru_cache` — call `.cache_clear()` in tests if overriding env vars
- **Python 3.14 `AsyncGenerator`**: Single type param `AsyncGenerator[T]` is valid (second param defaults to `None`); ruff UP043 flags the two-param form as unnecessary
