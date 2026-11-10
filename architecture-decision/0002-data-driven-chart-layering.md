# ADR-0002: Data-Driven Chart Layering (Business → Data → Metric → Visualization)

- Status: Proposed
- Date: 2026-07-24
- Deciders: WPO frontend team

## Context

For a data-driven oilfield system, ECharts must **not** be the starting point of
chart design. The common anti-pattern is:

> Backend API → Frontend ECharts option

This couples business logic, data, metrics and presentation into a single layer.
Any change — a new KPI, a data-source swap, or switching a line chart to a gauge
— ripples through the whole system.

Instead, ECharts should be treated as the **presentation layer** at the bottom of
a layered pipeline. What actually needs designing is:

> Business Model → Data Model → Metric Model → Visualization Model → ECharts

## Decision

Adopt a **6-layer, fully decoupled** chart pipeline. Each concern lives in its own
layer; a change in one layer does not leak into the others.

```
Business Layer  (业务领域模型)
      │
      ▼
Data Layer      (原始数据)
      │
      ▼
Metric Layer    (指标计算中心 / KPI)
      │
      ▼
Visualization Model (图表模型：指标 → 用什么图)
      │
      ▼
Chart Builder   (ChartModel → ECharts Option)
      │
      ▼
Angular Component + ECharts (渲染)
```

### Layer 1 — Business Model (业务模型)

Domain objects, **not** chart objects. Do not think about charts here.

```ts
interface Well {
  id: string;
  name: string;
  field: string;
  oilRate: number;
  waterCut: number;
  pressure: number;
  status: 'open' | 'close';
}
```

Sub-domains: `Well` (井) / `Production` (产量) / `Equipment` (设备), served by a
**Domain Service** that holds business calculation logic.

### Layer 2 — Data Model (数据模型)

Raw data only. It does **not** know about Line / Bar / Pie.

```json
[
  { "date": "2026-01", "oil": 150, "water": 20 },
  { "date": "2026-02", "oil": 170, "water": 25 }
]
```

### Layer 3 — Metric Layer (指标模型 / KPI)

The most important — and most often missing — layer. Centralizes all metric
computation: daily rate, cumulative, growth rate, MoM/YoY, average, min/max,
completion ratio, etc. ECharts never knows *how* a value was computed.

```ts
interface Metric {
  id: string;
  name: string;
  unit: string;
  value: number;
  trend: number;
}
```

```json
{ "id": "oilRate", "name": "Oil Rate", "value": 320, "unit": "bbl/day", "trend": 12.4 }
```

### Layer 4 — Visualization Model (图表模型)

Decides *how* a metric is shown — without hardcoding `series:[{type:'line'}]`.

```ts
interface ChartModel {
  id: string;
  type: 'line' | 'bar' | 'pie' | 'gauge' | 'radar';
  metricId: string;
}
```

```json
{ "id": "oil-production", "metricId": "oilRate", "chartType": "line" }
```

### Layer 5 — Chart Builder (Builder Pattern)

Only here is the ECharts `option` finally produced. One builder per chart type.

```ts
class LineChartBuilder {
  build(chart: ChartModel, data: unknown[]): EChartsOption {
    return { xAxis: /* … */, yAxis: /* … */, series: [/* … */] };
  }
}
```

`Bar` / `Pie` / `Radar` / `Gauge` each get their own builder → **Builder Pattern**.

### Layer 6 — Chart Registry (Open/Closed Principle)

Do **not** branch with `if (type === 'line') … else if (type === 'pie') …`.
Register builders and look them up by type:

```ts
registry.register('line', new LineBuilder());

const builder = registry.get(chart.type);
const option = builder.build(chart, data);
```

Adding `Sankey` / `Funnel` requires **no changes to existing code** — just a new
builder registration. This satisfies the Open/Closed Principle.

## Recommended Angular directory layout

```
src/
  business/
    well/
    production/
    equipment/
  metric/
    oil-rate.metric.ts
    water-cut.metric.ts
  chart/
    models/      chart.model.ts
    builders/    line.builder.ts  pie.builder.ts  gauge.builder.ts
    registry/    chart.registry.ts
    services/    chart.service.ts
  components/
    production-chart/
```

## Alternatives Considered

- **Direct API → ECharts option** — fastest to write, but business/data/metric/
  presentation are fused; every change is a cross-cutting edit. Rejected.
- **Per-chart config files only** (current `*.config.ts` convention) — good for a
  handful of fixed charts, but has no metric layer and no builder registry, so it
  does not scale to many metrics or AI-generated dashboards.

## Consequences

- **Decoupling** — business change (new KPI), data-source change (DB/API), or
  presentation change (line → gauge) each touch only their own layer.
- **Extensible** — new chart types added via a new builder + registry entry (OCP);
  no edits to a growing `switch`.
- **AI-ready** — an AI (auto-recommend charts, auto-build dashboards, NL query)
  only emits a small intent object and never writes ECharts option directly:

  ```json
  { "metric": "oilRate", "chart": "line", "group": "monthly" }
  ```

  The Chart Engine resolves: `Metric → Data Query → Builder → ECharts Option → Render`.
- **Cost** — more upfront structure (extra layers/files) than writing an option
  inline; worthwhile for a data-intensive oilfield system, likely overkill for a
  single one-off chart.

## Source Mapping (knowledge system ↔ `wpo-app`)

Principle: **the knowledge system holds the "why" and the business semantics; the
source code (`wpo-app`) is the single executable source of truth.** Docs point at
source paths (a "code map"); source files point back at this ADR in a header
comment. Never duplicate concrete values (interface fields, computed formulas) in
both places — define them once in code and describe their *meaning* in docs.

| Layer | Knowledge system (this repo) | Source code (`wpo-app`) |
| --- | --- | --- |
| Business | [business-model/](../business-model/README.md), [data-model/entities/](../data-model/entities/README.md) — object meaning, field semantics | `src/business/**` — `interface Well`, domain services |
| Data | [data-model/](../data-model/README.md) — sources, field semantics | data services, API DTOs |
| Metric | [domain-knowledge/](../domain-knowledge/README.md) — metric definition, unit, calculation口径 (most important) | `src/metric/*.metric.ts` — the actual computation |
| Visualization | [design-system/charts/](../design-system/charts/README.md) — theme tokens; "which metric → which chart" strategy | `ChartModel` definitions + config data |
| Builder / Registry | this ADR — Builder Pattern / OCP rationale | `src/chart/builders/*.ts`, `src/chart/registry/chart.registry.ts` |
| Render | [frontend/charts/README.md](../frontend/charts/README.md) — `com-chart` conventions | `libs/shared/src/lib/components/com-chart/` |

### Keeping the two in sync

- **Docs → code**: reference source paths, do not copy implementations.
- **Code → docs**: add a header comment on key files, e.g.
  `// Architecture: see ADR-0002 (data-driven chart layering) in oil-field-know-all`.
- **On change**: when the code structure changes, update the paths above and this
  ADR's status (Proposed → Accepted / Superseded), and log it in
  [feature-history/](../feature-history/README.md). Do not let the map rot.
- **Do NOT put in the knowledge system**: volatile code values (interface fields,
  color hex already tokenized in source), tool-enforceable rules (prefer
  lint/format config), or throwaway implementation detail.

## Implementation Notes — `libs/wso` Production-Method KPI pattern

The `wso` feature already implements a config-driven "load KPIs by Production
Method" pattern that closely matches this ADR (a partial, KPI-only realization of
the Visualization Model + Registry layers).

### How it works

- **Config = source of truth** — [`libs/wso/src/lib/configs/wso-kpi-card.config.ts`](../../../wpo-new-2026.7.16/wpo-app/libs/wso/src/lib/configs/wso-kpi-card.config.ts):
  - `WsoProductionMethodKey = 'OILSF' | 'OILESP' | 'GASF' | 'OILGL'`.
  - `WsoKpiCardTemplate { id; title; unit; showTrendIcon?; showTableIcon? }` —
    **presentation metadata only, no values** (data/presentation separation).
  - Two template sets: `OIL_KPI_CARDS`, `GAS_KPI_CARDS`.
  - **Registry** `WSO_KPI_CARD_CONFIG: Record<Key, Template[]>` maps method → set
    (`OILSF/OILESP → OIL`, `GASF/OILGL → GAS`).
  - Resolvers `resolveWsoProductionMethodKey(label|key)` + `getWsoKpiCardTemplates(method)`
    (accepts either a config key or a filter-bar label).
- **Reactive data flow** — `WsoOverviewComponent.productionMethod` is a `signal`
  (default `OILSF`); a `constructor` `effect()` re-runs on change → `loadKpiCards()`
  → `WsoMockDataService.getKpiCards(method)` = `getWsoKpiCardTemplates(method)
  .map(fill value)`; result flows through `kpiCardsSig` → `kpiCards` computed →
  `KpiCardRowComponent` (`@Input cards`, a dumb presentational component).
  For the full runtime flow (triggers, sequence diagram, stage-by-stage) see
  [frontend/ui-patterns/wso-kpi-by-production-method.md](../frontend/ui-patterns/wso-kpi-by-production-method.md#runtime-kpi-data-flow-deep-dive).

### Mapping to this ADR

| ADR layer | `wso` realization |
| --- | --- |
| Metric / KPI | `WsoKpiCardTemplate` (id / title / unit) |
| Visualization Model | `WSO_KPI_CARD_CONFIG` (method → template set) |
| Registry (no if/else) | `Record<Key, Template[]>` + `resolve*()` resolvers |
| Data/presentation split | template = metadata; value filled from mock/API |
| Render | `KpiCardRowComponent` (dumb component) |

### Known gaps / risks (vs domain knowledge)

1. **GL mapping is questionable** — `OILGL → GAS_KPI_CARDS`, so GL wells show
   **Gas** rate KPIs. Per [gl-wells-monitoring.md](../domain-knowledge/production/gl-wells-monitoring.md),
   GL primarily produces **oil** and needs a dual **Oil Production + Gas Injection**
   summary; the injection KPIs (Injection Rate / Pressure / Efficiency) and the
   summary toggle are not modelled — GL merely reuses the GAS template.
2. **ESP lacks equipment-health KPIs** — `OILESP → OIL_KPI_CARDS` only has
   production KPIs; the Motor Current / PIP / Pump Efficiency KPIs described in
   [esp-wells-monitoring.md](../domain-knowledge/production/esp-wells-monitoring.md)
   are absent.
3. **Positional value mapping is fragile** — `MOCK_KPI_VALUES = [5120,7055,235,234,234]`
   is aligned to templates by array `index`; key values by `template.id` instead.

### Suggested improvements (to better satisfy OCP)

- Model GL's Gas Injection as its own template set and support a dual-summary
  toggle (a `signal`) in the overview.
- Fill values via `Record<kpiId, value>` matched by `id`, removing positional
  coupling.
- To add a well type without editing existing code, replace the static
  `WSO_KPI_CARD_CONFIG` Record with a registration function
  (`registerKpiSet(key, templates)`) — the OCP-friendly registry from this ADR.

## Related

- [design-system/charts/README.md](../design-system/charts/README.md) — chart visual language / theme tokens.
- [frontend/charts/README.md](../frontend/charts/README.md) — charting library conventions (`com-chart`, ECharts 6).
- Production-method domain knowledge:
  [oil-rate-kpis.md](../domain-knowledge/production/oil-rate-kpis.md),
  [esp-wells-monitoring.md](../domain-knowledge/production/esp-wells-monitoring.md),
  [sf-gas-wells-monitoring.md](../domain-knowledge/production/sf-gas-wells-monitoring.md),
  [gl-wells-monitoring.md](../domain-knowledge/production/gl-wells-monitoring.md).
