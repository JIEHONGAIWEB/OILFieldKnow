# Coding Memory

Append-only log of coding conventions, gotchas, and decisions discovered while working in this codebase.

> Source: `wpo-app/docs/implementation/IMPL-*.md` (frontend project).

## Conventions & gotchas (2026-07)
- **Shared wrappers over PrimeNG primitives**: use `com-chart` / `com-map` / `com-table` / `com-card` (in `libs/shared`) instead of raw `p-*`, so theming and behavior stay consistent.
- **Single map entry**: `com-map` is the only map component; `com-map-bridge` was deleted. Legacy map params are bridged inside `com-map`.
- **`com-chart` export**: when `columns` is empty, it derives export rows/cols from `dataset/series/xAxis` to avoid blank CSV.
- **`com-chart` self-resize**: has its own ResizeObserver; splitter width changes auto-resize (do not hand-roll resize hacks — but a post-transition second resize is used where transitions delay layout).
- **PrimeNG v20**: DOM class names differ from older versions — `p-carousel` was dropped in favor of a custom `com-carousel-indicator`. Verify class-name assumptions against v20.
- **Theme detection**: read `data-theme` from `document.documentElement/body`; use `MutationObserver` to rebuild ECharts options on theme switch, and disconnect in `ngOnDestroy`. WSO implements this locally to avoid cross-feature deps.
- **Chart theme colors** (align across features, source `chart-panel-options.util`): axisLabel dark `#86A1CF` / light `#818F99`; axisLine & splitLine dark `#1E3A5F`; legend dark `#B8C7D6` / light `#4F5E6A`; tooltip dark text `#DBE6F1`.
- **ECharts tooltip ghosting**: set `confine: true` + `transitionDuration: 0`.
- **Chart config separation**: chart options live in `config.ts` / `*.config.ts` next to the component.
- **State placement**: cross-feature/global state → NgRx or `libs/shared` services; feature-only state → services scoped in that feature lib. Global filter registers pages in `global-filter.config.json`.
- **MFE remote expose**: standalone-route libs still need an NgModule wrapper (`RouterModule.forChild(ROUTES)`) for `webpack.config.js` `exposes` to resolve.
- **API large batches**: prefer POST with JSON body for endpoints taking many ids (avoid 414).
- **Interaction highlight**: inactive elements degrade via `opacity/saturate` only (still interactive); use `stopPropagation` on inner controls (slider/toolbar) to avoid triggering activate.
