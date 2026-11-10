# WPO Application — Project Overview

> Source analysed: `wpo-new-2026.7.16/wpo-app` (extracted 2026-07-22).

## What it is

**WPO (Well Performance Optimization)** is an oilfield well-surveillance and
well-performance web application. It is delivered as an Angular **micro-frontend
remote** that plugs into a host shell via Module Federation, and reads/writes
oilfield data through the **PDM (Petroleum Data Management)** platform using a
generic **Business Object (BO) query** API.

## Tech stack

| Area | Technology |
|------|-----------|
| Framework | Angular 20 (v20.3.x), RxJS 7.8, Zone.js 0.15 |
| Micro-frontend | `@angular-architects/module-federation` (remote) |
| State | NgRx (`@ngrx/store`, `effects`, `entity`, `router-store`) |
| UI kit | PrimeNG 20, Angular Material 20, PrimeFlex, `@webframework/*` |
| Charts | ECharts 6 + `ngx-echarts` |
| Maps | Leaflet 1.9 + `leaflet.markercluster`, `@nextgengraphics/webviz-map` |
| 3D | `@nextgengraphics/webviz-3d` (Three.js 0.150) |
| i18n | `@ngx-translate/core` |
| Auth | Keycloak (`keycloak.json`), JWT (`jwt-decode`) |
| Data grid | `@webframework/grid`, `angular-gridster2` (dashboards) |
| Geospatial | `proj4`, `@turf/turf` |
| Export | `xlsx`, `html2canvas` |

## High-level structure

```
wpo-app/
├── src/app/                 # host/remote shell (bootstrap, routing, core services)
│   ├── model/               # PDM BOQuery models + app enums
│   └── services/            # ApiService (PDM), WAF rules service
├── libs/                    # feature modules (lazy-loaded, monorepo-style)
│   ├── well-surveillance/   # main surveillance feature
│   ├── wpe/                 # Well Performance Evaluation
│   ├── wso/                 # Well Surveillance Optimization
│   ├── demo/                # demo/test route
│   └── shared/              # shared code
├── configs/, CICD/          # build & pipeline config
└── docs/                    # existing in-repo documentation
```

## The three feature domains

- **WPE** — Well Performance Evaluation (`/wpe` → `WpeModule`)
- **WSO** — Well Surveillance Optimization (`/wso` → `WsoModule`)
- **Well Surveillance** — surveillance core (run-life analysis, survival analysis,
  well-test management, real-time monitoring)

See `domain-knowledge/` and `business-model/` for the detail.
