# Architecture Memory

Append-only log of architectural facts an AI assistant should remember across sessions.

## 2026-07-22 (extracted from wpo-new-2026.7.16/wpo-app)
- App = **WPO (Well Performance Optimization)**, Angular 20 oilfield surveillance app.
- It is a **Module Federation remote** (project name `sampleSolution`); boots via
  `main.ts` → dynamic `import('./bootstrap')`. Exposes `DemoModule`,
  `WellSurveillanceModule`, `WpeModule`, `WsoModule`.
- Feature libs live in `libs/` (not `src/`): `well-surveillance` (core), `wpe`,
  `wso`, `demo`, `shared`. Routes: `/wpe`, `/wso`, `/demo` (+`/wpo-test`).
- Data access is **PDM Business Object queries**: `ApiService.getDatabyBoQuery`
  → POST `/dspdmservice/common` with a `BOQuery`. Success = `status.statusCode===1`;
  rows at `data.<boName>.list`.
- `ApiService.postApi` auto-injects `language:'en'` + `timezone` (moment), and
  runs `WafRulesWellSurvellianceService.byPassWAFRequestBody` (WAF bypass) — keep both.
- Feature service routes via `SERVICES_ROUTES` / `MODULE_END_POINT`; API base is
  resolved per MFE context by `MfeInit` from host `activePage` NgRx state.
- State: NgRx. Known slices: `activePage`, `SDHFilter` (Surveillance Data Hub filters).
- Viz: ECharts (`ngx-echarts`), Leaflet + markercluster, `@nextgengraphics/webviz-*`
  (map + 3D on Three.js). Dashboards via `angular-gridster2`.
- Analytics domains: Run Life Analysis (AERL/MEANTIME), Survival Analysis
  (hazard/survival, Weibull), Well Test Management (`WELL_TEST`,
  `WELL_TEST_PERIOD`), Model Quality (Good/Moderate/Bad/no-model).

## 2026-07-22 (wpe & wso deep dive)
- Newer libs `wpe`/`wso` are **standalone-component** + **Angular Signals**
  (no local NgRx); global scope via `libs/shared` (`GlobalFilterService`,
  `DateRangeStore`).
- They call **`MicroHttpService`** (`libs/shared`), NOT PDM `ApiService`.
  URL pattern: `api/router/<routerService>/<version>/<microService>/<endpoint>`.
- WPE (`/wpe`, `WPE_ROUTES`): shell `WpeComponent` + 3 child routes —
  `well-test-management`, `well-test-validation-overview`,
  `well-test-validation-analysis`. Services hit `routerService='wpo'`, v1,
  micro-services `wpeService`/`wpoService` (well-test CRUD, diagnosis-esp/sf,
  status approve/reject, optimizations/data-analyses trends).
- WSO (`/wso`, single `WsoOverviewComponent`): dashboard with kpi/chart/map/
  detail-table subcomponents. `WsoApiService` uses
  `routerService='wellsurveillance'`, v1, micro-services `wpoService`+`opService`
  (esp-production-summaries, oil-rate-comparison, reservoir-guideline-compliance,
  wells/esp/map, operation-surveillance/wells/overview?type=losses).
- KPI variants: WSO (optimized) vs NSO (baseline) vs WT (well-test) vs
  Allocation vs Potential; loss + FBHP/WC compliance analysis.

## 2026-07-22 (merged from wpo-app/docs implementation notes)
- Package name `dfs-wpo`; MFE via `ngx-build-plus` + custom `webpack.config.js`.
- Additional feature libs: `mfe-module`, `migration` (MFE plumbing / migration).
- **Shared component layer** `libs/shared` is the single source for `com-chart`
  (ECharts), `com-map` (Leaflet — only map entry after `com-map-bridge` was
  deleted), `com-table`/`dfs-table`, `com-card`, `global-filter`,
  `date-range-filter`. Prefer `com-*` wrappers over raw `p-*`.
- **Auth**: Keycloak via `@webframework/client-core` (`AuthGuard`, `keycloak.json`).
- **Theming**: CSS-variable light/dark on `[data-theme]`; ECharts observe
  `data-theme` via `MutationObserver` and rebuild options on switch.
- **Large-batch endpoints** migrated GET→POST (JSON body) to carry thousands of
  wellIds and avoid 414 URL-length errors (e.g. `getMapInfo`, `getKpiTrend`).
- **WSO** currently mock-driven (`USE_WSO_API=false`, `WsoMockDataService`);
  API wired to fall back to mock on failure.

## 2026-07-24 (WSO chart component architecture analysis)
- **WSO charts = container/presentational + data-driven.** Smart container
  `WsoOverviewComponent` (signals: `chartPages`, `activeChartViewId`,
  `activeChartId`) feeds dumb components `WsoChartPanelComponent` and
  `ChartViewSwitcherComponent` (pure `@Input`/`@Output`, `@ContentChild('viewItem')`
  projection). Charts described as data: `WsoChartModel { id, options, configurable?,
  sliderValue? }` → `com-chart` renders from `CommonChartOptionsLite`.
- **Data-driven confirmed**: tabs/charts come from `WsoMockDataService.getChartPages()`;
  views via `*ngFor`; switching id-driven (`views.findIndex(v => v.id === activeViewId)`).
- **Extensible** for new tabs/charts (push a `WsoChartPageModel`) and mock↔API swap
  (`USE_WSO_API` + mapper). **Coupling points to refactor** for true "add business
  layer without touching container/dumb": (1) hard-coded `viewId` checks in
  `chartScopedWellMeta` ('allocation'/'potential'); (2) fixed toolbar in
  `wso-chart-panel.html` ("Last Test Rate" + single slider, `configurable` is bool
  only); (3) dedicated builders `buildComparisonChartOptions`/`buildLossChartOptions`
  (want a type-keyed `ChartOptionsFactory` registry per ADR-0002).
- Full write-up: [frontend/charts/wso-chart-panel-architecture.md](../frontend/charts/wso-chart-panel-architecture.md).

## 2026-07-24 (WSO chart refactor — coupling points resolved)
- The 3 coupling points above were refactored to data-driven in `libs/wso`:
  1. **Well scope** — added `WsoChartPageModel.wellScope: 'all'|'even'|'odd'`;
     `WsoOverviewComponent.chartScopedWellMeta` now reads `activeChartPage()?.wellScope`
     via `applyWellScope()` (removed hard-coded `viewId==='allocation'|'potential'`;
     the `'allocation'` branch was dead since page ids are `production`/`potential`).
  2. **Toolbar** — replaced `WsoChartModel.configurable/sliderValue` with
     `toolbarControls: WsoChartToolbarControl[]` (discriminated union, currently
     `kind:'slider'`); `wso-chart-panel.html` renders controls generically via `*ngFor`,
     values tracked in `sliderValues` keyed by control id.
  3. **Builder registry** — `WsoMockDataService` now has `chartOptionBuilders`
     (mapped-type `Record<type, builder>`) + `buildChartOptions(spec)`; pages declared
     as data via `getChartPageSpecs(): WsoChartPageSpec[]` with a `WsoChartOptionSpec`
     union (`comparison`|`loss`). Add a chart type = 1 union member + 1 registry entry
     (OCP, no if/else). Matches ADR-0002 Builder/Registry layer.
- Behavior preserved (chart section still commented out in `wso-overview.html`);
  compile-clean. New model types exported from `libs/wso/src/lib/shared/models`.
- How-to guide for extending with a new business layer:
  [frontend/charts/adding-a-business-layer.md](../frontend/charts/adding-a-business-layer.md)
  (Scenario A reuse types = data-only; B new chart type = union+builder+registry entry;
  C new toolbar kind = union+1 HTML branch; D real API = `USE_WSO_API` mapper + mock fallback).
  Chinese manual: [frontend/charts/chart-extension-manual-zh.md](../frontend/charts/chart-extension-manual-zh.md).

## 2026-07-24 (WSO map component architecture analysis)
- **WSO map = generic engine + domain adapter + data-driven Adapter arch.** Domain
  adapter `WsoMapPanelComponent` (signals: `wellsSig`; `computed` `mapContext`,
  `mapInfo`) maps `WsoMapWellModel[]` → generic `ComMapInfoResponse` and owns
  popup / legend / layer sidebar. Dumb `MapDisplayControlComponent` = pure
  `@Input`/`@Output` filter UI.
- **Generic engine `ComMapComponent` (`com-map`, `libs/shared`) imports zero WSO
  types** — depends only on neutral contracts `ComMapContext` / `ComMapInfoResponse`
  / `ComMapSelection` (`com-map.types.ts`). `context.source` (`'wso'`) = reserved
  hook to distinguish caller. Rendering delegated to stateless pure functions:
  `builders/com-map-point.builder`, `handlers/com-map-*.handler`,
  `utils/com-map-{filter,icon-attributes,render,lifecycle}.util`, over
  `@nextgengraphics/webviz-*` GIS lib.
- **Data-driven confirmed**: view = fn(data); `buildComMapRenderPoints` walks
  platform/well structure; icon key derived from status fields (`legendIconKey` if
  explicit, else from `wtvStatus`/`priorityStatus`/`kpiStatus`/`modelCalibrationStatus`);
  filter via `matchNode` reads `well[node.field]` dynamically.
- **Extensible** for new data sources (write another adapter panel), arbitrary fields
  (`[key:string]:unknown` on well/platform info), new filter dims, and pre-resolved
  color (builder honors explicit `legendIconKey`). **Coupling points to refactor for
  "add business layer without touching shared engine"**: (1) `ComMapLegendIconKey` is
  a closed 4-key union → want registrable icon provider; (2) `isWellWithActions`
  hard-codes domain alert rules in the engine → move to adapters; (3) only
  `type:'platform'|'well'`, no `layer` abstraction for overlays.
- Decision recorded in **ADR-0003**; full write-up:
  [frontend/components/wso-map-panel-architecture.md](../frontend/components/wso-map-panel-architecture.md).
