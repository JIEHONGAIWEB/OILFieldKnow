# WPE — Well Performance Evaluation (deep dive)

> Source: `libs/wpe/src/lib/` (extracted 2026-07-22)

Standalone-component Angular feature. Route `/wpe` → `WpeModule` /
`WPE_ROUTES` (`wpe.routes.ts`). Focused on **well test** entry, review,
validation and diagnosis.

## Routing & pages

Parent shell `WpeComponent` (`wpe.component.ts`) with three lazy child routes
(all `loadComponent`, standalone):

| Path | Component | Purpose |
|------|-----------|---------|
| `well-test-management` | `WellTestManagementComponent` | Create / edit / delete well tests & measurements. |
| `well-test-validation-overview` | `WellTestValidationOverviewComponent` | Filterable dashboard of well tests to review (batch view). |
| `well-test-validation-analysis` | `WellTestValidationAnalysisComponent` | Deep-dive on one well test: diagnosis + measured-vs-model trend charts, approve/reject. |

Folder layout: `features/<feature>/{components,configs,services}`,
plus lib-level `services/`, `models/`, `configs/`, `util/`.

## Services & endpoints

All calls go through `MicroHttpService` (see
`api/rest/microservice-api.md`) with `routerService = 'wpo'`, version `v1`.

**`WpeService`** (`services/wpe.service.ts`)
- Holds `selectedDateRange` signal.
- `getAllWellFlowTest(wellIds, dateRange, hasCalibration, wellTestType='Flow Test')`
  → GET `wpo`/`v1`/`wpeService`/`wtv/wells/well-tests/review/history`.
  Flattens `wellTestDetail[]` and copies well metadata onto each row.

**`WellTestManagementService`** (`features/well-test-management/services/`)
- `addWellTest(model)` → POST `wpeService` `wtv/wells/well-tests`.
- `updateWelltest(model)` → PUT `wpeService` `wtm/wells/well-tests/{wellTestId}`.
- `deleteWelltest(wellTestId, wellTestPeriodId)` → DELETE
  `wtm/wells/well-tests/{id}/well-test-periods/{periodId}`.
- Builds a rich `wellTestMeasurements` payload (see measurement fields below).

**`WellTestValidationAnalysisService`** (`features/well-test-validation-analysis/services/`)
- `getdiagnosis(wellTestId, producingMethod)` → GET
  `wpeService` `wtv/wells/well-tests/{id}/diagnosis-{esp|sf}`
  (ESP/GL → `esp`, otherwise → `sf`).
- `getWellTrendsData(type, wellId, params, dateRange)` → GET
  `wpoService` `/wpo/wells/{wellId}/optimizations/data-analyses`
  with `realtimeSeries` (type `realtime`) or `wellTestSeries` (type `test`).
- `updateValidationStatus(wellTestId, wellTestPeriodID, 'Approved'|'Rejected')`
  → PUT `wpeService` `/v1/wtv/wells/well-tests/status`.

## Well test measurement fields (payload)

`chokeSize, fthp, waterContent, totalGOR, gLIP, mlglp, separatorTemperature,
separatorPressure, pumpIntakePressure (pI), pumpDischargePressure (pD),
frequency, fGOR, iGLR, wellSalinity, tGLR, liquidRate, gasLiftRate (gLIR),
oilRate, totalGasRate, waterRate, formGas, condensate, wGR, cGR`.
Header: `startDate, endDate, remark, testDuration, wellId, wellTestPeriodId`.

## State

Uses **Angular Signals** (not NgRx) for local state — e.g. `selectedDateRange`
in `WpeService`, selection/linkage state across the validation flow. Global
scope comes from `libs/shared` (`GlobalFilterService`, `DateRangeStore`).

## Models

`models/well-test.model.ts` currently holds the commented-out reference shape
(`WellTest`: `oilRate/gasRate/waterRate/waterCut/gor/buildup/status`,
`WellTestStatus = Approved|Pending|Rejected|Draft`) — live payloads are
untyped (`any`). Producing methods seen: ESP, GL, SRP, SF.

## Visualization

- ECharts (`ngx-echarts`) for validation distribution + measured-vs-model
  multi-axis trend cross-plots.
- PrimeNG `Splitter` for resizable overview panels; Table/Dialog/Card for
  well-test lists and forms.
