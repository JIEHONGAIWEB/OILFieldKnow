# components

Design-level (not code-level) component specs: states, sizes, anatomy.

Built on **PrimeNG 20** (`p-*`) + `@webframework/*` widgets, wrapped by the
shared `com-*` components. Visual conventions (from
`wellsurveillance-theme.scss`):

## Buttons
- Primary `.p-button`: bg `--background-common-button`, text
  `--text-common-button`, padding `9px 24px`, font 14px, hover
  `--background-common-button-hover`.
- Secondary `.p-button-secondary`: bg/border `--background-secondary-button`,
  text `--text-secondary-button`.

## Cards
- `.p-card` text uses `--textColor`. `.box` container: radius 4px + layered
  border shadow. `com-card` is the standard widget shell (header toolbar +
  body).

## Tables
- `com-table` / `dfs-table` wrap `p-table` (filter/sort/lazy/virtual scroll).
- Table status icons: `.tablei_success` (`--color-success`),
  `.tablei_error` (`--color-error`), 20px; header filter via `.tableFilterTh`.

## Dialogs / drawers
- `p-dialog`: borderless header (padding 10px), footer padding `8px 33px`,
  inputs/selects/datepicker normalized to 28px height.
- `p-drawer` used for detail tables (fixed `30vh`, padding cleared) and map
  layer/filter sidebars.

## Charts / map
- `com-chart` (ECharts) and `com-map` (Leaflet) are the standard viz shells;
  theme-synced colors, bottom legends, toolbar actions
  (`detail / fullscreen / save image / export excel / refresh`).

## Tooltips
- `[data-theme] .p-tooltip`: max-width 1000px, wraps; bg
  `--background-tooltip-color`.
