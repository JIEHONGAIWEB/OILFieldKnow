# KPI Layers per Business Layer

The **KPI / Metric Layer is not flat** — KPIs stratify by the **business layer**
they belong to. This is the concrete taxonomy behind the Metric Layer in
[ADR-0002](../architecture-decision/0002-data-driven-chart-layering.md): a KPI
should belong to exactly one business layer, and each business layer owns its own
KPI set.

## Two orthogonal stratifications

KPIs are organized along two independent axes:

1. **By business-capability layer** (the digital-oilfield platform layers).
2. **By domain object** (the ADR-0002 Business Layer: Well / Production / Equipment).

A third axis — **Production Method** (SF Oil / ESP / SF Gas / GL) — cross-cuts both
and selects *which* KPI set within a layer applies (see
[frontend/ui-patterns/wso-kpi-by-production-method.md](../frontend/ui-patterns/wso-kpi-by-production-method.md)).

## Axis 1 — KPI layer per business-capability layer

```
Digital Oilfield
├── ① Production Monitoring   → Production KPI layer
├── ② Asset Health           → Equipment/Reliability KPI layer
├── ③ Well Model Management   → Model-Quality KPI layer
└── ④ Production Optimization → Potential/Opportunity KPI layer
```

| Business layer | KPI layer | Example KPIs | Source of truth |
| --- | --- | --- | --- |
| ① Production Monitoring | Production KPIs | Oil/Gas Rate (WSO/WT/Allocation) | [oil-rate-kpis](../domain-knowledge/production/oil-rate-kpis.md), [sf-gas](../domain-knowledge/production/sf-gas-wells-monitoring.md) |
| ② Asset Health | Equipment / Reliability KPIs | Motor Current, PIP, Pump Efficiency, MTBF, RUL, Failure Count | [esp-wells-monitoring](../domain-knowledge/production/esp-wells-monitoring.md) |
| ③ Well Model Management | Model-Quality KPIs | Validation status, Calibration status, Model KPI/Accuracy, Test Priority | [well-model-management](../domain-knowledge/well-model-management.md) |
| ④ Production Optimization | Potential / Opportunity KPIs | Potential Oil/Gas Rate, Shut-in loss, Gas-Lift efficiency | [gl-wells-monitoring](../domain-knowledge/production/gl-wells-monitoring.md) |

## Axis 2 — KPI layer per domain object (ADR-0002 Business Layer)

```
Business Layer
├── Well        → wellbore KPIs (WHP, Tubing/Casing Pressure, Fluid Level)
├── Production  → production KPIs (Oil/Gas Rate, Water Cut, GOR, Allocation)
└── Equipment   → equipment KPIs (ESP Motor Current/Temp, Compressor, Choke)
```

Each domain object contributes its own KPIs; a dashboard composes the layers it
needs (e.g. an ESP dashboard = Production + Equipment; a Gas dashboard =
Production + Wellbore-pressure + Compression).

## The stratified KPI stack (per method)

A digital-oilfield dashboard typically layers KPIs like this (GL example):

| KPI layer | KPIs |
| --- | --- |
| Production | Oil Rate, Water Rate, Gas Rate, Allocation, Potential |
| Equipment | Pump Frequency, Motor Current, Voltage, Power, Temperature, Runtime |
| Wellbore | PIP, Tubing Pressure, Casing Pressure, Fluid Level |
| Reliability | Health Score, Failure Risk, RUL, MTBF, Failure Count |
| Economics | Power Cost, Cost per Barrel, Deferred Production, Loss |

## Mapping to ADR-0002 and the code

- **ADR-0002 Metric Layer** = the union of these KPI layers; each layer is one
  cohesive metric set.
- **Registry keyed by (business layer, production method)** — the `libs/wso`
  `registerKpiSet(method, summaries)` keys KPI sets by production method and
  stratifies by business layer via summaries: `OILESP` registers a Production
  summary **and** an Equipment-Health summary; `OILGL` registers Production +
  Gas-Injection. `OILSF` / `GASF` are Production-only.
- **Design rule**: a KPI lives in exactly one business layer; dashboards compose
  layers rather than duplicating KPIs across them.

## Design guidance

- Put a new KPI in the **one** business layer that owns it; don't scatter it.
- Model each business layer as its own **summary / template set**; a well type
  registers the layers it needs (Production always; Equipment for ESP; Wellbore +
  Compression for Gas; Gas-Injection for GL).
- Keep the layer taxonomy in config (registry), so adding a layer or a method is a
  registration, not a central `switch` edit (OCP).

## Related

- [ADR-0002](../architecture-decision/0002-data-driven-chart-layering.md) — Metric Layer + registry rationale.
- [frontend/ui-patterns/wso-kpi-by-production-method.md](../frontend/ui-patterns/wso-kpi-by-production-method.md) — how the method axis is implemented in `libs/wso`.
- Domain KPIs: [production/](../domain-knowledge/production/README.md), [well-model-management](../domain-knowledge/well-model-management.md).
