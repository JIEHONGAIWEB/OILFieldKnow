# DFS Security & SCSS Integrity Checklist

<!-- Source: https://dfs-docs-ds365ai-dfsdev-docs-b57f547be34ca2b58644088b1b6770c1be.gitlab.io/home/code-quality-guardrail/ai-code-governance/instructions/ -->
<!-- Section: 2.9 — Rule 3.1 expanded; Section 6.x SCSS rules -->
<!-- Scope: Security vectors (Rule 3.1) + SCSS styling integrity (Rules 6.x) -->
<!-- Verified: 2026-05-11 -->

This document is loaded automatically by `/dfs-frontend-review` at invocation. It covers
two "no hidden damage" concern categories: security vulnerabilities expanded from Rule 3.1
(XSS vectors, injection risks, and unsafe Angular bindings) and SCSS styling integrity from
rules 6.x (patterns that cause unintended global style side effects or maintainability debt).

Apply this document during review steps 3 (TypeScript) and 5 (SCSS).

---

## Rule 3.1 — Security Vulnerabilities (Critical)

**Verbatim statement:** *Identify bugs, performance risks, maintainability issues, and
security vulnerabilities.*

Rule 3.1's security aspect is expanded below into concrete Angular + PrimeNG attack
vectors. Security findings are always **Critical** severity. Findings are report-only —
do not auto-apply fixes.

### 3.1a — XSS via `[innerHTML]` Binding

| Vector | What to Flag | Why It's Dangerous |
|--------|-------------|-------------------|
| `[innerHTML]="userContent"` | Any binding of user-controlled or API-sourced data to `[innerHTML]` without sanitisation. | Angular does NOT sanitise `innerHTML` bindings automatically — unescaped HTML is injected directly into the DOM, enabling XSS attacks. |
| `this.el.nativeElement.innerHTML = value` | Direct assignment to `.innerHTML` via `ElementRef`. | Same risk as template binding — bypasses Angular's security model entirely. |

**Safe pattern:**
```typescript
// Use DomSanitizer for trusted HTML only — and only when truly necessary
import { DomSanitizer } from '@angular/platform-browser';

constructor(private sanitizer: DomSanitizer) {}

getSafeHtml(html: string): SafeHtml {
  return this.sanitizer.sanitize(SecurityContext.HTML, html) ?? '';
}
```

### 3.1b — `bypassSecurityTrust*` API Misuse

| Method | What to Flag | Guidance |
|--------|-------------|---------|
| `bypassSecurityTrustHtml(value)` | Called with user-supplied or API-sourced `value`. | Flag unless `value` is a compile-time constant or a hardcoded template string. |
| `bypassSecurityTrustScript(value)` | Any usage. | Always flag — there is almost never a legitimate reason to bypass script trust in an Angular app. |
| `bypassSecurityTrustUrl(value)` | Called with user-supplied URLs. | Flag unless the URL is validated against an allowlist before calling. |
| `bypassSecurityTrustResourceUrl(value)` | Called with user-supplied URLs. | Same as above — especially dangerous for `<iframe>` and `<script src>`. |
| `bypassSecurityTrustStyle(value)` | Called with user-supplied style strings. | Flag — CSS injection can exfiltrate data or redirect users. |

**Rule:** Every call to a `bypassSecurityTrust*` method MUST have a code comment
explaining why it is necessary and what input validation guarantees safety. Flag any
call without such justification.

### 3.1c — Unsafe Angular Bindings Summary

| Binding | Status | Notes |
|---------|--------|-------|
| `{{ interpolation }}` | ✅ Safe | Angular escapes by default. |
| `[attr]="value"` | ✅ Safe (most) | Angular validates attribute context. |
| `[innerHTML]="value"` | ⚠️ Flag | Only safe with `DomSanitizer.sanitize()` output. |
| `[href]="value"` | ⚠️ Flag if dynamic | Flag dynamic URLs not validated against allowlist. |
| `[src]="value"` | ⚠️ Flag if dynamic | Same as `[href]`. |
| `bypassSecurityTrust*` | ❌ Always flag | Requires explicit justification comment. |
| Direct `.innerHTML =` | ❌ Always flag | No Angular security context — raw DOM injection. |

---

## 6.x — SCSS/CSS Styling Integrity

Apply these rules to every SCSS file in the review scope.

| Rule | Statement | Severity | What to Flag |
|------|-----------|----------|--------------|
| 6.1 | Prohibit inline static styles; extract all styles into style sheets. | Critical | Any `style="..."` attribute in HTML templates with static values (not Angular style bindings). TypeScript code that sets `element.style.*` properties for static visual styling (not dynamic state-driven styles). |
| 6.2 | When using `::ng-deep`, always scope with `:host` to prevent global style pollution. | Critical | Any `::ng-deep` selector that is NOT immediately preceded by `:host`. Example: `::ng-deep .p-button { }` must become `:host ::ng-deep .p-button { }`. |
| 6.3 | Minimize `::ng-deep`; prefer PrimeNG's `styleClass`, `pt`, or CSS variables. | Medium | Any `::ng-deep` usage where the PrimeNG component offers a `styleClass` input, `pt` (pass-through) API, or an exposed CSS variable (`--primary-color`, etc.) as an alternative. |
| 6.4 | Prohibit `!important`. | High | Any `!important` declaration in SCSS files. There are no legitimate exceptions in DFS code — specificity issues must be resolved through proper selector scoping. |
| 6.5 | Use theme color variables instead of hardcoded hex values. | Medium | Any hardcoded hex colour values (e.g., `color: #1a73e8`, `background: #fff`) where a PrimeNG theme variable or DFS design token should be used instead. |

### PrimeNG Alternatives to `::ng-deep` (Rule 6.3 Reference)

When flagging 6.3, suggest the specific PrimeNG alternative:

| Instead of `::ng-deep` on... | Use instead |
|------------------------------|-------------|
| PrimeNG component root class | `styleClass` input property |
| PrimeNG internal elements | `pt` (pass-through) API |
| Colour / spacing tokens | CSS variables (`var(--primary-color)`, `var(--surface-ground)`, etc.) |
| PrimeNG theme customisation | `themes/` overrides in SCSS via PrimeNG theme API |

---

## Severity Reference Summary

| Severity | Count in this doc | Example violations |
|----------|------------------|-------------------|
| Critical | 3 | 3.1a–c (XSS / unsafe bindings), 6.1 (inline styles), 6.2 (unscoped `::ng-deep`) |
| High | 1 | 6.4 (`!important`) |
| Medium | 2 | 6.3 (unnecessary `::ng-deep`), 6.5 (hardcoded hex) |
