# dfs-frontend-review

A GitHub Copilot skill that performs structured code reviews of Angular + PrimeNG frontend
code against the full DFS coding standards (rules 1.x–7.x), producing severity-annotated
findings grouped by file type with actionable fix recommendations.

---

## Usage

Install the skill via the DFS development skills package (see repo root README), then invoke
in GitHub Copilot chat:

```
/dfs-frontend-review [file-path | folder | glob]
```

### Examples

| What you type | What happens |
|---------------|--------------|
| `/dfs-frontend-review` | Skill checks active editor file; if nothing is open, asks what to review |
| `/dfs-frontend-review src/app/user-profile.component.ts` | Reviews `.ts` file + auto-detects sibling `.html` and `.scss` |
| `/dfs-frontend-review src/app/user-profile/` | Reviews all `.ts`, `.html`, and `.scss` files in the folder |
| `/dfs-frontend-review "src/**/*.component.ts"` | Reviews all component TypeScript files matched by the glob |

---

## What the Skill Does

1. **Parses the argument** — uses it as the review scope; falls back to the active editor
   file, then asks if nothing is available
2. **Resolves scope and detects siblings** — for `.ts` input, auto-finds the matching
   `.html` and `.scss` files with the same base name
3. **Reviews TypeScript** — applies naming rules (1.x), code style rules (2.x), and
   Angular logic/bug rules (3.x) + architecture rules (4.x)
4. **Reviews HTML templates** — applies HTML semantics rules (7.x): semantic tags,
   `alt` attributes, template binding issues
5. **Reviews SCSS** — applies styling integrity rules (6.x): inline styles, unscoped
   `::ng-deep`, `!important`, hardcoded hex values
6. **Applies i18n check** — applies rules 5.x across all files: hardcoded user-facing
   strings and malformed translation keys
7. **Assigns severity** — classifies each finding as Critical / High / Medium / Low
8. **Produces the review report** — outputs `【Issue Summary】` + `【Fix Recommendations】`
   grouped by file type (TS / HTML / SCSS)

---

## Companion Documents

The skill loads these reference documents automatically:

| Document | Contents |
|----------|----------|
| `references/code-quality-standards.md` | DFS naming conventions (Rules 1.1–1.6) and TypeScript code style rules (Rules 2.1–2.14) with severity and violation indicators |
| `references/angular-patterns.md` | Angular logic and bug prevention (Rules 3.x), performance and architecture (Rules 4.x), i18n (Rules 5.x), and HTML semantics (Rules 7.x) |
| `references/security-checklist.md` | Security vectors expanded from Rule 3.1 (XSS via `[innerHTML]`, `bypassSecurityTrust*` misuse, unsafe bindings) plus SCSS styling integrity (Rules 6.1–6.5) |

---

## DFS-Specific Coverage

This skill is tuned for DFS Angular + PrimeNG project patterns:

- **PrimeNG event binding:** Flags incorrect event binding syntax (e.g., `(click)` vs `(onClick)`)
  and missing error handling on PrimeNG event exceptions (Rule 2.6)
- **RxJS subscription leaks:** Detects `subscribe()` calls without `takeUntilDestroyed` or
  `takeUntil` — the most common Angular bug in DFS codebases (Rule 3.4)
- **Module encapsulation:** Flags unscoped `::ng-deep` usage that bleeds into global styles
  and prefer-over guidance for PrimeNG `styleClass` / `pt` API (Rules 6.2, 6.3)
- **i18n enforcement:** Detects hardcoded user-facing strings and malformed `MODULE.FEATURE.KEY`
  translation keys (Rules 5.1, 5.2)
- **Security:** Flags `[innerHTML]` XSS vectors and `bypassSecurityTrust*` API misuse with
  Angular sanitisation guidance (Rule 3.1 expanded)

---

## UAT: Quick Test Prompts

Use these to verify the skill is working after installation:

1. `/dfs-frontend-review`
   → Skill should check active editor; if nothing is open, it should ask: *"What file or
   folder do you want to review?"*

2. `/dfs-frontend-review src/app/some-component.component.ts`
   → Skill should report that it is also checking `some-component.component.html` and
   `some-component.component.scss` (sibling detection). Should produce findings grouped
   under **TS**, **HTML**, and **SCSS** headings with `Rule X.X · Line X ·` format.

3. Open a `.ts` file with `let` instead of `const`, a missing JSDoc on a public method,
   and `console.log`. Invoke `/dfs-frontend-review` with no argument.
   → Should surface: Rule 2.1 (Medium), Rule 2.5 (Medium), Rule 2.3 (Low) with line
   numbers and fix recommendations.

---

## Source Reference

DFS Code Quality Guardrail — AI Code Governance Instructions (GitHub Copilot Full Markdown Template, Section 2.9):
https://dfs-docs-ds365ai-dfsdev-docs-b57f547be34ca2b58644088b1b6770c1be.gitlab.io/home/code-quality-guardrail/ai-code-governance/instructions/
