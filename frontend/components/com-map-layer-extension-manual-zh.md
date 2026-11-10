# com-map 业务层扩展使用手册（中文）

面向：需要在共享地图 `com-map` 上**新增一个业务层**（新增图层叠加、新增标记语义、
接入一个全新业务数据源）的开发者。

核心理念：**地图由数据驱动，扩展是「加配置 + 注册 + 写适配器」，不改共享引擎**。
`ComMapComponent`（`com-map`）只认三个契约 `ComMapContext` / `ComMapInfoResponse` /
`ComMapSelection`，对业务零依赖（OCP）。设计背景见
[wso-map-panel-architecture.md](wso-map-panel-architecture.md)，架构决策见
[ADR-0003](../../architecture-decision/0003-com-map-generic-engine-domain-adapter.md)。

## 涉及文件（按场景取用）

| 文件 | 作用 | 扩展时是否要改 |
| --- | --- | --- |
| 你自己的适配容器（如 `libs/<biz>/.../<biz>-map-panel.component.ts`） | 把业务数据映射成 `ComMapInfoResponse`；持有弹窗/图例/图层开关 | ✅ 一定改（或新建） |
| `libs/shared/.../com-map/com-map.legend-icons.ts` | 图标注册表 `registerComMapLegendIcon()` | ⬜ 仅新增图标语义时（在业务侧调用，不改此文件） |
| `libs/shared/.../com-map/com-map.types.ts` | `ComMapIconResolver` / `ComMapLayerConfig` / `layerId` 契约 | ❌ 只读引用 |
| `ComMapComponent`（`com-map`）/ builder / utils | 通用引擎 + 渲染管线 | ❌ **永不改** |

> 所有公共 API 都从 `libs/shared/src/public-api` 导出：`ComMapComponent`、
> `ComMapIconResolver`、`ComMapLayerConfig`、`ComMapLegendIconKey`、
> `registerComMapLegendIcon` 等。

## 关键概念（先理解再动手）

- **契约 `ComMapInfoResponse`** = `ComMapPlatformInfo[]`，每个 platform 带 `wellData[]`。
  业务只要把自己的数据映射成这个结构即可复用整个地图引擎。
- **业务字段随意挂**：`ComMapWellInfo` / `ComMapPlatformInfo` 带 `[key: string]: unknown`
  索引签名——过滤器按 `field` 动态取值，所以你可以往 well 上挂任意字段。
- **图层 `ComMapLayerConfig`** = `{ id, label?, visible? }`。给 well 打上 `layerId`
  （或 `layerKey`），再把 `layers` 传给 `com-map`；`visible === false` 的图层里的井不渲染，
  **没有 `layerId` 的井永远显示**（所以旧的单图层用法不受影响）。
- **图标解析优先级**（越具体越优先）：
  1. 数据里井上显式的 `legendIconKey`（业务已算好颜色，如 WTV 的 Map Side Filter）；
  2. `com-map` 的 `@Input() iconResolver`（业务自持的告警/状态规则）；
  3. 引擎内置 `isWellWithExceptions` 默认规则（兜底）。
- **图标注册表**：`ComMapLegendIconKey` 是开放类型；用 `registerComMapLegendIcon(key, svg)`
  在 bootstrap 时注册新图标 key，引擎渲染时按 key 查表——**无需改共享库**。

---

## 场景一：给地图叠加一个新业务层（图层开关）

例：在井层之上叠加「管线层 Pipelines」，并支持勾选显隐。**纯配置改动。**

### 第 1 步 — 映射时给数据打 `layerId`（适配容器）
在你把业务数据转成 `ComMapInfoResponse` 的方法里，为不同业务的点位打上层标识：
```ts
// wells 层
{ wellId, wellName, latitude, longitude, layerId: 'wells', /* ...业务字段 */ }
// pipelines 层（复用 wellData 承载点位，或作为独立 platform）
{ wellId: pipeId, wellName: pipeName, latitude, longitude, layerId: 'pipelines' }
```

### 第 2 步 — 声明图层配置（signal 驱动显隐）
```ts
readonly showPipelines = signal(true);
readonly layers = computed<ComMapLayerConfig[]>(() => [
  { id: 'wells',     label: 'Wells',     visible: true },
  { id: 'pipelines', label: 'Pipelines', visible: this.showPipelines() },
]);
```

### 第 3 步 — 传给 `com-map`
```html
<com-map [context]="mapContext()" [mapInfo]="mapInfo()" [layers]="layers()"
         (selectionChange)="onMapSelection($event)"></com-map>
```
✅ 完成。切换 `showPipelines()` 即隐藏/显示管线层的点位，**不改引擎、不改 builder**。
没打 `layerId` 的旧数据继续照常显示。

---

## 场景二：为新业务层自定义标记语义（新图标 + 规则）

例：管线层要用一个「橙色告警」图标，且颜色由自己的规则决定。

### 第 1 步 — 注册图标（bootstrap 时一次即可）
```ts
import { registerComMapLegendIcon } from 'libs/shared/src/public-api';

const PIPELINE_ALERT_SVG = `<svg ...>...橙色...</svg>`;
const PIPELINE_OK_SVG    = `<svg ...>...灰色...</svg>`;

constructor() {
  registerComMapLegendIcon('pipeline-alert', PIPELINE_ALERT_SVG);
  registerComMapLegendIcon('pipeline-ok', PIPELINE_OK_SVG);
}
```

### 第 2 步 — 提供业务自持的 `iconResolver`
```ts
readonly pipelineIconResolver: ComMapIconResolver = (well) => {
  if (well['layerId'] !== 'pipelines') {
    return null;            // 非本层交回引擎默认规则处理
  }
  return Number(well['pressureDrop']) > 100 ? 'pipeline-alert' : 'pipeline-ok';
};
```

### 第 3 步 — 绑定
```html
<com-map ... [iconResolver]="pipelineIconResolver"></com-map>
```
> 也可以完全不写 resolver，直接在映射数据时给井写死 `legendIconKey: 'pipeline-alert'`
> （优先级最高）。两种方式二选一即可。

✅ 完成。新图标语义完全在业务侧定义，共享库零改动。

---

## 场景三：接入一个全新业务数据源

例：新建一个 `WeeMapPanelComponent`，复用同一个 `com-map`。

1. **写适配容器**（照抄 `WsoMapPanelComponent` 结构）：用 signal 持有原始业务数据，
   `computed` 出 `mapContext`（带 `source` 标识本业务）和 `mapInfo`（映射成
   `ComMapInfoResponse`）。
   ```ts
   readonly mapContext = computed<ComMapContext>(() => ({ source: 'wee', wellIds: /* ... */ }));
   readonly mapInfo    = computed<ComMapInfoResponse>(() => this.buildMapInfo(this.dataSig()));
   ```
2. **实现 `buildMapInfo()`**：把业务实体分组成 platform → wellData，挂上经纬度与业务字段
   （需要过滤/上色的字段照常挂，参考场景一/二）。
3. **处理选择回调** `(selectionChange)`：按 `event.level` / `event.wellIds` 做弹窗或联动。
4. 需要图层/图标时按场景一、二追加 `layers` / `iconResolver`。

✅ 新业务不改共享引擎，只写一个适配容器即可上地图。

---

## 约定与检查清单

**约定**
- `layerId` 命名带业务/层前缀（`wells` / `pipelines` / `geology-*` / `equipment-*`）。
- 自定义图标 key 带业务前缀（`pipeline-*` / `esp-*`），避免覆盖内置 4 个 key
  （`well-*` / `tower-*`）。
- 业务的告警/状态规则放在**适配容器**里（`iconResolver` 或预先写 `legendIconKey`），
  不要下沉进引擎。
- 需要过滤/上色的字段直接挂在 well 上（利用 `[key: string]: unknown`）。

**提交前检查**
- [ ] 每个自定义图标 key 在 bootstrap 时已 `registerComMapLegendIcon` 注册（否则该点位无图标）。
- [ ] `iconResolver` 对「非本层」的井返回 `null`，交回引擎默认（避免误改其它层颜色）。
- [ ] `layers` 里每个 `id` 与数据里的 `layerId` 一一对应；未打 `layerId` 的点位确认应始终显示。
- [ ] 适配容器把业务数据正确映射成 `ComMapInfoResponse`（platform → wellData，含经纬度）。
- [ ] 编译无错（`get_errors` / `nx build shared`）；本地 `nx serve` 验证图层开关与图标。
- [ ] 未改动 `com-map` 引擎 / builder / utils（若改了，说明偏离本模式，需复核）。

## 相关

- [wso-map-panel-architecture.md](wso-map-panel-architecture.md) — 地图 as-built 架构与可扩展性分析。
- [ADR-0003](../../architecture-decision/0003-com-map-generic-engine-domain-adapter.md) — 架构决策 + 三点配置化实现说明。
- [frontend/ui-patterns/wso-kpi-extension-manual-zh.md](../ui-patterns/wso-kpi-extension-manual-zh.md) — 姊妹篇：KPI 扩展手册。
- [frontend/charts/chart-extension-manual-zh.md](../charts/chart-extension-manual-zh.md) — 姊妹篇：图表扩展手册。
