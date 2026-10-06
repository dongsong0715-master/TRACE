# 固定演示数据

来源是 docs/一期样例数据 的已生成基线，内容按字节复制，不改变 demo-v1 / rules-v1 标识。
manifest 位于 demo/v1，其中 rules.json、diagnosis_template.json 的相对位置为 ../../rules/v1。
运行 python scripts/validate_data.py 检查新目录内容；原校验器仍验证 docs/一期样例数据 的字段、计数和确定性案例。
后续导入与检索直接读取 data 目录。禁止修改原版本后继续沿用旧哈希，应创建新版本并保存新规则和案例。
这些文件不是招聘信息、真实学生资料或专家审定规则。当前起步只实现账号与资料，不自动导入岗位或问卷。
