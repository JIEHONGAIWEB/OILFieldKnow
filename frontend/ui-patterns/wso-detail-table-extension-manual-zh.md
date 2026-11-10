# WSO Detail Table 扩展使用手册（中文）

面向：需要给 WSO 明细表（底部抽屉表格）**新增一个 business layer** 的开发者。

核心理念：**明细表全部由配置驱动，扩展是「加配置 + 注册」，不改壳组件**。抽屉、卡片
（标题/搜索/导出/关闭）、`dfs-table` 引擎都是层无关的（OCP）。架构分析见
[wso-detail-table-architecture.md](wso-detail-table-architecture.md)，通用模式见
[config-driven-ui-patterns.md](config-driven-ui-patterns.md)，同构的 KPI 手册见
[wso-kpi-extension-manual-zh.md](wso-kpi-extension-manual-zh.md)。

## 涉及文件（只需动这几个）

| 文件 | 作用 | 扩展时是否要改 |
| --- | --- | --- |
| `libs/wso/src/lib/configs/wso-detail-table.config.ts` | 列 + dataKey + 导出名 + 卡片配置 + 注册表 | ✅ 一定改 |
| `libs/wso/src/lib/shared/models/*.model.ts` | 新层的行模型（可选，仅为类型清晰） | ⬜ 建议加 |
| 宿主模板（如 `wso-overview.component.html`） | 传 `layer` + 数据源 | ✅ 挂载时改 |
| `WsoDetailTableComponent`（壳） | 抽屉 + 卡片 + 表格编排 | ❌ **永不改** |

## 关键概念（先理解再动手）

- **业务层键 `WsoDetailLayerKey`**：一个联合类型，每个字符串键 = 一个 business layer。
- **配置 `WsoDetailTableConfig`**：`{ columns, dataKey, exportFilename, cardConfig }`——
  一个 layer 需要的全部差异都在这里。
- **注册表 `registerWsoDetailTableConfig(key, config)`**：把键映射到配置；
  `getWsoDetailTableConfig(key)` 读取。默认已注册 `'productionLosses'`。
- **壳输入**：`[rows]`（数据）、`[visible]`（抽屉开关）、`[layer]`（选层，默认
  `'productionLosses'`）、可选 `[config]`（直接传配置，绕过注册表）；输出 `(visibleChange)`。
- **取值方式**：`dfs-table` 按 `column.field` 从每行取值；`dataKey` 是行唯一标识字段。

---

## 场景一：用注册表新增一个 business layer（推荐）

例：新增「Downtime Events（停机事件）」明细层。**壳零改动**。

### 第 1 步 — （可选）定义行模型（`shared/models/`）
仅为类型清晰，非必需（壳的 `rows` 是 `unknown[]`）：
```ts
export interface WsoDowntimeRowModel {
  wellName: string;
  reason: string;
  startTime: string;
  durationHours: number;
}
```

### 第 2 步 — 在联合类型加键（`wso-detail-table.config.ts`）
```ts
export type WsoDetailLayerKey = 'productionLosses' | 'downtimeEvents';
```

### 第 3 步 — 定义列元数据
`field` 必须与行对象字段名一致；按需开启排序/过滤：
```ts
const DOWNTIME_COLUMNS: DfsTableColumn[] = [
  { field: 'wellName', header: 'WELL NAME', sortable: true, filterable: true, filterType: 'INPUT' },
  { field: 'reason', header: 'REASON', sortable: true, filterable: true, filterType: 'INPUT' },
  { field: 'startTime', header: 'START TIME', sortable: true },
  { field: 'durationHours', header: 'DURATION (H)', sortable: true },
];
```

### 第 4 步 — 注册（唯一改变行为的一段）
```ts
registerWsoDetailTableConfig('downtimeEvents', {
  columns: DOWNTIME_COLUMNS,
  dataKey: 'wellName',
  exportFilename: 'wso-downtime-events',
  cardConfig: {
    title: 'DOWNTIME EVENTS',
    bordered: false,
    isShowSearch: true,
    actions: ['close', { type: 'menu', kind: 'menu', tooltip: 'More', items: ['exportExcel'] }],
    bodyStyle: { height: '100%', overflow: 'hidden' },
  },
});
```

### 第 5 步 — 宿主挂载（传 `layer` + 数据源）
```html
<wso-detail-table
  layer="downtimeEvents"
  [rows]="downtimeRows()"
  [visible]="downtimeVisible()"
  (visibleChange)="onDowntimeVisibleChange($event)">
</wso-detail-table>
```

完成。**没有修改 `WsoDetailTableComponent`**，只加了配置 + 注册 + 一处挂载。

---

## 场景二：一次性 / 动态配置，不进注册表

当配置来自运行时（如后端返回列定义），直接传 `[config]`，它优先于 `layer`：
```html
<wso-detail-table [config]="dynamicConfig()" [rows]="rows()" [visible]="v()"
  (visibleChange)="onVisibleChange($event)"></wso-detail-table>
```
```ts
readonly dynamicConfig = computed<WsoDetailTableConfig>(() => ({
  columns: this.apiColumns(), dataKey: 'id',
  exportFilename: 'export', cardConfig: { title: this.apiTitle(), isShowSearch: true },
}));
```

---

## 检查清单

- [ ] `WsoDetailLayerKey` 已加新键（TS 会强制 `register`/`getWsoDetailTableConfig` 用合法键）。
- [ ] 列 `field` 与行对象字段名逐一对应（否则单元格空白）。
- [ ] `dataKey` 指向行内唯一字段（用于选择/过滤，重复会导致行为异常）。
- [ ] `exportFilename` 不含扩展名。
- [ ] `cardConfig.actions` 含 `close` + 导出菜单（与既有层一致，除非有意不同）。
- [ ] 宿主模板 `layer="<新键>"` 与数据源 `[rows]` 都已接线；`(visibleChange)` 已回写 visible。
- [ ] 保存后对改动文件跑编译诊断，无 TS 错误。

## 常见坑

- **不要改壳组件**：任何「为新层加分支」的冲动都应落到配置/注册表层（OCP）。
- **`rows` 是 `unknown[]`**：类型安全靠自己的行模型 + 列 `field` 约定，不由壳强制。
- **`layer` 未注册**：`resolvedConfig` 会回退到默认层 `'productionLosses'`——若看到「串了
  别的层」，多半是 `layer` 键拼写错或忘了 `register`。
- **`[config]` 覆盖 `[layer]`**：两者同传时以 `config` 为准，排查时先确认没误传 `config`。
