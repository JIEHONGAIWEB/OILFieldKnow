# WTV Overview 今日功能完成说明：NA 状态展示与统计一致性（2026-11-19）

- Shipped: 2026-11-19
- Owner: Jiehong-WANG_hal
- Related ADRs: —
- 关联提交: `5520a70 feat(wpe): align NA legend and map status display`
- 源文档: `wpo-app/docs/implementation/WTV_NA_STATUS_UPDATE_2026-11-19.md`（`EEE-WPO` 仓库）

> 范围：`wpo-app/libs/wpe/src/lib/features/well-test-validation-overview/`

## What shipped

### 1. Validation / Calibration 环图支持 NA legend

- 在状态语义配置中为 `validation` 和 `calibration` 增加 `NA` 条目。
- 在 legend 顺序配置中为 `validation` 和 `calibration` 增加 `NA`，保证展示顺序稳定。

实现位置：

- `libs/wpe/src/lib/features/well-test-validation-overview/shared/config/status-semantic.config.ts`
- `libs/wpe/src/lib/features/well-test-validation-overview/shared/config/legend.config.ts`

### 2. 统一 NA 调色为 KPI Trend 语义色

- `NA` 颜色统一为 `#818F99`（与 KPI Trend 保持一致）。

实现位置：

- `libs/wpe/src/lib/features/well-test-validation-overview/shared/config/palette.config.ts`

### 3. 统计映射规则明确化（mapper）

在 donut 统计映射中（`validation/calibration`）：

- 原始状态为 `NA` / `N/A` -> 归一为 `NA`
- 原始状态为 `null` / 空字符串 / `-` -> 归一为 `-`

说明：`-` 不会计入 `NA` 计数，避免将“缺失值”误计为 “NA 状态”。

实现位置：

- `libs/wpe/src/lib/features/well-test-validation-overview/shared/util/wtv-overview-stat.mapper.ts`

### 4. Map Popup 状态展示规则收敛

在 map popup（Action Summary）里：

- 状态文本保持“原值优先”；仅在空值/无效值时回退为 `-`
- 不再按 domain 强制把空值显示为 `NA`
- 清理未使用方法 `toDisplayColor`

实现位置：

- `libs/wpe/src/lib/features/well-test-validation-overview/components/map-panel/map-panel.component.ts`

## Why

- 补齐 `validation/calibration` 维度对 `NA` 状态的展示与统计一致性。
- 统一 `NA` 颜色语义（与 KPI Trend 一致）。
- 避免把“缺失值”（`null` / 空 / `-`）误计为 “NA 状态”，并收敛 map popup 的展示规则。

## Current visible behavior

### 文本展示

- 真实返回 `NA`：显示 `NA`
- 返回 `null` / 空 / `-`：显示 `-`

### 颜色展示（Map Popup）

颜色由状态分组判定：

- 红色（告警）：命中各 domain 的 alert 状态集合
- 绿色（非告警）：状态可识别且不在 alert 集合
- 无颜色：状态为空、`-` 或无法映射为 canonical 状态

## Impact

- WTV Overview 状态环图（Validation / Calibration）
- WTV Overview 地图弹窗（Action Summary）
- 相关状态筛选项（依赖状态语义配置的下游组件）

## What changed since

- 2026-07-23: Map 侧栏筛选语义改为决定图标颜色，详见 [2026-07-23-wtv-map-filter-color.md](2026-07-23-wtv-map-filter-color.md)。本文件中 map popup 的颜色规则基于同一套 alert 分组（`ALERT_STATUS_BY_GROUP`），未被该变更取代。
- 参见 [requirements-index.md](requirements-index.md#map-with--without-actions-classification-req-20260722) 中的 With/Without Actions 分类表。
