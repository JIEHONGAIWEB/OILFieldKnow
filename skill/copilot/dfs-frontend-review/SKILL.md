---
name: dfs-frontend-review
description: "Review Angular/PrimeNG frontend code against DFS coding standards"
argument-hint: "[file-path | folder | glob]"
allowed-tools: Read, Write, Edit, Bash, Agent, AskUserQuestion
---

<objective>
Perform a strict, structured code review of Angular + PrimeNG frontend code against the
full DFS coding standards (rules 1.x–7.x). The skill checks TypeScript, HTML templates,
and SCSS files for naming violations, code style issues, logic bugs, performance and
architecture problems, i18n gaps, and styling anti-patterns — then outputs structured
findings with actionable fix recommendations.

This skill is for **code quality governance**, not for Angular migration (use
`/dfs-angular-upgrade` for that). Invoke it on any `.ts`, `.html`, or `.scss` file,
a folder, or a glob pattern to get severity-annotated findings grouped by file type.
</objective>

<execution_context>
@skills/dfs-frontend-review/references/code-quality-standards.md
@skills/dfs-frontend-review/references/angular-patterns.md
@skills/dfs-frontend-review/references/security-checklist.md
</execution_context>

<process>
1. **Parse argument.** If `[file-path | folder | glob]` is provided, use it as the review
   scope. If no argument is given, check whether the user has a file or code block active
   in the editor and use that. If nothing is active, ask: "What file or folder do you want
   to review?"
2. **Resolve scope and detect siblings.** Expand the argument to a list of files to review.
   If a `.ts` file is in scope, automatically check for sibling `.html` and `.scss` files
   with the same base name (e.g., `user-profile.component.ts` → look for
   `user-profile.component.html` and `user-profile.component.scss`). Include them if found.
3. **Review TypeScript files.** Apply rules 1.x (naming conventions) from
   `code-quality-standards.md` and rules 2.x (code style) from `code-quality-standards.md`.
   Then apply rules 3.x (logic and bug prevention) and 4.x (performance and architecture)
   from `angular-patterns.md`. Note the exact line number for every violation found.
4. **Review HTML template files.** Apply rules 7.x (HTML structure and semantics) from
   `angular-patterns.md`. Flag missing `alt` attributes, non-semantic tags, and template
   binding issues. Note the line number for every violation.
5. **Review SCSS files.** Apply rules 6.x (SCSS/CSS styling) from `security-checklist.md`.
   Flag inline styles, unscoped `::ng-deep`, `!important`, and hardcoded hex values.
6. **Apply i18n check across all files.** Apply rules 5.x (internationalization) from
   `angular-patterns.md`. Flag hardcoded user-facing strings in TypeScript and HTML, and
   translation keys that do not follow the `MODULE.FEATURE.KEY` hierarchy.
7. **Assign severity to each finding.** Use four tiers — **Critical**, **High**,
   **Medium**, **Low** — guided by the following:
   - **Critical** — Security vulnerabilities, unscoped style pollution, direct DOM manipulation (e.g., Rule 3.1, Rule 6.2 without `:host` scope, Rule 3.5).
   - **High** — Runtime bugs, subscription leaks, broken type safety (e.g., Rule 3.4, Rule 2.2 `any`, Rule 2.6 uncaught HTTP errors).
   - **Medium** — Code quality and maintainability issues, dead code (e.g., Rule 2.10, Rule 2.9 empty `catch`, Rule 3.6 DRY).
   - **Low** — Naming, style, and comment cleanup (e.g., Rules 1.x, Rule 2.3 `console.log`, Rule 2.11 commented code).
8. **Produce the review report.** Output findings strictly in this format — grouped by
   file type (TS / HTML / SCSS):

   ```
   【Issue Summary】
   Rule X.X · Line X · Issue description (clear and concise)

   【Fix Recommendations】
   Provide directly copyable code examples for each issue.
   Group fixes by file type (TS / HTML / SCSS).
   ```

   Only report violations against the DFS standards defined in the companion docs — no
   subjective opinions. Be strict, precise, and constructive. Do not explain basic
   concepts; focus on issues and actionable fixes. If no violations are found in a
   category, state "No issues found" for that section.
</process>
