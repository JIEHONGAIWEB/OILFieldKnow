# interaction

Motion, transitions, and interaction/feedback conventions.

## Transitions
- Buttons: `background-color .2s`.
- Splitter gutter: `background-color 120ms ease` on hover.
- ECharts tooltip: `transitionDuration: 0` + `confine: true` to avoid
  ghosting/重影.

## Highlight / active-inactive pattern
- Selecting one item (e.g. a chart) highlights it; others go **inactive**
  via `opacity` / `saturate` degradation but **remain interactive**
  (not disabled). Inner controls (slider, toolbar) call `stopPropagation`
  to avoid accidentally triggering activation.
## Chart ↔ map/table linkage (standing convention)
- **Applies to every chart going forward, not only donut slices.** Selecting a
  data element in any chart (donut slice, bar, line point, scatter point, KPI
  card, etc.) drives a shared **highlight + dimming** linkage: the selected
  element and its corresponding map points / table rows are highlighted, while
  non-selected slices/points/rows are dimmed (reduced `opacity` / `saturate`)
  but **remain interactive** (not disabled/removed).
- Linkage is bidirectional (chart ↔ map ↔ table) and clears on deselect.
- New chart types **must** wire into the same linkage mechanism rather than
  inventing a per-chart interaction.

## Map interactions
- Auto-fit runs **once** on initial load; later interactions do not re-zoom.
- Clicking a well shows a **popup only** (no linkage write-back, no data
  refresh); popup anchors to click coordinates, with dual tabs
  (`ACTION SUMMARY / INFORMATION`).
- Cursor: `pointer` over well points, `grab` over empty map.
- Side filter (Map Display Control) does **not** remove points; on **Apply** it
  re-scopes which status domains are evaluated for each well's **icon color**
  (red = any selected domain With-Actions, else green). All wells stay visible.

## Panels / splitter
- Manual collapse hides the map → chart takes full width; an overlay button
  restores the splitter layout. Min-size constraints prevent panels from
  being dragged to an unusable width. (Auto-collapse-on-min-width was
  intentionally removed to reduce state complexity.)

## Toolbar model (charts/cards)
- Standardized order: `detail → expand/fullscreen → menu`
  (`Save Image / Export Excel / Refresh Data`).
