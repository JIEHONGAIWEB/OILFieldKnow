# Well Model KPI — Calculation Rules by Lift Type

How the WPO workflow classifies **Well Model KPI** (Excellent / Good / Average /
Poor / N/A) for each well type. The KPI measures how closely the calculated
(model) well behavior matches measured behavior.

> Related: [well-model-management.md](well-model-management.md) (the dashboard that
> displays this KPI), [production/oil-rate-kpis.md](production/oil-rate-kpis.md).

## Shared: liquid-rate / gas-rate deviation bands

Used directly by natural-flow wells, and as the **fallback** for ESP and Gas Lift.

| Deviation (calculated vs. well-test rate) | Model KPI |
| --- | --- |
| ≤ 10% | Excellent |
| > 10% and ≤ 15% | Good |
| > 15% and ≤ 20% | Average |
| > 20% | Poor |

## By well type

### Natural Flow Oil Producer
Compare the **calculated liquid rate** with the **well-test liquid rate**; classify
with the deviation bands above.

### Natural Flow Gas Producer
Same deviation bands, using the **calculated gas rate** vs. the **well-test gas
rate**.

### ESP
When real-time **intake pressure (Pi)** and **discharge pressure (Pd)** are
available, compare calculated vs. measured Pi and Pd. Deviation is evaluated
relative to the variability of the real-time measurements and expressed in
**standard deviations (SD)** — lower SD = closer model/measurement agreement.

**The poorer of the Pd and Pi classifications determines the Model KPI.**

Each pressure is banded: ≤ 1 SD → level 1, 1–2 SD → level 2, 2–3 SD → level 3,
> 3 SD → level 4. Resulting matrix (Table 4, ESP model quality KPI ranges):

| Pd Dev \ Pi Dev | ≤ 1 SD | 1–2 SD | 2–3 SD | > 3 SD |
| --- | --- | --- | --- | --- |
| **≤ 1 SD** | Excellent | Good | Average | Poor |
| **1–2 SD** | Good | Good | Average | Poor |
| **2–3 SD** | Average | Average | Average | Poor |
| **> 3 SD** | Poor | Poor | Poor | Poor |

(Band edges: "1–2 SD" means > 1 and ≤ 2 SD, etc.)

**Fallbacks**
1. No valid Pi/Pd comparison, but a valid liquid-rate comparison exists → use the
   liquid-rate deviation bands.
2. No new real-time measurements → retain the previously calculated Well Model KPI.

### Gas Lift
When a valid **GLIP** measurement is available, compare the calculated GLIP with
the variability (SD) of real-time GLIP data over the **preceding 24-hour
assessment window**.

| GLIP deviation | Model KPI |
| --- | --- |
| ≤ 1 SD | Excellent |
| > 1 SD and ≤ 2 SD | Good |
| > 2 SD and ≤ 3 SD | Average |
| > 3 SD | Poor |

**Minimum-SD rule**: if the SD of the real-time GLIP data is **< 1% of the average
GLIP**, use a default SD equal to **5% of the average GLIP** instead (avoids
over-penalizing wells with near-flat signals).

**Fallback**: no valid GLIP comparison but a valid liquid-rate comparison → use
the liquid-rate deviation bands.

## Final fallback (all well types)

If a current KPI cannot be calculated, **retain the previous Well Model KPI** when
available; otherwise display **N/A**.

## Decision flow (ESP / Gas Lift)

```
Real-time Pi/Pd (ESP) or GLIP (Gas Lift) valid?
   ├─ yes → SD-based classification
   └─ no  → valid liquid-rate comparison?
              ├─ yes → liquid-rate deviation bands
              └─ no  → previous KPI exists? → keep it : N/A
```

## Note on the dashboard's generic table

[well-model-management.md](well-model-management.md) lists a generic error table
(< 5% / 5–10% / 10–20% / > 20%). The rules on this page are the lift-type-specific
workflow definition; where they differ, this page is the more detailed source.
