# Business Domains — WPE / WSO / Well Surveillance

The WPO app is split into three lazy-loaded business domains plus a demo module.
Each maps to a route and a feature library under `libs/`.

## 1. Well Surveillance (core)

Location: `libs/well-surveillance/`. The heart of the product — monitors well
health and equipment. Sub-features:

- **Run Life Analysis (RLA)** — equipment run-life results, mean-time, AERL,
  confidence intervals. Endpoints under `/well-equipment-results`, `/overview`.
- **Survival Analysis** — survival & hazard curves (incl. Weibull models) for
  equipment failure prediction. Endpoint `/survival-hazards`.
- **Well Test Management** — manage well tests, flow rates and test periods
  (`WELL_TEST`, `WELL_TEST_PERIOD` business objects).
- **WPO / Production Optimization** — production optimization tooling.
- **KPIs & Model Qualities** — model quality scoring (Good / Moderate / Bad /
  Wells without Model) at `/wells/model-qualities`.

## 2. WPE — Well Performance Evaluation

Location: `libs/wpe/`. Route `/wpe` → `WpeModule`. Evaluates well performance,
including overview model-quality (`wpe/overview/`), well lists (`wpe/wells`),
and well-test validation (WTV/WTE).

## 3. WSO — Well Surveillance Optimization

Location: `libs/wso/`. Route `/wso` → `WsoModule`. Surveillance optimization
workflows.

## Cross-cutting

- **Filtering** — a shared `common-lib-filter` component drives data refinement
  across features; filter state is held in NgRx (e.g. `SDHFilter`).
- **MFE context** — the active page/module (`activePage` state) determines the
  backend service route and API base for each feature (see `MfeInit`).
