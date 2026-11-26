# WPE Well Test Validation Overview 维护性评估（2026-11-26）

评估对象：`libs/wpe/src/lib/features/well-test-validation-overview`

---

## 一句话总结

`well-test-validation-overview` 的分层思路是清晰的（chart/map/table + shared store/service），具备良好演进基础；主要风险集中在**超大组件体量**、**弱类型 API 契约**和**部分路由/错误回退策略**。

---

## 评分模型（总分 100）

- 模块边界清晰度（20）
- 依赖方向与耦合度（20）
- 一致性与命名规范（15）
- 类型安全与可演进性（15）
- 复杂度可控性（20）
- 错误处理与可观测性（10）

---

## 总分

**74 / 100**

---

## 子项评分与说明

### 1) 模块边界清晰度：16/20

**正向**
- 功能拆分明确：`chart-panel / map-panel / detail-table`，共享能力放在 `shared`（store/service/config/util）。
- 页面入口较薄：`well-test-validation-overview.component.ts` 仅约 101 行。

**风险**
- `map-panel`（约 757 行）和 `detail-table`（约 663 行）承担职责偏多，已有“次级聚合组件”迹象。

参考：
- `components/well-test-validation-overview/well-test-validation-overview.component.ts`
- `components/map-panel/map-panel.component.ts`
- `components/detail-table/detail-table.component.ts`

---

### 2) 依赖方向与耦合度：15/20

**正向**
- 未发现对 `well-test-management / model-calibration / well-test-validation-analysis` 内部文件的反向 import。
- 组件之间通过 `WellTestValidationLinkageStore` 协同，解耦优于直接互调。

**风险**
- 仍有跨模块导航耦合（跳转 WSO 模块路由）：`map-panel`、`detail-table` 直接拼接并跳转 `well-analysis`。

参考：
- `shared/state/well-test-validation-linkage.store.ts`
- `components/map-panel/map-panel.component.ts:223`
- `components/detail-table/detail-table.component.ts:422`

---

### 3) 一致性与命名规范：12/15

**正向**
- 文件和目录命名整体统一，`parts` 子模块职责命名清晰。

**风险**
- 同一域内仍有多种响应形态约定（`items` / `data` / 数组本体）并行，语义一致性成本较高。

参考：
- `components/chart-panel/parts/chart-panel-api.util.ts`

---

### 4) 类型安全与可演进性：10/15

**正向**
- 关键业务枚举与语义配置已结构化：`WtvDomain`、`STATUS_SEMANTIC_CONFIG`。

**风险**
- API 服务大量 `Observable<unknown>` 返回；上层需手动判型与容错，编译期保护弱。
- `entityIds` 使用字符串化数组（`"[1,2]"`）作为入参契约，长期不利于类型治理。

参考：
- `shared/services/well-test-validation-api.service.ts:25`
- `shared/services/well-test-validation-api.service.ts:39`
- `shared/services/well-test-validation-api.service.ts:53`
- `shared/services/well-test-validation-api.service.ts:67`
- `components/chart-panel/parts/chart-panel-api.util.ts`

---

### 5) 复杂度可控性：14/20

**正向**
- `chart-panel` 通过 `parts/*.util.ts` 把 API、时间、主题、loading、options 进行了拆分，结构化程度较好。

**风险**
- `map-panel`、`detail-table` 文件过长，维护时认知成本高，回归影响面偏大。

参考：
- `components/chart-panel/chart-panel.component.ts`
- `components/map-panel/map-panel.component.ts`
- `components/detail-table/detail-table.component.ts`

---

### 6) 错误处理与可观测性：7/10

**正向**
- 空 wells 输入时主动短路，避免无效请求。

**风险**
- `getMapInfo` 使用 `catchError(() => of([]))` 静默回退，真实故障与“确实无数据”难区分。
- `context` 读取使用 `try/catch` 后返回 `null`，无错误记录，排障信号不足。

参考：
- `shared/services/well-test-validation-api.service.ts:105`
- `shared/services/well-test-validation-context.service.ts`

---

## 关键设计观察

### 值得保留

1. **Linkage Store 事件中枢**
   - `chart → table/map` 的联动通过 `signal` + 事件对象完成，可继续扩展。
2. **图表逻辑模块化**
   - `chart-panel` 的 `parts` 分层可作为后续其它模块的模板。

### 需要优先治理

1. **路由一致性风险**
   - 入口路由定义为 `well-test-validation-analysis`，但 overview 中 `goToAnalysis()` 导航到 `['wpe','well-test-validation','analysis']`，建议统一并加 e2e 覆盖。
   - 参考：
     - `libs/wpe/src/lib/wpe.routes.ts`
     - `components/well-test-validation-overview/well-test-validation-overview.component.ts:69`
2. **API 返回模型标准化**
   - 从 `unknown` 逐步替换为显式 DTO（优先 status / map / trend 三条链路）。
3. **组件瘦身**
   - 优先拆 `map-panel`：弹窗交互、图层处理、导航跳转拆为 facade/adapter。

---

## 改进空间（分阶段）

### P0（本周）
- 修正并统一 `goToAnalysis` 路由目标；补充 1 条导航回归用例。
- 为 `getMapInfo` 增加可观测错误通道（日志/埋点），区分“空数据”与“请求失败”。

### P1（1-2 周）
- 给 `WellTestValidationApiService` 增加 typed response（先覆盖 status/map/trend）。
- 将 `entityIds: string` 迁移为 `number[]`（兼容期内在 API adapter 做转换）。

### P2（2-4 周）
- 拆分 `map-panel`、`detail-table` 为“容器 + 纯展示组件 + 导航适配器”。
- 收敛跨模块导航拼接逻辑到单点 helper/service。

