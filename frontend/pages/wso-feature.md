# WSO — Well Surveillance Optimization (deep dive)

> Source: `libs/wso/src/lib/` (extracted 2026-07-22)

Single-page surveillance/production dashboard. Route `/wso` → `WsoModule` /
`WSO_ROUTES` (`wso.routes.ts`) → one standalone component `WsoOverviewComponent`.

## Layout & components

`WsoOverviewComponent` (`components/wso-overview/`) composes the dashboard from
sub-component folders under `components/`:

| Area | Folder | Role |
|------|--------|------|
| KPI cards | `kpi/` | Row of metric cards (oil/gas/liquid rates: WSO vs NSO vs WT vs Allocation). |
| Charts | `chart/` | ECharts panels + a view switcher (Oil Production / Allocation / Potential). |
| Map | `map/` | Leaflet map of platforms → wells with status markers. |
| Detail table | `detail-table/` | "Top Losers" / production-loss analytical table. |

Shared UI lives in `shared/` (`com-carousel-indicator/`, `models/`,
`services/`) plus `configs/`.

## Services & endpoints

**`WsoApiService`** (`shared/services/wso-api.service.ts`) — all via
`MicroHttpService`, `routerService = 'wellsurveillance'`, version `v1`.
Two downstream micro-services: `wpoService` and `opService`.

| # | Method | HTTP | Micro-service · endpoint |
|---|--------|------|--------------------------|
| 1 | `getProductionSummaries` | GET | `wpoService` · `wpo/wells/esp-production-summaries` (KPI cards) |
| 2 | `getOilRateComparison` | GET | `wpoService` · `wpo/wells/oil-rate-comparison` |
| 3/5 | `getLossesOverview` | GET | `opService` · `ws/operation-surveillance/wells/overview?type=losses` |
| 4 | `getReservoirGuideline` | POST | `wpoService` · `wpo/well/reservoir-guideline-compliance` |
| 6 | `getMapInfo` | GET | `wpoService` · `wpo/wells/esp/map` |

Common params: `wellIds=[...]`, `date`, `timezone` (`WsoWellsRequest`).

**`WsoMockDataService`** (`services/wso-mock-data.service.ts`) — UI config /
local mapping for dashboard cards & chart layouts.

## State

Component-local **Signals** + `computed`; reacts to global scope via
`GlobalFilterService` and `DateRangeStore` (from `libs/shared`). No local NgRx.

## Models (`shared/models/`)

- `WsoWellsRequest` — `{ wellIds[], date, timezone }`.
- `WsoProductionSummary` — `oilRate/gasRate` × `Wso/Nso/Wt/Alloc`, `diffRatio`.
- `WsoStatisticalResponse` / `WsoStatisticalItem` — bar-chart data
  (`fieldName, statisticalType|key, totalValue|totalCount`).
- `WsoReservoirGuidelineRequest` — POST payload with `parameterCategories`
  (`FBHP` / `WC` + `volumeRanges`).
- `WsoLossesResponse` / `WsoLossDetailRow` — `wellName, field,
  productionLosses, wellTestLiquidRate, wellTestOilRate, downTime`.
- `WsoMapPlatform` — `{ platformName, longitude, latitude, wellData[] }`.
- also: `wso-chart.model.ts`, `wso-chart-view.model.ts`, `wso-kpi.model.ts`,
  `wso-map-filter.model.ts`, `wso-map-well.model.ts`.

## Domain meaning of the KPI variants

- **WSO** — well-surveillance-optimized rate, **NSO** — non-surveillance/baseline,
  **WT** — well-test rate, **Allocation** — allocated rate, **Potential** —
  theoretical potential. The dashboard compares these to surface production loss
  and reservoir-guideline compliance (FBHP / water-cut).

## Visualization

ECharts (KPI sparklines, grouped Measured/Allocated/Potential bars, compliance
gauges/pies) + Leaflet map (status markers, clusters). Legacy map payloads
normalized via `legacy-map-info-normalizer.service.ts` (shared).
