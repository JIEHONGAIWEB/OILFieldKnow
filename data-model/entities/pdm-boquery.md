# PDM BOQuery — Core Data Access Model

> 中文版：[pdm-boquery-zh.md](pdm-boquery-zh.md)
>
> Source: `src/app/model/pdm-data.model.ts`, `src/app/model/app.enums.ts`

All oilfield data in WPO is read/written through **PDM (Petroleum Data
Management)** using a generic **Business Object (BO) query**. There is no fixed
per-entity model class; instead a `BOQuery` describes *what* to fetch from *which*
business object.

## `BOQuery` (extends `BaseQuery implements IQuery`)

Key fields:

| Field | Type | Purpose |
|-------|------|---------|
| `boName` | `string` | The business object to query (e.g. `WELL_TEST`). |
| `selectList` | `string[]` | Attributes to return. |
| `criteriaFilters` | `CriteriaFilters[]` | WHERE-style filters. |
| `aggregateSelectList` | `AggregateSelectList[]` | Aggregations (MAX/MIN...). |
| `havingFilters` | `HavingFilters[]` | HAVING-style filters over aggregates. |
| `orderBy` | `OrderBy[]` | Sort (`boAttrName` + `ASC`/`DESC`). |
| `pagination` | `Pagination` | `recordsPerPage` + `pages[]`. |
| `simpleJoins` | `SimpleJoin[]` | Joins to related BOs. |
| `joinAlias` | `string` | Alias for joined BO. |
| `unitPolicy` | `string` | Unit conversion policy for numeric attributes. |
| `language`, `timezone` | `string` | Locale/tz (auto-injected by ApiService). |
| `readChildBO` | `BOQuery[]` | Nested child-BO queries. |
| `read*` flags | `boolean` | `readBack`, `readUnique`, `readMetadata`, `readRecordsCount`, `readAllRecords`, etc. |

## Supporting classes

- **`CriteriaFilters`** — `{ boAttrName, operator, values[] }`
- **`AggregateSelectList`** — `{ boAttrName, aggregateFunction, alias }`
- **`HavingFilters`** — `{ aggregateColumn, operator, values }`
- **`OrderBy`** — `{ boAttrName, order }`
- **`Pagination`** — `{ recordsPerPage, pages[] }`
- **`SaveBOQuery`** — write path: `{ data, dspdmUnits[], operationName, deleteCascade, ... }`

## Response contract

- Success is signalled by `status.statusCode === 1`.
- Records are nested under `data.<boName>.list`.
- Any other status code is treated as an error (promise rejected).

See `data-model/enums/pdm-query-enums.md` for operators and functions.
