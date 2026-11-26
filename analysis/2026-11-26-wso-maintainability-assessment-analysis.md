# WSO 三模块长期维护性评估（限定范围，已按代码复核）

日期：2026-11-26  
范围（仅本次指定）：

1. `libs/wso/src/lib/features/wso-overview`
2. `libs/wso/src/lib/features/well-analysis/components/analysis-chart`
3. `libs/wso/src/lib/features/trend-analysis`

> 说明：本版不展开其它 `well-analysis` 子模块。路径均相对 `wpo-app/libs/wso/src/lib/`。
> 本版重新对照源码核对了上一版的行数、行号与 `any` 计数，并补充了上一版未覆盖的证据（见文末"相对上一版的修正"）。

---

## 评分模型（总分 100）

- 模块边界清晰度（20）
- 依赖方向与耦合度（20）
- 一致性与命名规范（15）
- 类型安全与可演进性（15）
- 复杂度可控性（20）
- 错误处理与可观测性（10）

---

## 总览评分

| 模块 | 源文件数 | 分数 | 结论 |
| --- | ---: | ---: | --- |
| `wso-overview` | 61 | **75** | 分层较好、全模块零 `any`；但有两处依赖 `well-analysis`，且多处错误被静默降级。 |
| `analysis-chart` | 72 | **69** | 分层工程化较强、无反向依赖；但两个超大组件、`any` 多（121 处）。 |
| `trend-analysis` | 14 | **57** | 功能完整，但主组件和图表服务过重、`any` 高达 155 处，且依赖 `analysis-chart` 内部文件。 |

三个模块合计 **0 个 spec 文件**（整个 `libs/wso` 也没有），重构缺少测试保护。

---

## 1) wso-overview（75/100）

### 优点

- 结构分层清晰（`components / configs / shared`）；图表域有 `core / parts` 细分。
- 全模块 `any` 使用为 0，类型纪律最好。
- 主入口 `overview-main/overview.component.ts` 349 行，体量可控。

### 风险点（证据）

- 跨 feature 依赖 `well-analysis` 的导航模型（两处）：
  - `components/overview-main/overview.component.ts:47`（import `well-analysis/model/analysis-navigation-date`）、`:134` 起使用
  - `components/detail-table/wso-detail-table/wso-detail-table.component.ts:42`，并在 `:284` 硬编码跳转 `${wsoBase}/well-analysis`
- 静默空值/兜底回退（共 4 处）：
  - `overview-main/overview.component.ts:189`、`:301`：`catchError(() => of(null))`
  - `chart/parts/common/loading/wso-overview-chart-loader.util.ts:110`：出错回退为 `createFallbackOptions`
  - `chart/core/loaders/wso-overview-chart.loaders.ts:192`
- 大文件：`components/map/wso-map.component.ts` 1211 行、`components/chart/wso-overview-chart.component.ts` 844 行（上一版只提了入口文件，漏了这两个）。
- 模块内无任何日志调用，错误回退后无法追踪。

### 子项评分

- 模块边界清晰度：15/20
- 依赖方向与耦合度：14/20
- 一致性与命名规范：12/15
- 类型安全与可演进性：13/15
- 复杂度可控性：14/20
- 错误处理与可观测性：7/10

---

## 2) analysis-chart（69/100）

### 优点

- 结构设计较成熟：`core / parts / well-trend` 分层明确；请求、渲染、交互责任分区比较清晰。
- 未发现对 `trend-analysis`、`wso-overview` 的反向依赖，依赖方向干净。

### 风险点（证据）

- 超大文件：
  - `analysis-chart/analysis-chart.component.ts` 1399 行
  - `analysis-chart/well-trend/analysis-well-trend-panel.component.ts` 1241 行
- 类型债务：
  - 模块内 `any` 共 121 处（主组件仅 6 处，其余分散在子文件）
  - `analysis-chart.component.ts:132`：`input<any>`（`selectedWellInput`）
  - `well-analysis/servies/analysis-chart.service.ts:75` 起，`Observable<any>` 共 7 处
- 目录名拼写错误 `servies`（应为 `services`），影响检索与一致性。
- 错误回退点 7 处，日志调用仅 2 处。

### 子项评分

- 模块边界清晰度：15/20
- 依赖方向与耦合度：14/20
- 一致性与命名规范：11/15
- 类型安全与可演进性：9/15
- 复杂度可控性：13/20
- 错误处理与可观测性：7/10

---

## 3) trend-analysis（57/100）

### 优点

- 目录结构完整（`components / services / utils / models`），文件仅 14 个，易于整体重构。
- 模块入口清晰，路由接入明确。

### 风险点（证据）

- 超大文件：
  - `trend-analysis.component.ts` 1236 行（`any` 43 处）
  - `services/trend-analysis-chart.service.ts` 1024 行（`any` 52 处，为全模块最多；上一版未提）
- `any` 全模块 155 处，分布在 11 个文件，不是个别文件的问题。
- 依赖 `analysis-chart` 的内部实现（深层路径 import）：
  - `trend-analysis.component.ts:44`（`well-trend/analysis-well-trend-parameter-resolver`）
  - `trend-analysis.component.ts:45`（`well-trend/analysis-well-trend-default-params`）
  - `config.ts:5`（同一个 parameter-resolver）
- API 错误被空数组静默降级：
  - `services/trend-analysis-api.service.ts:190`、`:206`（`catchError` 后返回空数组，文件内 `:163` 的注释也承认这点）
  - 全模块仅 3 处日志调用。

### 子项评分

- 模块边界清晰度：11/20
- 依赖方向与耦合度：10/20
- 一致性与命名规范：10/15
- 类型安全与可演进性：7/15
- 复杂度可控性：13/20
- 错误处理与可观测性：6/10（上一版给 9，但静默吞错且日志极少，不应高分）

---

## 改进空间（按优先级）

1. **P0：切断跨模块深层依赖**
   - 把 `well-trend` 的 `parameter-resolver`、`default-params` 提到 `well-analysis` 公共层（或 `shared`），`trend-analysis` 只依赖公共入口；
   - `wso-overview` 的两处不再直接引用 `well-analysis/model`，导航状态与路径改为共享 contract。

2. **P1：拆分超大组件**
   - 优先级：`trend-analysis.component.ts`、`trend-analysis-chart.service.ts`、`analysis-chart.component.ts`、`analysis-well-trend-panel.component.ts`、`wso-map.component.ts`；
   - 拆成编排层 + 展示层，逻辑下沉到 service/util。

3. **P1：补关键类型**
   - 先覆盖主请求链路：`analysis-chart.service.ts` 的 7 处 `Observable<any>`、`input<any>`，再处理 `trend-analysis-chart.service.ts` 与 `trend-analysis.component.ts`。

4. **P1：统一错误策略**
   - 避免 `of(null)` / 空数组静默成功回退，增加可观测错误态（UI 提示 + 统一日志）；
   - 涉及 `overview.component.ts`、图表 loader、`trend-analysis-api.service.ts`。

5. **P2：补测试与小修**
   - 为拆分前的核心逻辑（参数解析、请求计划、数据转换）补单测，再做重构；
   - 修正 `servies` 目录拼写。

---

## 相对上一版的修正

| 项 | 上一版 | 复核后 |
| --- | --- | --- |
| `overview.component.ts` 行数 | 约 310 | 349 |
| `overview.component.ts` 跨依赖使用行 | 135 | 134 |
| `analysis-chart.component.ts` 行数 | 约 1260 | 1399 |
| `trend-analysis.component.ts` 行数 | 约 1070 | 1236 |
| `trend-analysis.component.ts` 的 `any` | 约 44 | 43 |
| 分数（overview / chart / trend） | 76 / 71 / 64 | 75 / 69 / 57 |

行号 `analysis-chart.component.ts:132`、`analysis-chart.service.ts:75`、`overview.component.ts:47/189/301`、`trend-analysis.component.ts:44/45`、`trend-analysis-api.service.ts:190/206` 经核对均准确。
