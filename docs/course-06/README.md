# 课程 06：对话、线程与 WebSocket

**目标**：在 mini 里落地 **M6** — `threads` 表、REST 元数据、Dashboard 风格 **WebSocket** 假流式（**echo**，不调 harness/LLM）。

| 名称 | 路径 |
|------|------|
| 本实验室 | `D:\study\Octop\octop-mini` |
| 官方跟读 | `D:\study\Octop\Octop-main` |

## 先修

- **课程 05**：`agents` 表、归属、`start` mock
- **课程 03～04**：JWT、`assert_agent_owner`、薄路由
- 能区分：`thread_id`（DB 对话容器）与运行时会话键（官方 `session_key`，本课先简化）

## 文档

| 文件 | 用途 |
|------|------|
| [03-起点与里程碑-M6.md](./03-起点与里程碑-M6.md) | M6 积木与协议草图 |
| [01-微课.md](./01-微课.md) | 微课 6.1～6.6 |
| [02-章末复习.md](./02-章末复习.md) | 官方精读与验收 |

## 建议顺序

1. [03-起点与里程碑-M6.md](./03-起点与里程碑-M6.md)  
2. [01-微课.md](./01-微课.md) — **6.3/6.4/6.6 可只读官方**，实现从 6.1 → 6.5  
3. [02-章末复习.md](./02-章末复习.md)

## 本课程结束后（目标形态）

```text
infra/db/migrations/005_threads.sql    # v5
infra/db/repos/threads.py
infra/db/repos/messages.py             # 可选：简单历史
infra/chat/echo.py                     # WS 回显 + 写入 messages
api/routers/threads.py                 # GET/POST …/agents/{id}/threads
api/routers/chat/ws.py                 # WS /api/agents/{id}/chat/ws?token=
api/deps.py                            # resolve_user_from_token（供 WS）
tests/test_threads_api.py
tests/test_chat_ws.py
```

## 常用命令

```powershell
cd D:\study\Octop\octop-mini
uv run pytest tests -q
uv run octop-mini run
```

```powershell
cd D:\study\Octop\Octop-main
uv run pytest tests/unit -k "chat or thread or ws" -m "not live" -q
```

## 与官方的刻意缩小

| 官方 | mini 课程 06 |
|------|----------------|
| `GlobalProcessor`、harness 流 | **WS echo** + JSON `{type,user_text,assistant_text}` |
| `session_key` / channel 多样 | 固定 `channel_type=dashboard` |
| `history/projection` 全量 | 直读 `messages` 表或内存 |
| IM 入站 | **不做**（课程 07） |

上一课：[课程 05](../course-05/README.md) · 下一课预告：课程 07（Gateway 与 IM）