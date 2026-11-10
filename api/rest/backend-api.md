# REST / Backend API

> Source: `src/app/services/api.service.ts`, `waf-ws-rules.service.ts`,
> `src/app/model/app.enums.ts`

WPO talks to two backend surfaces: the **PDM data service** (generic BO queries)
and **feature micro-services** (run-life, optimization, performance evaluation)
resolved per MFE context.

## PDM data service (`dspdmservice`)

`ApiService` is the single gateway (`providedIn: 'root'`).

- `postApi(serviceName, inputData, contentType, isLangTz=true)`
  - URL: `/dspdmservice/${serviceName}` (POST)
  - Auto-injects `language: 'en'` and `timezone: 'GMT'+moment().format('Z')`
    when `isLangTz` is true.
  - Runs `wafRulesService.byPassWAFRequestBody(inputData)` before sending.
- `getApi(serviceName)` → GET `/dspdmservice/${serviceName}`
- `getDatabyBoQuery(queryData: BOQuery, boName?)`
  - Calls `postApi('common', queryData, 'application/json')`.
  - Resolves `data.<boName>.list` when `boName` given, else `data.data`.
  - Rejects when `status.statusCode !== 1`.
- PDM business-api path also seen: `/api/router/dspdm-app/businessapi/`.

## Feature micro-service routes

Backend service names come from `SERVICES_ROUTES`:

| Feature | Service route |
|---------|---------------|
| Run Life Analysis | `wellsurv-app-runlifeanalysis` |
| Production Optimization | `wpoProductionOptimizationService` |
| Performance Evaluation | `wellsurv-perfevaluation` |

Module/path segments from `MODULE_END_POINT` (e.g. `rla`, `wpe/wells`,
`well-monitor`, `/well-tests`) combine with the MFE-resolved base to build the
final URL. `EndpointUrl` provides the leaf paths
(`/well-equipment-results`, `/survival-hazards`, `/kpis`,
`/wells/model-qualities`).

## WAF handling

`WafRulesWellSurvellianceService.byPassWAFRequestBody()` rewrites request bodies
so PDM queries pass the Web Application Firewall. The `wafByPassRules` endpoint
supplies the rules. **Do not bypass this service** when adding new PDM calls.
