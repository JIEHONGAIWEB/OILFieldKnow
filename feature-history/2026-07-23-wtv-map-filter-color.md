# WTV 地图「Map Side Filter → 图标颜色」语义重构 + 侧栏改版（2026-07-23）

> 范围：`wpo-app/libs/wpe/src/lib/features/well-test-validation-overview/`（`map-panel`、`map-filter-panel`）
> 及 `wpo-app/libs/shared/src/lib/components/`（`com-map-filter-sidebar`、`com-map/builders/com-map-point.builder.ts`）
> 对应需求 REQ-20260723；**取代** REQ-20260722b 的「过滤井」语义与「可展开树」结构。

## 背景

REQ-20260722b 的旧语义是：Map Side Filter（Map Display Control）**过滤**地图上的井——
勾选的状态域决定「哪些井显示」，无动作（绿色）井始终显示，有动作（红色）井仅在其
「有动作的域」中至少一个被勾选时显示（否则从地图上移除）。

新需求把侧栏的职责从「**过滤井**」改为「**决定图标颜色**」：所有有坐标的井**始终显示**，
侧栏勾选的状态域只决定「评估哪些属性来判定红/绿图标」。

## 1. 图标颜色语义（核心变更）

每口井有四个状态属性：Validation Status / Calibration Status / Well Model KPI / Priority Status。

- **红色图标（`well-with-exceptions`）**：**被勾选**的属性中，至少一个为 "With Action"。
- **绿色图标（`well-without-exceptions`）**：**被勾选**的属性全部为 "Without Action" 或空（null）。
- **未勾选**的属性在判色时**被忽略**。
- 侧栏默认**四个属性全部勾选**（评估全部四项）。
- **不再从地图移除任何井**——所有有坐标的井（经 Global Filter 后）始终显示。

### 初始加载
- 首次加载时四个属性均被勾选 → 按全部四项评估 → 有动作的井显示为**红色**。
- （注：需求初稿中「首次加载全部为绿色」一句经确认**不采用**，保持按勾选项评估。）

## 2. 实现要点

### `map-panel.component.ts`
- 原 `applyStatusFilter()`（会 `filter` 掉井并丢弃空 platform）替换为 **`applyIconColor()`**：
  - 保留所有井，不做删除；
  - 逐井调用 `resolveWellIconKey(well, selected)`，按**被勾选的域**计算 `legendIconKey`
    （`'well-with-exceptions'` / `'well-without-exceptions'`），并写回每口井的数据。
- `selected` 取 `checkedDomains()`，为 `null`（未 Apply 过）时等价于「四个域全选」。
- 复用既有 `wellActionDomains(well)` 判定某井在哪些域「有动作」。
- 移除已不再使用的 `isWellVisible()`。

### `com-map/builders/com-map-point.builder.ts`（shared 通用层）
- `createWellPoint()` 新增 `resolveWellLegendIconKey(well, withActions)`：
  - 若井数据**已显式携带** `legendIconKey`（WTV 侧已按勾选项算好），**优先采用**；
  - 否则回退到内置的「四域全评估」`isWellWithActions()`。
- 保持 shared 组件通用：颜色判定的「选择范围」知识留在 WTV 功能层，builder 只尊重外部传入值。

## 3. Map Side Filter 侧栏改版

### 只保留分类（去掉子节点）
- `map-filter-panel` 由「展开箭头 + 复选框 + 分类 + 可展开状态子级」精简为**扁平的四个分类复选框**。
- 移除：chevron 展开按钮、状态叶子列表、`expandedDomains`/`isExpanded`/`toggleExpand`、
  `expandedChange` 输出、`initialExpandedDomains` 输入、`statuses` 字段及 `STATUS_SEMANTIC_CONFIG` 引用。
- `map-panel` 侧同步移除 `filterExpandedDomains` / `expandedDomains` / `onFilterExpandedChange` 及模板绑定。

### 按钮居中成组
- `com-map-filter-sidebar` 的 `.map-filter-sidebar__actions` 由 `justify-content: space-between`
  改为 **`center` + `gap: 12px`**，Reset / Apply 作为一组居中显示。

### 样式改用主题变量（背景色）
- 侧栏背景 `rgba(255,255,255,.98)` → **`var(--background-card)`**；
  标题/图标/文字颜色 → **`var(--color-text)`**；分隔线 → **`var(--border-color-divider)`**。
- 过滤面板内框：边框 → `var(--border-color-divider)`，背景 → `var(--background-card)`，
  标签色 → `var(--color-text)`。
- 由主题变量自动适配明暗，移除冗余的 `[data-theme='dark']` 硬编码色值覆盖（仅保留 toggle 边框与阴影）。

## 4. 主要改动文件

- `libs/wpe/.../well-test-validation-overview/components/map-panel/map-panel.component.{ts,html}`
- `libs/wpe/.../well-test-validation-overview/components/map-filter-panel/map-filter-panel.component.{ts,html,scss}`
- `libs/shared/.../components/com-map/builders/com-map-point.builder.ts`
- `libs/shared/.../components/com-map-filter-sidebar/com-map-filter-sidebar.component.scss`

## 5. 与旧文档的关系

- **取代** [2026-07-22-wtv-map-ui.md](2026-07-22-wtv-map-ui.md) 第 2 节的「可展开树 + 状态持久化」结构
  与第 4 节的「过滤（移除井）」语义。分类/状态的 with/without-action 归属（`ALERT_STATUS_BY_GROUP`）**保持不变**。
- 状态-属性到「With/Without Action」的映射表见
  [requirements-index.md](requirements-index.md#map-with--without-actions-classification-req-20260722)。

## 6. 备注
- 所有改动均通过编译校验（无 TS / 模板错误）。
