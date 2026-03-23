# Get CRM Kit

**Open-source CRM for international trade SOHO sellers (外贸 SOHO)**

English | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

---

## Features

- **Profit Calculator** — Real-time cost and margin analysis per product
- **Tiered Pricing** — Automatic quantity-based price breaks for quotations
- **5-Document Export** — Generate invoice, packing list, contract, PI, and CI in one click
- **Customer Follow-up** — Track communication history and schedule reminders
- **Script Templates** — Reusable email and message templates for common scenarios

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI · Python 3.14 · SQLAlchemy · Alembic |
| Console | TanStack Start · TypeScript |
| Website | Next.js 16 · TypeScript |
| Database | PostgreSQL 18 · Redis 8 |
| Tooling | uv · Bun · Turbo · Biome · Ruff · Mypy |
| Infra | Docker Compose · Overmind |

## Quick Start

```bash
# Prerequisites: Bun, Python 3.14+, uv, Docker, Overmind
make setup    # Install deps + start DB
make dev      # Start all services via Overmind
```

The API runs at `http://localhost:8000`, the console at `http://localhost:3000`, and the website at `http://localhost:3001`.

## Project Structure

```
getcrmkit.com/
├── api/                # FastAPI backend
│   ├── src/            # Application source
│   ├── tests/          # Pytest test suite
│   └── pyproject.toml
├── web/                # Frontend monorepo (Turbo)
│   ├── apps/console/   # TanStack Start — CRM console
│   ├── apps/website/   # Next.js 16 — Marketing site
│   └── package.json
├── docker-compose.yml  # PostgreSQL + Redis
├── Makefile            # Developer commands
└── Procfile.dev        # Overmind process definitions
```

## Development Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install all dependencies and start databases |
| `make dev` | Start all services via Overmind |
| `make lint` | Run Ruff (API) and Biome (Frontend) |
| `make test` | Run Pytest |
| `make format` | Auto-format all code |
| `make typecheck` | Run Mypy (API) and TypeScript check (Frontend) |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Open a pull request

## License

MIT
