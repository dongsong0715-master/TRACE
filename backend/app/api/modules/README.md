# 一期模块待实现

新增岗位、诊断、推荐、面试、收藏、投递和公共内容维护路由时，在此按业务拆文件，并由 main.py 注册。
统一复用 dependencies.py 的 DB、CurrentUser、StudentUser、require_admin，以及 errors.py 的响应结构。
服务逻辑放 app/services，模型放 app/models，输入输出约束放 app/schemas。
个人资源必须按服务端鉴权 user.id 限定归属；客户端不得传入另一个 user_id。
新业务表添加 Alembic revision。不要执行文档 SQL 后再运行 0001_accounts；两者会重复建表。
不提前创建二期 forecast、aid 或 counselor 路由。
