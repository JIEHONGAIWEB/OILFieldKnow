# Well Model Management Dashboard

Subject-matter grounding for the **Well Model Management** dashboard — a
Production-Engineering / Production-Optimization module, **not** a production
monitor. It does not answer *"how much oil did we produce today?"* but rather:

> **Are our well models trustworthy? Which wells need re-calibration? Which wells
> should be well-tested first?**

> Related: [wpo-surveillance-concepts.md](wpo-surveillance-concepts.md) (WPE / Well
> Test Validation / Model Quality) and the production-monitoring docs under
> [production/](production/README.md).

## Where it sits in the digital-oilfield platform

```
Digital Oilfield
│
├── ① Production Monitoring   • Oil/Gas Rate • Allocation • Potential
├── ② Asset Health            • ESP • Compressor • Pump
├── ③ Well Model Management   ← this dashboard
│      • Well Test Validation • Model Calibration • Model KPI • Test Priority
└── ④ Production Optimization • Nodal Analysis • Lift Optimization • Forecast
```

This page is a **well-model governance center** for production engineers, and is
typically the quality-control link between field data (**SCADA / Historian**) and
production-optimization models (**PIPESIM, PROSPER, GAP, OLGA**).

## The lifecycle it manages (Well Model Lifecycle)

```
Well Production Data
      → Well Test
      → Validate Test
      → Well Model Calibration
      → KPI Evaluation (model scoring)
      → Priority Management
      → Engineer Action
```

## Panels

### Well Test Validation Status (top-left)
Validation state of well-test data. After a test, data is not used immediately:
`field test → upload → auto-validate → user confirm → put in use`. Each well has a
status:

| Color | Status | Meaning |
| --- | --- | --- |
| Green | Approved | Data trustworthy |
| Yellow | Pending User Action | Needs manual confirmation |
| Red | Rejected | Data anomaly |
| Grey | Awaiting Processing | Not yet started |

E.g. `368 Wells`, most Approved → good data quality.

### Well Model Calibration Status (middle-left)
State of the well model (built in Prosper / GAP / PipeSim / OLGA). Models must be
continuously **calibrated**: if theoretical `1,000 bbl/day` vs actual `850`, the
deviation is too large → re-calibrate. Statuses: Approved / Pending / Failed /
Rejected. All grey usually means calibration not started (or demo data).

### Well Model KPI Status (bottom-left)
**Model scoring**, not production KPI. Per-well **Accuracy**:

| Error | Rating |
| --- | --- |
| < 5% | Excellent |
| 5–10% | Good |
| 10–20% | Average |
| > 20% | Poor |

Answers *"how good is the model?"* — not well quality. Many `NA` = wells without a
Model KPI yet.

### Well Test Priority Status (center)
What engineers care about most: which wells to **test first**. The system computes
Priority from many factors — model error + production change + time since last test
+ alarms + water-cut change — then buckets into **Low / Medium / High**. Many High
= many wells need re-testing.

### Well Model KPI Trend (bottom)
Model-KPI trend over time — e.g. share of `Excellent` per month (2024: 50% →
2025: 80% = models getting more accurate). A **platform** KPI, not per-well.

### Map (right) — GIS + Dashboard
The most important panel. Each point is a well (e.g. `LMK-Well-0032`); clicking
opens Well Detail. The map shows **well status**, not production.

#### Map Display Control
Switch how the map is colored:
- **Well Test Validation** → colored by validation (green Approved / red Rejected).
- **Model Calibration Status** → colored by calibration state.
- **Well Model KPI** → colored by model quality (green Excellent / red Poor).

#### Legend
- Green = **Well Without Actions** — nothing to do.
- Red = **Well With Actions** — engineer must act (re-test / re-calibrate /
  re-validate).

## Business logic

```
                    Well Model Dashboard
                           Wells
        ┌────────────────────┼──────────────────┐
        ▼                    ▼                  ▼
 Well Test              Well Model         Engineer Action
 Validation             Calibration
        │                    │
        ▼                    ▼
 Validation KPI      Calibration KPI
        └──────────────┬─────┘
                       ▼
                Model KPI Evaluation
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Excellent        Average         Poor
                       ▼
               Well Priority Ranking
                       ▼
              Map Visualization (GIS)
                       ▼
             Engineer selects a Well
                       ▼
           Validate → Calibrate → Close
```

## Glossary

| Term | Meaning |
| --- | --- |
| Well Model | Physics/nodal model of a well (Prosper, GAP, PipeSim, OLGA) |
| Well Test Validation (WTV) | Validating well-test data before use |
| Model Calibration (WMC) | Tuning the model so predicted ≈ actual rates |
| Model KPI / Accuracy | How closely the model matches measured production |
| Test Priority | Ranking of which wells to well-test first |
| SCADA / Historian | Field data acquisition / time-series store |
| Well With/Without Actions | Whether a well needs engineer intervention |

## Source Mapping — `libs/wpe` Well Test Validation Overview

This dashboard is implemented as the **WTV (Well Test Validation) Overview**
feature. It is config-driven around four *status domains* that map 1:1 to the
left-hand panels and the map coloring.

- **Feature root**:
  `libs/wpe/src/lib/features/well-test-validation-overview/`
  - `components/` — `well-test-validation-overview/` (page), `chart-panel/`
    (KPI trend), `detail-table/`, `map-panel/`, `map-filter-panel/`.
  - `shared/` — `services/` (`well-test-validation-api.service.ts`,
    `well-test-validation-context.service.ts`), `config/`, `models/`, `state/`,
    `util/`, and `com-legend-popover/` (see
    [frontend/components/README.md](../frontend/components/README.md)).
- **Status domains = source of truth**:
  `shared/config/status-semantic.config.ts`
  - `WtvDomain = 'validation' | 'calibration' | 'kpi' | 'priority'` — the four
    domains behind the panels/map (the same config-by-key pattern as
    [ADR-0002](../architecture-decision/0002-data-driven-chart-layering.md)).
  - `STATUS_SEMANTIC_CONFIG: Record<WtvDomain, StatusSemantic[]>` — the statuses
    per domain (see table below).
  - `WTV_DOMAIN_LABELS` — panel titles; `WTV_DOMAIN_WELL_FIELD` — the well field
    each domain colors the map by; `WTV_FILTER_DOMAIN_ORDER` — map-filter order.

### Domain → panel → statuses → map field

| WtvDomain | Panel (`WTV_DOMAIN_LABELS`) | Statuses (`STATUS_SEMANTIC_CONFIG`) | Map field (`WTV_DOMAIN_WELL_FIELD`) |
| --- | --- | --- | --- |
| `validation` | Well Test Validation Status | Approved · Rejected · Pending User Action · Awaiting Processing | `wtvStatus` |
| `calibration` | Model Calibration Status | Failed Auto Calibration · Pending User Action · Approved · Rejected · Awaiting Processing | `modelCalibrationStatus` |
| `kpi` | Well Model KPI | Excellent · Good · Average · Poor · NA | `kpiStatus` |
| `priority` | Well Test Priority | Low · Medium · High | `priorityStatus` |

- **KPI trend** (bottom panel) comes from `WellTestValidationApiService` (KPI-trend
  endpoint). Its series fields are `excellent/good/moderate/poor/wellWithoutModel
  Percentage` — note the trend uses **`moderate`** and a **`wellWithoutModel`**
  bucket, whereas the KPI status domain uses **`Average`** and **`NA`**; treat
  these as the same concepts under different labels.
- Colors/legend for each status come from `shared/config/palette.config.ts` and
  `legend.config.ts`, rendered via `com-legend-popover`.
