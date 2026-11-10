# components

Shared component documentation: props, variants, usage guidance.

Shared, reusable components live in `libs/shared/src/lib/components/`
(exported via `components/index.ts` and `shared.ts`).

## Architecture write-ups
- [wso-map-panel-architecture.md](wso-map-panel-architecture.md) — as-built WSO map
  (generic `com-map` engine + `WsoMapPanelComponent` domain adapter), data-driven
  analysis + extensibility gaps. See [ADR-0003](../../architecture-decision/0003-com-map-generic-engine-domain-adapter.md).
- [com-map-layer-extension-manual-zh.md](com-map-layer-extension-manual-zh.md) — 中文
  手册：如何在 `com-map` 上新增业务层（图层开关 / 自定义图标 / 接入新业务），配置化、
  不改共享引擎。

## Shared components (`libs/shared`)

| Component | Folder | Purpose |
| --- | --- | --- |
| `com-card` | `com-card/` | Standard dashboard/widget container |
| `com-chart` | `com-chart/` | ECharts wrapper (theme sync + data updates) |
| `com-map` | `com-map/` | Leaflet map wrapper |
| `com-map-filter-sidebar` | `com-map-filter-sidebar/` | Collapsible map filter sidebar shell: toggle button + panel chrome (title) + Reset/Apply footer; body via `<ng-content>`. Emits `(apply)`/`(reset)`; `overlayElements()` for fullscreen relocation. |
| `com-table` | `com-table/` | Wrapper around PrimeNG `p-table` (filter/sort/lazy) |
| `dfs-table` | `dfs-table/` | Alternate/platform table wrapper |
| `global-filter` | `global-filter/` | Centralized data-scoping filter (well/field/date) |
| `date-range-filter` | `date-range-filter/` | Date-range picker filter |

### Reuse notes — shared

- **`com-map-filter-sidebar`** — import `ComMapFilterSidebarComponent` from
  `libs/shared/src/public-api`. Wrap your own filter body:
  ```html
  <com-map-filter-sidebar title="Map Display Control"
    (apply)="onApply()" (reset)="onReset()" (openChange)="onOpenChange()">
    <my-filter-content></my-filter-content>
  </com-map-filter-sidebar>
  ```
  Inputs: `title`, `applyDisabled`. Outputs: `apply`, `reset`, `openChange`.
  Methods: `open()/close()/toggle()`, `overlayElements()` (host relocates the
  toggle + panel into a fullscreen host for map fullscreen). Apply/Reset emit
  then auto-close; the host reads the projected content's selection on apply.

## Feature-local reusable components

Not in `libs/shared` (feature-scoped), but reusable within their lib:

| Component | Path | Purpose |
| --- | --- | --- |
| `com-legend-popover` | `libs/wpe/.../well-test-validation-overview/shared/com-legend-popover/` | Info (i) trigger + PrimeNG popover showing a titled, grouped, color-coded status legend. Custom arrow (anchored `right:6px`), border/radius/shadow, dark-theme handled globally. Signal inputs `[title]`, `[groups]` (`{title, items:{label,color}[]}`), `[ariaLabel]`. |
| `wso-detail-table` | `libs/wso/.../components/detail-table/wso-detail-table/` | Config-driven business **shell** = bottom `p-drawer` + `com-card` (title/search/export/close) + platform `dfs-table` engine. Columns / dataKey / export / card config resolved from a per-layer registry (`configs/wso-detail-table.config.ts`). Inputs: `[rows]`, `[visible]`, `[layer]` (default `'productionLosses'`), optional `[config]` override; output `(visibleChange)`. Add a business layer by registering a config — no shell change. See [ui-patterns/wso-detail-table-architecture.md](../ui-patterns/wso-detail-table-architecture.md). |

## Conventions
- UI primitives come from **PrimeNG 20** (+ `primeflex`, `primeicons`) and
  Angular Material/CDK; platform widgets come from `@webframework/*`
  (grid, toolbar, notification, progress-spinner, color-picker).
- Prefer composing the `com-*` wrappers over using `p-*` primitives
  directly, so theming and behavior stay consistent.
- Feature-specific components stay inside their own lib
  (`libs/wso/.../components`, `libs/wpe/.../features`,
  `libs/well-surveillance/...`), not in `shared`.
