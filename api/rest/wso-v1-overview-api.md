# WSO Overview — V1 Backend API Inventory

> Source: `wpo-app/libs/wso/src/lib/shared/services/wso-api.service.ts`,
> `libs/wso/src/lib/shared/models/wso-api.model.ts`,
> `libs/wso/src/lib/configs/wso-kpi-card.config.ts`.
> Router client: `libs/shared/src/lib/services/micro-http.service.ts`
> (see [microservice-api.md](microservice-api.md)).

The WSO Overview page (`WsoOverviewComponent`) is served by six V1 endpoints
exposed through `WsoApiService`, all routed via `MicroHttpService`.

> **Status:** `USE_WSO_API = false` in `wso-overview.component.ts` — the page
> currently renders `WsoMockDataService` data. The API wiring below is
> implemented (fetch + map) and falls back to mock on any failure. Flip the flag
> to `true` once the backend endpoints are live in the environment.

## URL pattern

```
api/router/wpo/<microService>/msp/v1/<endpoint>
```

- `routerService` = `wpo`
- `apiVersion` = `v1`
- `microService` = `wpoService` (5 endpoints) or `wpoCommonService` (losses)

> Routes are registered in `wpo-app/src/reg_app.json` (`wpo/wpoService` →
> `wpo-prodoptimization-service`, `wpo/wpoCommonService` → `wpo-common-service`).
> This replaces the legacy `wellsurveillance/wpoService` +
> `wellsurveillance/opService` routing.

## Endpoint inventory

| # | UI area | Method | Micro-service | Endpoint | Request | Response |
|---|---------|--------|---------------|----------|---------|----------|
| 1 | **Oil/Gas Production Summary** (KPI cards) | GET | wpoService | `wpo/wells/esp-production-summaries` | `WsoWellsRequest` | `WsoProductionSummary` |
| 2 | Oil Rate Comparison chart | GET | wpoService | `wpo/wells/oil-rate-comparison` | `WsoWellsRequest` | `WsoStatisticalResponse` |
| 3 | Prod Loss chart | GET | wpoCommonService | `ws/operation-surveillance/wells/overview?type=losses` | see below | `WsoLossesResponse` |
| 4 | Reservoir Guideline Compliance | POST | wpoService | `wpo/well/reservoir-guideline-compliance` | `WsoReservoirGuidelineRequest` | `WsoStatisticalResponse` |
| 5 | Production Losses table | GET | wpoCommonService | *(same as #3)* `ws/operation-surveillance/wells/overview?type=losses` | see below | `WsoLossesResponse.detailItems` |
| 6 | Map view | GET | wpoService | `wpo/wells/esp/map` | see below | `WsoMapPlatform[]` |

> #3 and #5 share a single request; the chart reads `statisticalItems.topLosers`,
> the table reads `detailItems.topLosers`.

## Request parameters

### `WsoWellsRequest` (endpoints #1, #2)
Built by `wellsParams()`:

| Param | Example | Notes |
|-------|---------|-------|
| `wellIds` | `[101,102,103]` | JSON-array string of numeric well ids |
| `date` | `07/24/2026` | `MM/DD/YYYY` (matches the v1/old backend format) |
| `timezone` | `GMT+08:00` | from `getTimeZone()` |

### Losses / Map extra params (endpoints #3/#5, #6)

| Param | Value |
|-------|-------|
| `entity_type` | `Well` |
| `entity_ids` | `[101,102,103]` |
| `type` | `losses` *(losses endpoint only)* |
| `date` / `timezone` | as above |

### `WsoReservoirGuidelineRequest` (endpoint #4, POST body)
Extends `WsoWellsRequest` with:

```ts
parameterCategories: Array<{
  parameterType: 'FBHP' | 'WC';
  volumeRanges: Array<{ key: string; start: number; end: number | null }>;
}>;
```

## KPI card → API field mapping (endpoint #1)

`WsoProductionSummary` is the single source for **all** KPI cards. Each card
template (`wso-kpi-card.config.ts`) names its `valueKey`; the card value is
`summary[valueKey]` (rounded to a whole number) and the change % comes from
``diffRatio[`${valueKey}DiffRatio`]`` — mirroring the v1 field-matching logic in
`libs/well-surveillance/src/lib/wpo/overview/kpi-view` (`handleData()`).

### Oil Production Summary (BOPD)

| Card title | Card id | `valueKey` (API field) |
|------------|---------|------------------------|
| Oil Rate (WSO) | `oil-rate-wso` | `oilRateWso` |
| Oil Rate (WT) | `oil-rate-wt` | `oilRateWt` |
| Oil Rate - Allocation | `oil-rate-allocation` | `oilRateAlloc` |
| Potential Oil Rate - SH-IN (NSO) | `potential-oil-rate-shin` | `oilRateNso` |
| Potential Oil Rate (WSO) | `potential-oil-rate-mob` | `oilRateNso` |

### Gas Production Summary (MSCFD)

| Card title | Card id | `valueKey` (API field) |
|------------|---------|------------------------|
| Gas Rate (WSO) | `gas-rate-wso` | `gasRateWso` |
| Gas Rate (WT) | `gas-rate-wt` | `gasRateWt` |
| Gas Rate - Allocation | `gas-rate-allocation` | `gasRateAlloc` |
| Potential Gas Rate - SH-IN | `potential-gas-rate-shin` | `gasRateNso` |
| Potential Gas Rate (WSO) | `potential-gas-rate-mob` | `gasRateNso` |

> Which summary/cards render depends on Production Method
> (`OILSF` / `OILESP` / `GASF` / `OILGL`) via the KPI-set registry. GL adds a
> second **Gas Injection** summary and ESP an **Equipment Health** summary; both
> are **mock-only** — `WsoProductionSummary` has no injection/equipment fields yet.

## Response contracts (summary)

- `WsoProductionSummary` — `oilRate{Wso,Nso,Wt,Alloc}`, `gasRate{Wso,Nso,Wt,Alloc}`, optional `diffRatio: Record<string, number>` keyed by `` `${valueKey}DiffRatio` `` (e.g. `oilRateWsoDiffRatio`).
- `WsoStatisticalResponse` — `statisticalItems[]` (`fieldName`, `statisticalType`/`key`, `totalValue`/`totalCount`).
- `WsoLossesResponse` — `statisticalItems[].topLosers.data[]` (chart) + `detailItems[].topLosers[]` (table rows: `wellName`, `field`, `productionLosses`, `wellTestLiquidRate`, `wellTestOilRate`, `downTime`).
- `WsoMapPlatform[]` — `platformName`, `longitude`, `latitude`, `wellData[]`.

## Related

- [microservice-api.md](microservice-api.md) — shared `MicroHttpService` router pattern.
- `feature-history/2026-07-24-wso-kpi-production-method.md` — KPI-by-production-method enhancement.
- ADR-0002 — data-driven chart layering.
