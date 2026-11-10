# GL Wells — Gas Lift Production & Injection KPIs

Subject-matter grounding for the **GL Wells (Gas Lift Wells)** dashboard. Same page
template as the other production methods, but GL is unique: **it produces oil AND
must inject gas to lift that oil.** Hence the dashboard adds a summary toggle:

- ● Oil Production Summary
- ○ Gas Injection Summary (SCMD)

> Read alongside [oil-rate-kpis.md](oil-rate-kpis.md),
> [esp-wells-monitoring.md](esp-wells-monitoring.md) and
> [sf-gas-wells-monitoring.md](sf-gas-wells-monitoring.md). The four dashboards
> share one template switched by **Production Method**
> ([ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)).

## What is Gas Lift (GL)?

An artificial-lift method: continuously inject high-pressure gas downhole.

```
        Surface
          │
     Production Tubing
          ▲
          │
      Oil + Gas ↑↑↑
          │
──────────┼────────────
          │
     Gas Lift Valve
          ◀──── Inject Gas
          │
──────────┼────────────
          │
       Reservoir
```

Injected gas lowers the oil-column density → the fluid column gets lighter →
reservoir pressure can push the oil up. In short: **not pumped up, but "blown" up
with gas.**

## Why Gas Lift is needed

As a field depletes, reservoir pressure drops: early on it is enough for **Self
Flow**; years later the oil can no longer reach surface. Artificial-lift options
include ESP, Rod Pump and Gas Lift. GL suits **deep wells, high-rate wells,
offshore platforms and sandy wells** — so offshore fields use GL heavily.

## Why the dashboard has two summaries

GL simultaneously manages `Gas → Injection → Oil Production`, so it must watch two
sides:

- **Oil Production Summary** — "after injecting gas, how much oil was produced?"
  (Oil Rate, Allocation, Potential Oil)
- **Gas Injection Summary** — "how much gas was injected to produce it?"
  (Injection Rate, Injection Pressure, Gas Consumption)

A GL dashboard therefore always has one extra **Gas Injection View** vs an ESP
dashboard.

> Note: a demo may still show `Gas Rate` under Oil Production Summary — that is
> placeholder data; in production it switches to `Oil Rate`. Same class of config
> pitfall noted for SF Gas Wells.

## Oil Production Summary KPIs

| KPI | Meaning |
| --- | --- |
| Oil Rate | Oil the gas-lift well produces now (e.g. 5,120 BOPD) |
| Well Test | True measured rate; calibrates the gas-lift model |
| Allocation | Platform total metered, then split per GL well |
| Potential Oil | Extra oil achievable by tuning gas injection |

**Potential Oil example**: at `2 MMSCFD` injection → `600 BOPD`; raise to
`2.5 MMSCFD` → `720 BOPD`, so Potential = 720.

## Gas Injection Summary KPIs

| KPI | Meaning |
| --- | --- |
| Injection Gas Rate | Gas injected per day (SCMD or MMSCFD) |
| Injection Pressure | e.g. 2,500 psi; too low → lift fails |
| Injection Temperature | Temperature of the injected gas |
| Gas Lift Valve Status | Whether each valve stage is open/closed (Valve 1 Open, Valve 2 Closed) |
| Compressor Status | GL's biggest equipment; gas must be compressed — compressor down → all GL wells drop |
| Gas Injection Efficiency | The most important GL KPI — oil gained per gas injected (e.g. 15 bbl / 1,000 m³) |

**Gas Injection Efficiency** is what engineers optimize daily: inject `1,000 m³` →
gain `15 bbl` → efficiency `15 bbl / 1,000 m³`.

## GL dashboard business logic

```
                    GL Wells Dashboard
                           │
      ┌────────────────────┴────────────────────┐
      ▼                                         ▼
Oil Production Summary               Gas Injection Summary
      │                                         │
      ▼                                         ▼
 Oil Rate                             Injection Rate
 Well Test                            Injection Pressure
 Allocation                           Compressor Status
 Potential Oil                        Gas Lift Valve
      │                                         │
      └────────────────────┬────────────────────┘
                           ▼
                  Production Optimization
                           │
                           ▼
                Gas → Oil Conversion Efficiency
```

## The four production methods compared

| Method | Full name | Artificial lift? | Lift mechanism | Key KPIs |
| --- | --- | --- | --- | --- |
| **SF Oil Wells** | Self Flow Oil | No | Natural reservoir pressure | Oil Rate, Pressure, Potential Oil |
| **ESP Wells** | Electric Submersible Pump | Yes | Downhole electric pump | Motor Current, Pump Efficiency, Oil Rate |
| **SF Gas Wells** | Self Flow Gas | No | Natural gas flow | Gas Rate, Wellhead Pressure, Compressor |
| **GL Wells** | Gas Lift | Yes | Injected high-pressure gas | Oil Rate, Gas Injection Rate, Injection Pressure, Gas Lift Efficiency |

## Digital-oilfield product architecture

The four dashboards are four **Production Methods** under one data model:

```
Production Method
│
├── SF Oil
│     ├── Production KPI
│     └── Reservoir KPI
│
├── ESP
│     ├── Production KPI
│     ├── Pump KPI
│     └── Electrical KPI
│
├── SF Gas
│     ├── Gas Production KPI
│     ├── Pressure KPI
│     └── Compression KPI
│
└── GL
      ├── Oil Production KPI
      ├── Gas Injection KPI
      ├── Compressor KPI
      └── Gas Lift Efficiency KPI
```

Common platform design (Halliburton, SLB, Baker Hughes): **keep one page frame,
dynamically load KPIs/charts/logic by Production Method** — not a separate page per
well type. See [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md).

## Glossary

| Term | Meaning |
| --- | --- |
| GL | Gas Lift — lifting oil by injecting high-pressure gas |
| Gas Lift Valve | Downhole valve admitting injected gas into the tubing |
| Injection Rate | Gas injected per day (SCMD / MMSCFD) |
| Injection Pressure | Pressure of the injected gas (psi) |
| Gas Injection Efficiency | Oil gained per unit of gas injected |
| SCMD | Standard Cubic Metre per Day |
| Compressor | Equipment that compresses the lift/injection gas |
