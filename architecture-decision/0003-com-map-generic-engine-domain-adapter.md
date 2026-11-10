# ADR-0003: com-map Generic Engine + Domain Adapter (data-driven map layering)

- Status: Accepted (implemented 2026-07-24)
- Date: 2026-07-24
- Deciders: WPO frontend team

## Context

The shared `com-map` component (`libs/shared`) is consumed by multiple business
areas (WSO overview, WTV overview). We want one map engine that any business can feed
without the engine knowing business specifics, and we want to add new *business layers*
(new icon semantics, new alert rules, eventually overlay layers) without editing the
shared library.

The **as-built** design already gets most of the way there (see
[frontend/components/wso-map-panel-architecture.md](../frontend/components/wso-map-panel-architecture.md)):

> `WsoMapPanelComponent` (domain adapter) → `ComMapComponent` (generic engine) →
> pure `builders/handlers/utils` → `webviz-*` GIS library.

The engine consumes only neutral contracts and imports **no** business types:

```
ComMapContext { source?, wellIds?, dateRange? }
ComMapInfoResponse = ComMapPlatformInfo[]   // platform → wellData[]
ComMapSelection { wellIds, level, platformName, anchor* }
```

But three things still leak business concerns into the shared engine and block true
open-for-extension:

1. `ComMapLegendIconKey` is a **closed union** of 4 keys — a new marker semantic forces
   a shared-library edit.
2. `isWellWithActions` (in `com-map-point.builder.ts`) **hard-codes** the
   validation/priority/calibration/kpi domains and their alert-value sets — WSO/WTV
   domain rules living in a generic engine.
3. Only `type: 'platform' | 'well'` exists — there is no `layer` abstraction for
   overlaying multiple business layers.

## Decision

Keep the **generic engine + domain adapter + data-driven contracts** architecture, and
evolve the three leak points so the engine stays business-agnostic:

1. **Registrable icon provider (replace the closed union).** Expose an icon registry so
   a business can register `{ key, svg }` (or a canvas provider) at bootstrap. The
   engine renders whatever `legendIconKey` the data carries; it does not enumerate keys.
2. **Domain-owned status → move alert logic to adapters.** Each business adapter
   computes the well's `legendIconKey` / color from its own status rules and passes it
   in explicitly (the builder already honors an explicit `legendIconKey`). Remove the
   hard-coded `ALERT_STATUS_BY_GROUP` domain evaluation from the shared builder, or keep
   it only as an opt-in default behind a flag.
3. **Introduce a `layer` abstraction (future).** Add a layer concept to the contract so
   multiple business layers (wells, pipelines, geology, equipment) can be toggled and
   overlaid, instead of a single well/platform primitive.

Adopting (1) and (2) is enough to reach "add a business layer without touching the
shared engine" for the common case; (3) is a larger, forward-looking change.

## Alternatives Considered
- **Keep hard-coded icon union + engine-side alert rules** — simplest, but every new
  business semantic requires a shared-library change and a redeploy of `libs/shared`;
  couples domains into the engine. Rejected for extensibility.
- **Each business forks its own map component** — removes coupling but duplicates the
  GIS wiring, selection/cursor handlers, and lifecycle guards. Rejected for
  maintenance cost.
- **Full plugin/layer framework now** — most flexible but over-engineered for current
  needs (only wells/platforms exist today). Deferred to (3) when a real overlay
  requirement appears.

## Consequences
- **Easier**: onboarding a new business (write an adapter that maps to
  `ComMapInfoResponse`); adding new marker semantics (register an icon + pass
  `legendIconKey`); keeping `libs/shared` free of business domain rules.
- **Harder / migration cost**: existing callers relying on the engine's built-in
  `isWellWithActions` default must move that computation into their adapter (WSO's
  `buildMapInfo` and WTV's `applyIconColor` are the touch points).
- **Contract stability**: `ComMapContext` / `ComMapInfoResponse` / `ComMapSelection`
  remain the stable seam; the index-signature (`[key: string]: unknown`) on well /
  platform info continues to carry business-specific fields for data-driven filtering.

## Implementation (2026-07-24)

All three points were implemented on the shared engine in a **backward-compatible**
way (built-in defaults preserved; existing WSO/WTV callers unchanged):

1. **Registrable icon provider** — `com-map.legend-icons.ts`: `ComMapLegendIconKey` is
   now an open type (`ComMapBuiltinLegendIconKey | (string & {})`); a `Map`-backed
   registry seeds the 4 built-ins and exposes `registerComMapLegendIcon(key, svg)` /
   `unregisterComMapLegendIcon` / `hasComMapLegendIcon`. `getComMapLegendSvg` now returns
   `string | undefined`; the icon-canvas util guards the undefined case. Exported via
   `components/index.ts`.
2. **Injectable icon/alert resolver** — new `ComMapIconResolver` type; `com-map` gains an
   `@Input() iconResolver`. Resolution order in `com-map-point.builder.ts`: explicit
   per-well `legendIconKey` → `iconResolver(well, context)` → built-in
   `isWellWithActions` default. Businesses can now own their alert rule without editing
   the engine (the built-in stays as opt-out default).
3. **Layer abstraction** — new `ComMapLayerConfig` type + `layerId` on
   `ComMapWellInfo`/`ComMapPointAttributes`; `com-map` gains an `@Input() layers`. The
   builder filters wells whose `layerId` is not in a visible layer (`visible !== false`);
   wells without a `layerId` are always shown, so existing single-layer usage is
   unaffected.

Touch points: `com-map.legend-icons.ts`, `com-map.types.ts`,
`builders/com-map-point.builder.ts`, `com-map.component.ts`,
`utils/com-map.icon-canvas.util.ts`, `components/index.ts`. No changes required in the
WSO or WTV adapters (verified type-clean).

How-to guide: [frontend/components/com-map-layer-extension-manual-zh.md](../frontend/components/com-map-layer-extension-manual-zh.md)
(adding a new business layer: layer toggle / custom icon / new business adapter).
