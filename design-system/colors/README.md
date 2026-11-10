# colors

Color palette and usage rules (semantic color tokens, when to use which).

Colors are CSS variables, switched by `[data-theme=dark|light]`. Most tokens
come from `@webframework/client-theme`; the app adds/overrides the ones below
in `src/wellsurveillance-theme.scss`.

## Semantic status colors (app overrides)

| Token | Dark | Light | Meaning |
| --- | --- | --- | --- |
| `--critical` | `#DD7D89` | `#C71A2F` | Critical alarm |
| `--major` | `#D9B100` | `#776100` | Major alarm |
| `--minor` | `#32B877` | `#238153` | Minor alarm |
| `--data-analysis-summary-color` | `#6A85CE` | `#2A51B9` | Analysis summary |
| `--navigation-link-backgroundcolor` | `#6F9ECD` | `#2A639C` | Nav link bg |
| `--navigation-link-color` | `#141D27` | `#E8ECED` | Nav link text |
| `--tootip-bg-color` | `#2b3847` | `#ffffff` | Tooltip bg |
| `--hyperlink-color` | `#6F9ECD` | `#2A639C` | Hyperlink |

Platform tokens also used: `--color-success`, `--color-error`,
`--color-warning`, `--textColor`, `--background-common-button` (+ `-hover`),
`--background-secondary-button`, `--text-common-button`,
`--background-tooltip-color`, `--cutomize-layout-border`.

## Chart color tokens (ECharts)

Chart-specific colors (axis, legend, tooltip, series, donut center/no-data) live
in one place: **[design-system/charts/README.md](../charts/README.md)** — see the
"Shared tokens" and "Status series colors" tables there. Source of truth:
WTV `chart-panel-options.util`.

## Map exception status

- Wells **with exceptions** → red / warning icon (`exceptions > 0`).
- Wells **without exceptions** → green icon.
