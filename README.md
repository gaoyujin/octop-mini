# octop-mini（教学实验室）

与官方 Octop **独立**：在本地练架构；跟读对照 `D:\study\Octop\Octop-main`。

## 课程 01 文档（从这里学）

**[docs/course-01/README.md](docs/course-01/README.md)** — 配置与进程模型（微课 1.1～1.6）

## M0：当前能力

- `GET /health` → `{"ok": true}`

## 启动（M1：读 `~/.octop-mini/config.json`）

```powershell
cd D:\study\Octop\octop-mini
uv sync
uv run octop-mini
```

自定义数据目录：`$env:MINI_HOME = "D:\tmp\mini-lab"`；覆盖端口：`$env:MINI_PORT = "9000"`。

仍可用开发热重载：`uv run uvicorn mini.api.main:app --reload --host 127.0.0.1 --port 8765`

- <http://127.0.0.1:8765/health>
- <http://127.0.0.1:8765/docs>

## 验收（微课 1.2）

- [ ] `/health` 返回 200 且 `ok: true`
- [ ] 存在 `src/mini/api/` 与 `src/mini/infra/` 两个包

## 下一步

打开 [docs/course-01/01-微课.md](docs/course-01/01-微课.md)，从 **1.3（M1 配置）** 继续。