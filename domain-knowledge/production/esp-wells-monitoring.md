# ESP Wells — Monitoring & Equipment-Health KPIs

Subject-matter grounding for the **ESP Wells** production-monitoring dashboard.
It mirrors the general Oil-Rate dashboard, but the monitored objects are **ESP
Wells (Electric Submersible Pump wells)**, so it adds equipment-health KPIs.

> Read alongside [oil-rate-kpis.md](oil-rate-kpis.md) — the production KPIs (Oil
> Rate WSO / WT / Allocation, Potential, Shut-in) are identical; only the
> monitored well population differs.

## ESP (Electric Submersible Pump)

ESP is one of the most common **artificial-lift** methods. When reservoir pressure
is too low to lift oil to surface naturally, an electric submersible pump is
installed downhole (hundreds to thousands of metres) to lift the oil.

```
        Surface
   ───────────────
       Wellhead
        ↑ Oil
        │
   Production Tubing
        ↑
   ESP Pump (multistage centrifugal)
        │
   Electric Motor
        │
   Power Cable
        │
   Reservoir
```

How it works:
1. Reservoir fluid enters the pump intake.
2. The motor drives a multistage centrifugal pump.
3. The pump raises pressure stage by stage.
4. Oil is lifted to surface.

Because of this, ESP wells typically have: **high output**, **high power draw**,
**higher maintenance cost**, and **pump failures directly stop production**.

## Why the ESP dashboard keeps the same production KPIs

The lift method changed, but the focus is still **production capacity**. The KPI
names are unchanged; only the monitored object becomes the ESP well group.

| KPI | Meaning for an ESP well |
| --- | --- |
| Oil Rate (WSO) | Actual daily oil the ESP is lifting now |
| Oil Rate (WT) | Well-test measured actual rate |
| Oil Rate — Allocation | Rate the system allocates to this ESP well |
| Potential Oil Rate | Theoretical output if the ESP is tuned to optimum |
| Potential Oil Rate — SH-IN | Theoretical output lost while the ESP is shut in |

## Extra KPIs ESP wells watch (equipment health)

ESP engineers care about equipment status daily, so the dashboard adds:

### 1. Pump Intake Pressure (PIP)
Pressure at the pump intake (`Reservoir → Pump Intake → ESP`). If too low: the
pump may run dry, cause **gas lock**, and efficiency drops.

### 2. Motor Current
`120A → sudden 180A` may indicate the pump is stuck, wax/scale buildup, sand
plugging, or increased friction. An important alarm indicator.

### 3. Motor Temperature
`120°C → 140°C → protective shutdown`. Overheating can burn out the motor.

### 4. Pump Efficiency
Input power vs output flow. A drop can mean pump wear, gas interference, or rising
water content.

### 5. Power Consumption
ESPs are power-hungry (e.g. 800 bbl/day ≈ 500 kWh). Engineers compute **energy per
barrel** — a key economic indicator.

### 6. Runtime
`24 h scheduled → 18 h actually running` = 6 h down. The more downtime, the larger
the lost production.

### 7. ESP Failure Count
E.g. `12 ESP failures this year`, including motor burnout, cable damage, pump wear,
gas lock, scaling, sand sticking. A key equipment-reliability KPI.

## Potential Oil is more actionable for ESP

ESP output can be raised by tuning run parameters. Example:

```
Pump Frequency 45 Hz → 500 bbl/day
tune to        55 Hz → 650 bbl/day

Potential Oil 650 · Actual 500 · Opportunity 150 bbl/day
```

This is the concrete value of the dashboard's Potential Oil.

## Full ESP dashboard business logic

```
                 ESP Wells Dashboard
                    Equipment status
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Pump Status        Motor Status         Power Status
                          │
                          ▼
                    Oil Production
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Actual Rate         Allocation           Well Test
                          │
                          ▼
                  Production Analysis
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Current Oil        Potential Oil       Lost Production
```

## KPI layers on a digital-oilfield ESP dashboard

A dedicated ESP dashboard (Halliburton, SLB, etc.) usually adds an **Equipment
Health** layer, forming a closed loop of *equipment operation → production
capacity → economics*:

| Layer | KPIs |
| --- | --- |
| Production | Oil Rate, Water Rate, Gas Rate, Allocation, Potential Oil |
| Equipment | Pump Frequency, Motor Current, Voltage, Power, Temperature, Runtime |
| Wellbore | Pump Intake Pressure (PIP), Tubing Pressure, Casing Pressure, Fluid Level |
| Reliability | ESP Health Score, Failure Risk, Remaining Useful Life (RUL), MTBF, Failure Count |
| Economics | Power Cost, Cost per Barrel, Deferred Production, Production Loss |

## Glossary

| Term | Meaning |
| --- | --- |
| ESP | Electric Submersible Pump — downhole artificial-lift pump |
| Artificial Lift | Assisting production when reservoir pressure is insufficient |
| PIP | Pump Intake Pressure |
| Gas Lock | Gas at the pump intake stalling the pump |
| Runtime | Hours the ESP actually ran vs scheduled |
| RUL | Remaining Useful Life |
| MTBF | Mean Time Between Failures |
| Cost per Barrel | Energy/operating cost divided by barrels produced |
