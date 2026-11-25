# 课程 04：FastAPI 与路由层

**目标**：薄路由、统一错误、依赖注入、可读 OpenAPI — 把 M0～M4 整理成「像样的 API 层」。

| 名称 | 路径 |
|------|------|
| 本实验室 | `D:\study\Octop\octop-mini` |
| 官方跟读 | `D:\study\Octop\Octop-main` |

## 先修

- **课程 03** 完成：login、JWT 中间件、`/api/auth/me`
- 能说清：`api/` 不直接写 SQL

## 文档

| 文件 | 用途 |
|------|------|
| [03-起点与现状.md](./03-起点与现状.md) | 已有代码 vs 本课要整理什么 |
| [01-微课.md](./01-微课.md) | 微课 4.1～4.5 |
| [02-章末复习.md](./02-章末复习.md) | 验收与设计题 |

## 建议顺序

1. [03-起点与现状.md](./03-起点与现状.md)  
2. [01-微课.md](./01-微课.md) 从 4.1  
3. [02-章末复习.md](./02-章末复习.md)

## 本课程结束后（目标形态）

```text
api/
  app.py              # 只 assemble：router + middleware + exception handlers
  deps.py             # get_runtime / get_services / current_user
  errors.py           # HTTP 映射
  routers/
    health.py         # /health（或迁到 /api/health）
    auth.py
    settings.py       # GET 绑定信息（只读 config）
infra/
  errors.py           # MiniError + ErrorCode 子集
```

## 常用命令

```powershell
cd D:\study\Octop\octop-mini
uv run pytest tests -q
uv run octop-mini run
# http://127.0.0.1:8765/docs
```

```powershell
cd D:\study\Octop\Octop-main
# 对照 build_app
uv run python -c "import inspect; from octop.api.app import build_app; print('ok')"
```

上一课：[课程 03](../course-03/README.md) · 下一课：[课程 05](../course-05/README.md)