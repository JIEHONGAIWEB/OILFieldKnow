# feature-history

Chronological record of how major features evolved — what shipped, what changed, and why, so history isn't lost when people rotate off the project.

## Index

| Date | Doc | Summary |
|---|---|---|
| 2026-07-24 | [2026-07-24-wso-kpi-production-method.md](2026-07-24-wso-kpi-production-method.md) | WSO Overview KPI-by-Production-Method enhancements: static Record → `registerKpiSet()` registry; GL dual Oil-Production + Gas-Injection summaries; values keyed by `template.id` (oil/gas-aware `mapSummaryToCards`); wired `p-select` production-method selector + `p-selectButton` summary toggle. |
| 2026-07-23 | [2026-07-23-wtv-map-filter-color.md](2026-07-23-wtv-map-filter-color.md) | WTV Map Side Filter re-scoped from **filtering wells** to **driving icon color**: all wells always shown; selected status domains decide red/green. Sidebar redesigned to category-only checkboxes, centered Reset/Apply, theme-variable styling. Supersedes REQ-20260722b filter semantics + tree structure. |
| 2026-07-22 | [2026-07-22-wtv-map-ui.md](2026-07-22-wtv-map-ui.md) | WTV map UI: legend With/Without-Actions `p-popover` (design spec + custom arrow) and the "Map Display Control" well side filter (toggle button, tree, state persistence, layout). ⚠️ §2 tree + §4 filter semantics superseded by 2026-07-23. |

See also [requirements-index.md](requirements-index.md) for the REQ list.
