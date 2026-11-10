---
name: project-context-scaffold
description: Scaffolds a full "AI-context-first" project directory structure — docs/ (requirements, decisions, architecture, implementation, runbooks, knowledge, open-questions, and a docs/context/ tree covering business-model, data-model, api, frontend, design-system, workflow, skills, and project-memory), plus top-level skills/, prompts/, templates/, memory/, scripts/, and src/ folders. Use this whenever the user wants to initialize a new project's folder layout, set up a docs/context structure for AI-assisted development, bootstrap project documentation conventions, or asks for this specific directory tree by name (e.g. "生成这个项目结构", "scaffold my project docs", "set up docs/context", "init project skeleton with memory and templates"). Always use this instead of manually running mkdir for each folder one at a time — the bundled script creates the entire tree plus starter README.md files and template content in one shot.
---

# Project Context Scaffold

Creates the opinionated project layout below: a `docs/` tree split into normal
project docs and a `docs/context/` subtree meant to give an AI assistant
durable, structured context about the project, plus top-level `skills/`,
`prompts/`, `templates/`, `memory/`, `scripts/`, and `src/` folders.

```
project/
├── docs/
│   ├── requirements/       # PRD, user stories
│   ├── decisions/          # ADRs, design decisions
│   ├── architecture/       # system architecture
│   ├── implementation/     # implementation plans
│   ├── runbooks/           # operational runbooks
│   ├── knowledge/          # general reference knowledge
│   ├── open-questions/     # unresolved questions
│   └── context/            # AI project context
│       ├── business-model/{domains,workflows,glossary.md,terminology.md}
│       ├── data-model/{entities,relationships,enums,examples}
│       ├── api/{rest,graphql,websocket,contracts}
│       ├── frontend/{pages,components,state,routing,charts,ui-patterns}
│       ├── design-system/{colors,typography,spacing,components,interaction}
│       ├── workflow/{business,development,deployment}
│       ├── skills/{chart,angular,testing,git,code-review}
│       └── project-memory/{architecture,business,coding,bug,feature}-memory.md, timeline.md
├── skills/{Angular,TypeScript,RxJS,ECharts,MapLibre,Cytoscape,Git,Azure,Oilfield}
├── prompts/{coding,review,architecture,requirement,documentation}
├── templates/{ADR,Feature,API,Bug,Skill,Decision}.md
├── memory/{conversations,summaries,checkpoints}
├── scripts/
└── src/
```

## How to run it

1. Figure out the target directory. If the user hasn't given a path, default
   to the current working directory or a sensibly-named new folder — don't
   block on asking unless it's genuinely ambiguous.
2. Run the bundled script:

   ```bash
   python3 /mnt/skills/.../project-context-scaffold/scripts/scaffold.py <target_dir> --project-name "<Name>"
   ```

   (Adjust the script path to wherever this skill is mounted.)

3. The script is idempotent — re-running it **skips any file that already
   exists** rather than clobbering it. Pass `--force` only if the user
   explicitly wants existing files overwritten.
4. Report what got created (the script prints a summary). Don't dump the
   full file list into chat — a short summary plus the top-level tree is
   enough; point to the generated README.md files for detail.

## What the script actually produces

Not just empty folders — every folder gets a short `README.md` explaining
what belongs there (so the structure is self-documenting), and these are
pre-populated with real starter content rather than left blank:

- `templates/ADR.md`, `Feature.md`, `API.md`, `Bug.md`, `Skill.md`,
  `Decision.md` — fill-in-the-blank Markdown templates.
- `docs/context/project-memory/*.md` — append-only memory logs
  (architecture, business, coding, bug, feature) plus `timeline.md`, each
  with a dated-entry format ready to append to.
- `docs/context/business-model/glossary.md` and `terminology.md` — starter
  tables/notes.
- A top-level `README.md` summarizing the whole layout.

## Customizing the tree

If the user wants to add/remove/rename folders from the default layout,
edit the `FOLDER_NOTES` dict in `scripts/scaffold.py` (keys are relative
paths, values are the one-line purpose note used to generate that folder's
README) before running it, rather than manually creating folders afterward
— keeps the generated READMEs accurate.

## When NOT to use this

- If the user already has an existing, differently-organized project and
  just wants one new file (e.g. "add an ADR for X") — just create that file
  using the relevant template's format, don't re-scaffold the whole tree.
- If the user wants a technology-specific project scaffold (e.g. "create a
  new Angular app") — that's a different task; this skill only builds the
  documentation/context/memory layout, not application boilerplate.