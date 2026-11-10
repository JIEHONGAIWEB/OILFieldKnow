# requirements

PRDs, user stories, acceptance criteria. What we're building and why.

> Source of truth: `wpo-app/docs/requirements/REQ-*.md` (frontend project).
> This page is a synchronized index/summary; open the source REQ files for
> full acceptance criteria.

## Naming

`REQ-<YYYYMMDD>-<slug>.md`

## Requirements index

| ID | Requirement | Status | Scope | Summary |
| --- | --- | --- | --- | --- |
| REQ-20260702 | Well Test Validation V2 (from V1) | Draft | `libs/wpe` | Keep V1 information architecture & key user paths; improve map/chart readability at high well density; standardized card model; tighter overview→detail→action linkage. Does not replace V1 core modules. |
| REQ-20260714 | API GET→POST for large wellId batches | Draft | `libs/wpe` | Migrate `wtv/wells/well-tests/map-info` and `wpe/wells/model-quality/trends` from GET (query string) to POST (JSON body) to carry 1000s of wellIds and avoid 414. Response schema unchanged. **V1 (`libs/well-surveillance`) untouched; backend must keep GET for backward compat.** |
| REQ-20260721 | WSO Overview — map / chart / KPI | Draft | `libs/wso` | Well Surveillance Overview page: right map (`com-map` + legend + popup + layers filter), left charts (two per page via `com-chart`, active/inactive highlight, detail table, slider-configurable), top KPI row (per production method, trend dialog, detail table). Mock-driven (`USE_WSO_API=false`). |
| REQ-20260722 | WTV map legend — With / Without Actions breakdown | Draft | `libs/wpe` | On the WTV overview map legend, each of the two markers (green = *Well Without Actions*, red = *Well With Actions*) gets an info (i) affordance that opens a panel explaining, per status domain, which status values fall under that bucket. Layout follows the design (image 1); bucket membership follows the logic (image 2 = `ALERT_STATUS_BY_GROUP`). Also fixes the legend typo *Exeptions* → wording changed to *Actions*. |
| REQ-20260722b | WTV map — well side filter (Map Display Control) | Superseded by REQ-20260723 | `libs/wpe` | Right-side “Map Display Control” panel on the WTV overview map, toggled by a layer-group button (vertically centered on the right edge). *(Original:* a bordered tree of the four status domains, each a checkbox with an expand/collapse chevron revealing status values as label-only children; semantics = the panel **filters** wells (actionable well shown only while ≥1 of its action domains is enabled).*)* **Superseded 2026-07-23** — see REQ-20260723. |
| REQ-20260723 | WTV map — side filter drives icon color (not filtering) | Draft | `libs/wpe`, `libs/shared` | Re-scope the Map Side Filter: **all** wells with coordinates are always shown; the selected status domains only decide **icon color**. A well is red if **any selected** domain is With-Action, green if **all selected** domains are Without-Action/empty; unselected domains are ignored. Default = all 4 domains selected (action wells red on first load). Sidebar redesigned to **category-only** checkboxes (no expand/sub-nodes), **centered** Reset/Apply, theme-variable styling (`--background-card` / `--color-text` / `--border-color-divider`). Impl: `map-panel.applyIconColor()` writes per-well `legendIconKey`; shared `com-map-point.builder` honors an explicit `legendIconKey` when present. |

## Key domain requirements captured

- **WTV V1 baseline (inherited by V2)**: left stats area = 2×2 status donuts
  (Validation / Calibration / KPI / Priority) + KPI Trend; right map with
  towers & wells, hover/click tooltip and drill-down; global filter
  (Field / WHP / Well / Date Range); links to Well Test Analysis / Model
  Calibration.
- **Production methods** driving KPI card config: `OILSF`, `OILESP`, `GASF`,
  `OILGL`.
- **Exception status**: wells rendered red (with exceptions) vs green
  (without exceptions) based on action-exception conditions.

## Map “With / Without Actions” classification (REQ-20260722)

A well is flagged **With Actions** (red marker) when **any** of its four status
domains holds an action-requiring value; otherwise it is **Without Actions**
(green marker). Source of truth in code: `ALERT_STATUS_BY_GROUP` in
`libs/wpe/.../well-test-validation-overview/components/map-panel/map-panel.component.ts`
(mirrored in `libs/shared/.../com-map/builders/com-map-point.builder.ts`).

| Status domain | Legend title | With Actions (red) | Without Actions (green) |
| --- | --- | --- | --- |
| validation | Well Test Validation Status | Rejected, Pending User Action | Approved, Awaiting Processing |
| calibration | Model Calibration Status | Failed Auto Calibration, Pending User Action | Approved, Rejected, Awaiting Processing |
| kpi | Well Model KPI | Average, Poor, NA | Excellent, Good |
| priority | Well Test Priority | High | Low, Medium |

Notes:
- **Selection-scoped coloring (REQ-20260723)**: since 2026-07-23 the Map Side Filter
  no longer removes wells — all wells stay on the map and the marker color is computed
  over **only the currently-selected domains** (red if any selected domain is With-Actions,
  else green). The table below still defines each domain's With/Without-Actions membership;
  the sidebar just chooses which domains participate. Default = all 4 selected.
- **Logic (image 2) governs bucket membership**, which resolves the design/logic
  discrepancy: the mockup (image 1) omitted validation from the *With Actions*
  panel and Calibration *Rejected* was explicitly crossed out (→ counts as
  *Without Actions*). Code follows image 2.
- `kpiStatus` null/empty from backend is treated as **NA** (→ With Actions).
- Status priority alias: backend `Pending` under priority maps to `Medium`.
- Swatch colors in the panels come from `WTV_STATUS_PALETTE` (per-status), not the
  alert-red marker color.

## Template

```markdown
# [功能名称]

**日期：** YYYY-MM-DD
**状态：** Draft | Review | Approved | Deprecated
**负责人：**

## 背景

## 目标

## 用户故事
- As a ... I want to ... so that ...

## 验收标准
- [ ] ...

## 超出范围
-
```
