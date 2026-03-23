# Get CRM Kit

**专为外贸 SOHO 打造的开源 CRM 系统**

[English](README.md) | 简体中文 | [繁體中文](README.zh-TW.md)

---

## 核心功能

- **利润计算器** — 按产品实时分析成本与利润率
- **阶梯报价** — 根据数量自动生成梯度价格
- **五单一键导出** — 一键生成发票、装箱单、合同、形式发票和商业发票
- **客户跟进** — 追踪沟通记录，设置跟进提醒
- **话术模板** — 常用邮件和消息的可复用模板

## 技术栈

| 层级 | 技术 |
|------|------|
| API | FastAPI · Python 3.14 · SQLAlchemy · Alembic |
| 控制台 | TanStack Start · TypeScript |
| 官网 | Next.js 16 · TypeScript |
| 数据库 | PostgreSQL 18 · Redis 8 |
| 工具链 | uv · Bun · Turbo · Biome · Ruff · Mypy |
| 基础设施 | Docker Compose · Overmind |

## 快速开始

```bash
# 前置条件：Bun、Python 3.14+、uv、Docker、Overmind
make setup    # 安装依赖 + 启动数据库
make dev      # 通过 Overmind 启动所有服务
```

API 运行在 `http://localhost:8000`，控制台运行在 `http://localhost:3000`，官网运行在 `http://localhost:3001`。

## 项目结构

```
getcrmkit.com/
├── api/                # FastAPI 后端
│   ├── src/            # 应用源码
│   ├── tests/          # Pytest 测试
│   └── pyproject.toml
├── web/                # 前端 monorepo（Turbo）
│   ├── apps/console/   # TanStack Start — CRM 控制台
│   ├── apps/website/   # Next.js 16 — 营销官网
│   └── package.json
├── docker-compose.yml  # PostgreSQL + Redis
├── Makefile            # 开发命令
└── Procfile.dev        # Overmind 进程定义
```

## 开发命令

| 命令 | 说明 |
|------|------|
| `make setup` | 安装所有依赖并启动数据库 |
| `make dev` | 通过 Overmind 启动所有服务 |
| `make lint` | 运行 Ruff（API）和 Biome（前端） |
| `make test` | 运行 Pytest |
| `make format` | 自动格式化所有代码 |
| `make typecheck` | 运行 Mypy（API）和 TypeScript 检查（前端） |

## 参与贡献

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/my-feature`）
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT
