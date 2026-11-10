# pages

One file per page/route: purpose, key components, data dependencies.

Page-level (route) components live inside the `libs/` feature libraries of
`wpo-app`. Top-level routes are registered in
`src/app/app-routing.module.ts` and delegate to each library's own routes.

## Routes & page components

### `/wso` — Well Surveillance Overview
- Lib: `libs/wso` (`wso.routes.ts`)
- Page: `WsoOverviewComponent` (`components/wso-overview/`)
- Sub-widgets: `chart/`, `detail-table/`, `kpi/`, `map/`

### `/wpe` — Well Performance Engineering
- Lib: `libs/wpe` (`wpe.routes.ts`), shell `WpeComponent` with child routes:
  - `well-test-management` → `WellTestManagementComponent`
  - `well-test-validation-overview` → `WellTestValidationOverviewComponent`
  - `well-test-validation-analysis` → `WellTestValidationAnalysisComponent`
- Feature code under `libs/wpe/src/lib/features/`

### Well analysis (well-surveillance)
- Lib: `libs/well-surveillance` (`src/lib/wpo/`)
  - `overview/` — asset overview pages
  - `well-analysis/` → `esp/`, `srp-new/`, `well-analysis-common/`
    (ESP and Sucker Rod Pump analysis, incl. dynacard & well-trend charts)

### `/demo`, `/wpo-test`
- Lib: `libs/demo` — sandbox / demo routes.

> Commented-out routes in `app-routing.module.ts` (`map`, `start`, `iframe`,
> `shared-store`, remote `tdemo`…) are inactive; do not assume they are live.
