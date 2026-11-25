# 课程 03：用户认证与 JWT

在 **`D:\study\Octop\octop-mini`** 边做边学；官方教材在 **`D:\study\Octop\Octop-main\docs\teaching\`**。

## 先修

- **课程 02** 完成：`UserRepo`、`schema_version == 2`
- 能说清：请求应从 `api` 进、`infra` 存哈希与查用户

## 路径约定

| 名称 | 路径 |
|------|------|
| 本实验室 | `D:\study\Octop\octop-mini` |
| 官方跟读 | `D:\study\Octop\Octop-main` |

## 文档清单

| 文件 | 用途 |
|------|------|
| [01-微课.md](./01-微课.md) | **主路径**：微课 3.1～3.5 |
| [02-章末复习.md](./02-章末复习.md) | 验收、官方实验 |
| [03-起点与里程碑-M4.md](./03-起点与里程碑-M4.md) | 课程 02 已有啥、M4 要叠啥 |

## 建议顺序

1. [03-起点与里程碑-M4.md](./03-起点与里程碑-M4.md)
2. [01-微课.md](./01-微课.md) 从 **3.1** 起（3.1/3.5 部分只读官方）
3. [02-章末复习.md](./02-章末复习.md)

## 本课程结束后 mini 应具备（目标）

- 迁移 **003**：`users.password_hash`
- `UserManager`（或等价的 `infra/users` 服务）argon2 校验
- `POST /api/auth/login` → JWT
- 中间件：无 token 访问受保护路由 **401**；`/health` 仍公开

## 常用命令

```powershell
cd D:\study\Octop\octop-mini
uv run pytest tests -q
uv run octop-mini run
# 打开 http://127.0.0.1:8765/docs 试登录
```

```powershell
cd D:\study\Octop\Octop-main
uv run pytest tests/unit -k "auth or jwt or users" -q
```

上一课：[课程 02](../course-02/README.md) · 下一课：[课程 04](../course-04/README.md)