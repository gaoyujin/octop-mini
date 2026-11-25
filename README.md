# octop-mini（教学实验室）

与官方 Octop **独立**：在本地练架构；跟读对照 `D:\study\Octop\Octop-main`。

## 课程文档

| 课程 | 入口 |
|------|------|
| 01 配置与进程 | [docs/course-01/README.md](docs/course-01/README.md) |
| 02 数据库与迁移 | [docs/course-02/README.md](docs/course-02/README.md) |
| **03 用户认证与 JWT（当前）** | **[docs/course-03/README.md](docs/course-03/README.md)** |

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

打开 **[docs/course-03/README.md](docs/course-03/README.md)**，先读 **03-起点与里程碑-M4**，再跟 **01-微课** 从 3.1 起。