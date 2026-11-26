# 🔍 <mark>分析沉淀:需求分析与方案取舍</mark>

`analysis/`

需求分析与方案分析沉淀区。用于把项目分析过程以文档形式保存，便于后续人员复盘、接手与追踪。

## 适用内容

- 需求澄清记录（范围、边界、假设）
- 方案对比与选型依据（为什么选 A，不选 B）
- 风险识别与缓解策略
- 影响评估（业务、接口、数据、前端、测试、发布）
- 待确认事项与决策清单

## 命名建议

`YYYY-MM-DD-<topic>-analysis.md`

例如：

- `2026-11-09-wtv-map-side-filter-analysis.md`
- `2026-11-10-wso-kpi-data-source-analysis.md`

## 示例

- [2026-11-09-project-doc-entry-optimization-analysis.md](2026-11-09-project-doc-entry-optimization-analysis.md) — 项目文档入口优化与沉淀机制分析（示例）
- [2026-11-10-ai-agent-trend-exploration-analysis.md](2026-11-10-ai-agent-trend-exploration-analysis.md) — AI Agent 驱动 Model Management / Scheduler 的趋势探索
- [2026-11-10-wpo-mcp-requirement-analysis.md](2026-11-10-wpo-mcp-requirement-analysis.md) — WPO 引入 MCP:需求分析与可探索方向

- [2026-11-10-wpo-agent-native-opportunity-analysis.md](2026-11-10-wpo-agent-native-opportunity-analysis.md) — WPO Agent-Native:用 Agent 取代界面操作的机会分析
- [2026-11-23-lmk-well-0403-esp-flow-test-analysis.md](2026-11-23-lmk-well-0403-esp-flow-test-analysis.md) — LMK-Well-0403 ESP Flow Test 数据分析(产能、GOR 单位疑点、IPR/VLP 所需补充数据)

- [2026-11-26-wso-maintainability-assessment-analysis.md](2026-11-26-wso-maintainability-assessment-analysis.md) — WSO 三模块(wso-overview、analysis-chart、trend-analysis)长期维护性评估(限定范围版,已按源码复核)
- [2026-11-26-wpe-well-test-validation-overview-maintainability-assessment-analysis.md](2026-11-26-wpe-well-test-validation-overview-maintainability-assessment-analysis.md) — WPE Well Test Validation Overview 维护性评估(74/100:大组件体量、弱类型 API、路由/错误回退)
- [2026-11-26-shared-com-chart-com-map-maintainability-assessment-analysis.md](2026-11-26-shared-com-chart-com-map-maintainability-assessment-analysis.md) — Shared 组件 com-chart(81/100)/ com-map(75/100)维护性评估与改进优先级
- [2026-11-26-maintainability-cross-module-comparison-analysis.md](2026-11-26-maintainability-cross-module-comparison-analysis.md) — 维护性横向对比总表:WSO / WPE / shared 各模块统一口径评分与跨模块优先级路线图
- [2026-11-26-dev-local-branch-evaluation-analysis.md](2026-11-26-dev-local-branch-evaluation-analysis.md) — 本地 dev 分支评估(双评分制)
- [2026-11-26-developer-retention-assessment-analysis.md](2026-11-26-developer-retention-assessment-analysis.md) — 开发人员保留与人员配置评估(初步判断,含验证周期与决策矩阵;涉及个人评价,敏感)

- [2026-11-26-mid-vs-senior-developer-difference-analysis.md](2026-11-26-mid-vs-senior-developer-difference-analysis.md) — 中级与高级开发人员差异(结合 Angular / DFS / WPO 举例,含团队盘点五问;涉及个人判断,敏感)

## 推荐写作流程

1. 从模板创建新文档：[_template.md](_template.md)
2. 在“背景/目标/范围”中明确需求边界
3. 在“方案对比”中记录取舍理由
4. 在“结论与下一步”中沉淀可执行动作
5. 关联到需求、ADR、功能历史（见下方）

## 关联文档

- 需求索引：[feature-history/requirements-index.md](../feature-history/requirements-index.md)
- 架构决策（ADR）：[architecture-decision/](../architecture-decision/README.md)
- 功能演进历史：[feature-history/](../feature-history/README.md)
- 每日过程记录：[daily-log/](../daily-log/README.md)
