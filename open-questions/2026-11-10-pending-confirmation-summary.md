# 待确认问题汇总(共 4 项)

**日期:** 2026-11-10
**状态:** 待确认

| # | 待确认问题 | 要确认的内容 | 确认对象 | 结论 |
| --- | --- | --- | --- | --- |
| 1 | Global Filter 的 Well List 来源 | Global Filter 里的井列表从哪里来(哪个 API / 数据源) | 待补充 | 待确认 |
| 2 | DFS Base API 的启用方式 | 如何启用 DFS Base API(开关 / 配置 / 环境) | 待补充 | 待确认 |
| 3 | Different Production Method 的固定 Parameter List | 不同生产方式(如 OILSF / OILESP / GASF / OILGL)是否各有固定的参数列表,具体清单是什么 | 待补充 | 待确认 |
| 4 | Save Template API 的使用必要性 | 是否必须使用 Save Template API,还是可以不用 | 待补充 | 待确认 |

> 「要确认的内容」一列是根据标题推断的,请核对后修正;「确认对象」和「结论」确认后回填。
> 确认后按 [README](README.md) 约定,把结论迁入 architecture-decision/ 或 domain-knowledge/。

## 沟通术语

| 术语 | 说明 |
| --- | --- |
| Global Filter | 页面全局筛选(如 Field / WHP / Well / Date Range),见 [requirements-index](../feature-history/requirements-index.md) |
| Well List | Global Filter 中的井列表 |
| DFS Base API | DFS 基础 API |
| Production Method | 生产方式:`OILSF`、`OILESP`、`GASF`、`OILGL` |
| Parameter List | 某生产方式下固定展示/使用的参数清单 |
| Save Template API | 保存模板的接口 |
