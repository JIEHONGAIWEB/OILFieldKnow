# typography

Type scale, font families, weight/usage rules.

## Font family

- Primary UI font: **Barlow** (provided via `@webframework/client-theme`
  `themes/main`), with icon fonts `Font Awesome 5 Free` and `primeicons`
  in the fallback stack.

## Observed type scale (from `wellsurveillance-theme.scss`)

| Usage | Size | Weight |
| --- | --- | --- |
| Form group label | 12px | bold |
| Tooltip / small text | 12px | — |
| Button text | 14px | — |
| Header title | 16px | 600 |
| Status/table icons | 20px | — |

- Body/base sizing inherits from the platform theme; the app only overrides
  specific component text sizes rather than defining a full scale.
