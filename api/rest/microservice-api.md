# MicroHttpService — Micro-service API router

> Source: `libs/shared/src/lib/services/micro-http.service.ts` + `.types.ts`

Newer feature libs (`wpe`, `wso`) do **not** use `ApiService`/PDM directly.
They call registered micro-services through the typed `MicroHttpService`, which
targets the WPO API router.

## URL pattern

```
api/router/<routerService>/<apiVersion>/<microService>/<endpoint>
```

- `routerService` — top-level router entry (e.g. `wpo`, `wellsurveillance`).
- `apiVersion` — `v1` | `v2` | `v3`.
- `microService` — downstream service (e.g. `wpeService`, `wpoService`, `opService`).
- `endpoint` — path segment after the micro-service prefix.

## Methods

`get`, `post`, `put`, `delete` — all typed generics:

```ts
microHttp.get<WsoProductionSummary>(
  'wellsurveillance', 'v1', 'wpoService',
  'wpo/wells/esp-production-summaries', { params });

microHttp.post<Result, Payload>(
  'wpo', 'v1', 'wpeService', 'wtv/wells/well-tests', { body });
```

Query params are URL-encoded via a `StrictHttpParameterCodec`. Types
(`RouterServiceName`, `MicroServiceName`, `ApiVersion`, `ApiResponse`,
`RequestOptions`, `MutationRequestOptions`) live in `micro-http.types.ts`.

## Endpoint inventory (from wpe / wso)

| Router | Version | Micro-service | Endpoint | Used by |
|--------|---------|---------------|----------|---------|
| wpo | v1 | wpeService | `wtv/wells/well-tests/review/history` | WpeService |
| wpo | v1 | wpeService | `wtv/wells/well-tests` (POST) | WellTestManagementService.add |
| wpo | v1 | wpeService | `wtm/wells/well-tests/{id}` (PUT) | update |
| wpo | v1 | wpeService | `wtm/wells/well-tests/{id}/well-test-periods/{pid}` (DELETE) | delete |
| wpo | v1 | wpeService | `wtv/wells/well-tests/{id}/diagnosis-{esp\|sf}` | validation analysis |
| wpo | v1 | wpeService | `/v1/wtv/wells/well-tests/status` (PUT) | approve/reject |
| wpo | v1 | wpoService | `/wpo/wells/{id}/optimizations/data-analyses` | well-trend cross-plots |
| wellsurveillance | v1 | wpoService | `wpo/wells/esp-production-summaries` | WSO KPI cards |
| wellsurveillance | v1 | wpoService | `wpo/wells/oil-rate-comparison` | WSO chart |
| wellsurveillance | v1 | wpoService | `wpo/well/reservoir-guideline-compliance` (POST) | WSO compliance |
| wellsurveillance | v1 | wpoService | `wpo/wells/esp/map` | WSO map |
| wellsurveillance | v1 | opService | `ws/operation-surveillance/wells/overview` | WSO losses (chart + table) |

> Full WSO Overview inventory (request params, response contracts, KPI card →
> API field mapping): [wso-v1-overview-api.md](wso-v1-overview-api.md).

## Relationship to PDM `ApiService`

- `ApiService` (`/dspdmservice/...`, BO queries) = generic PDM data platform,
  used by the older `well-surveillance` core.
- `MicroHttpService` (`api/router/...`) = purpose-built feature micro-services,
  used by newer `wpe` / `wso` libs. Prefer it for new feature endpoints.
