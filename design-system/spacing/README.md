# spacing

Spacing scale and layout grid rules.

## Layout / grid

- Legacy PrimeNG grid columns (`.p-col-1` … `.p-col-12`) use `7px 7px` padding.
- Utility height classes exist for percentage layouts: `.height10`,
  `.height20`, `.height30`, `.height35`, `.height40`, `.height50`,
  `.height60`, `.height65`, `.height70`, `.height80`, `.height90`,
  `.height100`, `.height11`, `.height89` (used for splitter/panel sizing).
- Card container `.box`: `border-radius: 4px`, subtle multi-shadow using
  `--cutomize-layout-border`.

## Common spacing values (observed)

- Form group: `margin: 0 10px`, width `240px` (`.formGroup`) / `488px`
  (`.formGrouptext`).
- Button padding: `9px 24px`.
- Dialog header padding: `10px`; dialog footer: `8px 33px`.
- Header bar height: `45px`; detail header height: `35px`.
- Border radius: `4px` (cards/tooltips), `2px` (splitter gutter/handle).

## Splitter (shared mixin `libs/shared/src/lib/styles/_splitter.scss`)

- Gutter `#d3dbe4` (hover `#8ca0b5`), handle `#5f7388` width `3px`; vertical
  handle `48px × 3px`. Dark: gutter `#243546`, hover `#3b546d`, handle
  `#8ea8c2`. Include via `@include splitter.base;` + `splitter.dark`.
