# Angular Migration Strategy

Reference source: https://dfs-docs-ds365ai-dfsdev-docs-b57f547be34ca2b58644088b1b6770c1be.gitlab.io/home/ai-assistance/development/Angular20-Migration-Guide/
Note: MCP-related content in that guide does not function — treat it as a git project reference only.

---

## Node.js Version Requirements

| Angular Version | Minimum Node.js |
|-----------------|-----------------|
| 12              | 12.14.x         |
| 13              | 12.20.x         |
| 14              | 14.15.x         |
| 15              | 14.20.x         |
| 16              | 16.14.x         |
| 17              | 18.13.x         |
| 18              | 18.19.x         |
| 19              | 18.19.x         |
| 20              | 18.19.x         |

Before starting any migration, confirm your Node.js version meets the target requirement:

```bash
node --version
```

Use nvm to switch versions if needed:

```bash
nvm install 18 && nvm use 18
```

---

## Incremental vs. Big-Bang Strategy

### DFS Recommendation: Incremental

DFS projects (especially ONGCAPP) use an **incremental migration** — one major version at a time.

| Approach | When to Use | Risk |
|----------|-------------|------|
| Incremental (one hop) | Default for all DFS projects | Low — compiler catches each breaking change before the next hop |
| Big-bang (multiple hops) | Only for simple apps with no MF, no PrimeNG | High — compound breaking changes are difficult to diagnose |

**Incremental rule:** Always upgrade from N to N+1, validate fully (build passes, tests pass, app runs), then proceed to N+2.

---

## ng update Workflow

### Standard Upgrade Command

For each major version hop:

```bash
# Upgrade Angular core and CLI together
ng update @angular/core@<TARGET> @angular/cli@<TARGET>

# Example: upgrading to Angular 18
ng update @angular/core@18 @angular/cli@18
```

`ng update` will:
- Update `package.json` versions
- Run automatic code migrations (schematics)
- Report any migrations it could not apply automatically

### What ng update Auto-Fixes

- Constructor injection → `inject()` call migration (Angular 14+)
- `TestBed.inject` migration
- `Router` API updates
- Some decorator changes

### What ng update Does NOT Fix

- PrimeNG component renames (manual — see `dependency-upgrade-checklist.md`)
- SCSS `@import` → `@use` migrations
- Custom webpack config for Module Federation
- Third-party library peer dependencies
- TypeScript version conflicts

### Handling Peer Dependency Conflicts

If `ng update` fails due to peer dependency conflicts:

```bash
# Option 1: Force update (use with caution)
ng update @angular/core@<N> @angular/cli@<N> --force

# Option 2: Legacy peer deps mode
npm install --legacy-peer-deps
```

After either option, run:

```bash
npm ls 2>&1 | grep -E "WARN|ERR"
```

Resolve any `UNMET PEER DEPENDENCY` warnings before proceeding to the next hop.

---

## DFS Angular 16 → 20 Path (ONGCAPP)

The ONGCAPP project migrated from Angular 16/PrimeNG 16 to Angular 20/PrimeNG 20.

### Hop Sequence

1. 16 → 17
2. 17 → 18
3. 18 → 19
4. 19 → 20

Run full validation (build + start + tests) after each hop.

### TypeScript Configuration for Angular 20

After reaching Angular 20, update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "lib": ["es2022"]
  }
}
```

---

## Module Federation–Specific Steps

ONGCAPP and other DFS apps use `@angular-architects/module-federation` with webpack.
MF projects need additional steps at each hop.

### Version Compatibility

| Angular Version | @angular-architects/module-federation |
|-----------------|---------------------------------------|
| 16              | 16.x                                  |
| 17              | 17.x (stay on webpack builder — see warning in version-breaking-changes.md) |
| 18              | 18.x                                  |
| 19              | 19.x                                  |
| 20              | 18.x or compatible                    |

### webpack Version Pin

Pin webpack to 5.94.0 to avoid compatibility issues with Angular's build tools:

```json
// package.json
{
  "overrides": {
    "webpack": "5.94.0"
  }
}
```

### webpack.config.js — Key Changes

#### strictVersion → false (all versions)

In your MF config, set `strictVersion: false` on all shared dependencies to prevent
runtime version mismatch errors:

```javascript
shared: share({
  "@angular/core": { singleton: true, strictVersion: false, requiredVersion: "auto" },
  "@angular/common": { singleton: true, strictVersion: false, requiredVersion: "auto" },
  // ... all other angular packages
})
```

#### ngDevMode DefinePlugin (Angular 17+)

Add this to your webpack `plugins` array to prevent build errors:

```javascript
new webpack.DefinePlugin({
  ngDevMode: JSON.stringify(false)
})
```

#### Expand shared deps (Angular 18+)

Explicitly share all `@angular/*` packages used in your app. Check your imports and add
missing entries to the `shared` map.

### Confirming remoteEntry.js Builds

After each hop for MF projects:

```bash
# Verify remote entry builds successfully
npm run build -- --configuration=production

# Check the output directory for remoteEntry.js
ls dist/*/remoteEntry.js
```

---

## SCSS @import → @use Migration

Angular 17+ warns about deprecated `@import`. Angular 20 may error on them.

### Migration Pattern

**Before:**
```scss
@import 'variables';
@import '~primeng/resources/themes/lara-light-blue/theme.css';
```

**After:**
```scss
@use 'variables' as *;
// For PrimeNG themes: switch to new theme package (see dependency-upgrade-checklist.md)
```

Run `ng update` first — it will migrate many cases automatically.

---

## Pre-Migration Checklist

Before starting any migration:

- [ ] Create a dedicated upgrade branch: `git checkout -b upgrade/angular-<N>-to-<M>`
- [ ] Confirm Node.js version meets the target Angular requirement (see table above)
- [ ] Run `npm ls` — baseline should have no `WARN` or `UNMET PEER DEPENDENCY`
- [ ] Run `npm run build` — baseline build must pass
- [ ] Run `npm test` — baseline tests must pass
- [ ] Note current `@angular-architects/module-federation` version (if applicable)
- [ ] Note current PrimeNG version (if applicable)

---

## Post-Migration Checklist

After completing all hops:

- [ ] `npm run build` passes without errors
- [ ] `npm start` serves the app successfully
- [ ] `npm test` — all tests pass (or failures are documented/unrelated to migration)
- [ ] `npm ls` — no `UNMET PEER DEPENDENCY` warnings
- [ ] MF projects: `remoteEntry.js` present in build output
- [ ] PrimeNG component renames applied (see `dependency-upgrade-checklist.md`)
- [ ] `tsconfig.json` updated per Angular 20 requirements (if migrating to 20)
- [ ] SCSS `@import` warnings resolved
- [ ] PR description documents each hop taken and any manual fixes applied
