# Business Memory

Append-only log of business/domain facts learned over time.

> Source: `wpo-app/docs` (frontend project). Domain: oilfield well surveillance & performance.

## Domain facts
- App is a **Well Performance / Well Surveillance** suite (oilfield production monitoring).
- **WSO** = Well Surveillance Overview (route `/wso`): map + charts + KPI row + detail drawer for a fleet of wells.
- **WPE** = Well Performance Engineering (route `/wpe`): includes **Well Test Management** and **Well Test Validation (WTV)** overview & analysis.
- **WTV** (Well Test Validation) tracks well-test status across four dimensions: **validation, calibration, KPI, priority** (shown as four donuts).
- **Production methods** drive KPI card config: `OILSF` (oil, single/self flow?), `OILESP` (ESP), `GASF` (gas), `OILGL` (gas lift). Well types across app: ESP, SRP (sucker rod pump), GL (gas lift), SF oil.
- **Well analysis** covers **SRP** (sucker rod pump — dynacard, well-trend charts) and **ESP** wells.
- Map points represent **wells**; a well is flagged **with exceptions** (red / warning icon) when it hits an action-exception condition, else **without exceptions** (green). `exceptions > 0` → warning status.
- Wells are grouped by **field** and **platform**.
- Data can span thousands of wells per request (drove GET→POST API change).
