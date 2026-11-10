# DFS Code Quality Standards — Naming Conventions & TypeScript Code Style

<!-- Source: https://dfs-docs-ds365ai-dfsdev-docs-b57f547be34ca2b58644088b1b6770c1be.gitlab.io/home/code-quality-guardrail/ai-code-governance/instructions/ -->
<!-- Section: 2.9 — GitHub Copilot Full Markdown Template -->
<!-- Rules covered: 1.x (Naming Conventions) + 2.x (Code Style & TypeScript Rules) -->
<!-- Verified: 2026-05-11 -->

This document is loaded automatically by `/dfs-frontend-review` at invocation. It provides
the authoritative DFS naming convention rules (1.x) and TypeScript code style rules (2.x)
with severity assignments and Angular-specific violation indicators used during review steps
3 and 4.

---

## 1.x — Naming Conventions

Apply these rules to every TypeScript, HTML, and SCSS file in the review scope.

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 1.1 | File names for components, services, etc., MUST use kebab-case (e.g., `user-profile.component.ts`). | Low | Any file using camelCase, PascalCase, or underscores (e.g., `UserProfile.component.ts`, `user_profile.service.ts`). |
| 1.2 | A component's TS, HTML, and SCSS files MUST share the same base name. | Low | Mismatched base names across the three files of the same component (e.g., `user.component.ts` paired with `user-profile.component.html`). |
| 1.3 | Classes, interfaces, types, enums, components, directives, pipes, services, modules MUST use PascalCase. | Low | Any class/interface/type/enum declared with camelCase, kebab-case, or ALL_CAPS naming (e.g., `class userProfileService`). |
| 1.4 | Variables, functions, method parameters MUST use camelCase. | Low | Any local variable, function name, or parameter using PascalCase, UPPER_SNAKE_CASE, or kebab-style names (not applicable in TS, but flag `const UserName`, `function GetUser()`). |
| 1.5 | Constants MUST use UPPER_SNAKE_CASE. | Low | `const` declarations that represent fixed values but use camelCase (e.g., `const maxRetries = 3` where it is a fixed constant, not a computed variable). |
| 1.6 | All names MUST be semantic and business-relevant. | Low | Names like `data`, `temp`, `obj`, `val`, `x`, `item` with no business context; single-letter variables outside loop indices; abbreviations with no obvious meaning. |

---

## 2.x — Code Style & TypeScript Rules

Apply these rules to every TypeScript file in the review scope. These rules are enforced
in code review — they are not treated as "build concern only" (see D-10 in CONTEXT.md).

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 2.1 | Use `const` by default; use `let` only if reassignment is required. Never use `var`. | Medium | Any `var` declaration. Any `let` declaration where the variable is never reassigned after initialisation. |
| 2.2 | Prohibit `any`. Use specific types or `unknown` instead. | High | Any explicit `: any` type annotation. Implicit `any` in function signatures without a return type. |
| 2.3 | Prohibit `console.log` / `debugger` in production code. | Low | Any `console.log(`, `console.warn(`, `console.error(` or `debugger` statement left in non-test code. |
| 2.4 | All functions MUST explicitly declare a return type. | High | Any function or method missing a `: ReturnType` annotation (e.g., `getUser() {` without `: User` or `: Observable<User>`). |
| 2.5 | All public methods MUST have complete JSDoc comments. | Medium | Any `public` method lacking a `/** ... */` JSDoc block above it. Incomplete JSDoc (missing `@param` or `@returns`) also qualifies. |
| 2.6 | All HTTP requests and PrimeNG event exceptions MUST be caught and properly notified to users. | High | `HttpClient` calls without a `.catch()` or `catchError()` operator. PrimeNG event handlers that do not surface errors to the user via a notification service or toast. |
| 2.7 | Use enums for fixed status/type values; prohibit magic strings or magic numbers. | Medium | String literals used as status flags (e.g., `if (status === 'active')`). Numeric literals used as business values (e.g., `if (role === 2)`). Use an `enum` or `const` with a named export instead. |
| 2.8 | All complex objects MUST use explicit `interface` or `type`; inline untyped objects are prohibited. | High | Function parameters typed as `{}` or `object`. Response mapping to untyped inline objects (e.g., `const user = { name: data.name }` without a `User` interface). |
| 2.9 | Prohibit empty `catch` blocks; errors must be handled or re-thrown. | Medium | Any `catch (e) {}` or `catch (e) { // TODO }` with no meaningful error handling. |
| 2.10 | Remove all unused imports, variables, parameters, and dead code. | Medium | Imported symbols never referenced in the file. Variables declared but never read. Dead conditional branches that can never be reached. |
| 2.11 | Remove large commented-out code blocks; rely on Git for history. | Low | Blocks of 3+ consecutive commented-out lines that represent old implementation code. Single-line inline comments explaining the current code are acceptable. |
| 2.12 | Use strict equality `===` instead of `==`. | Medium | Any `==` or `!=` operator (excluding TypeScript type-narrowing contexts where `=== null` is already handled). |
| 2.13 | Add debounce for frequent submit/click events to prevent duplicate requests. | High | Click or submit handlers on buttons or form controls that trigger HTTP requests without a debounce, `disabled` guard, or loading state to prevent double submission. |
| 2.14 | Use optional chaining `?.` and nullish coalescing `??` to avoid NPE risks. | High | Manual null checks using `if (x && x.y)` or `x !== null && x !== undefined` where `x?.y` or `x ?? defaultValue` would be cleaner and safer. |

---

## Severity Reference Summary

| Severity | Count in this doc | Example rules |
|----------|------------------|---------------|
| High | 6 | 2.2, 2.4, 2.6, 2.8, 2.13, 2.14 |
| Medium | 6 | 2.1, 2.5, 2.7, 2.9, 2.10, 2.12 |
| Low | 8 | 1.1–1.6, 2.3, 2.11 |
