# Third-Party Dependency Upgrade Checklist

Follow this checklist after each major Angular version hop. Not all sections apply to
every project — check which libraries your project uses with `npm ls | grep <library-name>`.

---

## PrimeNG

### Version Alignment

| Angular Version | PrimeNG Version |
|-----------------|-----------------|
| 16              | 16.x            |
| 17              | 17.x            |
| 18              | 18.x            |
| 19              | 19.x            |
| 20              | 20.x (also compatible with PrimeNG 19.x) |

Upgrade PrimeNG separately after upgrading Angular core:

```bash
npm install primeng@<target-major>
```

### PrimeNG 19/16 → 20: Component Renames

Apply these renames in TypeScript imports, HTML templates, and NgModule declarations.

**Full rename table is in `version-breaking-changes.md` → "19 → 20" section.**

Quick search — find affected files:

```bash
# TypeScript files using old component names
grep -rl "Dropdown\|Calendar\|InputSwitch\|InputTextarea\|OverlayPanel\|TabView\|TabPanel" \
  src/ --include="*.ts"

# HTML templates using old selectors
grep -rl "p-dropdown\|p-calendar\|p-inputSwitch\|p-inputTextarea\|p-overlayPanel\|p-tabView\|p-tabPanel" \
  src/ --include="*.html"
```

### New @primeng/themes Package (PrimeNG 19+)

PrimeNG 19+ ships a new theming system. The old CSS import approach is deprecated.

**Remove from `angular.json` styles:**

```json
// REMOVE these legacy style entries:
"node_modules/primeng/resources/themes/lara-light-blue/theme.css"
"node_modules/primeng/resources/primeng.min.css"
"node_modules/primeicons/primeicons.css"
```

**Install the new theme package:**

```bash
npm install @primeng/themes
```

**Configure in `app.config.ts`:**

```typescript
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { providePrimeNG } from 'primeng/config';
import Aura from '@primeng/themes/aura';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
        preset: Aura
      }
    })
  ]
};
```

---

## NgRx

### Version Alignment

NgRx major version MUST match Angular major version:

| Angular Version | NgRx Version |
|-----------------|--------------|
| 16              | 16.x         |
| 17              | 17.x         |
| 18              | 18.x         |
| 19              | 19.x         |
| 20              | 20.x         |

Upgrade NgRx after Angular core:

```bash
ng update @ngrx/store @ngrx/effects @ngrx/entity @ngrx/router-store
```

Or manually (install all `@ngrx/*` packages you use to the same version simultaneously):

```bash
npm install @ngrx/store@<N> @ngrx/effects@<N> @ngrx/entity@<N> @ngrx/router-store@<N>
```

### API Stability

- **Actions, reducers, selectors, effects:** Stable across Angular 12–20. No breaking renames.
- **`createReducer` / `on()`:** Stable.
- **`createEffect`:** Stable. `{ dispatch: false }` pattern unchanged.
- **`createFeatureSelector` / `createSelector`:** Stable.

### NgRx Signals Store (NgRx 17+)

Available but optional. Existing `@ngrx/store` usage does NOT need to migrate.

---

## RxJS

### Angular / RxJS Version Matrix

| Angular Version | RxJS Version |
|-----------------|--------------|
| 12–13           | 6.x or 7.x   |
| 14–16           | 7.x          |
| 17–20           | 7.x          |

Angular 20 does not require RxJS 8. RxJS 7.x is still the default peer dependency.

### RxJS 6 → 7 Migration (if still on 6)

```bash
npm install rxjs@7
```

Key operator changes:

- `throwError(new Error('msg'))` → `throwError(() => new Error('msg'))` (factory function required)
- `toPromise()` deprecated — use `lastValueFrom()` or `firstValueFrom()` instead
- `combineLatest([...])` — array syntax (already default in v6 pipeable)

### Deprecated Operators to Replace

| Deprecated              | Replacement                                    |
|-------------------------|------------------------------------------------|
| `toPromise()`           | `lastValueFrom(obs$)`                          |
| `throwError(err)`       | `throwError(() => err)`                        |
| `tap(null, errFn)`      | `tap({ error: errFn })`                        |
| `catchError` + rethrow  | `catchError(err => throwError(() => err))`     |

---

## Angular Material

### Version Alignment

Angular Material major version must match Angular major version:

```bash
ng update @angular/material@<N>
```

`ng update` will run Material schematics automatically.

### M2 → M3 Migration

Angular Material 17+ ships Material Design 3 (M3) as opt-in. Angular Material 20 makes M3
the default for new projects.

**For existing projects on M2:** You do NOT need to migrate to M3 during an Angular version
upgrade. M2 continues to work in Angular 20. Migrate M2 → M3 as a separate dedicated task.

**To stay on M2 explicitly:**

```typescript
// In your theme SCSS file:
@use '@angular/material' as mat;

$theme: mat.define-theme((
  color: (
    theme-type: light,
    use-system-variables: false,
  )
));
```

---

## @webframework (DFS Internal Packages)

DFS projects using `@webframework/*` packages must align versions with Angular.

```bash
# Check current installed versions
npm ls | grep @webframework

# Update to match Angular target version
# (contact DFS platform team for the version compatibility matrix)
npm install @webframework/core@<N> @webframework/components@<N>
```

If `@webframework` packages have peer conflicts after Angular upgrade:

1. Check the DFS internal Confluence/Teams channel for the compatible version matrix.
2. Use `--legacy-peer-deps` as a temporary measure while the platform team publishes a
   compatible version.

---

## Module Federation: @angular-architects/module-federation

### Version Alignment

```bash
ng update @angular-architects/module-federation@<N>
```

Or:

```bash
npm install @angular-architects/module-federation@<N>
```

Match the major version to Angular (e.g., Angular 18 → `@angular-architects/module-federation@18`).

### Post-Update webpack.config.js Review

After each upgrade, review `webpack.config.js` for:

1. **Shared deps expanded** — add any new `@angular/*` or `@ngrx/*` packages introduced during
   the upgrade
2. **`strictVersion: false`** — confirm still set on all Angular/NgRx shared packages
3. **webpack pin** — confirm `"webpack": "5.94.0"` still in `overrides`

---

## @ngx-translate

@ngx-translate maintains its own version support matrix.

```bash
# Check compatibility: https://github.com/ngx-translate/core#installation
npm install @ngx-translate/core@<compatible>
```

Common version map:

| Angular Version | @ngx-translate/core |
|-----------------|---------------------|
| 16              | 15.x                |
| 17              | 15.x                |
| 18              | 15.x or 16.x        |
| 19–20           | 16.x                |

---

## General Third-Party Audit

After completing all Angular/major-lib upgrades:

```bash
# Check for unmet peer dependencies
npm ls 2>&1 | grep -E "WARN|ERR|UNMET"

# Check for outdated packages (optional — separate task from migration)
npm outdated
```

For any remaining peer dependency warnings:

1. Check the library's GitHub releases for an Angular-compatible version.
2. If no compatible version exists, use `--legacy-peer-deps` and document the exception.
3. Open a tech-debt ticket for libraries with no Angular 20 compatible release.
