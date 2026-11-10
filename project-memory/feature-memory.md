# Feature Memory

Append-only log of feature decisions and their current status.

> Source: `wpo-app/docs/implementation/IMPL-*.md` (frontend project).

## 2026-07-23 — Chart↔map/table linkage is now a project-wide convention
- The highlight + dimming linkage originally built for donut slices is promoted to
  a **standing convention for every chart** (bar / line / scatter / KPI card / etc.):
  selecting a data element highlights it + its map points/table rows and dims the
  rest (still interactive). Bidirectional, clears on deselect.
- New chart types must wire into this shared mechanism, not a per-chart one.
  See `design-system/interaction/README.md` → "Chart ↔ map/table linkage".

## 2026-07-23 — WTV map side filter re-scoped to icon color (REQ-20260723)
- Map Side Filter no longer **filters** wells; it drives **icon color**. All wells with
  coordinates stay on the map; selected status domains decide red/green.
  - Red if **any selected** domain is With-Actions; green if **all selected** are
    Without-Actions/empty; unselected domains ignored. Default = all 4 selected
    (action wells red on first load — the “all green on first load” wording was dropped).
- `map-panel.component.ts`: `applyStatusFilter()` (removed wells) → **`applyIconColor()`**
  writes per-well `legendIconKey` via `resolveWellIconKey(well, selected)`; reuses
  `wellActionDomains()`; dropped `isWellVisible()`.
- shared `com-map/builders/com-map-point.builder.ts`: `createWellPoint()` now honors an
  explicit per-well `legendIconKey` (`resolveWellLegendIconKey`) and only falls back to the
  built-in all-domain `isWellWithActions()` when none is supplied — selection knowledge
  stays in the WTV layer.
- Sidebar redesign: `map-filter-panel` reduced to **category-only** checkboxes (removed
  chevron/expand, status leaf nodes, `expandedDomains`/`expandedChange`/`initialExpandedDomains`,
  `STATUS_SEMANTIC_CONFIG` usage); `map-panel` dropped the expand wiring.
- `com-map-filter-sidebar` actions `space-between` → **centered** group (`gap: 12px`);
  colors switched to theme vars (`--background-card` / `--color-text` / `--border-color-divider`),
  removed redundant dark-theme color overrides.
- **Supersedes** REQ-20260722b filter semantics + collapsible-tree structure.

- New standalone component `wtv-map-filter-panel`
  (`libs/wpe/.../well-test-validation-overview/components/map-filter-panel`).
- Content mirrors V1 `wfc-gis-side`: `p-tree` of 4 status domains
  (Validation / Priority / Model Calibration / KPI) with per-status checkboxes,
  category select-all, Reset/Apply. Style/shell mirrors WIM `map-host`
  (right panel + layer-group toggle button).
- Wired into `map-panel`: toggle button + `map-filter` panel; `applyFilter`
  event drives `statusFilter` signal; `mapInfo` computed filters the payload
  (faceted AND across domains, OR within a domain; full-domain selection =
  no restriction; kpi null → NA).
- Config added: `WTV_DOMAIN_LABELS`, `WTV_DOMAIN_WELL_FIELD`,
  `WTV_FILTER_DOMAIN_ORDER` in `status-semantic.config.ts`.
- Refinements (review feedback): filter toggle button vertically centered on the
  right edge and hidden while the panel is open; legend With/Without-Actions
  popup switched to PrimeNG `p-popover`. Filter toggle + panel are relocated into
  the fullscreen overlay host (like legend/well popup) so they work in fullscreen.
- Redesign to **Map Display Control** (per reference): bordered tree, each of the
  4 domains is a top-level `p-checkbox` + expand/collapse chevron revealing its
  status values as label-only children (V1 gis-side structure); header
  “Map Display Control” with layer-group icon. Filter is now **category-level**:
  emits the enabled domains; map shows a well unless it is actionable only in
  disabled domains (non-actionable/green wells always shown).

## 2026-07-22 — WTV map legend: With / Without Actions breakdown (REQ-20260722)
- Map legend labels renamed `Exeptions` → **Actions** (`Well Without Actions` /
  `Well With Actions`); each row gets an info (i) toggle.
- Info opens a per-domain panel listing which status values are in that bucket,
  driven by `ALERT_STATUS_BY_GROUP` (logic = image 2) + `STATUS_SEMANTIC_CONFIG`
  + `WTV_STATUS_PALETTE`; design/layout = image 1.
- With-Actions sets: validation {Rejected, Pending User Action}, calibration
  {Failed Auto Calibration, Pending User Action}, kpi {Average, Poor, NA},
  priority {High}. A well is With-Actions if ANY domain matches.
- Resolved design/logic mismatch in favour of logic: validation IS part of
  With-Actions; calibration Rejected is NOT (crossed out in image 2).
- Files: `map-panel.component.{ts,html,scss}` in
  `libs/wpe/.../well-test-validation-overview/components/map-panel`.

## 2026-07 — Well Test Validation (WTV) V2 — Overview
- Status: **Preview / 可运行预览版** (not yet a full V1 production replacement).
- Four status donuts (validation / calibration / kpi / priority) render from real API; empty-wells requests are short-circuited.
- KPI Trend chart with `YTD/1Y/5Y/10Y/MAX` range switching (top preset buttons later removed; range moved into `com-card` header / local date-range filter).
- Chart toolbars standardized to `detail → expand → menu` with `Save Image / Export Excel / Refresh Data`.
- Donut slice ↔ map/table linkage: highlight + dimming interaction.
- Detail table: `dfs-table` integration, styling + search, response reuse/cache.
- Map panel: well-only points (towers removed); red/green by action-exception hit; real side-filter; fit-once on load; click shows popup only (no linkage write-back); dual-tab popup (`ACTION SUMMARY / INFORMATION`).
- Map collapse/splitter: manual collapse→chart full width, overlay button to restore; auto-collapse-on-min-width branch removed to reduce state complexity.
- Folder consolidation + route update for WTV features.

## 2026-07 — Well Trends chart
- Toolbox actions (save image / export excel / refresh) standardized; reusable chart process extracted.

## 2026-07-20/21 — Well Surveillance Overview (WSO), route `/wso`
- Status: **Implemented (mock-driven)**, `USE_WSO_API=false`; API wired but falls back to `WsoMockDataService` on failure.
- Layout: `p-splitter` chart 60% / map 40%; top global-filter + Date Range (default YTD); top KPI row; bottom detail drawer.
- KPI cards configurable per production method (`OILSF/OILESP/GASF/OILGL`); trend icon → `p-dialog` trend, table icon → detail drawer.
- Chart panel renders single `com-chart` per page, two charts per page, active/inactive highlight, `configurable` charts show `p-slider`.
- Page switching via custom `com-carousel-indicator` (dropped `p-carousel` due to PrimeNG v20 DOM class differences); component lives in WSO's own `shared/`.
- Map panel uses `ComMapComponent`; exceptions>0 → with-exceptions icon; Layers button → right `p-drawer` map filter.
- Dark theme: chart colors aligned with WTV `chart-panel-options.util`; `MutationObserver` on `data-theme` rebuilds options.
- WSO exposed as Module Federation remote via new `WsoModule` (`RouterModule.forChild(WSO_ROUTES)`).

## 2026-07-14 — API GET→POST migration
- `getMapInfo()` and `getKpiTrend()` migrated GET→POST to carry thousands of wellIds in body (avoids 414 URL-length errors); response schema unchanged.
