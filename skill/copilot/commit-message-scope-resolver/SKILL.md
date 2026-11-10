---
name: commit-message-scope-resolver
description: 'Suggest Conventional Commit scope from changed file paths. Use when drafting commit messages and you want path-based scope recommendations such as srp-new or well-trends.'
user-invocable: false
---

# Commit Message Scope Resolver

## What This Skill Produces

Path-based scope suggestions for Conventional Commit messages, with confidence notes and a final recommended message pattern.

## When To Use

- User asks for commit message help.
- Scope is unclear from multiple changed paths.
- Team uses Conventional Commits with meaningful scopes.

## Required Inputs

- Changed file paths from staged diff (preferred) or working tree diff.
- Optional commit type (`feat`, `fix`, `chore`, etc.).

## Procedure

1. Run [scope resolver script](./scripts/suggest-scope.sh).
2. Review top candidate scopes ranked by changed path frequency.
3. If one scope dominates, recommend that scope.
4. If multiple scopes are close, provide 2-3 options with trade-offs.
5. Output final message template:
- `<type>(<scope>): <summary>`

## Validation

- Scope recommendation is derived from actual path distribution.
- Result includes candidate list and selected scope rationale.
- Output includes at least one ready-to-use Conventional Commit line.

## Example Prompts

- Suggest commit scope from staged files and propose a `chore(...)` message.
- Analyze changed paths and give top 3 scope candidates.
- Pick the best scope for this commit and output final conventional message.
