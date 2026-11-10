---
name: oilfield-project-context
description: >
  Scaffolds an "Oilfield Project Context" directory structure for
  oilfield/petroleum software projects — business-model, data-model, api,
  frontend, design-system, workflow, skill, project-memory, plus
  oilfield-specific additions such as domain-knowledge (covering 石油专业知识
  like drilling, reservoir, production, well-operations, units-and-standards),
  coding-standards, architecture-decision (ADR), feature-history,
  bug-knowledge, performance, testing, deployment, ai-rules, and
  open-questions. Use this whenever the user wants to initialize or
  bootstrap an oilfield project's context/documentation layout, mentions
  "石油项目上下文", "oilfield project context", or asks for this specific
  structure by name. Always use this instead of manually creating folders
  one at a time — the bundled script builds the entire tree with README
  stubs and starter templates in one shot.
---

# Oilfield Project Context Scaffold

Creates a flat, domain-aware AI-context tree for oilfield software projects.
Unlike a generic project scaffold, this bakes in oilfield-specific
categories so an AI assistant working on the codebase has both software
context (data model, API, frontend) and subject-matter grounding (drilling,
reservoir, production) plus project-history categories (ADRs, feature
history, bug knowledge, performance notes) that accumulate over time.

```
<project>/
├── business-model/{domains,workflows,glossary.md,terminology.md}
├── data-model/{entities,relationships,enums,examples}
├── api/{rest,graphql,websocket,contracts}
├── frontend/{pages,components,state,routing,charts,ui-patterns}
├── design-system/{colors,typography,spacing,components,interaction}
├── workflow/{business,development,deployment}
├── skill/{chart,angular,testing,git,code-review}
├── project-memory/{architecture,business,coding,bug,feature}-memory.md, timeline.md
├── domain-knowledge/{drilling,reservoir,production,well-operations,units-and-standards,glossary.md}   ⭐ 石油专业知识
├── coding-standards/            ⭐ 编码规范
├── architecture-decision/       ⭐ ADR (has _template.md)
├── feature-history/             ⭐ 功能演进 (has _template.md)
├── bug-knowledge/               ⭐ Bug 沉淀 (has _template.md)
├── performance/                 ⭐ 性能优化经验 (has _template.md)
├── testing/                     ⭐ 测试策略
├── deployment/                  ⭐ 发布流程
├── ai-rules/                    ⭐ AI 编码规则 (has rules.md)
└── open-questions/              ⭐ 待确认事项
```

## How to run it

1. Determine the target directory (default to cwd or a sensibly-named new
   folder if the user hasn't specified one — don't block on asking).
2. Run the bundled script:

   ```bash
   python3 /mnt/skills/.../oilfield-project-context/scripts/scaffold.py <target_dir> --project-name "<Name>"
   ```

3. Idempotent — re-running **skips existing files**. Only pass `--force` if
   the user explicitly wants overwrites.
4. Report a short summary of what was created (the script prints file
   counts) — don't dump the full file list into chat.

## What gets pre-populated (not just empty folders)

- Every folder gets a `README.md` explaining its purpose (some in Chinese
  where the category is domain-specific, e.g. `domain-knowledge/`).
- `architecture-decision/_template.md`, `feature-history/_template.md`,
  `bug-knowledge/_template.md`, `performance/_template.md` — ready-to-copy
  templates for each of those recurring doc types.
- `project-memory/*.md` — append-only memory logs with a dated-entry format.
- `ai-rules/rules.md` — starter structure for Always / Never / domain-gotcha
  rules an AI assistant should follow (e.g. explicit unit handling, since
  oilfield data mixes metric and imperial units constantly).
- `domain-knowledge/glossary.md` and `business-model/glossary.md` — starter
  glossary tables.
- A top-level `README.md` summarizing the whole layout.

## Customizing

If the user wants different oilfield sub-categories under
`domain-knowledge/` (e.g. adding "seismic" or "HSE"), or wants to
rename/remove a top-level category, edit the `FOLDER_NOTES` dict in
`scripts/scaffold.py` — keys are relative paths, values are the one-line
purpose note used to generate that folder's README — rather than creating
folders manually afterward, so the generated READMEs stay accurate.

## Relationship to the generic project-context-scaffold skill

This is a domain-specialized sibling of the generic `project-context-scaffold`
skill: same underlying idea (AI-context-first project layout), but flatter
(no `docs/` wrapper) and with oilfield-specific categories baked in instead
of generic engineering docs (`docs/requirements`, `docs/runbooks`, etc.). If
the user wants the generic structure instead, use that skill; if they
explicitly want the oilfield-flavored one, use this one.

## When NOT to use this

- If the user already has this structure and just wants one new file (e.g.
  "add an ADR for X") — create that file directly using the relevant
  `_template.md`, don't re-scaffold the whole tree.
- If the user wants an application code scaffold (e.g. "set up a new Angular
  app") — this skill only builds the context/documentation layout, not
  application boilerplate.