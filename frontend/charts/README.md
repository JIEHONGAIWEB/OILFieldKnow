# charts

Charting/visualization conventions and library-specific notes.

## Libraries
- **ECharts 6** via `ngx-echarts` — primary analytical charts
  (time-series well trends, dynacards, KPIs).
- **Leaflet** (+ `leaflet.markercluster`, `proj4`, `@turf/turf`) and
  `@nextgengraphics/webviz-map` — map visualization.
- **webviz-3d** / `three` — 3D visualization.

## Where
- Shared ECharts wrapper: `libs/shared/src/lib/components/com-chart/`
  (handles theme sync and data updates).
- Shared map wrapper: `libs/shared/src/lib/components/com-map/`.
- WSO overview charts/map/KPIs:
  `libs/wso/src/lib/components/{chart,map,kpi}/`.
- Well-analysis charts (dynacard, well-trend):
  `libs/well-surveillance/src/lib/wpo/well-analysis/` (SRP/ESP).

## Conventions
- Prefer the shared `com-chart` wrapper over raw `ngx-echarts` so theming
  stays consistent with the app's light/dark themes.
- Chart option definitions are commonly separated into `config.ts` /
  `*.config.ts` files next to the component.
- Shared chart header/option types keep dropdowns & toolboxes consistent
  across charts.

## Deep dives
- [wso-chart-panel-architecture.md](wso-chart-panel-architecture.md) — as-built
  WSO chart component architecture (container/presentational + data-driven),
  extensibility assessment, and coupling points vs ADR-0002.
- [adding-a-business-layer.md](adding-a-business-layer.md) — step-by-step how-to for
  extending the WSO charts with a new business layer (new tab / chart type /
  toolbar control / API source) without touching container or dumb components.
- [chart-extension-manual-zh.md](chart-extension-manual-zh.md) — 中文扩展使用手册
  （新增 tab / 图表类型 / 工具栏控件 / 真实 API，四场景 + 检查清单）。
- [wso-analysis-chart-tooltip-field-mapping.md](wso-analysis-chart-tooltip-field-mapping.md) —
  Well Analysis chart tooltip field mapping: main API sources, analysis-parameters
  enrichment precedence, and per-chart fallback chains.
