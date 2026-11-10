# Project Timeline

Chronological log of significant project events.

> Source: `wpo-app/docs/implementation/IMPL-*.md` (frontend project).

| Date | Event |
|---|---|
| 2026-07-01 | Well Trends chart toolbox actions (save/export/refresh) standardized |
| 2026-07-02 | WTV Overview: four-donut real-data logic + KPI Trend; reusable well-trends process |
| 2026-07-03 | `com-chart` + `com-map` bridge; deleted `com-map-bridge`; WTV V2 gap checklist |
| 2026-07-07 | WTV V2 map collapse/splitter, chart toolbar & theme tuning; summary report |
| 2026-07-08 | WTV folder consolidation + route update; KPI Trend export/refresh/title fixes |
| 2026-07-10 | WTV `dfs-table` integration; KPI trend theme; map fullscreen popup/zoom |
| 2026-07-13 | WTV overview chart card action fixes; detail-table styling + search |
| 2026-07-14 | API GET→POST plan for large wellId batches (avoid 414) |
| 2026-07-15 | WSO page technical delivery plan; WTV V2 test cases |
| 2026-07-16 | WTV detail-table response cache; donut slice linkage highlight/dimming; KPI trend local date-range filter |
| 2026-07-20 | `com-map` null KPI status → N/A exception marker; WSO exposed as MF remote; WSO V1 chart API inventory |
| 2026-07-21 | WSO Overview map/chart/KPI implementation (mock-driven); shared splitter SCSS mixin |
| 2026-07-22 | Analysed `wpo-app`; extracted architecture/data-model/API/frontend/domain docs; project-memory populated from `wpo-app/docs/implementation` |
| 2026-07-22 | WTV map UI: legend With/Without-Actions `p-popover` (12px/600 · 400, 16×8 swatch, info.svg, custom arrow) + "Map Display Control" well side filter (WIM-style toggle, collapsible tree, Apply/Reset auto-close, state persistence, adaptive height). See feature-history/2026-07-22-wtv-map-ui.md |
| 2026-07-23 | WTV Map Side Filter re-scoped from filtering wells to driving icon color (all wells always shown; selected domains decide red/green; default all-4-selected). Sidebar redesigned to category-only checkboxes, centered Reset/Apply, theme-variable styling. Supersedes REQ-20260722b. See feature-history/2026-07-23-wtv-map-filter-color.md |
| 2026-07-24 | WSO Overview V1 backend API inventory documented (6 endpoints, request params, response contracts, KPI card → `WsoProductionSummary` field mapping). See api/rest/wso-v1-overview-api.md |
