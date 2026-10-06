# TRACE GitHub 首次上传检查清单

检查日期：2026-10-06。对象：当前 0.1.0 起步项目。最初按“先检查要上传哪些文件”整理范围，随后按用户“帮我上传到 GitHub”的要求补齐提交前的排除规则。既定开发计划与业务代码未改变；下列检查结果保留审计时的状态，准备阶段更新见最后一节。

按用户最新要求，截图和设计对照资料全部留在本机。首次上传源码、可复现的依赖与迁移、开发文档、团队协作约定、固定合成样例及页面实际使用的两张图片。逐文件范围见 [GitHub首次上传文件清单.txt](GitHub首次上传文件清单.txt)，最终共 112 个文件。清单已由原先的 130 个文件剔除 16 张设计图片、截图对照报告和署名 Word 阅读版；后续新增或修改文件时需重新核对。

## 1. 建议上传的内容

| 内容 | 路径与说明 |
| --- | --- |
| 项目入口与协作约定 | `README.md`、`CONTRIBUTING.md`、`.editorconfig`、`.gitattributes`、`.gitignore` |
| 前端源码与配置 | `frontend/src/`、`index.html`、`vite.config.ts`、`tsconfig.json`、`.prettierrc.json` |
| 前端依赖与实际页面素材 | `frontend/package.json`、`package-lock.json`、`public/images/` 两张图片。图片是页面运行需要的生成素材，不能作为临时截图排除 |
| 后端源码与配置模板 | `backend/app/`、`backend/scripts/`、`pyproject.toml`、`requirements.lock`、`backend/.env.example` |
| 数据库迁移与测试 | `backend/alembic/`、`alembic.ini`、`backend/tests/`。新成员通过迁移创建当前已实现的表 |
| 本地配置与校验脚本 | `scripts/setup_local.py`、`lock_backend.py`、`validate_data.py`、`compare_design.ps1` |
| 开发数据库配置 | `compose.yaml`、根目录 `.env.example`。真实密码由各成员在本机生成 |
| 持续集成与 PR 模板 | `.github/workflows/ci.yml`、`.github/pull_request_template.md`，方便成员提交后执行检查 |
| 需求与设计规划 | 不含真实姓名的 `docs/TRACE需求分析与开发文档.md`、`TRACE数据库结构.sql`、`TRACE配置示例.env`；原 Word 仅保留本机 |
| 起步交接文档 | `docs/团队开发接力说明.md`、`起步接口说明.md`、`起步验证记录.md`，以及本检查报告与逐文件清单 |
| 固定演示数据与规则 | `data/` 以及 `docs/一期样例数据/`。后者含原基线、校验器和模型提示词；现有校验与 CI 依赖两套文件，暂不能删除其中一套 |
| 当前视觉约定与素材说明 | 配色令牌、共享组件、接力说明、就业图片生成提示词。截图和设计对照报告不上传 |
| 索引目录占位 | 仅 `artifacts/indexes/.gitkeep`。真实 BGE 索引以后由脚本生成，不上传生成产物 |

## 2. 不上传的内容

| 内容 | 原因与当前状态 |
| --- | --- |
| `backend/.env`、根目录真实 `.env` 及其他真实环境配置 | 本机密钥、密码与地址；现有 `.gitignore` 已忽略。只上传示例模板 |
| `backend/trace.db` 和其他本机数据库文件 | 含本机账号、密码哈希和测试记录；已忽略。成员使用空库迁移并自行注册 |
| `node_modules/`、`.venv/`、Conda 环境、`*.egg-info/` | 各机器独立安装；依赖由锁文件恢复，不上传整个 py312 环境 |
| `dist/`、`*.tsbuildinfo`、缓存、日志、测试产物 | 可重新生成；现有忽略规则已覆盖主要产物 |
| 原始 `附件1：沧州交通学院大学生创新训练计划项目申报书-0615修订.docx` | 原始申报材料涉及成员个人信息，不作为开发仓库的默认上传内容；已被 `/附件*.docx` 忽略 |
| `docs/TRACE需求分析与开发文档.docx` | 署名阅读版本仅保留本机，公开仓库使用按职责分工的 Markdown；已忽略 |
| `docs/.work/`、旧 `design/` 预览目录 | 内部文档处理与旧原型；已忽略 |
| 未采用的 `docs/design/style-*.png`、`implementation-*-v*.*`、`comparison-v*.png` | 旧风格与迭代产物；已忽略 |
| `docs/design/` 中全部 PNG/JPG/JPEG 图片及根目录 `design-qa.md` | 用户最新要求不上传截图与设计对照资料；已补充忽略规则，文件仍保留本机 |
| `.superpowers/` 整个目录 | 本地设计工具状态，含 `.last-token` 临时令牌文件；**当前尚未忽略，必须在提交前补充忽略规则**。本次没有读取或在报告中输出令牌值 |
| `docs/design/login-employment-mobile-v1.jpg` | 中间版本，正式 mobile 截图已有；**当前尚未忽略，应在提交前排除** |
| `docs/前端页面生成提示词.md` | 旧提示词要求 Tailwind、lucide、旧色值和无图片登录设计，并禁止玻璃效果，与用户后来确认的实现不一致；建议本次暂不上传，后续更新后再纳入，或明确归档为历史方案 |
| BGE 模型权重、向量索引、真实学生/招聘数据 | 本次没有交付这些内容；后续用下载/构建命令和独立数据管理方式提供 |

检查后已按上传要求补齐以下规则；正式提交按实际暂存清单再次确认：

```gitignore
/.superpowers/
/docs/design/login-employment-mobile-v*.jpg
/docs/design/*.png
/docs/design/*.jpg
/docs/design/*.jpeg
/design-qa.md
# 旧提示词更新之前暂时排除；更新后删除此规则
/docs/前端页面生成提示词.md
```

当前 README 中的 `git add .` 命令应在补齐上述排除项之后执行。不能直接按现有忽略规则全量添加。

## 3. 文档与代码核对结果

### 分期范围与实现进度

Markdown 与 Word 开发文档的主要范围一致：一期保留基础 BGE/RAG、真实大模型 API、基础收藏与手动投递；ARIMA、分级帮扶和辅导员闭环安排到二期。数据库按业务需求规划 12 张表，没有强制缩减到 6～8 张。

当前代码只完成注册、登录、退出、本人资料管理及相应页面与基础结构。RAG、真实 API、职业诊断、岗位业务、面试、持久化收藏/投递和管理业务仍待实现。设计预览中的收藏、投递与解释仅为页面原型，不是已经完成的业务功能。README、接力说明和验证记录已说明这些边界。

### 阅读顺序与契约优先级

1. `README.md`：环境准备、本机配置、启动和检查命令。
2. `docs/团队开发接力说明.md` 与 `CONTRIBUTING.md`：认领模块、分支协作、迁移与数据规则。
3. `docs/起步接口说明.md`：当前已经实现的认证与资料接口。
4. `docs/TRACE需求分析与开发文档.md`：一期后续需求、完整数据库、API 与二期规划。
5. `data/README.md`、样例提示词及验证记录：固定数据、测试依据和实际验证范围。

规划文档的 `/student/home`、`/student/profile` 与当前代码的 `/workspace`、`/profile` 不同。当前调试以 README、路由代码和起步接口说明为准；后续模块集成时统一路由并同步文档。`/api/v1/health` 是现有健康接口，规划中的 `/health/ready` 仍是后续目标。

Word 是阅读与分享版本，其中部分长接口名、表名含排版用的零宽字符；复制代码与标识符应使用 Markdown、SQL 或真实源码。

### 数据库与配置文件的使用边界

`docs/TRACE数据库结构.sql` 是完整一期设计，不是当前起步初始化脚本。现有 Alembic revision `0001_accounts` 只建立 `users` 与 `student_profiles`；不要在迁移前再运行整份 SQL。后续按模块增加迁移并保持单一 head。

`docs/TRACE配置示例.env` 是完整一期的配置规划；它的模型字段使用 `AI_*`，起步模板预留的是 `LLM_*`，当前 Settings 尚未消费模型配置。现阶段用 `scripts/setup_local.py` 生成配置，以 `backend/.env.example` 为运行模板。实现真实模型适配时统一这些命名并更新文档。

旧前端提示词需要更新或归档。正式风格依据应使用 `docs/团队开发接力说明.md`、现有 CSS 令牌、共享组件及可运行的 `/design-preview`；当前图标是 Phosphor，页面为蓝白风格，登录含就业背景，登录后导航为玻璃吸顶效果。设计参考图片和截图仅保留本机。

### 敏感信息与仓库可见性

对建议上传内容中的 108 个文本文件（包含 Word 正文提取内容）执行了常见 API/GitHub/AWS 密钥、私钥、手机号、邮箱特征检查，未发现匹配项；人工核对的 `.env.example` 和 `TRACE配置示例.env` 为占位值或空密钥。CI 中的 MySQL 密码明确用于临时测试服务，不是本机凭据。

初次检查发现开发文档的分工表包含真实成员及指导老师姓名，Word 也有这些内容。最终公开上传采用职责名称替代真实姓名的 Markdown，并排除署名 Word；原稿备份保存在已忽略的本机目录。业务需求、分工职责和阶段计划保持一致。当前没有 LICENSE 文件，不擅自指定开源授权。

## 4. 本轮实际检查与限制

- 已检查目录、现有忽略规则、前后端依赖文件、账号模型与迁移、路由、配置模板、CI、开发与交接文档。
- 已用电脑已有 Conda `py312` 重新运行 `scripts/validate_data.py` 和 `docs/一期样例数据/validate_samples.py`，两项均通过。
- 本轮没有修改应用代码，因此没有重复运行全套构建和账号回归；已有测试结果见 `docs/起步验证记录.md`。其中记录后端 29 项测试通过和前端构建通过。
- MySQL 8 实际运行、GitHub Actions 与真实 BGE/模型 API 联调尚未完成，不作为此次上传检查已经通过的项目。
- 为检查忽略规则，仅在已忽略的 `.cache/upload-audit/` 中创建了临时审计 Git 元数据，项目根目录仍没有 `.git`。该临时目录不属于上传范围。

## 5. 正式上传前的下一步

先确定 GitHub 仓库地址和可见性，再补齐本报告列出的忽略项、处理旧提示词，初始化根目录 Git 仓库并逐项核对暂存范围。首次提交应包含本清单中的协作基础，不包含本机环境和原始申报书。完成推送后再确认 GitHub Actions 的实际运行结果，并为成员提供仓库链接与 README 启动入口。

## 6. 上传准备更新（2026-10-06）

已补充 `.superpowers/`、就业背景中间截图及旧前端提示词的忽略规则。旧提示词继续保留在本机，正式设计依据不变。README 已更新为团队克隆后使用功能分支的协作方式。首次提交按逐文件清单核对，最终远程地址、提交信息和 CI 结果由上传完成后的回执提供，不将准备状态当成上传成功。

暂存检查发现 Git 默认换行转换会改变固化 JSON 的字节哈希，已在 `.gitattributes` 对 `data/**/*.json` 与 `docs/一期样例数据/*.json` 禁用文本换行转换，保留原始字节。提交前核对暂存区中的数据字节与 manifest、原基线一致，避免成员拉取或 Linux CI 首次校验即失败。

用户随后自行创建并明确选择公开仓库 [dongsong0715-master/TRACE](https://github.com/dongsong0715-master/TRACE)。插件已确认账号有写入权限；仓库可见性按用户选择执行，原始申报书、真实配置与本机数据继续排除。README 已加入已核实的仓库克隆地址。

用户进一步要求截图资料不上传。最终仓库文件树剔除全部截图、设计参考与对照图片和 `design-qa.md`；这些文件只从待提交范围中排除，不删除本机文件。页面实际引用的两张 `frontend/public/images/` 素材继续保留，相关文档已移除对未上传截图的开发依赖。

创建公开文件树时，自动审批因署名开发文档包含成员及指导老师个人信息而拒绝操作。已采用更安全的公开版本：Markdown 的五个实名分工替换为职责名称，署名 Word 不纳入远程提交，原 Markdown 备份至本机已忽略目录。完成这些处理后重新上传最终 112 文件树，不改变应用功能或业务方案。
