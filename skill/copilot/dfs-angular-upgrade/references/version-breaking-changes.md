# Angular Version Breaking Changes

Quick reference for DFS developers migrating Angular projects.
Each section covers one major-version hop.

---

## Quick Reference Table

| Hop     | Key Risk                                    | PrimeNG Impact? | MF Impact?                |
|---------|---------------------------------------------|-----------------|---------------------------|
| 12 → 13 | Ivy-only, View Engine removed               | No              | Low                       |
| 13 → 14 | Typed reactive forms                        | No              | Low                       |
| 14 → 15 | Standalone components default path begins   | No              | Low                       |
| 15 → 16 | Required inputs, signals preview            | No              | Medium                    |
| 16 → 17 | New build system (esbuild), standalone default | No           | HIGH — stay on webpack    |
| 17 → 18 | Zoneless preview, strict SSR                | No              | Medium                    |
| 18 → 19 | Signal-based inputs/outputs GA              | Minor           | Low                       |
| 19 → 20 | Signals stable, standalone fully default    | CRITICAL renames | Medium                   |

---

## 12 → 13

**Minimum Node.js:** 12.20.x
**TypeScript:** 4.4–4.6

### Key Changes

- **Ivy-only:** View Engine is removed. If your app has `enableIvy: false` anywhere, remove it.
- **APF (Angular Package Format) v13:** Library authors must update. Consuming apps: no action
  unless you build an Angular library.
- **`TestBed.inject` required:** `TestBed.get()` is removed. Replace with `TestBed.inject()`.

### Common Errors

- `Cannot find module '@angular/compiler'` — remove `enableIvy: false` from tsconfig
- `TestBed.get is not a function` — replace with `TestBed.inject`

---

## 13 → 14

**Minimum Node.js:** 14.15.x
**TypeScript:** 4.6–4.8

### Key Changes

- **Standalone components (developer preview):** `@Component({ standalone: true })` available
  but not required.
- **Typed Reactive Forms:** `FormControl`, `FormGroup`, `FormArray` are now typed.
  Untyped versions (`UntypedFormControl`, etc.) available for gradual migration.
- **`inject()` function:** Replaces constructor DI in functions/factories.
- **`ChangeDetectionStrategy.Default` stricter:** Some change detection edge cases surface.

### Common Errors

- `Type 'AbstractControl<any>' is not assignable to...` — migrate to typed forms or use
  `UntypedFormControl`
- `NullInjectorError` when using `inject()` outside injection context — move `inject()` calls
  to field initializers

---

## 14 → 16 (covers 14→15 then 15→16)

**Minimum Node.js (16):** 16.14.x
**TypeScript (15):** 4.8–5.0 | **TypeScript (16):** 4.9–5.1

### 14 → 15 Key Changes

- **`@NgModule` now optional path:** Standalone APIs promoted.
- **`RouterModule` functional guards:** `CanActivateFn` replaces `CanActivate` class-based guards.
- **`providedIn: 'root'` default:** Most services should use this.
- **Angular Material:** M3 migration path available.

### 15 → 16 Key Changes

- **Required inputs:** `@Input({ required: true })` available.
- **Signals (developer preview):** Avoid using in production code until Angular 17.
- **`DestroyRef`:** New injection token for cleanup — use instead of `ngOnDestroy` in many cases.
- **esbuild builder (developer preview):** Do NOT switch MF projects to esbuild yet — use
  `@angular-devkit/build-angular:browser` builder.

### Common Errors

- `NG0303: Can't bind to 'routerLink'` — add `RouterModule` or import `RouterLink` standalone
- `NG6999: injected dependencies not in constructor` — expected with `inject()` pattern

---

## 16 → 17

**Minimum Node.js:** 18.13.x
**TypeScript:** 5.2–5.3

### Key Changes

- **New build system (esbuild) is now default for new projects.** Existing projects are NOT
  auto-migrated.
- **⚠️ MF WARNING:** Do NOT switch to the new `@angular-devkit/build-angular:application`
  builder if your project uses `@angular-architects/module-federation`. Stay on
  `@angular-devkit/build-angular:browser` until MF officially supports esbuild.
- **Standalone is now the default** for new components generated via CLI. Existing components
  unchanged.
- **`@if`, `@for`, `@switch` control flow:** New built-in control flow syntax replaces `*ngIf`,
  `*ngFor`. Old syntax still works — migration is optional but recommended.
- **`ngDevMode`:** Webpack config must define it explicitly (see `migration-strategy.md`
  MF section).

### MF Projects: Required webpack.config.js Change

```javascript
// Add to plugins array
new webpack.DefinePlugin({
  ngDevMode: JSON.stringify(false)
})
```

### Common Errors

- `Cannot read properties of undefined (reading 'ɵfac')` — usually a peer dependency version
  mismatch post-upgrade
- Build failing on `ngDevMode` undefined — add `DefinePlugin` as shown above
- `Module not found: Error: Can't resolve '@angular/core'` in remotes — check `shared` config
  in `webpack.config.js`

---

## 17 → 18

**Minimum Node.js:** 18.19.x
**TypeScript:** 5.4

### Key Changes

- **Zoneless change detection (developer preview):** Available via
  `provideExperimentalZonelessChangeDetection()`. Do NOT use in production yet.
- **`@let` template syntax (developer preview):** Local template variable declarations.
- **SSR (Server-Side Rendering):** Promoted to stable; SSR scaffold improved.
  Non-SSR apps: no action needed.
- **`afterNextRender` / `afterRender` APIs:** Replace `ngAfterViewInit` for some use cases.
- **`provideRouter` with `withComponentInputBinding()`:** Pass route params as component
  inputs directly.

### Common Errors

- `NullInjectorError: No provider for HttpClient` — add `provideHttpClient()` to `app.config.ts`
- Zone.js deprecation warnings — expected; ignore unless opting into zoneless

---

## 18 → 19

**Minimum Node.js:** 18.19.x
**TypeScript:** 5.5–5.6

### Key Changes

- **Signal inputs/outputs GA:** `input()`, `output()`, `model()` are stable API.
- **`linkedSignal` (developer preview):** Avoid in production.
- **Incremental hydration (developer preview):** SSR feature — ignore for non-SSR apps.
- **TypeScript 5.5:** Inferred type predicates. Some stricter type checks may surface.
- **PrimeNG 18 → 19:** Minor API changes. Check PrimeNG 19 changelog for any components
  you use.

### Common Errors

- `@Input()` with `transform` property warnings — consider migrating to signal inputs if on
  signals path
- TypeScript 5.5 stricter predicate inference — review any custom type guard functions

---

## 19 → 20

**Minimum Node.js:** 18.19.x
**TypeScript:** 5.7–5.8

### Key Changes

- **Signals stable:** Full signals-based component authoring is production-ready.
- **Standalone fully default:** `bootstrapApplication()` and `app.config.ts` are the standard.
  `NgModule`-based apps still work but new CLI scaffolding is standalone-only.
- **`effect()` stable API changes:** `effect()` runs in the injection context by default.
  Review any effects using `allowSignalWrites`.
- **`@angular/forms` signal-based controls:** `FormControl` from signals available but not
  required.
- **TypeScript 5.7+:** Stricter `noUncheckedIndexedAccess` patterns.

### ⚠️ PrimeNG 19/16 → 20: CRITICAL Component Renames

**These renames break at compile time — must be applied after each ng update.**

#### TypeScript/Component Class Renames

| Old Name        | New Name       |
|-----------------|----------------|
| `Dropdown`      | `Select`       |
| `Calendar`      | `DatePicker`   |
| `InputSwitch`   | `ToggleSwitch` |
| `InputTextarea` | `Textarea`     |
| `OverlayPanel`  | `Popover`      |
| `TabView`       | `Tabs`         |
| `TabPanel`      | `Tab`          |

#### HTML Template Selector Renames

| Old Selector       | New Selector      |
|--------------------|-------------------|
| `p-dropdown`       | `p-select`        |
| `p-calendar`       | `p-datepicker`    |
| `p-inputSwitch`    | `p-toggleswitch`  |
| `p-inputTextarea`  | `p-textarea`      |
| `p-overlayPanel`   | `p-popover`       |
| `p-tabView`        | `p-tabs`          |
| `p-tabPanel`       | `p-tab`           |

#### Import Path Changes

Old: `import { DropdownModule } from 'primeng/dropdown'`
New: `import { SelectModule } from 'primeng/select'`

Apply for all renamed components (Calendar→datepicker, InputSwitch→toggleswitch, etc.).

### Common Errors (Angular 20)

- `'Dropdown' is not a known element` — rename to `Select`, update import path
- `Can't bind to 'ngModel' on 'p-select'` — add `FormsModule` or `ReactiveFormsModule`
- TypeScript errors from PrimeNG internals — add `skipLibCheck: true` to `tsconfig.json`
- `Cannot find module 'primeng/dropdown'` — update import path to `primeng/select`
