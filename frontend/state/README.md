# state

State management notes: stores, selectors, ownership boundaries.

Two complementary approaches are used:

## 1. NgRx (shared / cross-feature state)
- Packages: `@ngrx/store`, `@ngrx/effects`, `@ngrx/entity`,
  `@ngrx/router-store`.
- Well-surveillance store: `libs/well-surveillance/src/lib/ngrx/`
  with `actions/`, `effects/`, `reducers/`, `selector/`.
- Known feature slices: `activePage` (MFE context id/name/attributes, read by
  `MfeInit` to resolve backend routes) and `SDHFilter` (Surveillance Data Hub
  filters, `ngrx/reducers/SDHFilter.reducer.ts`).
- Effects handle async PDM / feature-service calls via `ApiService`.
- Used for global filters and shared surveillance state consumed across
  overview / analysis pages.

## 2. RxJS service state (local / feature state)
- Feature services expose `BehaviorSubject`/observables for local state,
  e.g. `libs/shared/src/lib/services/`:
  - `global-filter.service.ts` — global filter selection
  - `date-range.store.ts` — date-range selection
  - `micro-http.service.ts` (+ `micro-http.types.ts`) — HTTP for MFE
  - `dfs-util.service.ts`, `legacy-map-info-normalizer.service.ts`

## MFE initialization state
- `src/app/mfe-init.ts` resolves the active page/config, remote module
  loading, and asset/API path resolution for the micro-frontend shell.

## Ownership
- Cross-feature/global state → NgRx or shared services in `libs/shared`.
- Feature-only state → services scoped inside that feature lib.
