# WSO Detail Table — 架构模式分析（壳组件 + 数据驱动表格引擎）

> 范围：`wpo-app/libs/wso/src/lib/components/detail-table/wso-detail-table/`
> （`wso-detail-table.component.ts` / `.html` / `.scss`）
> 数据模型：`libs/wso/src/lib/shared/models/wso-detail-row.model.ts`
> 表格引擎：`@dfs/dfs-core`（`DfsTableComponent` / `DfsTableColumn`）
> 相关：[config-driven-ui-patterns.md](config-driven-ui-patterns.md)（模式 1/2/3/10）、
> [wso-kpi-by-production-method.md](wso-kpi-by-production-method.md)、ADR-0002。

> 状态：**已重构为配置驱动壳 + 注册表**（2026-07-24）。下文保留模式分析，并在
> 「当前实现」小节说明重构后的用法。

## 结论速览

- **架构模式**：组合式「业务壳（Shell）+ 通用数据驱动表格引擎」。壳组件本身几乎不含
  表格逻辑，只做**布局组合**与**事件转发**。
- **是否数据驱动**：**引擎层是**（`dfs-table` 传 `columns` 元数据 + `data` 即可渲染）；
  壳层重构后也变为**配置驱动**（列/行键/卡片/导出名均由注册表提供）。
- **可扩展性**：底层引擎可复用于任意 business layer；壳组件已参数化，
  **新增 business layer = 在注册表加一条配置**，无需复制壳（OCP）。

## 组合结构

```
WsoDetailTableComponent（业务壳）
├── p-drawer          底部抽屉布局容器（position=bottom, 30vh, 非模态）
├── com-card          通用卡片：标题 / 搜索框 / 导出 Excel / 关闭（ComCardConfig 声明式）
└── dfs-table         通用表格引擎（@dfs/dfs-core）
      ├── [columns]   = WSO_DETAIL_COLUMNS（DfsTableColumn[] 元数据）
      └── [data]      = rows（WsoDetailRowModel[]）
```

数据流：`rows`（`@Input`）→ `dfs-table [data]`；列元数据 `WSO_DETAIL_COLUMNS` →
`dfs-table [columns]`；卡片动作（search / close / exportExcel）经
`onCardAction()` 转发到 `dfs-table.search()` / `visibleChange` / `dfs-table.onExport()`。

## 命中的设计模式（对照 config-driven 目录）

| 模式 | 体现 |
| --- | --- |
| Config-Driven（模式 1） | 表格由 `DfsTableColumn[]` 元数据 + `data` 驱动渲染 |
| Strategy / Metadata（模式 2/6） | 列的 `sortable/filterable/filterType` 决定单元格/过滤行为 |
| Headless（模式 10） | `dfs-table` = 纯展示+交互引擎；壳注入布局与业务事件 |
| Slots/Composition（模式 5） | `com-card` 用 `<ng-content>` 承载表格体，drawer 承载卡片 |

## 「数据驱动」判定（分层）

| 维度 | 数据驱动？ | 说明 |
| --- | --- | --- |
| `dfs-table` 引擎 | ✅ 完全 | 排序/过滤/搜索/导出均由引擎按 `columns`+`data` 处理 |
| 列/行为配置方式 | ✅ 声明式 | 列是元数据数组；卡片行为是 `ComCardConfig` |
| **当前壳组件** | ❌ 硬编码 | `WSO_DETAIL_COLUMNS`、`WsoDetailRowModel`、标题 `'PRODUCTION LOSSES'`、`dataKey="wellName"`、`exportFilename` 全部写死为单一业务 |

## 当前实现（重构后，2026-07-24）

壳组件已参数化，业务差异全部收敛到注册表。

**新增文件** `libs/wso/src/lib/configs/wso-detail-table.config.ts`：

```typescript
export type WsoDetailLayerKey = 'productionLosses';
export interface WsoDetailTableConfig {
  columns: DfsTableColumn[]; dataKey: string;
  exportFilename: string; cardConfig: ComCardConfig;
}
const DETAIL_TABLE_REGISTRY = new Map<WsoDetailLayerKey, WsoDetailTableConfig>();
export function registerWsoDetailTableConfig(key, config) { REGISTRY.set(key, config); }
export function getWsoDetailTableConfig(key) { return REGISTRY.get(key); }
registerWsoDetailTableConfig('productionLosses', { columns, dataKey: 'wellName',
  exportFilename: 'wso-production-losses', cardConfig: { title: 'PRODUCTION LOSSES', ... } });
```

**壳组件输入**（`wso-detail-table.component.ts`）：

```typescript
@Input({ required: true }) rows: unknown[] = [];   // 不再锁死 WsoDetailRowModel
@Input() visible = false;
@Input() layer: WsoDetailLayerKey = 'productionLosses';  // 选定业务层
@Input() config?: WsoDetailTableConfig;                  // 显式覆盖（可选）
// columns / cardConfig / dataKey / exportFilename 均为 getter，从 resolvedConfig 取
// resolvedConfig = config ?? getWsoDetailTableConfig(layer) ?? 默认层
```

模板改为 `[dataKey]="dataKey"` `[exportFilename]="exportFilename"`（原为字面量）。

### 向后兼容

`[rows]` / `[visible]` / `(visibleChange)` 三个输入输出保持不变；`layer` 默认
`'productionLosses'`，故 `wso-overview` 现有绑定（`[rows]="filteredDetailRows()"`）
无需修改。`WsoDetailRowModel[]` 可赋值给 `unknown[]`。

### 新增 business layer 的步骤（OCP）

1. 在 `WsoDetailLayerKey` 联合类型加一个键。
2. `registerWsoDetailTableConfig('<newKey>', { columns, dataKey, exportFilename, cardConfig })`。
3. 宿主模板：`<wso-detail-table layer="<newKey>" [rows]="rows" [visible]="..." />`，
   或直接传 `[config]="myConfig"` 覆盖。**无需改壳组件**。

## 与既有资产的关系

- 与 [wso-kpi-by-production-method.md](wso-kpi-by-production-method.md) 的「按 Production
  Method 注册表加载 KPI」同构：两者都是「注册表 + 配置」对抗分支膨胀。detail-table 若照此
  改造，可与 KPI 模式风格统一。
- 复用惯例见 [../components/README.md](../components/README.md)：优先组合 `com-*` / 平台
  `dfs-table` 包装，而非直接用 `p-*` 原语。

## 开放项 / TODO

- [x] 将 `WsoDetailTableComponent` 重构为配置驱动壳 + 注册表（2026-07-24 完成）。
- [ ] 待出现第二个 business layer 时，明确 `WsoDetailLayerKey` 与 KPI 的 Production Method
  键是否统一（可共享一套业务层枚举）。
