# DFS Angular Patterns — Logic, Architecture, i18n & HTML

<!-- Source: https://dfs-docs-ds365ai-dfsdev-docs-b57f547be34ca2b58644088b1b6770c1be.gitlab.io/home/code-quality-guardrail/ai-code-governance/instructions/ -->
<!-- Section: 2.9 — GitHub Copilot Full Markdown Template -->
<!-- Rules covered: 3.x (Logic & Bug Prevention) + 4.x (Performance & Architecture) + 5.x (i18n) + 7.x (HTML) -->
<!-- Verified: 2026-05-11 -->

This document is loaded automatically by `/dfs-frontend-review` at invocation. It provides
Angular-specific rules for logic and bug prevention (3.x), performance and architecture
(4.x), internationalization (5.x), and HTML structure and semantics (7.x) — the categories
that separate Angular expert review from generic code review.

---

## 3.x — Logic & Bug Prevention

Apply these rules to every TypeScript file in the review scope.

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 3.2 | Comply with Angular official best practices: change detection, DI, RxJS usage. | High | Components using `ChangeDetectionStrategy.Default` where `OnPush` would apply. Services injected via constructor without `inject()` when the codebase has adopted the `inject()` pattern. RxJS misuse (e.g., nesting `subscribe()` inside `subscribe()`). |
| 3.3 | Audit PrimeNG component usage: lifecycle, event binding, template syntax, performance. | Medium | PrimeNG event handlers bound incorrectly (e.g., `(click)` on a `p-button` instead of `(onClick)`). Lifecycle methods that initialise PrimeNG state outside `ngOnInit`. Large PrimeNG datasets rendered without pagination or virtual scrolling. |
| 3.4 | All manual `subscribe()` calls MUST be unsubscribed using `takeUntilDestroyed` or `takeUntil`. | High | Any `.subscribe()` call in a component without a corresponding `takeUntilDestroyed()` (Angular 16+) or `takeUntil(this.destroy$)` operator in the pipe chain. Services may hold long-lived subscriptions intentionally — flag components only. |
| 3.5 | Do NOT manipulate DOM directly via `document.querySelector`; use `Renderer2` or host bindings. | Critical | Any call to `document.querySelector`, `document.getElementById`, `document.getElementsBy*`, or `ElementRef.nativeElement` used directly to set styles or attributes (not just to read a value). |
| 3.6 | Extract duplicate logic into reusable functions or private methods. | Medium | Identical or near-identical code blocks appearing two or more times in the same file. Logic that belongs in a shared utility or service but is implemented inline. |
| 3.7 | Avoid empty `if` blocks, redundant conditions, or always-true expressions. | Medium | `if (true)`, `if (x === x)`, empty `if () {}` blocks, or conditions that can be statically determined as always-true/always-false. |
| 3.8 | Use `Promise.all` for parallel independent async calls; avoid sequential awaiting. | Medium | Two or more `await` statements for independent async operations placed sequentially inside a single `async` function where `Promise.all([...])` would be equivalent and faster. |
| 3.9 | Prefer `async/await` over deep callback nesting. | Medium | Promise `.then().then().then()` chains more than two levels deep where `async/await` would flatten the logic. |

> **Note on Rule 3.1:** Rule 3.1 covers security vulnerabilities specifically (XSS, injection, unsafe Angular bindings). It is expanded with Angular-specific security patterns in `security-checklist.md` and applied during review step 3 alongside these rules.

---

## Supplementary: RxJS Subscription Management

Rule 3.4 is the most commonly violated Angular rule in DFS codebases. Use this quick reference
when flagging subscription issues:

| Pattern | Status | Notes |
|---------|--------|-------|
| `takeUntilDestroyed()` (Angular 16+) | ✅ Correct | Must be called inside injection context (constructor or field initialiser). |
| `takeUntil(this.destroy$)` + `Subject` | ✅ Correct | Legacy pattern; valid if `this.destroy$.next()` is called in `ngOnDestroy`. |
| `async` pipe in template | ✅ Correct | No unsubscribe needed — Angular manages lifecycle. |
| `.subscribe()` with no unsubscribe | ❌ Flag | Always flag at component level. |
| Nested `.subscribe()` | ❌ Flag | Flag as both a subscription leak and an RxJS anti-pattern (Rule 3.2). Use `switchMap`, `mergeMap`, etc. |

---

## 4.x — Performance & Architecture

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 4.1 | Components MUST follow the Single Responsibility Principle; split overly large "god components". | High | Components exceeding ~400 lines with mixed responsibilities (data fetching, business logic, and display logic all in one class). Multiple unrelated features managed in a single component. |
| 4.2 | Keep implementations simple; avoid over-engineering for basic requirements. | Medium | Unnecessary abstractions, generic factories, or builder patterns introduced for functionality that is used only once and in one place. |

---

## 5.x — Internationalization (i18n)

Apply these rules to TypeScript and HTML files.

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 5.1 | All user-facing text MUST use translation pipes or services; no hardcoded strings. | High | String literals in HTML templates not wrapped in a translation pipe (e.g., `<label>First Name</label>` instead of `<label>{{ 'USER.PROFILE.FIRST_NAME' \| translate }}</label>`). TypeScript code that sets user-visible messages as string literals instead of using `this.translateService.instant(key)`. |
| 5.2 | Translation keys MUST follow a hierarchical pattern: `MODULE.FEATURE.KEY`; avoid vague keys like `text1` or `label`. | Medium | Translation keys using single words, numbers, or non-descriptive names. Keys that do not follow the three-level hierarchy (`MODULE.FEATURE.KEY`). |

---

## 7.x — HTML Structure & Semantics

Apply these rules to every HTML template file in the review scope.

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 7.1 | Use semantic HTML tags wherever appropriate. | Low | `<div>` or `<span>` used as a button or interactive element without `role` attribute. Navigation menus using `<div>` instead of `<nav>`. Page sections using `<div>` where `<section>`, `<article>`, `<header>`, `<footer>`, or `<main>` would be semantically correct. |
| 7.2 | All `<img>` tags MUST include a meaningful `alt` attribute. | High | Any `<img>` without an `alt` attribute, or with `alt=""` when the image conveys information (decorative images may use `alt=""`). `alt` values that are just file names or generic phrases like "image" or "photo". |

---

## Severity Reference Summary

| Severity | Count in this doc | Example rules |
|----------|------------------|---------------|
| Critical | 1 | 3.5 |
| High | 5 | 3.2, 3.4, 4.1, 5.1, 7.2 |
| Medium | 7 | 3.3, 3.6, 3.7, 3.8, 3.9, 4.2, 5.2 |
| Low | 1 | 7.1 |
