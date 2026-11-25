# Agent 回答"UI Entry 增删改查示例"让用户无法理解

**日期:** 2026-11-25
**状态:** 待确认
**来源:** 用户粘贴的 agent 回答(未注明是哪个 agent、用户原问题是什么)

## 回答内容摘要(原样整理)

回答以"当然,下面给你举一个完整的例子,并明确你必须提供哪些信息"开头,按 4 个操作各给一个 JSON 示例:

| 操作 | 声称"必须提供" | 示例 JSON 的关键字段 |
| --- | --- | --- |
| 创建 | app_id、名称、类型(entry 或 module)、配置内容 | `action: create`、`resource: entry`、`app_id: "APP123"`、`payload`(name/type/fields/layout/permissions) |
| 更新 | record_id、更新内容 | `action: update`、`record_id: "ENTRY456"`、`payload.fields` |
| 删除 | record_id、`confirm_delete: true` | `action: delete`、`record_id`、`confirm_delete` |
| 查询 | app_id(可选) | `action: query-by-appid`、`resource: entry`、`app_id` |

结尾:"如果你有具体的业务场景或字段需求,可以直接告诉我,我帮你生成更贴合实际的操作示例。"

## 为什么用户读不懂(我的判断,非用户原话,请核对)

1. **直接暴露内部调用格式**:`action` / `resource` / `payload` 是工具调用 schema,用户看到的是机器参数,不是"怎么操作"。
2. **术语未解释**:`app_id`、`record_id`、`entry` 与 `module` 的区别、`payload` 都没说明含义,也没说**去哪里找这些 ID**。
3. **示例值是虚构的**:`APP123`、`ENTRY456`、"生产报表""日期/产量/班组"并非用户系统里的真实数据,易被误认为真实可用值。`[未证实]` 这些字段名、取值(如 `layout: table`、`permissions: view/edit`)是否与真实接口一致。
4. **没说明谁来执行**:是用户自己拼 JSON 提交,还是 agent 代为调用?"你必须提供"与"我帮你生成"自相矛盾。
5. **语义不清**:不知道这些 UI Entry 是什么、属于哪个系统(如 harmony-ui)、与用户当前任务(如画产量曲线)有何关系;也没有说明哪些操作会修改线上数据。
6. **命名不一致**:查询用 `query-by-appid`,其余用 `create/update/delete`,又没有"按 record_id 查询"。
7. **删除风险只用 `confirm_delete: true` 带过**,没有提示不可恢复/影响范围。

## 待确认问题

| # | 问题 | 要确认的内容 | 确认对象 | 结论 |
| --- | --- | --- | --- | --- |
| 1 | 用户原问题与上下文 | 这条回答对应的用户问题是什么、来自哪个 agent(是否 dspdm-agent) | 待补充 | 待确认 |
| 2 | 示例是否对应真实接口 | `action/resource/payload`、`query-by-appid`、`confirm_delete` 等是否真实存在及其参数名 | 待补充 | 待确认 |
| 3 | 面向用户的表达 | 用户应该看到"操作步骤/表单项"而不是 JSON;是否需要在系统提示里规定"不向用户展示内部调用格式,必要时用自然语言 + 真实值" | 待补充 | 待确认 |
| 4 | ID 来源 | 用户如何获得 `app_id`、`record_id`(UI 上哪里看、能否由 agent 先查询再回填) | 待补充 | 待确认 |
| 5 | 虚构示例的标注 | 示例值必须标明"示例"并优先使用真实数据,或先查询真实 entry 再演示 | 待补充 | 待确认 |
| 6 | 写操作确认流程 | 创建/更新/删除前是否应由 agent 复述影响并让用户确认,而不是只靠参数 | 待补充 | 待确认 |

> 与 [dspdm-agent 合并趋势图行为待确认](2026-11-25-dspdm-agent-oil-rate-multiline-chart.md) 同为 agent 回答质量问题,可合并评估(如"回答要贴近用户任务、少暴露内部细节、先执行再说明")。
> 确认后按 [README](README.md) 约定迁入 architecture-decision/ 或 domain-knowledge/。
