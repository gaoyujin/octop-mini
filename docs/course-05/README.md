# 课程 05：Agent 与 Harness 运行时

**目标**：在 mini 里落地 **M5** — Agent 表、归属、启停状态机与工作区目录；**不接入真实 LLM / octop-harness**。

| 名称 | 路径 |
|------|------|
| 本实验室 | `D:\study\Octop\octop-mini` |
| 官方跟读 | `D:\study\Octop\Octop-main` |

## 先修

- **课程 04** 完成：薄路由、`MiniError`、`get_services`、`GET /api/settings/bind`
- 课程 03：**JWT** + `current_user`
- 能理解：业务在 `infra/`，HTTP 在 `api/routers/`

## 文档

| 文件 | 用途 |
|------|------|
| [03-起点与里程碑-M5.md](./03-起点与里程碑-M5.md) | M5 积木与目录演进 |
| [01-微课.md](./01-微课.md) | 微课 5.1～5.6 |
| [02-章末复习.md](./02-章末复习.md) | 官方精读与验收 |

## 建议顺序

1. [03-起点与里程碑-M5.md](./03-起点与里程碑-M5.md)  
2. [01-微课.md](./01-微课.md) — **5.1 只读**，再从 5.2  
3. [02-章末复习.md](./02-章末复习.md)

## 本课程结束后（目标形态）

```text
infra/
  db/migrations/004_agents.sql     # schema v4
  db/repos/agents.py
  agents/manager.py                # create / start / stop（内存 registry + mock）
  agents/workspace.py              # 在 MINI_HOME/agents/<agent_id>/ 建目录
api/
  routers/agents.py                # 列表、创建、启停（需 JWT + 归属）
tests/
  test_agents_repo.py
  test_agents_api.py
```

## 常用命令

```powershell
cd D:\study\Octop\octop-mini
uv run pytest tests -q
uv run octop-mini run
# /docs → agents 相关路由
```

```powershell
cd D:\study\Octop\Octop-main
rg "from octop_harness" src/octop/infra/agents -l
uv run pytest tests/unit/agents -m "not live" -q
```

## 与官方的刻意缩小

| 官方 | mini 课程 05 |
|------|----------------|
| `octop-harness`、`HarnessAgent` | **不装依赖**；`last_state` 字符串 + 内存表 |
| `providers`、模型解析 | 微课 5.4 **只读官方** |
| `BackendWorkspace` | 本地 `Path.mkdir` 占位，注释对照文档 |
| Dashboard 创建 Agent | 5.6 **只读官方** API 与路由索引 |

上一课：[课程 04](../course-04/README.md) · 下一课：[课程 06](../course-06/README.md)