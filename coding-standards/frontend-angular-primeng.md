# Frontend Coding Standards — Angular + PrimeNG

> **Authoritative standard for all frontend code in this project.**
> Applies to every `*.ts`, `*.html`, `*.scss` change under the frontend app
> (`wpo-app`, see [../frontend/README.md](../frontend/README.md)). All frontend
> code — whether written by a human or an AI assistant — MUST comply with these
> rules. Use them both when authoring new code and when reviewing changes.

Role context: act as a senior Angular architect with deep PrimeNG expertise.
Apply the rules strictly, precisely, and constructively.

## 1. Naming Conventions

- 1.1 File names for components, services, etc. MUST use kebab-case
  (e.g. `user-profile.component.ts`).
- 1.2 A component's TS, HTML, and SCSS files MUST share the same base name.
- 1.3 Classes, interfaces, types, enums, components, directives, pipes,
  services, and modules MUST use PascalCase.
- 1.4 Variables, functions, and method parameters MUST use camelCase.
- 1.5 Constants MUST use UPPER_SNAKE_CASE.
- 1.6 All names MUST be semantic and business-relevant.

## 2. Code Style & TypeScript Rules

- 2.1 Use `const` by default; use `let` only if reassignment is required.
  Never use `var`.
- 2.2 Prohibit `any`. Use specific types or `unknown` instead.
- 2.3 Prohibit `console.log` / `debugger` in production code.
- 2.4 All functions MUST explicitly declare a return type.
- 2.5 All public methods MUST have complete JSDoc comments.
- 2.6 All HTTP requests and PrimeNG event exceptions MUST be caught and
  properly notified to users.
- 2.7 Use enums for fixed status/type values; prohibit magic strings or
  magic numbers.
- 2.8 All complex objects MUST use an explicit `interface` or `type`;
  inline untyped objects are prohibited.
- 2.9 Prohibit empty `catch` blocks; errors MUST be handled or re-thrown.
- 2.10 Remove all unused imports, variables, parameters, and dead code.
- 2.11 Remove large commented-out code blocks; rely on Git for history.
- 2.12 Use strict equality `===` instead of `==`.
- 2.13 Add debounce for frequent submit/click events to prevent duplicate
  requests.
- 2.14 Use optional chaining `?.` and nullish coalescing `??` to avoid
  NPE risks.

## 3. Logic & Bug Prevention

- 3.1 Identify bugs, performance risks, maintainability issues, and security
  vulnerabilities.
- 3.2 Comply with Angular official best practices: change detection, DI,
  RxJS usage.
- 3.3 Audit PrimeNG component usage: lifecycle, event binding, template
  syntax, performance.
- 3.4 All manual `subscribe()` calls MUST be unsubscribed using
  `takeUntilDestroyed` or `takeUntil`.
- 3.5 Do NOT manipulate the DOM directly via `document.querySelector`;
  use `Renderer2` or host bindings.
- 3.6 Extract duplicate logic into reusable functions or private methods.
- 3.7 Avoid empty `if` blocks, redundant conditions, or always-true
  expressions.
- 3.8 Use `Promise.all` for parallel independent async calls; avoid
  sequential awaiting.
- 3.9 Prefer `async/await` over deep callback nesting.

## 4. Performance & Architecture

- 4.1 Components MUST follow the Single Responsibility Principle; split
  overly large "god components".
- 4.2 Keep implementations simple; avoid over-engineering basic requirements.

## 5. Internationalization (i18n)

- 5.1 All user-facing text MUST use translation pipes or services; no
  hardcoded strings.
- 5.2 Translation keys MUST follow a hierarchical pattern: `MODULE.FEATURE.KEY`;
  avoid vague keys like `text1` or `label`.

## 6. Styling (SCSS/CSS)

- 6.1 Prohibit inline static styles; extract all styles into style sheets.
- 6.2 When using `::ng-deep`, always scope with `:host` to prevent global
  style pollution.
- 6.3 Minimize `::ng-deep`; prefer PrimeNG's `styleClass`, `pt`, or CSS
  variables.
- 6.4 Prohibit `!important`.
- 6.5 Use theme color variables instead of hardcoded hex values.

## 7. HTML Structure & Semantics

- 7.1 Use semantic HTML tags wherever appropriate.
- 7.2 All `<img>` tags MUST include a meaningful `alt` attribute.

## 8. Code Organization (复杂功能的分组与分布)

适用于**功能复杂**的文件/模块(条目多、职责杂、config/builder/导出项多)。简单文件无需强行分组。

- 8.1 复杂功能 MUST 按职责**分组**,同一组的代码放在一起,不要按"想到什么写什么"的顺序堆叠。
- 8.2 每个分组 MUST 有一行**中文分组注释**作为标题,例如
  `// ==================== 常量与枚举 ====================`。
- 8.3 默认分组顺序(可按实际裁剪,但相对顺序保持一致):
  类型/接口 → 枚举与常量 → 配置 → 工具/纯函数 → 核心逻辑(类/服务/Builder)→ 导出。
- 8.4 **导出顺序**与分组顺序一致,同类导出相邻;对外导出(`export` / barrel `index.ts`)集中管理,
  不在文件中间零散穿插。
- 8.5 注释使用**中文**,说明"做什么 / 为什么",不复述代码字面含义。
- 8.6 **新增或修改的部分 MUST 同步补充中文注释**,并放入所属分组,不得追加在文件末尾了事。
- 8.7 过大的文件按分组拆分到多个文件(分布),各文件职责单一;拆分后用 `index.ts` 统一导出。
- 8.8 整理仅调整**顺序、分组与注释**,不得改动逻辑与行为;整理与功能变更分开提交。

## Review Output Format

When performing a code review against these rules, output in this format:

### 【Issue Summary】

List each violation as:

`Rule X.X · Line X · Issue description (clear and concise)`

### 【Fix Recommendations】

Provide directly copyable code examples for each issue, grouped by file
type (TS / HTML / SCSS).

Additional review rules:

- Review only against the standards above; do not add subjective opinions.
- Be strict, precise, and constructive.
- Do not explain basic concepts; focus on issues and actionable fixes.
- If no code is provided, ask the user to paste the code to be reviewed.
