---
name: dfs-angular-upgrade
description: "Guide developers through Angular version migrations step by step"
argument-hint: "<source-version> <target-version> [project-path]"
allowed-tools: Read, Write, Edit, Bash, Agent, AskUserQuestion
---

<objective>
Guide the developer through a complete Angular version migration. This skill
covers framework upgrade commands, version-specific breaking changes, third-party
library compatibility (PrimeNG, NgRx, RxJS, Angular Material), and DFS-specific
patterns for Module Federation projects.
</objective>

<execution_context>
@skills/dfs-angular-upgrade/references/migration-strategy.md
@skills/dfs-angular-upgrade/references/version-breaking-changes.md
@skills/dfs-angular-upgrade/references/dependency-upgrade-checklist.md
</execution_context>

<process>
1. **Parse arguments.** If `<source-version>` or `<target-version>` missing, ask the
   developer. Accept bare integers (16, 20) or prefixed (v16). If source ≥ target,
   report error. If gap > 1 major, confirm incremental vs. big-bang strategy.
2. **Detect project type.** Read `angular.json` and `webpack.config.js`. Determine:
   standalone vs. NgModule app; single project vs. monorepo; Module Federation
   host/remote (look for ModuleFederationPlugin). Note: MF projects need extra steps.
3. **Scope the migration path.** Load version-specific breaking changes from
   `version-breaking-changes.md` for each major hop in the migration range.
4. **Pre-migration checks.** Confirm: upgrade branch created; Node.js version meets
   Angular target requirement; `npm ls` baseline clean.
5. **Execute upgrade per hop.** For each major version hop: (a) run
   `ng update @angular/core@<N> @angular/cli@<N>`; (b) apply version-specific
   breaking-change fixes; (c) resolve peer conflicts; (d) build and fix compilation
   errors before advancing.
6. **Apply third-party upgrades.** Follow `dependency-upgrade-checklist.md` for
   PrimeNG component renames, NgRx, RxJS, Angular Material, and MF-specific config.
7. **Validate.** Run `npm start` and verify app serves. MF projects: confirm
   `remoteEntry.js` builds. Run test suite. Check `npm ls` for clean peer deps.
8. **Report.** Summarise changes made, remaining manual steps, and open warnings.
</process>
