# Production Monitoring KPIs — Oil Rate & Potential

Subject-matter grounding for the **Well Activity Hub** production-monitoring
dashboard (e.g. *SF Oil Wells*). The top-of-page KPI cards track a well group's
oil production from several independent sources. Each card typically shows a value
plus a **"FROM YESTERDAY ±x%"** day-over-day comparison.

> This is domain knowledge (what the numbers *mean*), not a spec of any one
> screen. For the surveillance product family see
> [wpo-surveillance-concepts.md](wpo-surveillance-concepts.md).

## Why there are multiple "Oil Rate" numbers

A well never produces pure oil — the wellhead stream is a mix:

```
Wellhead fluid
   ├── Oil
   ├── Gas
   └── Water
```

Production is measured/estimated by **two independent systems**, which is why the
dashboard shows several oil-rate values that rarely match exactly:

- **Allocation** — real-time, computed from total station flow split back to each
  well by algorithm.
- **Well Test (WT)** — a single well is routed to a Test Separator and its oil is
  physically measured.

## Quick read for table columns (WSO / WT / ALLOC)

In detail tables, these three columns are often shown side by side:

| Table column | In petroleum domain | Primary use |
| --- | --- | --- |
| OIL RATE_WSO | Well Stream Oil rate (current oil from mixed well stream) | Real-time production status |
| OIL RATE_WT | Well Test measured oil rate (single-well test separator result) | Ground-truth reference and model calibration |
| OIL RATE_ALLOC | Allocated oil rate (per-well attribution from shared total) | Accounting/attribution across commingled wells |

How to interpret differences:

- `WT` is usually closer to a measured single-well baseline, but updates by test frequency.
- `WSO` is usually more time-sensitive for daily operations.
- `ALLOC` is an attribution value and should be interpreted with allocation assumptions.
- Large divergence among the three is a surveillance signal, not automatically a data error.

## The KPIs

### 1. Oil Rate (WSO) — Well Stream Oil

- **Means**: the oil portion of the wellhead mixed stream (Well Stream Oil Rate).
- **Unit**: BOPD (Barrels Oil Per Day) or m³/day.
- **Example**: `5,120` → the well group currently produces ~5,120 bbl/day of oil.
- **Business value**: real-time production monitoring — "how much are we actually
  producing right now?"

### 2. Oil Rate (WT) — Well Test Oil Rate

- **Means**: oil rate physically measured during a **well test** (single well →
  Test Separator → Oil/Gas/Water measured). The *true* measured well rate.
- **Example**: `7,055` → the test measured ~7,055 bbl/day.
- **Business value**: validates production status and calibrates the well model.

### 3. Oil Rate — Allocation (Production Allocation)

One of the **core KPIs of the digital oilfield**.

- **Problem it solves**: many wells share one pipeline, so the total flow is known
  but the per-well share is not.

  ```
  10 wells → one pipeline → 10,000 bbl/day total
  → per-well share unknown
  ```

- **How**: the system splits the total using Well Test, Pressure, Choke, PI, GOR,
  Water Cut, etc.

  ```
  10,000 → Well A 1,000 · Well B 1,500 · Well C 900 · …
  ```

- **Example**: `235` → allocation assigns ~235 bbl/day to this well/group.
- **Business value**: production attribution when multiple wells share a line.

### 4. Potential Oil Rate — SH-IN (Shut-In / Lost Production)

- **SH-IN = Shut In** = the well is closed (maintenance, abnormal pressure, etc.).
- **Means**: how much the well *would* produce if it were **not** shut in — i.e.
  the production being lost right now.
- **Example**: `234` → ~234 bbl/day lost due to shut-in.
- **Business value**: this is **Lost / Deferred Production**. Operators track
  daily deferred production (from shut-in, maintenance, failure) to quantify loss
  and plan production recovery.

### 5. Potential Oil Rate (WSO) — Production Potential

- **Means**: theoretical producible capacity (not a loss). What the well *could*
  reach if optimized, vs what it actually produces.
- **Example**: actual `200`, potential `234` → ~34 bbl/day of upside, constrained
  by pump efficiency, choking, pressure or equipment limits.
- **Business value**: identifies uplift opportunities and optimization measures
  ("Production Potential").

## "FROM YESTERDAY +3.4%"

Day-over-day change used for daily production monitoring.

```
Yesterday 4,950 · Today 5,120 → +3.4%
```

## Relationship map

```
                 Oil Production Dashboard
                       Current production
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  Oil Rate (WSO)        Oil Rate (WT)        Allocation Rate
  wellhead actual       well-test measured   allocated/computed
        │
        ▼
  vs yesterday (+3.4%)
──────────────────────────────────────────────────────────────
                     Potential Production
        ┌───────────────────────────────────┐
        ▼                                   ▼
  Potential Rate                     Shut-in Potential
  theoretical max capacity           capacity lost to shut-in
```

## Business questions each KPI answers

| KPI | Question | Business value |
| --- | --- | --- |
| Oil Rate (WSO) | How much oil are we actually producing now? | Real-time production monitoring |
| Oil Rate (WT) | What is the true measured single-well rate? | Validate status, calibrate model |
| Oil Rate — Allocation | How much should each well be credited? | Attribution when wells share a line |
| Potential Oil Rate (WSO) | With no limits, how much could we produce? | Spot uplift / optimization opportunities |
| Potential Oil Rate — SH-IN | How much is lost due to shut-in? | Quantify deferred production, plan recovery |

On digital-oilfield platforms (Halliburton, SLB, Baker Hughes) these are core
production-monitoring homepage indicators that production engineers watch daily.

## Glossary

| Term | Meaning |
| --- | --- |
| WSO | Well Stream Oil (oil portion of the wellhead stream) |
| WT | Well Test (oil rate physically measured at a Test Separator) |
| Allocation | Production Allocation — splitting total flow to individual wells |
| SH-IN | Shut In — the well is closed |
| BOPD | Barrels Oil Per Day |
| GOR | Gas-Oil Ratio |
| PI | Productivity Index |
| Water Cut | Water fraction of total produced liquid |
| Deferred / Lost Production | Production lost to shut-in, maintenance, failure |
| Production Potential | Theoretical producible capacity vs actual |
