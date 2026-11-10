# Micro-Frontend Architecture (Module Federation)

> Source: `webpack.config.js`, `src/main.ts`, `src/bootstrap.ts`,
> `src/app/mfe-init.ts`, `src/app/app.module.ts`, `reg_app.json`

## Status

Accepted (existing architecture, documented 2026-07-22).

## Context

WPO is not a standalone SPA — it runs inside a host shell alongside other
oilfield micro-frontends. It must share the host's state (active page, auth) and
resolve its backend service routes at runtime.

## Decision

- Build WPO as a **Module Federation remote** using
  `@angular-architects/module-federation` (project name `sampleSolution`).
- Bootstrap indirectly: `main.ts` → dynamic `import('./bootstrap')` so the MF
  runtime can initialize shared scopes before Angular boots.
- Expose feature modules (`DemoModule`, `WellSurveillanceModule`, `WpeModule`,
  `WsoModule`) for host consumption.
- Resolve per-feature backend routing at runtime via `MfeInit`, which reads the
  host's `activePage` NgRx state to derive `mfeId` / `mfeName` and build API
  base URLs (combined with `MODULE_END_POINT` / `SERVICES_ROUTES`).

## Consequences

- Feature code lives in `libs/<feature>/` and is lazy-loaded — keep it there.
- Never hardcode a remote/host URL; wiring comes from MF config + `reg_app.json`.
- Shared singletons (NgRx store, `@webframework/client-core`) must be declared as
  MF shared deps to avoid duplicate instances.
