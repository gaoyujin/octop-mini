# 课程 01：配置与进程模型

本目录是 **Phase 1** 教材副本，便于在 `octop-mini` 项目里边读边做。官方完整教学仍在主仓库：

`D:\study\Octop\Octop-main\docs\teaching\`

## 路径约定

| 名称 | 路径 |
|------|------|
| **本实验室（你正在写的代码）** | `D:\study\Octop\octop-mini` |
| **官方 Octop 源码（跟读用）** | `D:\study\Octop\Octop-main` |

动手命令都在**本实验室**执行；`阅读` 清单指 **Octop-main** 下的文件。

## 文档清单

| 文件 | 用途 |
|------|------|
| [01-微课.md](./01-微课.md) | **主路径**：微课 1.1～1.6，按顺序做 |
| [02-章末复习.md](./02-章末复习.md) | 整章验收、实验 A/B/C |
| [03-精读-launch与run_cmd.md](./03-精读-launch与run_cmd.md) | 微课 1.5 深读 |
| [04-ADR-单进程模型.md](./04-ADR-单进程模型.md) | 微课 1.1 必读 |
| [05-里程碑-M0-M2.md](./05-里程碑-M0-M2.md) | 本阶段要在本项目上叠的架子 |
| [07-微课-1.5-launch组合根-学习说明.md](./07-微课-1.5-launch组合根-学习说明.md) | 微课 1.5（`cli` → `launch`） |
| [08-微课-1.6-server-start第一段-学习说明.md](./08-微课-1.6-server-start第一段-学习说明.md) | **当前推荐**：微课 1.6（跟读 `OctopServer.start` 前半） |

## 建议顺序

1. [04-ADR-单进程模型.md](./04-ADR-单进程模型.md)（1.1）  
2. [01-微课.md](./01-微课.md) 从 **1.2** 起（M0 应已完成：`GET /health`）  
3. **当前节点**：[08-微课-1.6-server-start第一段-学习说明.md](./08-微课-1.6-server-start第一段-学习说明.md)  
4. 课程 01 收尾：[02-章末复习.md](./02-章末复习.md)

## 本实验室常用命令

```powershell
cd D:\study\Octop\octop-mini
uv sync
uv run pytest tests -q
uv run uvicorn mini.api.main:app --reload --host 127.0.0.1 --port 8765
```

## 下一课程

[课程 02：数据库与迁移](../course-02/README.md) · [课程 03：用户与 JWT](../course-03/README.md)

## 官方跟读常用命令

```powershell
cd D:\study\Octop\Octop-main
uv run octop run
uv run octop run --help
```