# routing

Routing structure, guards, and navigation conventions.

## Root router — `src/app/app-routing.module.ts`
Active routes (each lazy-loads a feature lib via `loadChildren`):

| Path | Module | Lib |
| --- | --- | --- |
| `/demo` | `DemoModule` | `libs/demo` |
| `/wpo-test` | `DemoModule` | `libs/demo` |
| `/wpe` | `WpeModule` | `libs/wpe` |
| `/wso` | `WsoModule` | `libs/wso` |

> Several routes are commented out (`map`, `start`, `secondary`, `iframe`,
> `request`, `url_data`, `shared-store`, remote `tdemo`) — inactive.

## Feature routes
- `libs/wso/src/lib/wso.routes.ts` — `''` → `WsoOverviewComponent`
  (uses `loadComponent`, standalone).
- `libs/wpe/src/lib/wpe.routes.ts` — `WpeComponent` shell with children:
  `well-test-management`, `well-test-validation-overview`,
  `well-test-validation-analysis`.

## Conventions
- **Lazy loading** everywhere: `loadChildren` for modules, `loadComponent`
  for standalone feature components.
- **Guards**: `AuthGuard` from `@webframework/client-core` (Keycloak) guards
  protected feature routes.
- **Module Federation**: remote modules can be loaded via `loadRemoteModule`
  (`@angular-architects/module-federation`).
