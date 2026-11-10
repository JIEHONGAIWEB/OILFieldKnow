# design-system

Visual design language, kept separate from component implementation.

> Source: `wpo-app` — `src/styles.scss`, `src/wellsurveillance-theme.scss`,
> `libs/shared/src/lib/styles/`, plus `@webframework/client-theme` and
> `@primeng/themes`.

## Foundations

- **Base themes**: PrimeNG themes (`@primeng/themes`) + `@webframework/client-theme`
  (`themes/main`) provide the core token set (`--color-success`,
  `--color-error`, `--textColor`, etc.). Angular Material `indigo-pink`
  prebuilt is also loaded. Icons: Font Awesome + PrimeIcons.
- **Light/Dark theming** is driven entirely by **CSS variables** switched on a
  `[data-theme="light" | "dark"]` attribute on the document root. Components
  read variables; they do not hardcode colors. ECharts charts observe
  `data-theme` via `MutationObserver` and rebuild options on switch.
- App-level style entry: `src/styles.scss`; app-specific overrides & tokens:
  `src/wellsurveillance-theme.scss`.

See sub-pages: [colors](colors/README.md), [typography](typography/README.md),
[spacing](spacing/README.md), [components](components/README.md),
[interaction](interaction/README.md), [charts](charts/README.md).
