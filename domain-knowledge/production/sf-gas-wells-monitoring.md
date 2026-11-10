# SF Gas Wells — Production Monitoring KPIs

Subject-matter grounding for the **SF Gas Wells (Self-Flow / Natural-Flow Gas
Wells)** production overview. Same dashboard template as SF Oil Wells / ESP Wells,
but the **primary monitored product changes from oil to gas**.

> Read alongside [oil-rate-kpis.md](oil-rate-kpis.md) and
> [esp-wells-monitoring.md](esp-wells-monitoring.md). The three dashboards share
> one page template driven by **Production Method** (see "Config note" below).

## Config note (known UI pitfall)

On the Gas page the 4th KPI is sometimes still labelled **"Potential Oil Rate -
SH-IN"**; on a Gas dashboard it should read **"Potential Gas Rate - SH-IN"**. This
is a leftover from an incomplete dashboard config — a common front-end
configuration bug when one template serves multiple production methods. It is
exactly the class of error the KPI-config abstraction is meant to prevent (see
[ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)).

## Gas production flow

Gas wells differ slightly from oil wells: they usually flow on **reservoir
pressure (Natural Flow)** and do **not** need artificial lift such as ESP.

```
Gas Reservoir
      │
      ▼
   Gas Well
      │
      ▼
  Wellhead
      │
      ▼
Gas Gathering Pipeline
      │
      ▼
Gas Processing Plant
      │
      ▼
 Sales Gas
```

So SF Gas Wells focus on: how much gas is produced now, how much could be
produced, and whether there is any shut-in loss.

## The KPIs

### 1. Gas Rate (WSO)
Here **WSO = Well Stream** (wellhead fluid), not Oil. Means **wellhead daily gas
rate**. Example `5,120`; in MMSCFD that is 5.12 Million Standard Cubic Feet per
Day (or Sm³/day). Answers: "how much gas are all SF Gas Wells producing now?"

### 2. Gas Rate (WT)
**WT = Well Test** → gas rate measured during a well test
(`Gas Well → Test Separator → Gas Meter → measured`). Example `7,055`. Well tests
are needed because many wells share one gathering system, so periodic tests
calibrate the allocation.

### 3. Gas Rate — Allocation
Splits total station flow to each well by algorithm (not a direct measurement).
Example: station total `100 MMSCFD`, 20 wells → Well A 15, Well B 8, Well C 10, …

### 4. Potential Gas Rate — SH-IN
Gas production **lost due to shut-in**. Example: normal `100 MMSCFD`, shut for
maintenance, loss `8 MMSCFD` → card shows `8`. Managers track daily **Lost Gas
Production**. (This is the KPI mislabelled as "Oil" in the config note above.)

### 5. Potential Gas Rate (WSO)
Theoretical achievable gas rate. Example: current `80 MMSCFD`, potential
`100 MMSCFD` → `20 MMSCFD` upside. Constraints: choke restriction, high line
pressure, insufficient compressor capacity, declining reservoir pressure, or
gathering-system bottlenecks.

## KPIs gas wells care about most (pressure & flow)

| KPI | Meaning / why it matters |
| --- | --- |
| Gas Rate | How much gas now — the primary KPI |
| Wellhead Pressure | Reservoir → Wellhead; a drop signals declining reservoir energy |
| Tubing Pressure | Judges wellbore flow condition |
| Casing Pressure | Anomaly may mean leakage, cross-flow, or casing problems |
| Choke Size | Choke opening controls gas flow; engineers adjust it daily |
| Line Pressure | Rising line pressure chokes flow → Gas Rate falls |
| Compressor Status | Compressor down → gas production drops immediately |

## Gas dashboard business logic

```
                  SF Gas Wells Dashboard
                     Gas Production
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   Gas Rate (WSO)    Well Test Rate    Allocation Rate
                           │
                           ▼
                 Production Performance
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    Current Gas      Potential Gas      Shut-in Loss
                           │
                           ▼
                  Pressure Management
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
 Wellhead Pressure   Tubing Pressure   Line Pressure
                           │
                           ▼
                   Compression System
                           │
                           ▼
                  Compressor Status
```

## Oil vs Gas dashboards

| Aspect | Oil Wells | Gas Wells |
| --- | --- | --- |
| Primary product | Oil | Gas |
| Core KPI | Oil Rate | Gas Rate |
| Main constraints | Pump, water cut, lift efficiency | Pressure, choke, compressor |
| Common equipment | ESP, Rod Pump, Gas Lift | Choke, Compressor, Gas Meter |
| Common units | BOPD | MMSCFD, Sm³/day |
| Focus | Lift efficiency, equipment health | Pressure management, flow control, compression capacity |

## Product-design takeaway

SF Oil Wells, ESP Wells and SF Gas Wells share **one page template**, switching
metrics and data sources by **Production Method**. Implement KPI lists and units
as **configuration** (per Oil / ESP / Gas) rather than three separate pages — this
also prevents leftover-label bugs like "Potential Oil Rate - SH-IN" appearing on
the Gas page. See [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md).

## Glossary

| Term | Meaning |
| --- | --- |
| SF | Self Flow / Natural Flow (no artificial lift) |
| WSO | Well Stream (wellhead fluid); on gas pages the stream's gas portion |
| WT | Well Test (rate measured at a Test Separator / Gas Meter) |
| Allocation | Splitting total station flow to individual wells by algorithm |
| SH-IN | Shut In — the well is closed |
| MMSCFD | Million Standard Cubic Feet per Day |
| Sm³/day | Standard cubic metres per day |
| Choke | Wellhead valve controlling flow rate |
| Line Pressure | Gathering-pipeline pressure |
