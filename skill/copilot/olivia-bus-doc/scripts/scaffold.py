#!/usr/bin/env python3
"""
Scaffold an "AI-context-first" project skeleton.

Usage:
    python3 scaffold.py <target_dir> [--project-name NAME] [--force]

Creates the full docs/context + skills/prompts/templates/memory/scripts/src
layout described in the project-context-scaffold skill, with a short
README.md in every leaf folder explaining what belongs there, and starter
content in templates/ so the tree is usable immediately instead of just
being empty folders.

Safe to re-run: existing files are never overwritten unless --force is passed.
"""
import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Folder -> short purpose note (used to generate a README.md stub per folder)
# ---------------------------------------------------------------------------
FOLDER_NOTES = {
    "docs": "Human- and AI-facing project documentation, organized by purpose rather than by team.",
    "docs/requirements": "PRDs, user stories, acceptance criteria. What we're building and why.",
    "docs/decisions": "Architecture Decision Records (ADRs) and other design-decision write-ups. One file per decision, immutable once accepted.",
    "docs/architecture": "System architecture: diagrams, component boundaries, data flow, deployment topology.",
    "docs/implementation": "Concrete implementation plans/notes for specific features or subsystems (the 'how', once the 'what' and 'why' are settled).",
    "docs/runbooks": "Operational runbooks: deploy steps, incident response, on-call procedures.",
    "docs/knowledge": "General reference knowledge that doesn't fit elsewhere (domain background, external system notes, research notes).",
    "docs/open-questions": "Tracked unresolved questions/spikes. Move a file out once it's answered (into decisions/ or knowledge/).",

    "docs/context": "AI project context root. Everything here exists to give an AI assistant durable, structured context about the project so it doesn't have to re-derive it every session.",

    "docs/context/business-model": "What the business/domain actually is: entities, workflows, vocabulary.",
    "docs/context/business-model/domains": "One file per business domain/bounded context, describing its responsibility and boundaries.",
    "docs/context/business-model/workflows": "Business process write-ups (as opposed to software workflows) — who does what, in what order, why.",

    "docs/context/data-model": "The data model of the system: entities, relationships, enums, and representative examples.",
    "docs/context/data-model/entities": "One file per core entity: fields, invariants, lifecycle.",
    "docs/context/data-model/relationships": "How entities relate to each other (cardinality, ownership, cascade rules).",
    "docs/context/data-model/enums": "Enumerations/status codes and their meaning, kept separate so they're easy to grep.",
    "docs/context/data-model/examples": "Representative example payloads/records for entities, useful as few-shot context for an AI.",

    "docs/context/api": "API surface documentation, split by protocol.",
    "docs/context/api/rest": "REST endpoints: routes, methods, request/response shapes.",
    "docs/context/api/graphql": "GraphQL schema notes: types, queries, mutations, subscriptions.",
    "docs/context/api/websocket": "WebSocket/real-time channel documentation: events, payloads, connection lifecycle.",
    "docs/context/api/contracts": "Cross-cutting API contracts/shared schemas consumed by multiple protocols or services.",

    "docs/context/frontend": "Frontend-specific context: what exists, how it's structured, and the conventions in use.",
    "docs/context/frontend/pages": "One file per page/route: purpose, key components, data dependencies.",
    "docs/context/frontend/components": "Shared component documentation: props, variants, usage guidance.",
    "docs/context/frontend/state": "State management notes: stores, selectors, ownership boundaries.",
    "docs/context/frontend/routing": "Routing structure, guards, and navigation conventions.",
    "docs/context/frontend/charts": "Charting/visualization conventions and library-specific notes (e.g. ECharts config patterns).",
    "docs/context/frontend/ui-patterns": "Recurring UI/interaction patterns (forms, tables, modals, empty/error states) so new work stays consistent.",

    "docs/context/design-system": "Visual design language, kept separate from component implementation.",
    "docs/context/design-system/colors": "Color palette and usage rules (semantic color tokens, when to use which).",
    "docs/context/design-system/typography": "Type scale, font families, weight/usage rules.",
    "docs/context/design-system/spacing": "Spacing scale and layout grid rules.",
    "docs/context/design-system/components": "Design-level (not code-level) component specs: states, sizes, anatomy.",
    "docs/context/design-system/interaction": "Motion, transitions, and interaction/feedback conventions.",

    "docs/context/workflow": "Process documentation split by audience: business, development, deployment.",
    "docs/context/workflow/business": "Business-facing process flows (approvals, review cycles, escalation paths).",
    "docs/context/workflow/development": "Dev workflow: branching model, code review process, release cadence.",
    "docs/context/workflow/deployment": "Deployment/release process: environments, pipelines, rollback procedure.",

    "docs/context/skills": "Project-specific 'how we do X here' notes, one subfolder per topic — narrower and more project-specific than the top-level /skills directory.",
    "docs/context/skills/chart": "Project conventions for building charts (library choice, theming, data-shape expectations).",
    "docs/context/skills/angular": "Project-specific Angular conventions (module structure, DI patterns, naming).",
    "docs/context/skills/testing": "Testing conventions: frameworks, coverage expectations, fixture patterns.",
    "docs/context/skills/git": "Git conventions: commit message format, branch naming, PR process.",
    "docs/context/skills/code-review": "Code review checklist and standards specific to this project.",

    "docs/context/project-memory": "Rolling, append-friendly memory files an AI assistant should read at the start of a session and update at the end.",

    "skills": "Reusable, technology-scoped skill packs (Angular, TypeScript, RxJS, etc.) that could in principle be shared across projects.",
    "skills/Angular": "Angular-specific patterns, gotchas, and house conventions.",
    "skills/TypeScript": "TypeScript conventions and idioms used in this codebase.",
    "skills/RxJS": "RxJS patterns and anti-patterns in use here.",
    "skills/ECharts": "ECharts configuration recipes and conventions.",
    "skills/MapLibre": "MapLibre GL usage patterns for this project.",
    "skills/Cytoscape": "Cytoscape.js graph-visualization patterns for this project.",
    "skills/Git": "Git tooling/workflow helpers (as opposed to docs/context/workflow/git's process notes).",
    "skills/Azure": "Azure-specific infrastructure/deployment knowledge.",
    "skills/Oilfield": "Domain-specific (oilfield) knowledge and terminology used across the codebase.",

    "prompts": "Reusable prompt templates for AI-assisted work, organized by task type.",
    "prompts/coding": "Prompts for implementation tasks.",
    "prompts/review": "Prompts for code/design review tasks.",
    "prompts/architecture": "Prompts for architecture/design exploration.",
    "prompts/requirement": "Prompts for turning ideas into requirements/user stories.",
    "prompts/documentation": "Prompts for generating or updating documentation.",

    "templates": "Fill-in-the-blank Markdown templates for common doc types.",

    "memory": "Long-running conversation/session artifacts, distinct from docs/context/project-memory's curated summaries.",
    "memory/conversations": "Raw or lightly-cleaned conversation transcripts worth keeping.",
    "memory/summaries": "Condensed summaries distilled from conversations/checkpoints.",
    "memory/checkpoints": "Point-in-time snapshots of project state/understanding.",

    "scripts": "Automation scripts for this project (build, data prep, migrations, etc.).",
    "src": "Application source code.",
}

# ---------------------------------------------------------------------------
# templates/*.md starter content
# ---------------------------------------------------------------------------
TEMPLATES = {
    "templates/ADR.md": """# ADR-NNNN: <short decision title>

- Status: Proposed | Accepted | Superseded by ADR-XXXX
- Date: YYYY-MM-DD
- Deciders: <names>

## Context
What problem are we solving? What forces/constraints are at play?

## Decision
What did we decide to do?

## Alternatives Considered
- **Option A** — pros / cons
- **Option B** — pros / cons

## Consequences
What becomes easier or harder as a result of this decision?
""",
    "templates/Feature.md": """# Feature: <name>

- Status: Draft | In Progress | Shipped
- Owner: <name>
- Related ADRs: <links>

## Problem / Motivation
Why does this feature need to exist?

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Design Summary
High-level approach (link to docs/implementation/ for detail).

## Open Questions
- ...
""",
    "templates/API.md": """# API: <endpoint or service name>

- Protocol: REST | GraphQL | WebSocket
- Status: Draft | Stable | Deprecated

## Summary
One paragraph describing what this API does.

## Request
```
METHOD /path
```
| Field | Type | Required | Description |
|---|---|---|---|

## Response
```json
{}
```

## Errors
| Code | Meaning |
|---|---|
""",
    "templates/Bug.md": """# Bug: <short title>

- Status: Open | In Progress | Fixed | Won't Fix
- Severity: Low | Medium | High | Critical
- Reported: YYYY-MM-DD

## Expected Behavior
...

## Actual Behavior
...

## Repro Steps
1. ...

## Root Cause
...

## Fix
...
""",
    "templates/Skill.md": """# Skill: <name>

## When to use this
Describe the trigger conditions/scenarios.

## Conventions
- Convention 1
- Convention 2

## Examples
```
<code or usage example>
```

## Pitfalls
- Known gotcha 1
""",
    "templates/Decision.md": """# Decision: <short title>

- Date: YYYY-MM-DD
- Participants: <names>

## Question
What were we deciding?

## Decision
What we chose.

## Reasoning
Why we chose it over the alternatives.

## Follow-ups
- [ ] ...
""",
}

PROJECT_MEMORY_FILES = {
    "docs/context/project-memory/architecture-memory.md": "# Architecture Memory\n\nAppend-only log of architectural facts an AI assistant should remember across sessions.\n\n## YYYY-MM-DD\n- ...\n",
    "docs/context/project-memory/business-memory.md": "# Business Memory\n\nAppend-only log of business/domain facts learned over time.\n\n## YYYY-MM-DD\n- ...\n",
    "docs/context/project-memory/coding-memory.md": "# Coding Memory\n\nAppend-only log of coding conventions, gotchas, and decisions discovered while working in this codebase.\n\n## YYYY-MM-DD\n- ...\n",
    "docs/context/project-memory/bug-memory.md": "# Bug Memory\n\nAppend-only log of tricky bugs and their resolutions, so the same bug isn't re-investigated from scratch.\n\n## YYYY-MM-DD\n- ...\n",
    "docs/context/project-memory/feature-memory.md": "# Feature Memory\n\nAppend-only log of feature decisions and their current status.\n\n## YYYY-MM-DD\n- ...\n",
    "docs/context/project-memory/timeline.md": "# Project Timeline\n\nChronological log of significant project events.\n\n| Date | Event |\n|---|---|\n",
}

# Glossary/terminology starter files (not empty, since they're named files not folders)
NAMED_FILES = {
    "docs/context/business-model/glossary.md": "# Glossary\n\n| Term | Definition |\n|---|---|\n",
    "docs/context/business-model/terminology.md": "# Terminology Notes\n\nLonger-form notes on terms that need more than a one-line glossary definition.\n",
}

ALL_FOLDERS = list(FOLDER_NOTES.keys())


def write_file(path: Path, content: str, force: bool):
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def scaffold(target: Path, project_name: str, force: bool):
    created, skipped = [], []

    # 1. Folders + per-folder README.md
    for rel in ALL_FOLDERS:
        folder = target / rel
        folder.mkdir(parents=True, exist_ok=True)
        note = FOLDER_NOTES[rel]
        readme = folder / "README.md"
        title = rel.split("/")[-1]
        content = f"# {title}\n\n{note}\n"
        if write_file(readme, content, force):
            created.append(str(readme.relative_to(target)))
        else:
            skipped.append(str(readme.relative_to(target)))

    # 2. Named starter files (glossary, terminology)
    for rel, content in NAMED_FILES.items():
        p = target / rel
        if write_file(p, content, force):
            created.append(rel)
        else:
            skipped.append(rel)

    # 3. Project-memory files
    for rel, content in PROJECT_MEMORY_FILES.items():
        p = target / rel
        if write_file(p, content, force):
            created.append(rel)
        else:
            skipped.append(rel)

    # 4. templates/*.md
    for rel, content in TEMPLATES.items():
        p = target / rel
        if write_file(p, content, force):
            created.append(rel)
        else:
            skipped.append(rel)

    # 5. Top-level README for the whole project
    top_readme = target / "README.md"
    top_content = f"""# {project_name}

## Project Layout

- `docs/` — human documentation (requirements, decisions, architecture, implementation, runbooks, knowledge, open questions)
- `docs/context/` — structured AI-facing project context (business model, data model, API, frontend, design system, workflow, project skills, project memory)
- `skills/` — reusable technology-scoped skill packs
- `prompts/` — reusable prompt templates by task type
- `templates/` — fill-in-the-blank doc templates (ADR, Feature, API, Bug, Skill, Decision)
- `memory/` — raw conversation/session artifacts and checkpoints
- `scripts/` — automation scripts
- `src/` — application source code

See the README.md inside each subfolder for what belongs there.
"""
    if write_file(top_readme, top_content, force):
        created.append("README.md")
    else:
        skipped.append("README.md")

    return created, skipped


def main():
    parser = argparse.ArgumentParser(description="Scaffold an AI-context-first project skeleton.")
    parser.add_argument("target_dir", help="Directory to scaffold into (created if missing).")
    parser.add_argument("--project-name", default=None, help="Project name for the top-level README (default: target dir name).")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files instead of skipping them.")
    args = parser.parse_args()

    target = Path(args.target_dir).resolve()
    project_name = args.project_name or target.name
    target.mkdir(parents=True, exist_ok=True)

    created, skipped = scaffold(target, project_name, args.force)

    print(f"Scaffolded project at: {target}")
    print(f"Created {len(created)} files, skipped {len(skipped)} existing files.")
    if skipped:
        print("\nSkipped (already existed, use --force to overwrite):")
        for s in skipped[:20]:
            print(f"  - {s}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")


if __name__ == "__main__":
    main()