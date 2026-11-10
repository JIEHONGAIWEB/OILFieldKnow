# How to Add a New Business Layer (WSO charts)

A step-by-step guide for extending the WSO chart system with a **new business layer**
(a new tab / page, new chart types, new toolbar controls) **without touching the
container or presentational components**.

- Audience: frontend engineers extending `libs/wso`
- Prerequisite reading: [wso-chart-panel-architecture.md](wso-chart-panel-architecture.md), [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)
- Golden rule: **you only edit data + (optionally) register one new builder.** The
  container (`WsoOverviewComponent`) and dumb components (`WsoChartPanelComponent`,
  `ChartViewSwitcherComponent`) stay untouched.

## Mental model

```
getChartPageSpecs()  ──►  WsoChartPageSpec[]        (WHAT to show: data)
        │                        │
        │                        ├─ wellScope         (how to narrow wells)
        │                        ├─ toolbarControls    (declarative controls)
        │                        └─ spec: WsoChartOptionSpec (which chart type + params)
        ▼
buildChartOptions(spec) ──► chartOptionBuilders[type] ──► CommonChartOptionsLite
        ▼
com-chart renders (no per-business code)
```

Extension surface = three data structures, all in the source files below:

| Concept | Type | File |
| --- | --- | --- |
| Page/tab | `WsoChartPageSpec` | `libs/wso/src/lib/services/wso-mock-data.service.ts` |
| Chart type + params | `WsoChartOptionSpec` (union) | same file |
| Builder registry | `chartOptionBuilders` (`Record<type, builder>`) | same file |
| Toolbar control | `WsoChartToolbarControl` (union) | `libs/wso/src/lib/shared/models/wso-chart.model.ts` |
| Well scope | `WsoWellScopeStrategy` | same model file |

## Scenario A — Add a new tab that reuses existing chart types

Cheapest case: your new business layer only needs existing chart types
(`comparison`, `loss`). **Edit data only — one array entry.**

In `getChartPageSpecs()` add a page:

```ts
{
  id: 'injection',              // unique tab id
  label: 'Injection',           // tab label
  wellScope: 'even',            // 'all' | 'even' | 'odd'
  charts: [
    {
      id: 'inj-rate-comparison',
      spec: { type: 'comparison', title: 'INJECTION RATE', unit: 'mscfd', categories: ['A', 'B', 'C'] },
      toolbarControls: [{ kind: 'slider', id: 'last-test-rate', label: 'Last Test Rate', value: 50 }]
    },
    {
      id: 'inj-downtime',
      spec: { type: 'loss', title: 'DOWNTIME (HRS)', unit: 'hrs' }
    }
  ]
}
```

Done. The new tab appears in the switcher, charts render, well-scope applies, and the
layout adapts to the chart count automatically. **No component edits.**

## Scenario B — Add a brand-new chart type

When the business layer needs a chart shape that doesn't exist yet (e.g. a `trend`
line chart). Three small, additive edits — this is the OCP path.

### 1. Extend the spec union (`wso-mock-data.service.ts`)

```ts
type WsoChartOptionSpec =
  | { type: 'comparison'; title: string; unit: string; categories: string[] }
  | { type: 'loss'; title: string; unit: string }
  | { type: 'trend'; title: string; unit: string; points: number[] };   // NEW
```

### 2. Write the builder (returns `CommonChartOptionsLite`)

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

### 3. Register it (one line — no `if/else`)

```ts
private readonly chartOptionBuilders: WsoChartOptionBuilders = {
  comparison: (spec, dark) => this.buildComparisonChartOptions(spec.title, spec.unit, spec.categories, dark),
  loss: (spec, dark) => this.buildLossChartOptions(spec.title, spec.unit, dark),
  trend: (spec, dark) => this.buildTrendChartOptions(spec.title, spec.unit, spec.points, dark)  // NEW
};
```

TypeScript enforces completeness: the mapped type `WsoChartOptionBuilders` requires an
entry for every `type` in the union, so a missing builder is a **compile error**, not a
runtime surprise. Now use `{ type: 'trend', ... }` in any page spec (Scenario A).

## Scenario C — Add a new toolbar control kind

Today `toolbarControls` only has `kind: 'slider'`. To add e.g. a dropdown:

### 1. Extend the control union (`wso-chart.model.ts`)

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

### 2. Render the new branch in `wso-chart-panel.component.html`

```html
<ng-container *ngIf="control.kind === 'select'">
  <span class="wso-chart-panel__slider-label">{{ control.label }}</span>
  <p-select [options]="control.options" [(ngModel)]="controlValues[control.id]" optionLabel="label" optionValue="value" />
</ng-container>
```

> Note: this is the one case that touches a presentational component — unavoidable,
> because a new control *kind* needs a new render branch. Adding more controls of an
> **existing** kind is still data-only.

## Scenario D — Feed the tab from the real API instead of mock

The business layer's data source is orthogonal to the chart config. Follow the existing
`USE_WSO_API` pattern in `WsoOverviewComponent`:

1. Add an endpoint method on `WsoApiService`.
2. Map the response into a `WsoChartPageModel[]` (or `WsoChartOptionSpec[]`), mirroring
   `mapSummaryToCards` — keep the mapper in the container/service, not the components.
3. On failure, fall back to `WsoMockDataService.getChartPages()` (the app already does
   this for KPIs and losses).

## What you must NOT do

- Do **not** add `if (viewId === '...')` branches in the container — use `wellScope`
  data or extend `WsoWellScopeStrategy`.
- Do **not** hard-code titles/units/controls in HTML — put them in the page spec.
- Do **not** copy concrete values into this knowledge repo — the source
  (`wpo-app`) is the single source of truth; docs describe the *how/why*.

## Checklist

- [ ] New tab added to `getChartPageSpecs()` with a unique `id`.
- [ ] Each chart references an existing (or newly registered) `WsoChartOptionSpec.type`.
- [ ] New chart type → union member + builder + registry entry (compiles clean).
- [ ] `wellScope` set if the tab needs a well subset (default `'all'`).
- [ ] Toolbar via `toolbarControls`; new *kind* also needs an HTML branch.
- [ ] `libs/wso` compiles with no errors; new model types exported from `shared/models`.

## Related
- [chart-extension-manual-zh.md](chart-extension-manual-zh.md) — 中文版扩展手册（本文的中文对照）。
- [wso-chart-panel-architecture.md](wso-chart-panel-architecture.md) — the as-built architecture this guide extends.
- [ADR-0002: Data-Driven Chart Layering](../../architecture-decision/0002-data-driven-chart-layering.md) — the target layered pipeline and Builder/Registry rationale.
- [frontend/ui-patterns/wso-kpi-by-production-method.md](../ui-patterns/wso-kpi-by-production-method.md) — sibling config-driven KPI-by-method flow.
