# PDM BOQuery — 核心数据访问模型

> 英文原文：[pdm-boquery.md](pdm-boquery.md)  
> 来源：`src/app/model/pdm-data.model.ts`、`src/app/model/app.enums.ts`

WPO 中所有油田数据都通过 **PDM（Petroleum Data Management，石油数据管理）**
进行读写，访问方式是通用的 **业务对象查询（Business Object Query, BOQuery）**。
系统不是“每个实体一个固定模型类”，而是通过 `BOQuery` 描述“从哪个业务对象获取什么数据”。

## `BOQuery`（`extends BaseQuery implements IQuery`）

核心字段：

| 字段 | 类型 | 作用 |
|------|------|------|
| `boName` | `string` | 要查询的业务对象（如 `WELL_TEST`）。 |
| `selectList` | `string[]` | 要返回的属性列表。 |
| `criteriaFilters` | `CriteriaFilters[]` | 类似 SQL `WHERE` 的过滤条件。 |
| `aggregateSelectList` | `AggregateSelectList[]` | 聚合计算（MAX/MIN...）。 |
| `havingFilters` | `HavingFilters[]` | 针对聚合结果的 `HAVING` 过滤。 |
| `orderBy` | `OrderBy[]` | 排序（`boAttrName` + `ASC`/`DESC`）。 |
| `pagination` | `Pagination` | `recordsPerPage` + `pages[]`。 |
| `simpleJoins` | `SimpleJoin[]` | 与关联 BO 的联结。 |
| `joinAlias` | `string` | 联结 BO 的别名。 |
| `unitPolicy` | `string` | 数值属性的单位换算策略。 |
| `language`, `timezone` | `string` | 语言/时区（由 ApiService 自动注入）。 |
| `readChildBO` | `BOQuery[]` | 子 BO 的嵌套查询。 |
| `read*` 标记 | `boolean` | `readBack`、`readUnique`、`readMetadata`、`readRecordsCount`、`readAllRecords` 等。 |

## 支撑类

- **`CriteriaFilters`**：`{ boAttrName, operator, values[] }`
- **`AggregateSelectList`**：`{ boAttrName, aggregateFunction, alias }`
- **`HavingFilters`**：`{ aggregateColumn, operator, values }`
- **`OrderBy`**：`{ boAttrName, order }`
- **`Pagination`**：`{ recordsPerPage, pages[] }`
- **`SaveBOQuery`**：写入路径，结构如 `{ data, dspdmUnits[], operationName, deleteCascade, ... }`

## 响应约定

- 成功标识：`status.statusCode === 1`。
- 记录路径：`data.<boName>.list`。
- 其他状态码均视为错误（Promise reject）。

运算符与聚合函数见 [pdm-query-enums.md](../enums/pdm-query-enums.md)。
