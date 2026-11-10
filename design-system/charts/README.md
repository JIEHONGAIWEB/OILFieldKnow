# charts

Chart visual design language (ECharts). Kept separate from charting *conventions*
(library choice / where charts live) which are in `frontend/charts/`.

> Source of truth: `wpo-app` WTV `chart-panel-options.util.ts`
> (`buildStatusDonutOption`, `buildTrendChartOption`), aligned with the
> `srp-new` well-trends theme tokens. Rendered via ECharts 6 (`ngx-echarts` /
> shared `com-chart`).

## Theming

- Every chart supports **light/dark**; components read the `[data-theme]` on the
  document root and **rebuild ECharts options** on theme switch (via
  `MutationObserver`), because ECharts bakes colors into the option object.
- Charts set `animation: false` for snappy re-render on filter/theme changes.
- Tooltips use `confine: true` + `transitionDuration: 0` to avoid ghosting.

## Shared tokens (light / dark)

| Element | Light | Dark |
| --- | --- | --- |
| Axis label text | `#818F99` | `#86A1CF` |
| Axis line / tick | `#3B4957` | `#1E3A5F` |
| Split line (grid) | `#E8ECED` | `#1E3A5F` |
| Legend text | `#4F5E6A` (donut) / `#141D27` (trend) | `#B8C7D6` (donut) / `#86A1CF` (trend) |
| Tooltip background | `rgba(255,255,255,0.96)` | `rgba(12,20,30,0.94)` |
| Tooltip text | `#2F3A44` | `#DBE6F1` |
| Center text (donut) | `#2F3A44` | `#D6E0EB` |
| "No Data" slice | `#D5DBE1` | `#435465` |
| Highlight border | `#141D27` | `#FFFFFF` |

## Donut (ring pie) chart

- Series `type: 'pie'`, `radius: ['50%','75%']`, `center: ['50%','42%']`, no labels/labelLines.
- Center graphic text: `"{n} Wells"`, **fontSize 18, weight 700**.
- Legend: bottom, `type: 'scroll'`, horizontal centered, `icon: 'roundRect'`,
  **itemWidth 16 × itemHeight 8**, `itemGap 12`, text **13px / weight 500**.
- Emphasis: `scale: true, scaleSize: 4`.
- Empty state: single `No Data` slice using the "No Data" color.
- Slice colors come from the status palette (`WTV_STATUS_PALETTE`).

## Line / trend chart

- `grid: { top:20, left:16, right:40, bottom:48, containLabel:true }`.
- Axis label **fontSize 10, weight 700**; y-axis `formatter: '{value}%'`, `min:0 max:100`.
- x-axis `boundaryGap:false`, `splitLine.show:false`, `axisLabel.margin 12`, `hideOverlap`.
- Legend: bottom, scroll, **itemWidth 22 × itemHeight 16**, `itemGap 18`, text **12px / weight 500**.
- Lines: `width 2`, `symbol:'circle'`, `symbolSize 6`, `smooth:false`.

## Status series colors (semantic, fixed)

| Status | Color |
| --- | --- |
| Excellent | `#51C38B` |
| Good | `#8EB3D8` |
| Average | `#D3A700` |
| Poor | `#C21228` |
| NA | `#818F99` |

## Interaction

- Active/inactive: an inactive (unselected) chart is **dimmed** (slice opacity
  `0.5`, center text opacity `0.3`) and `silent: true` (non-interactive), rather
  than removed.
- Selecting one slice dims the others in the same chart to opacity `0.3`.
