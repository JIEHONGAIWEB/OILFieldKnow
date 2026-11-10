# WSO KPI 扩展使用手册（中文）

面向：需要给 WSO Overview 增加新 KPI（新增业务层、新增井型/生产方式）的开发者。

核心理念：**KPI 全部由配置驱动，扩展是「加配置 + 注册」，不改组件**。选择器、汇总切换、
`effect`、卡片组件都是层无关的（OCP）。对应英文详版见
[wso-kpi-by-production-method.md](wso-kpi-by-production-method.md)，分层理念见
[business-model/kpi-layers.md](../../business-model/kpi-layers.md)，架构决策见
[ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)。

## 涉及文件（只需动这几个）

| 文件 | 作用 | 扩展时是否要改 |
| --- | --- | --- |
| `libs/wso/src/lib/configs/wso-kpi-card.config.ts` | KPI 模板 + summary + 注册表 | ✅ 一定改 |
| `libs/wso/src/lib/services/wso-mock-data.service.ts` | 按 id 提供 mock 值 | ✅ mock 场景改 |
| `libs/wso/src/lib/shared/models/wso-api.model.ts` | `WsoProductionSummary` 字段 | ⬜ 仅接真实 API 时改 |
| `WsoOverviewComponent` / `KpiCardRowComponent` / `KpiCardComponent` | 编排 + 渲染 | ❌ **永不改** |

## 关键概念（先理解再动手）

- **模板 `WsoKpiCardTemplate`**：只放展示信息（`id`/`title`/`unit`/图标）+ 可选 `valueKey`
  （对应 API 字段），**不含数值**。
- **汇总 `WsoKpiSummary`**：`{ id, label, templates }`。**一个 summary = 一个业务层**
  （生产层 / 设备层 / 井筒层 / 经济层…）。
- **注册表 `registerKpiSet(method, summaries[])`**：把一个生产方式映射到它需要的若干业务层。
  一个方法有多个 summary 时，顶部自动出现切换按钮（`p-selectButton`）。
- **取值方式**：mock 按 `template.id` 取；API 按 `template.valueKey` 取。

---

## 场景一：给已有井型加一个业务层 KPI（最常见）

例：给 SF Gas（`GASF`）加「井筒压力层」。**纯配置改动**。

### 第 1 步 — 定义模板集（`wso-kpi-card.config.ts`）
id 用业务层前缀命名（`gas-*`），避免和别的层冲突：
```ts
const GAS_WELLBORE_KPI_CARDS: WsoKpiCardTemplate[] = [
  { id: 'gas-whp', title: 'Wellhead Pressure', unit: 'psi', showTrendIcon: true },
  { id: 'gas-tubing-pressure', title: 'Tubing Pressure', unit: 'psi' },
  { id: 'gas-casing-pressure', title: 'Casing Pressure', unit: 'psi' },
  { id: 'gas-line-pressure', title: 'Line Pressure', unit: 'psi' },
];
```

### 第 2 步 — 包成一个 summary（= 业务层）
```ts
const GAS_WELLBORE_SUMMARY: WsoKpiSummary =
  { id: 'wellbore', label: 'Wellbore Pressure Summary', templates: GAS_WELLBORE_KPI_CARDS };
```

### 第 3 步 — 注册（唯一改变行为的一行）
```ts
registerKpiSet('GASF', [GAS_PRODUCTION_SUMMARY, GAS_WELLBORE_SUMMARY]);
```

### 第 4 步 — 补 mock 值（`wso-mock-data.service.ts`，按 id）
```ts
'gas-whp': 1850, 'gas-tubing-pressure': 1200, 'gas-casing-pressure': 900, 'gas-line-pressure': 650,
```

✅ 完成。`GASF` 现在有 2 个 summary → 顶部**自动出现**「Gas Production / Wellbore Pressure」切换按钮，卡片自动渲染。**不需要改任何组件或模板 HTML。**

---

## 场景二：这个业务层是真实 API 提供的

在场景一基础上多两步：

### 第 5 步 — 给 `WsoProductionSummary` 加字段（`wso-api.model.ts`）
```ts
export interface WsoProductionSummary {
  // ...existing...
  wellheadPressure: number;
  tubingPressure: number;
}
```

### 第 6 步 — 模板加 `valueKey` 指向该字段
```ts
{ id: 'gas-whp', title: 'Wellhead Pressure', unit: 'psi', valueKey: 'wellheadPressure' }
```
`mapSummaryToCards()` 会自动按 `valueKey` 取值和 `diffRatio`，**无需改取值逻辑**。

> 注意：接 API 时把顶部 `USE_WSO_API` 置为 `true`（当前为 `false`，走 mock）。

---

## 场景三：新增一整种井型 / 生产方式

例：新增「PCP Wells（螺杆泵）」。

1. 扩联合类型：
   ```ts
   export type WsoProductionMethodKey = 'OILSF' | 'OILESP' | 'GASF' | 'OILGL' | 'OILPCP';
   ```
2. 加选择器选项 + 标签映射：
   ```ts
   // WSO_PRODUCTION_METHOD_OPTIONS
   { label: 'PCP Wells', value: 'OILPCP' },
   // WSO_PRODUCTION_METHOD_LABEL_MAP
   'PCP Wells': 'OILPCP',
   ```
3. 定义并注册它需要的业务层：
   ```ts
   registerKpiSet('OILPCP', [OIL_PRODUCTION_SUMMARY, PCP_EQUIPMENT_SUMMARY]);
   ```
4. 补新模板 id 的 mock 值。

✅ 选择器里立即出现「PCP Wells」，切换即生效。

---

## 约定与检查清单

**约定**
- 一个 summary 只代表一个业务层；井型按需组合业务层（生产层必有；ESP 加设备层；
  Gas 加井筒/压缩层；GL 加注气层）。
- 模板 `id` 按业务层加前缀（`esp-*` / `gl-*` / `gas-*` / `pcp-*`）。
- 模板只放展示信息；数值来自 mock（按 id）或 API（按 valueKey）。

**提交前检查**
- [ ] 新模板的 `id` 全局唯一且有层前缀。
- [ ] mock 场景：每个新 `id` 在 `MOCK_KPI_VALUES` 有值。
- [ ] API 场景：每个新模板有 `valueKey`，且 `WsoProductionSummary` 有对应字段。
- [ ] `registerKpiSet` 里把新 summary 加进目标方法。
- [ ] 编译无错（`get_errors` / `nx build wso`）；本地 `nx serve` 看切换按钮与卡片。
- [ ] 未改动 `WsoOverviewComponent` / 卡片组件（若改了，说明偏离了本模式，需复核）。

## 相关

- [wso-kpi-by-production-method.md](wso-kpi-by-production-method.md) — 英文详版（数据流、运行时时序图、缺口）。
- [frontend/charts/chart-extension-manual-zh.md](../charts/chart-extension-manual-zh.md) — 姊妹篇：图表扩展手册。
- [business-model/kpi-layers.md](../../business-model/kpi-layers.md) — KPI 按业务层分层的理念。
- [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md) — 架构决策（Registry + Builder + 分层）。
