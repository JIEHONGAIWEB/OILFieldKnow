# dfs-angular-upgrade

A GitHub Copilot skill that guides developers through Angular version migrations step by step,
with DFS-specific patterns for Module Federation projects.

---

## Usage

Install the skill via the DFS development skills package (see repo root README), then invoke
in GitHub Copilot chat:

```
/dfs-angular-upgrade <source-version> <target-version> [project-path]
```

### Examples

| What you type                                  | What happens                                                           |
|------------------------------------------------|------------------------------------------------------------------------|
| `/dfs-angular-upgrade`                         | Skill asks for source and target version                               |
| `/dfs-angular-upgrade 16 20`                   | Full incremental migration plan: 16→17→18→19→20                        |
| `/dfs-angular-upgrade v16 v18`                 | Migration plan for 16→17→18                                            |
| `/dfs-angular-upgrade 16 20 ./apps/ongcapp`    | Migration scoped to the specified project path                         |

---

## What the Skill Does

1. **Parses your version arguments** — asks if not provided; validates source < target
2. **Detects project type** — reads `angular.json` and `webpack.config.js` to identify
   Module Federation projects
3. **Scopes the migration path** — loads version-specific breaking changes for each hop
   in your range
4. **Runs pre-migration checks** — confirms branch, Node.js version, clean baseline build
5. **Executes upgrade per hop** — runs `ng update`, applies breaking-change fixes, resolves
   peer conflicts
6. **Applies third-party upgrades** — PrimeNG renames, NgRx alignment, RxJS changes,
   Angular Material
7. **Validates** — builds, starts app, runs tests, confirms `remoteEntry.js` for MF projects
8. **Reports** — summarises all changes, remaining manual steps, and any open warnings

---

## Companion Documents

The skill loads these reference documents automatically:

| Document                          | Contents                                                                                               |
|-----------------------------------|--------------------------------------------------------------------------------------------------------|
| `references/migration-strategy.md`           | Node.js requirements, incremental vs big-bang, `ng update` workflow, MF-specific steps, SCSS migration, pre/post checklists |
| `references/version-breaking-changes.md`     | Per-hop breaking changes for Angular 12→13 through 19→20, PrimeNG component renames, MF warnings      |
| `references/dependency-upgrade-checklist.md` | PrimeNG, NgRx, RxJS, Angular Material, @webframework, @angular-architects/module-federation upgrade steps |

---

## DFS-Specific Coverage

This skill is tuned for DFS project patterns:

- **Module Federation (ONGCAPP):** Extra steps for `@angular-architects/module-federation`,
  webpack config updates, `strictVersion: false`, `ngDevMode` DefinePlugin, `webpack@5.94.0` pin
- **PrimeNG 16/19 → 20:** Full component rename table (Dropdown→Select, Calendar→DatePicker, etc.)
- **@webframework packages:** Alignment guidance for DFS internal packages
- **ONGCAPP path:** Angular 16/PrimeNG 16 → Angular 20/PrimeNG 20 incremental path tested

---

## UAT: Quick Test Prompts

Use these to verify the skill is working after installation:

1. `/dfs-angular-upgrade`
   → Skill should ask: *"What is your current Angular version?"* and *"What version do you want to upgrade to?"*

2. `/dfs-angular-upgrade 16 18`
   → Should produce a 16→17→18 incremental plan including: Node.js check (18.13.x required for 17),
   `ng update` commands per hop, MF webpack warning for 16→17 (ngDevMode DefinePlugin),
   NgRx and PrimeNG upgrade steps.

3. `/dfs-angular-upgrade 19 20`
   → Should include PrimeNG component rename table (Dropdown→Select, Calendar→DatePicker,
   InputSwitch→ToggleSwitch, etc.) and @primeng/themes migration.

---

## Source Reference

DFS internal Angular 20 Migration Guide (read-only reference — MCP functionality not available):
https://dfs-docs-ds365ai-dfsdev-docs-b57f547be34ca2b58644088b1b6770c1be.gitlab.io/home/ai-assistance/development/Angular20-Migration-Guide/
