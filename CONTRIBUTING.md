# 团队协作约定

先按 README 启动登录流程，检查本人资料可保存，再领取模块。共享后端入口、路由表、设计令牌及基础迁移由负责人协调修改。

## 分支与提交

从最新 main 建功能分支，例如 `feat/diagnosis`、`feat/rag-recommendations`、`feat/interviews`、`feat/job-records`。
一次 PR 解决一个可验收的功能；说明用户行为、接口或表变动、验证方式和未完成部分。合并前至少一名成员审阅。
各成员只提交源码与固定版本样例，不提交个人 `.env`、数据库、真实学生资料、模型权重或索引缓存。

## 公共契约

- API 统一 `/api/v1` 前缀和响应 envelope，ID 字符串传输。
- HttpOnly Cookie 是唯一浏览器认证方式，不新增 localStorage token。
- 写请求统一 Origin 校验。个人数据查询必须附加当前用户的归属条件，管理员权限复用后端依赖。
- 业务逻辑放 services，输入约束放 schemas，路由负责接收和响应，避免页面直接拼 SQL。
- 每次改表新增 Alembic revision，不修改已经被其他成员执行过的迁移；如果出现两个 head，先协调再创建 merge revision。
- 前端沿用白色与蓝色令牌、统一导航、字段和错误提示；新增图标使用 Phosphor，不手绘图标或使用 emoji。
- 不把视觉预览、随机分数或假模型调用混入真实业务。真实 API 失败要保留输入和明确状态。
- 原始数据版本不原地修改；新增版本后更新 manifest 和对应测试。`scripts/validate_data.py` 验证 data 与文档初始基线一致。

## 提交前检查

后端运行 pytest、Ruff 和 Alembic check；涉及数据库的改动在 MySQL 8 测试库验证。
前端运行 format:check 和 build，并在浏览器验证主要操作、刷新恢复、错误状态与窄屏。
CI 是本地检查的补充。首次上传后查看 Actions 的实际结果，再将团队开发基线标记为可用。

项目当前无许可证文件。仓库可见性和开源授权由项目组在创建 GitHub 仓库时决定。
