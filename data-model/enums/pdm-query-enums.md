# WPO Enumerations

> Source: `src/app/model/app.enums.ts`

## PDM query enums

- **`Operator`** — `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `LESS_THAN`,
  `GREATER_OR_EQUALS`, `LESS_OR_EQUALS`, `BETWEEN`, `NOT_BETWEEN`, `IN`,
  `NOT_IN`, `LIKE`, `NOT_LIKE`, `JSONB_FIND_LIKE`, `JSONB_FIND_EXACT`
- **`AggregateFunction`** — `MAX`, `MIN`
- **`OrderByOrder`** — `ASC`, `DESC`

## Endpoints & module routing

- **`EndpointUrl`** — `/well-equipment-results` (RUN_LIFE), `/overview`,
  `/survival-hazards` (SURVIVAL_ANALYSIS), `/kpis`, `wafByPassRules`,
  `/wells/model-qualities`
- **`MODULE_END_POINT`** — `rla` (Run Life Analysis), `wmc` (Well Model
  Calibration), `wte` (Well Test Evaluation), `wpe/overview/`, `wpo`,
  `well-monitor` (Real-time Operational), `/well-tests`, `wtv`, `wpe`, `ws`,
  `wpe/wells`, `monitor`
- **`SERVICES_ROUTES`** — `wellsurv-app-runlifeanalysis`,
  `wpoProductionOptimizationService` (well analysis optimization),
  `wellsurv-perfevaluation` (performance evaluation)

## Charts & analysis

- **`SurvivalAnalysisChartType`** — `HAZARD_TYPE`, `SURVIVAL_TYPE`
- **`SurvivalAnalysisChartDataType`** — `hazard`, `survival`, `weibullSurvival`,
  `wellbullHazard`
- **`ChartType`** — `PIE`, `AL_BAR`, `FAILURE`, `AERL`, `MEANTIME`,
  `CONFIDENCE_INTERVAL`
- **`PageName`** — `RUN_LIFE_DETAIL_PAGE`, `OVERVIEW_PAGE`,
  `SURVIVAL_ANALYSIS_PAGE`

## Domain values

- **`MODEL_QUALITY`** — `Good`, `Bad`, `Moderate`, `Wells without Model`
- **`RUN_LIFE_MODULE_EVENTS`** — `EXPORT_TO_EXCEL`, `REFRESH_CHARTS`,
  `REFRESH_FILTER_EVENT`, `RESET_FILTER_EVENT`
