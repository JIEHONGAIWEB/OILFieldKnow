# frontend

Frontend-specific context: what exists, how it's structured, and the conventions in use.

## Project location

- Path: `C:\Users\h224847\code\EEE-WPO\wpo-new-2026.7.16\wpo-app`
- Package name: `dfs-wpo` (see `package.json`)
- Framework: Angular (see `angular.json`, `package.json`)

> 约定：所有代码修改只在上述前端文件夹（`wpo-app`）下进行。

## Architecture overview

- **Micro-frontend (MFE)** shell built with **Webpack Module Federation**
  (`@angular-architects/module-federation`, `ngx-build-plus`, custom
  `webpack.config.js`). MFE bootstrap lives in `src/app/mfe-init.ts`,
  `src/bootstrap.ts`, `src/main.ts`.
- The shell (`src/app`) is thin; almost all functionality lives under
  `libs/` as lazy-loaded feature libraries.
- Auth via **Keycloak** through the `@webframework/client-core` platform
  (`AuthGuard`, `src/keycloak.json`).

### Tech stack (from `package.json`)

| Concern | Library |
| --- | --- |
| Framework | Angular 20.x |
| State | NgRx (`@ngrx/store`, `effects`, `entity`, `router-store`) |
| UI components | PrimeNG 20 (`primeng`, `@primeng/themes`, `primeflex`, `primeicons`), Angular Material/CDK |
| Charts | ECharts 6 (`echarts`, `ngx-echarts`) |
| Maps | Leaflet + markercluster, `proj4`, `@turf/turf`, `@nextgengraphics/webviz-map` |
| 3D / viz | `@nextgengraphics/webviz-3d`, `three` |
| Platform | `@webframework/*` (client-core, layout, grid, toolbar, notification…), `@dfs/dfs-core` |
| i18n | `@ngx-translate/core` |
| Misc | `moment`, `angular-gridster2`, `quill`, `html2canvas`, `@daypilot/daypilot-lite-angular` |

### Feature libraries (`libs/`)

- `demo` — demo/sandbox routes (`/demo`, `/wpo-test`).
- `wpe` — Well Performance Engineering: well-test management, validation
  overview & analysis (route `/wpe`).
- `wso` — Well Surveillance Overview (route `/wso`).
- `well-surveillance` — well analysis (SRP, ESP), overview, notes, filters,
  NgRx store.
- `shared` — shared components, services, models, configs, styles, utils.
- `mfe-module`, `migration` — MFE plumbing / migration helpers.

See the per-topic READMEs in this folder ([pages](pages/README.md),
[components](components/README.md), [state](state/README.md),
[routing](routing/README.md), [charts](charts/README.md),
[ui-patterns](ui-patterns/README.md), [testing](testing/README.md)) for detail.

## Unit testing

- Baseline guide: [testing/README.md](testing/README.md)
- Focus on business logic, rule engines, mappers/transformers, and state branches.
- For rule-based features, require test cases for positive, boundary, and negative paths.
- Keep tests close to source files (`xxx.ts` + `xxx.spec.ts`) for maintainability.
- In the same change set, update implementation + unit test + related docs together.

## Change log

代码修改记录（仅限 `wpo-app` 前端文件夹）：

<!-- 追加格式：
## YYYY-MM-DD
- 简述改动内容（涉及文件/功能）
-->

