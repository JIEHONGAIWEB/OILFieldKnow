---
name: commit-to-skill
description: "Convert a git commit snapshot markdown into reusable skill instructions. Use when you want a repeatable Purpose, Inputs, Rules, Workflow, Validation, and Output Contract from one successful commit."
argument-hint: "snapshot path and output skill name"
user-invocable: true
---

# Commit To Skill

## What This Skill Produces

- A reusable instructions file derived from a commit snapshot.
- Structured output with Purpose, Inputs, Rules, Workflow, Validation, and Output Contract.
- Safety-focused guidance that avoids destructive git commands and narrows applyTo scope.

## When To Use

- After a commit captures a repeatable optimization, feature pattern, or troubleshooting flow.
- When a team wants to reuse a proven process instead of repeating ad hoc steps.
- When a snapshot markdown is available from a commit-to-skill workflow.

## Required Inputs

- Snapshot file path.
- Target output file name.
- Intended module paths for applyTo scoping.

## Decision Logic

1. If no snapshot file is provided:
   - Find the most recent snapshot file named skill_*.md in the expected snapshot folder.
2. If no reusable pattern is visible in Message and Diff Summary:
   - Ask for problem boundaries before generating instructions.
3. If target output already exists:
   - Ask whether to overwrite or create a variant name.
4. If applyTo is too broad:
   - Propose the narrowest safe glob that still covers the affected modules.

## Procedure

1. Read the snapshot and extract Message and Diff Summary.
2. Identify capability boundaries:
   - Problem solved.
   - Affected modules and paths.
   - Explicit exclusions.
3. Derive reusable rules:
   - Ordered operations.
   - Safety constraints.
   - Validation checkpoints.
4. Generate the instructions file with the required sections.
5. Remove personal details and one-off branch specifics.
6. Return output path, assumptions, and refinement suggestions.

## Quality Checks

- Includes Purpose, Inputs, Rules, Workflow, Validation, and Output Contract.
- Keeps guidance reusable and implementation-agnostic.
- Uses non-destructive command suggestions.
- applyTo is minimally scoped and not blanket broad.

## Output Contract

The final response must include:

- Generated file path.
- Why applyTo scope is safe.
- Any assumptions or missing context.
- Optional next steps for refinement.
