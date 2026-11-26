# 维护性横向对比总表（2026-11-26）

本文件汇总以下 3 份评估，统一评分口径并输出跨模块优先级路线图：

- [WSO 维护性评估](2026-11-26-wso-maintainability-assessment-analysis.md)
- [WPE Well Test Validation Overview 维护性评估](2026-11-26-wpe-well-test-validation-overview-maintainability-assessment-analysis.md)
- [shared com-chart / com-map 维护性评估](2026-11-26-shared-com-chart-com-map-maintainability-assessment-analysis.md)

---

## 统一评分口径

- 模块边界清晰度（20）
- 依赖方向与耦合度（20）
- 一致性与命名规范（15）
- 类型安全与可演进性（15）
- 复杂度可控性（20）
- 错误处理与可观测性（10）

---

## 横向总表（按总分降序）

| 排名  | 模块                              | 归属     |  分数 | 核心风险关键词                   | 优先级 |
| --- | ------------------------------- | ------ | --: | ------------------------- | --- |
| 1   | `com-chart`                     | shared |  81 | store 弱类型选择器              | P1  |
| 2   | `wso-overview`                  | WSO    |  76 | 跨 feature 依赖、静默回退         | P0  |
| 3   | `com-map`                       | shared |  75 | map SDK 适配层 `any/unknown` | P1  |
| 4   | `well-test-validation-overview` | WPE    |  74 | 大组件、路由一致性、unknown 契约      | P0  |
| 5   | `analysis-chart`                | WSO    |  71 | **超大组件**、`any`/弱类型        | P1  |
| 6   | `trend-analysis`                | WSO    |  64 | **超大组件**、反向依赖、静默降级        | P0  |

---

## 关键问题聚类（跨模块）

### A. 跨模块/跨 feature 依赖边界不稳（P0）

- `wso-overview` 直接依赖 `well-analysis` 内部导航状态。
- `trend-analysis` 直接依赖 `analysis-chart` 内部实现。
- `well-test-validation-overview` 存在跨模块路由拼接跳转（含 WSO 跳转）。

**建议目标**：通过 shared contract / facade 统一对外能力，禁止跨 feature 直接引用内部路径。

### B. 大组件与高编排密度（P0/P1）

- `trend-analysis.component.ts`、`analysis-chart.component.ts`、`map-panel.component.ts`、`detail-table.component.ts` 体量偏大。

**建议目标**：拆分为“容器（编排） + 展示（纯 UI） + adapter（外部系统）”。

### C. 类型系统债务（P1）

- 多处 `any`、`unknown`、字符串化结构（如 `entityIds: "[1,2]"`）降低可演进性。

**建议目标**：先覆盖高频 API 链路（status/map/trend + analysis chart 主链路）完成 DTO 化。

### D. 错误可观测性不足（P1）

- `of(null)` / `of([])` 回退较多，失败与空数据混淆。

**建议目标**：建立统一错误态协议（UI 显示 + telemetry + 最小日志上下文）。

---

## 统一路线图（建议）

### Week 1（P0）

1. 依赖边界治理第一批：
   - 切断 `trend-analysis -> analysis-chart internal`；
   - 切断 `wso-overview -> well-analysis/model internal`；
   - 统一 WPE overview 的 analysis 路由目标并补回归用例。
2. 建立 “禁止跨 feature 深层 import” 的 lint 规则草案（先告警后阻断）。

### Week 2（P1）

1. 类型治理第一批：
   - WPE：`WellTestValidationApiService`（status/map/trend）DTO 化；
   - WSO：`analysis-chart` 主请求链路去 `any`。
2. 错误处理规范化：
   - 为静默回退点增加 error channel（可观测 + UI 可区分）。

### Week 3（P1/P2）

1. 大组件拆分第一批：
   - `trend-analysis.component.ts`
   - `analysis-chart.component.ts`
   - `map-panel.component.ts`
2. shared 侧适配层抽取：
   - `com-map` 最小 map/view adapter 接口。

---

## 验收指标（建议）

- 跨 feature 深层 import 数量：下降到 0（目标模块范围内）。
- 目标文件 `any/unknown` 数量：首批下降 40%+。
- 静默回退点：全部补齐错误可观测信号。
- 路由一致性：关键跳转路径增加自动化回归用例并通过。

---

## 待确认事项（Open Questions）

1. 是否接受在 Week 1 同步引入 lint 规则（先 warning）？
2. WPE `entityIds` 是否允许后端兼容 `number[]` 入参（用于替换字符串化数组）？
3. 错误 telemetry 的统一上报入口使用现有哪一层（shared service 还是各 feature facade）？

