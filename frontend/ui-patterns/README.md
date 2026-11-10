# ui-patterns

Recurring UI/interaction patterns (forms, tables, modals, empty/error
states) so new work stays consistent.

## Reference

- [config-driven-ui-patterns.md](config-driven-ui-patterns.md) — catalog of
  config-driven / low-code UI design patterns (Config-Driven, Strategy,
  Factory+Registry, Renderer, Slots/Composition, Metadata, Decorator, Observer,
  Abstract Factory, Headless) and when to use each.
- [wso-kpi-by-production-method.md](wso-kpi-by-production-method.md) — case study:
  how `libs/wso` loads KPI cards per Production Method from a config map (files,
  data flow, ADR-0002 mapping, known gaps).
- [wso-kpi-extension-manual-zh.md](wso-kpi-extension-manual-zh.md) — 中文使用手册：
  扩展 WSO KPI（加业务层 / 加井型）的分步复用指南与检查清单。
- [wso-detail-table-architecture.md](wso-detail-table-architecture.md) — 案例分析：
  `wso-detail-table` 的「壳组件 + 数据驱动表格引擎（`dfs-table`）」模式、
  分层数据驱动判定，以及新增 business layer 的可扩展性（参数化 + 配置注册表）。
- [wso-detail-table-extension-manual-zh.md](wso-detail-table-extension-manual-zh.md) — 中文使用手册：
  给 WSO 明细表新增一个 business layer 的分步指南（加键 + 列 + 注册 + 挂载）、
  `[config]` 动态覆盖用法、检查清单与常见坑。
- [wso-detail-table-exception-rulebook.md](wso-detail-table-exception-rulebook.md) —
  WSO 明细表异常高亮规则手册：规则类型语义、阈值与边界行为、完整规则目录、治理流程与评审清单。

## Theming
- App theme: `src/styles.scss` + `src/wellsurveillance-theme.scss`,
  driven by CSS variables for seamless light/dark switching.
- Built on PrimeNG themes (`@primeng/themes`) + `@webframework/client-theme`.
- Shared style assets: `libs/shared/src/lib/styles/`.

## Tables
- Standardize on the shared `com-table` (wraps PrimeNG `p-table`) with
  built-in filtering/sorting and lazy/virtual scrolling for large datasets.
- Use `dfs-table` where the platform grid variant is required.
- **Config-driven detail table**: `dfs-table` renders purely from
  `DfsTableColumn[]` metadata + `data`; feature shells (e.g. `wso-detail-table`)
  compose drawer + `com-card` + `dfs-table` and forward search/export/close.
  To reuse across business layers, parameterize columns/model/config via inputs
  and drive from a per-layer registry — see
  [wso-detail-table-architecture.md](wso-detail-table-architecture.md).

## Filters
- Global data scoping via `global-filter` + `date-range-filter`
  (shared components) backed by `global-filter.service` / `date-range.store`.

## Layout / widgets
- Dashboard widgets use `com-card` containers; grid layouts use
  `angular-gridster2`.
- Toolbars, notifications, spinners come from `@webframework/*`.

## Forms
- PrimeNG + Angular reactive forms with standardized group spacing and
  required-field styling.

## Config-driven KPIs by Production Method

One page template renders different KPI cards per **Production Method** (SF Oil /
ESP / SF Gas / GL) via a config map instead of separate pages. Implemented in
`libs/wso`:

- **Config = source of truth**: `libs/wso/src/lib/configs/wso-kpi-card.config.ts`
  — `WsoKpiCardTemplate` holds presentation metadata only (`id/title/unit/icons`,
  **no values**); `WSO_KPI_CARD_CONFIG: Record<WsoProductionMethodKey, Template[]>`
  maps method → template set; `getWsoKpiCardTemplates(method)` resolves a config
  key or a filter-bar label.
- **Reactive wiring**: `WsoOverviewComponent.productionMethod` is a `signal`; a
  `constructor` `effect()` re-derives cards on change → `getKpiCards(method)`
  fills values onto the templates → `kpiCards` computed →
  `KpiCardRowComponent` (dumb `@Input cards`).
- **Reuse rule**: add a new well type by editing the config map + label map, not
  by adding a page. Keep KPI values separate from KPI metadata.
- Design rationale, layer mapping, and known gaps (GL reusing the GAS set, ESP
  missing equipment KPIs, positional value mapping):
  see [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)
  and the production domain docs
  ([oil-rate-kpis](../../domain-knowledge/production/oil-rate-kpis.md),
  [esp](../../domain-knowledge/production/esp-wells-monitoring.md),
  [sf-gas](../../domain-knowledge/production/sf-gas-wells-monitoring.md),
  [gl](../../domain-knowledge/production/gl-wells-monitoring.md)).

## Conventions
- Reuse `com-*` wrappers instead of raw PrimeNG primitives to keep theming
  and behavior consistent across features.
