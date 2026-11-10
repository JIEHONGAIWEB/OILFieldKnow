# Config-Driven UI — Design Patterns

Design patterns for **config-driven / low-code UI** (Config-Driven UI, low-code
engines). Core idea: **decouple UI structure, behavior and interaction from
hardcoding — drive rendering from declarative config (JSON/DSL).** Guiding
principle throughout: **Open/Closed — put change in the config layer, not the
code layer.**

> Related in this repo: [ADR-0002](../../architecture-decision/0002-data-driven-chart-layering.md)
> (data-driven chart layering, Builder + Registry) and the Production-Method
> KPI pattern in [ui-patterns/README.md](README.md) — both are concrete,
> smaller-scope applications of the patterns below.

## 1. Config-Driven Pattern (foundation)

Externalize page structure, fields, validation and interaction as JSON/DSL; a
render engine reads the config and generates UI dynamically (e.g. Baidu AMIS,
Form Generator).

```json
{ "component": "el-input", "props": { "placeholder": "Name" },
  "rules": [{ "required": true }], "bind": "userName" }
```

Benefit: change UI by editing config, not source; one engine serves many business
scenarios.

## 2. Strategy Pattern

Encapsulate the **axes of variation** (render logic, validation, state behavior) as
interchangeable strategy objects, dispatched by type via a registry.

```js
const renderStrategies = {
  text:   (v) => <span>{v}</span>,
  image:  (v) => <img src={v} />,
  status: (v) => <Tag>{v}</Tag>,
};
const TableCell = ({ value, type }) => renderStrategies[type]?.(value);
```

Use for: table-cell rendering, form validation, state-machine behavior. Adding a
type = registering a new strategy (OCP).

## 3. Factory + Registry (self-registering factory)

A factory creates component instances; a registry enables dynamic extension and
removes if/else branch explosion.

```js
const componentRegistry = new Map();
componentRegistry.set('el-input', InputComponent);
function createComponent(type, props) {
  const Comp = componentRegistry.get(type);
  return Comp ? <Comp {...props} /> : null;
}
```

Advanced: a **self-registering** factory lets each component register itself at
definition time — zero-touch when adding components.

## 4. Renderer Pattern

The renderer bridges **Schema config → real DOM**, usually by recursively parsing
nested config, dynamically loading components, and mounting them.

```
JSON Schema → Parser → Renderer (recursive) → DOM
```

Responsibilities: recursive parsing of nested containers (Vertical/Horizontal/
Grid), dynamic component loading (by `componentName`), props injection & event
binding, and **design-time / runtime separation** (design-time has drag guides;
runtime renders clean).

## 5. Slots / Composition Pattern

Borrowing React `children` / Vue slots, reserve **extension points** inside a
component and inject the variable parts from outside.

```jsx
const ListItem = ({ avatar, title, avatarAddon, titleAddon }) => (
  <div>
    <div className="avatar">{avatar}{avatarAddon}</div>{/* extension point */}
    <div className="title">{title}{titleAddon}</div>   {/* extension point */}
  </div>
);
```

Value: the core component stays stable; customization is injected via slots, no
source edits.

## 6. Metadata-Driven Pattern

Describe a component's Props / Events / Slots / Style with a **JSON Schema** — the
contract between the platform and the render engine.

| Metadata type | Purpose |
| --- | --- |
| Prop Schema | Configurable props and types |
| Event Schema | Supported event hooks |
| Slot Schema | Available slot positions |
| Validation Schema | Validation rules and defaults |

## 7. Decorator Pattern

Layer capabilities (logging, permission, cache, tracking) onto a component without
modifying it.

```js
const PermissionButton = withPermission(Button, 'user:delete');
const LoggedButton = withLogger(PermissionButton, 'click');
```

Use for cross-cutting concerns: permissions, A/B testing, feature flags.

## 8. Observer Pattern

Powers reactive updates and cross-component communication: config change → notify
render engine → partial re-render. Global state (Redux/Zustand/Pinia) is the
engineered form of the observer pattern.

## 9. Abstract Factory Pattern

For multi-theme / multi-platform adaptation, encapsulate creation of a *family* of
related components per factory.

```
AbstractThemeFactory
  ├── LightThemeFactory → createButton / createInput / createDialog
  └── DarkThemeFactory  → createButton / createInput / createDialog
```

Switch theme by swapping the factory instance — zero business-code change.

## 10. Headless Component Pattern

Fully separate **presentation** from **interaction**: presentation is pure
props-driven; behavior is injected via a wrapper.

```
Presentation (pure UI)  ← reused across projects
Registration (Wrapper)  ← injects interaction logic
Business (Page/Hook)    ← state management & API calls
```

## Architecture overview

```
┌──────────────────────────────────────────┐
│           Config layer (JSON/DSL)        │  ← Strategy + Metadata-driven
├──────────────────────────────────────────┤
│           Render engine (Renderer)       │  ← Renderer + recursive parse
├──────────────────────────────────────────┤
│   Component registry + factory           │  ← Factory + Registry
├──────────────────────────────────────────┤
│   Slots / Composition                    │  ← Composition
├──────────────────────────────────────────┤
│   Decorator / permission / feature flag  │  ← Decorator
├──────────────────────────────────────────┤
│   State management / event bus           │  ← Observer
└──────────────────────────────────────────┘
```

## Choosing patterns

| Scenario | Preferred patterns |
| --- | --- |
| Dynamic form / page generation | Config-driven + Renderer + Metadata |
| Multi-platform / multi-theme | Abstract Factory + Strategy |
| Component capability extension | Slots + Decorator |
| Complex interaction switching | Strategy + State machine |
| Cross-component communication | Observer / Event bus |

These patterns are **combined**, not used in isolation — a mature config-driven
frontend is the synergy of several. The constant guiding idea is **Open/Closed:
let change happen in the config layer, not the code.**
