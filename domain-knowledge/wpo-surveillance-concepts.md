# WPO Domain Knowledge — Surveillance & Performance

> 中文版：[wpo-surveillance-concepts-zh.md](wpo-surveillance-concepts-zh.md)

Subject-matter grounding for the WPO application.

## The product family

- **WPO — Well Performance Optimization**: optimize production from wells.
- **WPE — Well Performance Evaluation**: assess how each well performs vs its
  model; surfaces model quality (Good / Moderate / Bad / no model).
- **WSO — Well Surveillance Optimization**: optimize the surveillance workflow.
- **Well Surveillance (core)**: continuous monitoring of well & equipment health.

## Key analytics

### Run Life Analysis (RLA)
Studies how long downhole equipment (e.g. ESP — Electric Submersible Pump) runs
before failure. KPIs: **AERL** (Average Estimated Run Life), **MEANTIME**,
failure counts, confidence intervals. Endpoint family `/well-equipment-results`,
service `wellsurv-app-runlifeanalysis`.

### Survival Analysis
Statistical failure modelling of equipment:
- **Survival curve** — probability of surviving past time *t*.
- **Hazard curve** — instantaneous failure rate at time *t*.
- **Weibull** variants (`weibullSurvival`, `wellbullHazard`) fit a Weibull
  distribution to the failure data.
Endpoint `/survival-hazards`.

### Well Test Management
A **Well Test** measures a well's flow rates over a **Well Test Period**. Used to
validate/ calibrate well models (WTV — Well Test Validation, WMC — Well Model
Calibration). Business objects: `WELL_TEST`, `WELL_TEST_PERIOD`.

### Model Quality
Each well's production model is rated `Good` / `Moderate` / `Bad`, or flagged as
`Wells without Model`. Surfaced on the WPE overview (`/wells/model-qualities`).

## PDM / Business Objects

The backend is **PDM (Petroleum Data Management)**. Domain data is exposed as
**Business Objects (BO)** queried via a generic `BOQuery` (see
`data-model/entities/pdm-boquery.md`). A BO has attributes with a `unitPolicy`
controlling unit conversion — critical because oilfield data mixes metric and
imperial units, and is timezone-sensitive (rates are per-day/per-hour).
