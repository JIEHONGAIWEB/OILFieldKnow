#!/usr/bin/env python3
"""
Scaffold an "Oilfield Project Context" skeleton.

Usage:
    python3 scaffold.py <target_dir> [--project-name NAME] [--force]

Builds a flat, domain-aware AI-context tree for oilfield software projects:
business model, data model, API, frontend, design system, workflow, skill,
project memory, plus oilfield-specific additions (domain knowledge, coding
standards, ADRs, feature history, bug knowledge, performance, testing,
deployment, AI rules, open questions).

Idempotent: existing files are skipped unless --force is passed.
"""
import argparse
from pathlib import Path

FOLDER_NOTES = {
    "business-model": "What the oilfield business/domain actually is at the software level: workflows, actors, terminology.",
    "business-model/domains": "One file per business domain/bounded context (e.g. drilling ops, production accounting), its responsibility and boundaries.",
    "business-model/workflows": "Business process write-ups — who does what, in what order, why.",

    "data-model": "The data model of the system: entities, relationships, enums, and representative examples.",
    "data-model/entities": "One file per core entity: fields, invariants, lifecycle.",
    "data-model/relationships": "How entities relate to each other (cardinality, ownership, cascade rules).",
    "data-model/enums": "Enumerations/status codes and their meaning, kept separate so they're easy to grep.",
    "data-model/examples": "Representative example payloads/records for entities, useful as few-shot context for an AI.",

    "api": "API surface documentation, split by protocol.",
    "api/rest": "REST endpoints: routes, methods, request/response shapes.",
    "api/graphql": "GraphQL schema notes: types, queries, mutations, subscriptions.",
    "api/websocket": "WebSocket/real-time channel documentation (e.g. live sensor/telemetry streams): events, payloads, connection lifecycle.",
    "api/contracts": "Cross-cutting API contracts/shared schemas consumed by multiple protocols or services.",

    "frontend": "Frontend-specific context: what exists, how it's structured, and the conventions in use.",
    "frontend/pages": "One file per page/route: purpose, key components, data dependencies.",
    "frontend/components": "Shared component documentation: props, variants, usage guidance.",
    "frontend/state": "State management notes: stores, selectors, ownership boundaries.",
    "frontend/routing": "Routing structure, guards, and navigation conventions.",
    "frontend/charts": "Charting/visualization conventions (e.g. well-log curves, production decline charts, ECharts config patterns).",
    "frontend/ui-patterns": "Recurring UI/interaction patterns (forms, tables, maps, dashboards) so new work stays consistent.",

    "design-system": "Visual design language, kept separate from component implementation.",
    "design-system/colors": "Color palette and usage rules (semantic color tokens, e.g. status colors for well states).",
    "design-system/typography": "Type scale, font families, weight/usage rules.",
    "design-system/spacing": "Spacing scale and layout grid rules.",
    "design-system/components": "Design-level (not code-level) component specs: states, sizes, anatomy.",
    "design-system/interaction": "Motion, transitions, and interaction/feedback conventions.",

    "workflow": "Process documentation split by audience: business, development, deployment.",
    "workflow/business": "Business-facing process flows (approvals, review cycles, field-to-office handoffs).",
    "workflow/development": "Dev workflow: branching model, code review process, release cadence.",
    "workflow/deployment": "Deployment/release process: environments, pipelines, rollback procedure.",

    "skill": "Project-specific 'how we do X here' notes, one subfolder per technology/topic.",
    "skill/chart": "Project conventions for building charts (library choice, theming, data-shape expectations).",
    "skill/angular": "Project-specific Angular conventions (module structure, DI patterns, naming).",
    "skill/testing": "Testing conventions: frameworks, coverage expectations, fixture patterns.",
    "skill/git": "Git conventions: commit message format, branch naming, PR process.",
    "skill/code-review": "Code review checklist and standards specific to this project.",

    "project-memory": "Rolling, append-friendly memory files an AI assistant should read at the start of a session and update at the end.",

    "domain-knowledge": "石油领域专业知识 — oilfield domain knowledge that isn't specific to any one piece of software: subject-matter grounding for AI assistants working on this codebase.",
    "domain-knowledge/drilling": "Drilling operations concepts: rig types, drilling parameters (WOB, RPM, ROP), well trajectory/directional drilling basics.",
    "domain-knowledge/reservoir": "Reservoir engineering concepts: pressure, porosity, permeability, decline curves, recovery factors.",
    "domain-knowledge/production": "Production operations concepts: artificial lift methods, well testing, production allocation.",
    "domain-knowledge/well-operations": "Well lifecycle concepts: completion, workover, plug and abandonment, HSE considerations.",
    "domain-knowledge/units-and-standards": "Units of measure, unit conversion rules, and industry standards/regulatory bodies referenced by the system (e.g. API, WITSML, PPDM).",

    "coding-standards": "Language/framework-agnostic coding standards for this project: naming, formatting, error handling, logging conventions.",
    "architecture-decision": "Architecture Decision Records (ADRs). One file per decision, immutable once accepted.",
    "feature-history": "Chronological record of how major features evolved — what shipped, what changed, and why, so history isn't lost when people rotate off the project.",
    "bug-knowledge": "Recurring/tricky bug patterns and their root causes and fixes, so the same bug class isn't re-investigated from scratch.",
    "performance": "Performance optimization notes: known bottlenecks, benchmarks, and the fixes that worked (e.g. large well-log dataset rendering, telemetry ingestion throughput).",
    "testing": "Testing strategy: test pyramid decisions, what's unit- vs integration- vs E2E-tested, domain-specific test data conventions.",
    "deployment": "Release/deployment process specifics: environments, field-vs-office connectivity considerations, rollback procedure.",
    "ai-rules": "Explicit rules for AI coding assistants working on this project — things it must always/never do here.",
    "open-questions": "Tracked unresolved questions. Move a file out once it's answered (into architecture-decision/ or domain-knowledge/).",
}

ALL_FOLDERS = list(FOLDER_NOTES.keys())

NAMED_FILES = {
    "business-model/glossary.md": "# Glossary\n\n| Term | Definition |\n|---|---|\n",
    "business-model/terminology.md": "# Terminology Notes\n\nLonger-form notes on terms that need more than a one-line glossary definition.\n",
    "domain-knowledge/glossary.md": "# Oilfield Domain Glossary\n\n石油领域术语表。\n\n| Term (EN) | 术语 (中) | Definition |\n|---|---|---|\n",
    "ai-rules/rules.md": """# AI Coding Rules

Rules an AI assistant must follow when working on this project. Keep this
short and enforceable — this is read at the start of every AI session.

## Always
- ...

## Never
- ...

## Domain-specific gotchas
- Unit conversions: always state units explicitly (metric vs imperial) —
  see domain-knowledge/units-and-standards/.
- ...
""",
}

PROJECT_MEMORY_FILES = {
    "project-memory/architecture-memory.md": "# Architecture Memory\n\nAppend-only log of architectural facts an AI assistant should remember across sessions.\n\n## YYYY-MM-DD\n- ...\n",
    "project-memory/business-memory.md": "# Business Memory\n\nAppend-only log of business/domain facts learned over time.\n\n## YYYY-MM-DD\n- ...\n",
    "project-memory/coding-memory.md": "# Coding Memory\n\nAppend-only log of coding conventions, gotchas, and decisions discovered while working in this codebase.\n\n## YYYY-MM-DD\n- ...\n",
    "project-memory/bug-memory.md": "# Bug Memory\n\nAppend-only log of tricky bugs and their resolutions.\n\n## YYYY-MM-DD\n- ...\n",
    "project-memory/feature-memory.md": "# Feature Memory\n\nAppend-only log of feature decisions and their current status.\n\n## YYYY-MM-DD\n- ...\n",
    "project-memory/timeline.md": "# Project Timeline\n\nChronological log of significant project events.\n\n| Date | Event |\n|---|---|\n",
}

TEMPLATES = {
    "architecture-decision/_template.md": """# ADR-NNNN: <short decision title>

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
    "feature-history/_template.md": """# Feature: <name>

- Shipped: YYYY-MM-DD
- Owner: <name>
- Related ADRs: <links>

## What shipped
...

## Why
...

## What changed since
- YYYY-MM-DD: ...
""",
    "bug-knowledge/_template.md": """# Bug pattern: <short title>

- First seen: YYYY-MM-DD
- Severity: Low | Medium | High | Critical
- Recurrence: one-off | recurring pattern

## Symptom
...

## Root Cause
...

## Fix
...

## How to recognize this class of bug in the future
...
""",
    "performance/_template.md": """# Perf note: <area>

- Date: YYYY-MM-DD

## Symptom / Bottleneck
...

## Measurement
Before: ...
After: ...

## Fix
...
""",
}


def write_file(path: Path, content: str, force: bool):
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def scaffold(target: Path, project_name: str, force: bool):
    created, skipped = [], []

    for rel in ALL_FOLDERS:
        folder = target / rel
        folder.mkdir(parents=True, exist_ok=True)
        readme = folder / "README.md"
        title = rel.split("/")[-1]
        content = f"# {title}\n\n{FOLDER_NOTES[rel]}\n"
        (created if write_file(readme, content, force) else skipped).append(
            str(readme.relative_to(target))
        )

    for rel, content in {**NAMED_FILES, **PROJECT_MEMORY_FILES, **TEMPLATES}.items():
        p = target / rel
        (created if write_file(p, content, force) else skipped).append(rel)

    top_readme = target / "README.md"
    top_content = f"""# {project_name} — Oilfield Project Context

## Layout

- `business-model/`, `data-model/`, `api/`, `frontend/`, `design-system/`,
  `workflow/`, `skill/`, `project-memory/` — general AI-context categories.
- `domain-knowledge/` — 石油领域专业知识 (drilling, reservoir, production,
  well operations, units & standards).
- `coding-standards/` — project coding conventions.
- `architecture-decision/` — ADRs (see `_template.md`).
- `feature-history/` — chronological feature evolution log (see `_template.md`).
- `bug-knowledge/` — recurring bug patterns and fixes (see `_template.md`).
- `performance/` — performance optimization notes (see `_template.md`).
- `testing/` — testing strategy.
- `deployment/` — release process.
- `ai-rules/` — rules an AI coding assistant must follow (`rules.md`).
- `open-questions/` — unresolved items.

See the README.md inside each folder for what belongs there.
"""
    (created if write_file(top_readme, top_content, force) else skipped).append("README.md")

    return created, skipped


def main():
    parser = argparse.ArgumentParser(description="Scaffold an Oilfield Project Context skeleton.")
    parser.add_argument("target_dir", help="Directory to scaffold into (created if missing).")
    parser.add_argument("--project-name", default=None, help="Project name for the top-level README.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    target = Path(args.target_dir).resolve()
    project_name = args.project_name or target.name
    target.mkdir(parents=True, exist_ok=True)

    created, skipped = scaffold(target, project_name, args.force)

    print(f"Scaffolded oilfield project context at: {target}")
    print(f"Created {len(created)} files, skipped {len(skipped)} existing files.")
    if skipped:
        print("\nSkipped (already existed, use --force to overwrite):")
        for s in skipped[:20]:
            print(f"  - {s}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")


if __name__ == "__main__":
    main()