# octop-mini（教学实验室）

与官方 Octop **独立**：在本地练架构；跟读对照 `D:\study\Octop\Octop-main`。

## 课程 01 文档（从这里学）

**[docs/course-01/README.md](docs/course-01/README.md)** — 配置与进程模型（微课 1.1～1.6）

## M0：当前能力

- `GET /health` → `{"ok": true}`

## 启动（微课 1.5：`cli` → `launch`）

```powershell
cd D:\study\Octop\Octop-mini
uv sync
uv run octop-mini run
uv run octop-mini run --port 9000 --reload
```

自定义数据目录：`$env:MINI_HOME = "D:\tmp\mini-lab"`；环境变量端口：`$env:MINI_PORT = "9000"`。

单测：`uv run pytest tests -q`

- <http://127.0.0.1:8765/health>
- <http://127.0.0.1:8765/docs>

## 验收（微课 1.2）

- [ ] `/health` 返回 200 且 `ok: true`
- [ ] 存在 `src/mini/api/` 与 `src/mini/infra/` 两个包

## 下一步

打开 **[docs/course-01/08-微课-1.6-server-start第一段-学习说明.md](docs/course-01/08-微课-1.6-server-start第一段-学习说明.md)**（微课 1.6，跟读官方 `OctopServer.start` 前半）。