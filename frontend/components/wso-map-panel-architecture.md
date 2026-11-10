# WSO Map Panel Architecture (current implementation)

Analysis of the map components actually shipped in `libs/wso` and their shared
`com-map` engine. Documents the *as-built* pattern, whether it is data-driven, and
how extensible it is when adding new business layers. Complements
[ADR-0003 (com-map generic engine + domain adapter)](../../architecture-decision/0003-com-map-generic-engine-domain-adapter.md),
which records the *target* extensibility direction.

- Status: Descriptive (as-built as of 2026-07-24)
- Scope: `libs/wso/src/lib/components/map/**` + `libs/shared/src/lib/components/com-map/**`

## Source map (`wpo-app`)

| Concern | Source path |
| --- | --- |
| Domain container (smart-ish) | `libs/wso/src/lib/components/map/wso-map-panel/wso-map-panel.component.ts` |
| Layer/filter UI (dumb) | `libs/wso/src/lib/components/map/map-display-control/map-display-control.component.ts` |
| Generic map engine | `libs/shared/src/lib/components/com-map/com-map.component.ts` |
| Engine contracts (types) | `libs/shared/src/lib/components/com-map/com-map.types.ts` |
| Render point builder | `libs/shared/src/lib/components/com-map/builders/com-map-point.builder.ts` |
| Icon/legend registry | `libs/shared/src/lib/components/com-map/com-map.legend-icons.ts` |
| Icon attribute mapping | `libs/shared/src/lib/components/com-map/utils/com-map-icon-attributes.util.ts` |
| Data-driven filtering | `libs/shared/src/lib/components/com-map/utils/com-map-filter.util.ts` |
| Selection / cursor / interaction | `libs/shared/src/lib/components/com-map/handlers/com-map-*.handler.ts` |
| Render / lifecycle utils | `libs/shared/src/lib/components/com-map/utils/com-map-render.util.ts`, `com-map-lifecycle.util.ts` |

## Pattern

**Generic map engine + domain adapter + stateless functional pipeline** — a
data-driven Adapter architecture. Three concerns:

```
WsoMapPanelComponent   (Domain adapter: WsoMapWellModel[] → ComMapInfoResponse; popup / legend / sidebar)
        │  [context] / [mapInfo]         ▲ (selectionChange)
        ▼                                │
ComMapComponent (com-map)   (Generic engine: knows only the 3 contracts, zero WSO types)
        │
        ▼
builders / handlers / utils   (Pure, stateless functions: build points, map icons, filter, resolve selection)
        │
        ▼
@nextgengraphics/webviz-*     (GIS rendering library)
```

| Layer | Responsibility |
| --- | --- |
| Domain adapter (`WsoMapPanelComponent`) | Maps WSO business data to the generic `ComMapInfoResponse` contract; owns popup, legend, layer sidebar |
| Generic engine (`ComMapComponent`) | Business-agnostic; consumes only `context` / `mapInfo` / `showWellLabels`, emits `selectionChange` |
| Functional pipeline (`builders/`, `handlers/`, `utils/`) | Stateless: render points, icon mapping, filtering, selection/cursor resolution |
| GIS library | `webviz-*` viewer / graphic factory does the actual drawing |

**Key signal of the pattern:** `ComMapComponent` imports **no WSO types** — it depends
only on the neutral contracts in `com-map.types.ts` (`ComMapContext` /
`ComMapInfoResponse` / `ComMapSelection`). `context.source` (`'wso'`) is the reserved
hook to distinguish the calling business.

## Is it data-driven? — Yes

Evidence in code:

1. **Declarative Signal derivation.** In `WsoMapPanelComponent` the view is a function
   of data:
   ```ts
   readonly mapContext = computed(() => ({ source: 'wso', wellIds: this.wellsSig().map(w => w.id) }));
   readonly mapInfo    = computed(() => this.buildMapInfo(this.wellsSig()));
   ```
   No imperative `map.addMarker()` — when `wells` changes, `mapInfo` recomputes and
   `com-map` re-renders via `ngOnChanges`.
2. **Rendering is decided by data structure.** `buildComMapRenderPoints` walks the
   platform/well structure in `mapInfo`; the icon key is derived from status fields
   (`legendIconKey` if explicit, else computed from `wtvStatus` / `priorityStatus` /
   `kpiStatus` / `modelCalibrationStatus`).
3. **Filtering is data matching.** `com-map-filter.util.ts` `matchNode` reads
   `well[node.field]` dynamically — filter criteria are configuration, not hard-coded
   `if/else`.

## Extensibility for new business layers

### Supported out of the box
- **Onboard a new business** — write another adapter container like
  `WsoMapPanelComponent` that maps its domain data to `ComMapInfoResponse`; reuse the
  same `com-map` engine. `context.source` differentiates the caller.
- **Attach arbitrary fields** — `ComMapWellInfo` / `ComMapPlatformInfo` use a
  `[key: string]: unknown` index signature, so a business can hang any field on a well
  and the filter reads it via `field`. Designed for extension.
- **Add a filter dimension** — data-driven; no engine change needed, just carry the
  field on the well + configure the sidebar node's `field`.
- **Pre-resolved icon color** — the builder honors an explicit per-well
  `legendIconKey`, so a business (e.g. WTV's Map Side Filter) can drive marker color
  itself without touching the engine.

### Coupling points that block "add a business layer without touching the shared engine"
1. **Icon registry is a closed union.** `ComMapLegendIconKey` in `com-map.legend-icons.ts`
   is 4 fixed keys (well/tower × with/without exceptions). A new layer needing a new
   icon / semantic color **must edit shared-library source**, not inject via config.
   *Suggested*: replace the closed union with a registrable icon provider.
2. **Alert rule hard-coded in the engine.** `isWellWithActions` in
   `com-map-point.builder.ts` hard-codes the `validation` / `priority` / `calibration`
   / `kpi` domains and their alert-value sets. These are WSO/WTV domain concepts living
   inside a supposedly generic engine. *Suggested*: move the domain status rule out to
   each business adapter (compute `legendIconKey` / color upstream) so the engine only
   renders.
3. **Only a single `well` primitive.** `type` is `'platform' | 'well'` — there is no
   `layer` abstraction. True multi-business-layer overlay (e.g. pipelines + geology +
   equipment stacked) is not structurally supported yet; introducing a `layer`
   abstraction is required.

## Conclusion

- **Pattern**: generic map engine (presentation) + domain adapter container + stateless
  functional render pipeline = a **data-driven Adapter architecture**.
- **Data-driven**: yes — the view is fully derived from `mapInfo`; render/filter/icon
  are all data-inferred.
- **Extensibility**: highly extensible for *onboarding a new data source* (copy an
  adapter panel); **semi-open** for *new layer types / new icon semantics / new alert
  rules* — those currently require editing the shared library.

## Related
- [ADR-0003: com-map Generic Engine + Domain Adapter](../../architecture-decision/0003-com-map-generic-engine-domain-adapter.md) — target extensibility (registry icons + domain-owned status + layer abstraction).
- [com-map-layer-extension-manual-zh.md](com-map-layer-extension-manual-zh.md) — 中文 how-to：新增业务层（图层开关 / 自定义图标 / 接入新业务）。
- [frontend/charts/wso-chart-panel-architecture.md](../charts/wso-chart-panel-architecture.md) — sibling as-built analysis for the chart side (same container/data-driven philosophy).
- [feature-history/2026-07-23-wtv-map-filter-color.md](../../feature-history/2026-07-23-wtv-map-filter-color.md) — the `legendIconKey`-driven side filter that exercises the explicit-icon extension hook.
