# 课程 02：数据库与迁移

在 **`D:\study\Octop\octop-mini`** 边做边学；官方教材在 **`D:\study\Octop\Octop-main\docs\teaching\`**。

## 先修

- **课程 01** 完成（含 1.6 `boot_control_plane`）
- 已在 mini 具备：`open_database`、`run_migrations` v1、`SharedServices` 壳子（见 § 起点）

## 路径约定

| 名称 | 路径 |
|------|------|
| 本实验室 | `D:\study\Octop\octop-mini` |
| 官方跟读 | `D:\study\Octop\Octop-main` |

## 文档清单

| 文件 | 用途 |
|------|------|
| [01-微课.md](./01-微课.md) | **主路径**：微课 2.1～2.5 |
| [02-章末复习.md](./02-章末复习.md) | 验收、实验、设计题 |
| [03-起点与里程碑.md](./03-起点与里程碑.md) | 1.6 已有什么、本课程要叠什么 |

## 建议顺序

1. 读 [03-起点与里程碑.md](./03-起点与里程碑.md)（避免重复造轮子）
2. 按 [01-微课.md](./01-微课.md) 从 **2.1** 或 **2.3** 开始（2.2/2.3 部分你已在 1.6 做过）
3. 章末：[02-章末复习.md](./02-章末复习.md)

## 常用命令

```powershell
cd D:\study\Octop\octop-mini
uv run pytest tests -q
uv run octop-mini run
```

```powershell
cd D:\study\Octop\Octop-main
uv run pytest tests/unit/db -q
```

上一课：[课程 01](../course-01/README.md) · 下一课预告：课程 03（用户 / JWT）