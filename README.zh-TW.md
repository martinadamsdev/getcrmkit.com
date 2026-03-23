# Get CRM Kit

**專為外貿 SOHO 打造的開源 CRM 系統**

[English](README.md) | [简体中文](README.zh-CN.md) | 繁體中文

---

## 核心功能

- **利潤計算器** — 按產品即時分析成本與利潤率
- **階梯報價** — 根據數量自動產生梯度價格
- **五單一鍵匯出** — 一鍵產生發票、裝箱單、合約、形式發票和商業發票
- **客戶跟進** — 追蹤溝通記錄，設定跟進提醒
- **話術範本** — 常用郵件和訊息的可重複使用範本

## 技術棧

| 層級 | 技術 |
|------|------|
| API | FastAPI · Python 3.14 · SQLAlchemy · Alembic |
| 控制台 | TanStack Start · TypeScript |
| 官網 | Next.js 16 · TypeScript |
| 資料庫 | PostgreSQL 18 · Redis 8 |
| 工具鏈 | uv · Bun · Turbo · Biome · Ruff · Mypy |
| 基礎設施 | Docker Compose · Overmind |

## 快速開始

```bash
# 前置條件：Bun、Python 3.14+、uv、Docker、Overmind
make setup    # 安裝依賴 + 啟動資料庫
make dev      # 透過 Overmind 啟動所有服務
```

API 運行在 `http://localhost:8000`，控制台運行在 `http://localhost:3000`，官網運行在 `http://localhost:3001`。

## 專案結構

```
getcrmkit.com/
├── api/                # FastAPI 後端
│   ├── src/            # 應用程式原始碼
│   ├── tests/          # Pytest 測試
│   └── pyproject.toml
├── web/                # 前端 monorepo（Turbo）
│   ├── apps/console/   # TanStack Start — CRM 控制台
│   ├── apps/website/   # Next.js 16 — 行銷官網
│   └── package.json
├── docker-compose.yml  # PostgreSQL + Redis
├── Makefile            # 開發指令
└── Procfile.dev        # Overmind 程序定義
```

## 開發指令

| 指令 | 說明 |
|------|------|
| `make setup` | 安裝所有依賴並啟動資料庫 |
| `make dev` | 透過 Overmind 啟動所有服務 |
| `make lint` | 執行 Ruff（API）和 Biome（前端） |
| `make test` | 執行 Pytest |
| `make format` | 自動格式化所有程式碼 |
| `make typecheck` | 執行 Mypy（API）和 TypeScript 檢查（前端） |

## 參與貢獻

1. Fork 本專案
2. 建立功能分支（`git checkout -b feature/my-feature`）
3. 提交變更
4. 發起 Pull Request

## 授權條款

MIT
