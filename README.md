# TRACE

大学生就业赋能平台 · 团队开发起步仓库

当前版本 **0.1.0**：Vue 3 + TypeScript 前端、FastAPI 后端、SQLAlchemy 数据访问、Alembic 迁移，已实现学生注册、登录、退出、本人资料编辑与受保护页面。前端采用最新确认的第 1 张设计：白色导航、蓝色强调、灰色个人画像侧栏，以及岗位列表与详情并排的三栏工作区。

完整需求依据：[一期与二期开发文档](docs/TRACE需求分析与开发文档.md)。本仓库是该计划的第一步，RAG、真实模型调用、诊断、面试、收藏、投递和内容维护尚待团队开发。ARIMA、分级帮扶及辅导员闭环属于二期。

## 先跑起来

先克隆团队仓库，再执行下面的环境准备。所有配置和账号都在成员自己的电脑生成。

```powershell
git clone https://github.com/dongsong0715-master/TRACE.git
cd TRACE
```

需要 Python 3.12、Node.js 22.12+（建议团队统一 Node 24），以及 Conda。MySQL 8 是业务数据库路线；本次起步同时支持 SQLite 快速开发，以便没有数据库服务的成员先验证登录。

### 1. 后端

在项目根目录执行。你的电脑已有 `py312`，直接激活即可；其他成员没有此环境时先运行 `conda create -n py312 python=3.12`。

```powershell
conda activate py312
python --version
cd backend
python -m pip install -r requirements.lock
python -m pip install -e . --no-deps
cd ..
python scripts/setup_local.py
cd backend
python -m alembic upgrade head
python -m uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

配置命令生成随机 JWT 密钥、`backend/.env` 和本机数据库地址，不覆盖已有配置。应用不会启动时自动建表，必须显式运行迁移。注册后密码以 Argon2id 哈希保存，没有默认账号或默认密码。

如果终端还不能识别 `conda`，你的电脑可直接使用：

```powershell
cd backend
& 'D:\Develop\anaconda_envs\envs\py312\python.exe' -m uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

这个绝对路径仅是当前电脑的快捷方式，团队其他成员使用各自已激活的环境。

### 2. 前端

另开终端，从项目根目录执行：

```powershell
cd frontend
npm ci
npm run dev
```

打开 **http://localhost:5173**，点击“创建学生账号”，注册后登录。可编辑昵称、学历、岗位方向和意向城市；刷新仍保持会话，退出后重新访问受保护页面会回到登录页。

前端通过 `/api` 代理到后端，不在浏览器保存 JWT，也不需要前端 API 密钥。开发时请使用 `localhost`；若改为 `127.0.0.1` 或其他地址，需要同步修改 `backend/.env` 的 `PUBLIC_ORIGIN` 并重启后端，否则写请求会被 Origin 校验拒绝。

其他入口：

- 已选风格的交互预览：http://localhost:5173/design-preview 。该页面明确标识演示内容，候选切换、收藏和投递只作用于当前预览，刷新后清空；不会调用 RAG 或写入业务表。
- API 文档：http://127.0.0.1:8000/docs 。写请求需要请求头 `Origin: http://localhost:5173`；推荐直接从页面验证登录流程。
- 健康检查：http://127.0.0.1:8000/api/v1/health 。

### 3. 使用 MySQL 8

本机现有的 MySQL 5.7 不是本项目的目标数据库，起步代码未启动或修改该服务。团队可安装 Docker Desktop，使用独立 MySQL 8.4 容器（绑定本机 3307，避免占用已有 3306）：

```powershell
# 新克隆、尚未生成 backend/.env 时，在根目录执行
python scripts/setup_local.py --database mysql
docker compose up -d --wait
cd backend
python -m alembic upgrade head
python -m uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

配置命令会创建根目录 `.env`，为数据库应用账号与 root 分别生成密码。已有 SQLite 配置时，命令会拒绝覆盖；请自行保存配置备份，再参照 `.env.example` 配置独立 MySQL，并修改 `backend/.env` 的 `DATABASE_URL`。切换连接后执行迁移；已有 SQLite 数据不会自动搬迁。

也可连接自己准备的 MySQL 8：使用 `mysql+pymysql://用户名:URL编码后的密码@主机:端口/数据库`，数据库需先创建，字符集为 utf8mb4。不要在业务环境使用测试数据库或 CI 中的临时密码。

`docs/TRACE数据库结构.sql` 是完整一期设计参考；**当前从空库运行 Alembic 即可，不要先执行该 SQL**，否则账号表重复创建。后续成员按模块逐次加入迁移，当前只落地 `users`、`student_profiles`，不限制最终表数。

## 目录与职责

```text
TRACE/
├─ frontend/
│  ├─ src/api/              # 类型、统一请求、账号接口
│  ├─ src/components/       # 导航、认证布局、共享字段
│  ├─ src/router/           # 路由与会话守卫
│  ├─ src/stores/           # Pinia 会话状态，不持久化令牌
│  ├─ src/styles/           # 设计令牌与基础样式
│  ├─ src/views/            # 真实登录、工作台、资料与独立预览
│  └─ src/dev/              # 仅供视觉预览的固定虚构内容
├─ backend/
│  ├─ app/api/              # 路由、身份和角色依赖
│  ├─ app/core/             # 配置、数据库、安全与错误响应
│  ├─ app/models/           # SQLAlchemy 模型
│  ├─ app/schemas/          # Pydantic 输入约束
│  ├─ app/services/         # 业务事务与资料版本控制
│  ├─ app/algorithms/       # diagnosis / retrieval 待开发边界
│  ├─ app/ai/               # provider / prompts / validation 待开发边界
│  ├─ scripts/              # 创建管理员；后续导入与索引命令
│  ├─ alembic/versions/     # 版本化迁移，0001 为账号基础
│  └─ tests/                # 权限、会话、资料与配置测试
├─ data/demo/v1/            # 已固化的虚构岗位、题库、画像和异常样例
├─ data/rules/v1/           # 固定问卷和初版规则
├─ artifacts/indexes/       # 后续真实 BGE 索引，产物不入 Git
├─ docs/                    # 需求、协作分工、接口约定、设计依据
├─ scripts/                 # 本地配置、样例校验、依赖锁定
├─ .github/                 # PR 模板与 SQLite/MySQL 测试流水线
└─ compose.yaml             # 仅本地 MySQL 服务
```

团队分工与开发顺序见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [团队开发接力说明](docs/团队开发接力说明.md)。不要只建一批空路由返回成功；新增模块需有自己的输入约束、事务、权限和可验证行为。

## 已实现接口

| 方法 | 地址 | 行为 |
| --- | --- | --- |
| POST | `/api/v1/auth/register` | 只能注册 student，同时创建本人资料；用户名统一小写 |
| POST | `/api/v1/auth/login` | 校验密码，设置 2 小时 HttpOnly Cookie |
| POST | `/api/v1/auth/logout` | 递增 token_version，使本账号全部现有会话失效 |
| GET | `/api/v1/me` | 返回本人账号与资料，ID 为字符串 |
| PATCH | `/api/v1/me/profile` | 学生修改自己的资料，必须提交当前 version |
| GET | `/api/v1/health` | 数据库及账号表连接检查 |

接口成功返回 `{data, request_id}`，失败返回 `{error: {code, message}, request_id}`。详见 [起步接口说明](docs/起步接口说明.md)。管理员使用 `cd backend` 后的 `python -m scripts.create_admin` 在本机交互创建，密码不回显；当前没有管理员内容维护界面。

## 检查与构建

```powershell
# backend 中
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m alembic check

# frontend 中
npm run format:check
npm run build

# 根目录
python scripts/validate_data.py
```

依赖分别锁定在 `backend/requirements.lock` 与 `frontend/package-lock.json`。更新后端依赖时，先改 `pyproject.toml`、安装并验证，再在根目录执行 `python scripts/lock_backend.py`，不要把整个共享 Conda 环境 `pip freeze` 到仓库。

CI 同时配置 SQLite 与专用 MySQL 8 测试库。只有显式设置 `TRACE_TEST_DATABASE_URL` 且库名为 `trace_test` 时，后端测试才使用 MySQL；测试会清理该测试库中的账号与资料。不要将这个变量指向业务库。

本机已执行情况见 [起步验证记录](docs/起步验证记录.md)。配置 CI 不代表已在 GitHub 执行；正式部署、真实 RAG/API 联调及后续业务验收另行开展。

## Git 与团队协作

`.gitignore` 已排除 `.env`、本机数据库、依赖、缓存、索引产物、内部文档处理目录、本地设计工具状态、截图与设计对照资料、过期设计提示词和包含成员信息的原始申报书。提交内容为项目代码、开发说明、页面运行素材及合成样例。首次范围检查见 [GitHub上传检查清单](docs/GitHub首次上传检查清单.md)。

项目组成员克隆仓库后，在自己的功能分支提交。每次提交前检查待提交清单与差异：

```powershell
git switch -c feat/your-module
git add .
git status --short
git diff --cached --stat
git diff --cached
git commit -m "feat: describe your module change"
git push -u origin feat/your-module
```

前端生产构建是静态文件，部署时要将 `/api` 反向代理给后端，并将其他前端路由回退到 `index.html`。生产配置要求 MySQL、HTTPS、`COOKIE_SECURE=true` 和对应 `PUBLIC_ORIGIN`；当前任务交付的是本地团队开发起步项目。
