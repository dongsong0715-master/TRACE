# 页面模块

auth、workspace、profile、system 为当前已实现页面。design 为已选视觉方向的独立演示原型，内容来自 dev/fixtures.ts，不使用真实推荐接口。
新增业务页面按 diagnosis、jobs、recommendations、interviews、favorites、applications、admin 分目录，按需创建真实路由。
不要将预览数据接入个人工作台或伪装成 RAG / AI 结果。复用 styles/tokens.css 和共享控件，不引入全新的视觉系统。
