# Bug Memory

Append-only log of tricky bugs and their resolutions, so the same bug isn't re-investigated from scratch.

> Source: `wpo-app/docs/implementation/IMPL-*.md` (frontend project).

## 2026-07
- **Blank export CSV**: `com-chart` export produced empty CSV when `columns` unset → fixed by deriving rows/cols from `dataset/series/xAxis`.
- **ECharts tooltip ghosting/重影** on donut/trend → fixed with `confine: true` + `transitionDuration: 0`.
- **Detail table drawer** default `p-drawer-content` padding + wrong height → fixed to `30vh` and cleared padding.
- **Small-screen map "collapsed with no scrollbar"** (<=1024) → added scroll fallback on map panel.
- **Map auto-zoom回跳**: repeated auto-fit on every map interaction → fit-once on initial load only.
- **Map data double-refresh** on point click → click shows popup only, no linkage-context write-back.
- **Map squeezed narrow** by residual `320px` side column → `__map-side` set `display:block; width:100%`.
- **414 URL too long** for large wellId batches → migrate `getMapInfo`/`getKpiTrend` GET→POST body.
- **MFE expose broken**: `webpack.config.js` pointed at non-existent `wso.module.ts` (WSO was standalone/routes-only) → added `WsoModule` wrapper.
- **PrimeNG v20 carousel class mismatch** → replaced `p-carousel` with custom indicator.

### Known open items / TODO
- `.wtv-overview-v2 { overflow: scroll }` may cause double scrollbars — confirm intended.
- `isMapCollapsed` semantics weakened to "manual collapse flag"; consider renaming `isMapHidden`.
- Legend text `Exeptions` typo → confirm fix to `Exceptions`.
- Red/green rule depends on V1 `sideNodes.action` config; consider a shared rule source.
