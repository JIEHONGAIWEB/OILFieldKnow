# WSO Chart 扩展使用手册（中文）

面向：需要给 WSO Overview 增加新图表业务层（新增 tab / 图表类型 / 工具栏控件 / 数据源）的开发者。

核心理念：**图表全部由数据驱动，扩展是「加数据 + 注册 builder」，不改组件**。容器
（`WsoOverviewComponent`）、展示组件（`WsoChartPanelComponent`、`ChartViewSwitcherComponent`）、
`com-chart` 渲染器都是层无关的（OCP）。对应英文详版见
[adding-a-business-layer.md](adding-a-business-layer.md)，as-built 架构见
[wso-chart-panel-architecture.md](wso-chart-panel-architecture.md)，架构决策见
[ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)。

## 涉及文件（只需动这几个）

| 文件 | 作用 | 扩展时是否要改 |
| --- | --- | --- |
| `libs/wso/src/lib/services/wso-mock-data.service.ts` | 页面/图表声明 + builder 注册表 + mock 值 | ✅ 一定改 |
| `libs/wso/src/lib/shared/models/wso-chart.model.ts` | `WsoChartModel` / `WsoChartPageModel` / 控件 / 作用域类型 | ⬜ 新增控件种类或字段时改 |
| `libs/wso/src/lib/components/chart/wso-chart-panel/*.html` | 工具栏控件渲染 | ⬜ **仅**新增控件「种类」时改一处分支 |
| `WsoOverviewComponent` / `ChartViewSwitcherComponent` | 编排 + 切换 | ❌ **永不改** |

## 关键概念（先理解再动手）

- **页面 `WsoChartPageSpec`**（在 service 内）：`{ id, label, wellScope?, charts[] }`。
  **一个 page = 一个 tab = 一个业务层视图**。
- **图表描述 `WsoChartOptionSpec`**：判别联合，如 `{ type: 'comparison' | 'loss', ... }`。
  只描述「用哪种图 + 参数」，**不含 ECharts option**。
- **builder 注册表 `chartOptionBuilders`**：`Record<type, builder>`（mapped type）。
  `type → builder → CommonChartOptionsLite`。加图表类型 = 加联合成员 + 加一条注册项。
- **工具栏 `toolbarControls`**：`WsoChartToolbarControl[]` 判别联合（当前 `kind: 'slider'`）。
  面板用 `*ngFor` 通用渲染，值按 `control.id` 存 `sliderValues`。
- **井作用域 `wellScope`**：`'all' | 'even' | 'odd'`，容器读 `activeChartPage()?.wellScope`
  过滤井集，**不再有 `viewId === '...'` 硬编码**。

---

## 场景一：新增一个 tab，复用已有图表类型（最常见）

例：加「Injection（注气）」tab，复用 `comparison` + `loss`。**纯数据改动，只加 `getChartPageSpecs()` 一条。**

```ts
{
  id: 'injection',              // 唯一 tab id
  label: 'Injection',           // tab 标签
  wellScope: 'even',            // 'all' | 'even' | 'odd'
  charts: [
    {
      id: 'inj-rate-comparison',
      spec: { type: 'comparison', title: 'INJECTION RATE', unit: 'mscfd', categories: ['A', 'B', 'C'] },
      toolbarControls: [{ kind: 'slider', id: 'last-test-rate', label: 'Last Test Rate', value: 50 }]
    },
    { id: 'inj-downtime', spec: { type: 'loss', title: 'DOWNTIME (HRS)', unit: 'hrs' } }
  ]
}
```

✅ 完成。切换器里**自动出现**新 tab，图表渲染、井作用域生效、布局按图表数量自适应（1 张占满 / 2 张各半 / 3 张各三分之一）。**不需要改任何组件。**

---

## 场景二：新增一整种图表类型（OCP 路径）

例：新增 `trend`（折线趋势图）。三处**追加式**改动。

### 第 1 步 — 扩联合类型（`wso-mock-data.service.ts`）
```ts
type WsoChartOptionSpec =
  | { type: 'comparison'; title: string; unit: string; categories: string[] }
  | { type: 'loss'; title: string; unit: string }
  | { type: 'trend'; title: string; unit: string; points: number[] };   // 新增
```

### 第 2 步 — 写 builder（返回 `CommonChartOptionsLite`）
```ts
private buildTrendChartOptions(title: string, unit: string, points: number[], darkTheme = false): CommonChartOptionsLite {
  const theme = this.resolveChartThemeColors(darkTheme);
  return {
    title,
    actions: WsoMockDataService.CHART_ACTIONS,
    chartOptions: {
      grid: { left: 48, right: 20, top: 28, bottom: 48 },
      xAxis: { type: 'category', data: points.map((_, i) => `T${i + 1}`), axisLabel: { color: theme.axisLabel } },
      yAxis: { type: 'value', name: unit, axisLabel: { color: theme.axisLabel } },
      series: [{ name: title, type: 'line', data: points }]
    },
    columns: [{ field: 'x', header: 'T' }, { field: 'y', header: unit }],
    data: points.map((y, i) => ({ x: `T${i + 1}`, y }))
  };
}
```

### 第 3 步 — 注册（唯一改变行为的一行，无 if/else）
```ts
private readonly chartOptionBuilders: WsoChartOptionBuilders = {
  comparison: (spec, dark) => this.buildComparisonChartOptions(spec.title, spec.unit, spec.categories, dark),
  loss: (spec, dark) => this.buildLossChartOptions(spec.title, spec.unit, dark),
  trend: (spec, dark) => this.buildTrendChartOptions(spec.title, spec.unit, spec.points, dark)  // 新增
};
```

> mapped type `WsoChartOptionBuilders` 强制每个 `type` 都要有 builder，漏写即**编译报错**，不是运行时才崩。之后在任意 page spec 里用 `{ type: 'trend', ... }` 即可（回到场景一）。

---

## 场景三：新增工具栏控件「种类」

当前 `toolbarControls` 只有 `kind: 'slider'`。要加下拉框：

### 第 1 步 — 扩控件联合（`wso-chart.model.ts`）
```ts
export interface WsoChartSelectControl {
  kind: 'select';
  id: string;
  label: string;
  options: Array<{ label: string; value: string }>;
  value?: string;
}
export type WsoChartToolbarControl = WsoChartSliderControl | WsoChartSelectControl;
```

### 第 2 步 — 面板 HTML 加一个渲染分支（`wso-chart-panel.component.html`）
```html
<ng-container *ngIf="control.kind === 'select'">
  <span class="wso-chart-panel__slider-label">{{ control.label }}</span>
  <p-select [options]="control.options" [(ngModel)]="controlValues[control.id]" optionLabel="label" optionValue="value" />
</ng-container>
```

> 这是唯一需要碰展示组件的情况——新「种类」必须有新渲染分支。加**同种类**更多控件仍是纯数据。

---

## 场景四：这个 tab 由真实 API 提供

图表配置与数据源是正交的。沿用 `WsoOverviewComponent` 里的 `USE_WSO_API` 模式：

1. 在 `WsoApiService` 加一个 endpoint 方法。
2. 把响应映射成 `WsoChartPageModel[]`（或 `WsoChartOptionSpec[]`），仿照 `mapSummaryToCards` —— mapper 放容器/服务，**不放组件**。
3. 失败回退 `WsoMockDataService.getChartPages()`（KPI / losses 已是这套回退）。

> 注意：接 API 时把顶部 `USE_WSO_API` 置为 `true`（当前为 `false`，走 mock）。

---

## 约定与检查清单

**约定**
- 一个 page 只代表一个业务层视图；tab id / 图表 id 全局唯一。
- 图表 id 按业务层加前缀（`inj-*` / `oil-*` / `gas-*`）。
- spec 只放「用哪种图 + 参数」；ECharts option 由 builder 生成；数值来自 mock 或 API。
- 井集收窄用 `wellScope` 数据，**禁止**在容器里加 `if (viewId === '...')`。

**提交前检查**
- [ ] 新 tab 加到 `getChartPageSpecs()`，`id` 全局唯一。
- [ ] 每个图表的 `spec.type` 是已注册（或新注册）的类型。
- [ ] 新图表类型：联合成员 + builder + 注册项都补齐（编译通过）。
- [ ] 需要井子集时设 `wellScope`（默认 `'all'`）。
- [ ] 工具栏用 `toolbarControls`；新「种类」才需加 HTML 分支。
- [ ] `libs/wso` 编译无错；新模型类型从 `shared/models` 导出。
- [ ] 未改动 `WsoOverviewComponent` / `ChartViewSwitcherComponent`（若改了，说明偏离本模式，需复核）。

## 相关

- [adding-a-business-layer.md](adding-a-business-layer.md) — 英文详版（四场景 + 禁止事项）。
- [wso-chart-panel-architecture.md](wso-chart-panel-architecture.md) — as-built 架构与耦合点重构记录。
- [wso-kpi-extension-manual-zh.md](../ui-patterns/wso-kpi-extension-manual-zh.md) — 姊妹篇：KPI 扩展手册。
- [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md) — 架构决策（Registry + Builder + 分层）。
