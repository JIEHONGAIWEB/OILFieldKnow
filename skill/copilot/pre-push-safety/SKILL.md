---
name: pre-push-safety
description: 'Run a pre-push safety gate before git push. Use to check untracked files, current branch naming, remote target, upstream tracking, and latest commit summary.'
user-invocable: false
---

# Pre-push Safety

## What This Skill Produces

A push readiness report with clear PASS/WARN/FAIL checks and actionable fixes before running `git push`.

## When To Use

- User asks to push code or verify push safety.
- Team wants a consistent pre-push checklist.
- Need to avoid pushing from wrong branch or remote.

## Required Inputs

- Optional remote name (default: `origin`).
- Optional expected branch pattern (for example `feature/*`, `release/*`).

## Procedure

1. Run [pre-push safety script](./scripts/pre-push-check.sh).
2. Review check sections in order:
- Working tree status (tracked/untracked files)
- Current branch and naming pattern
- Upstream and remote target
- Ahead/behind state
- Latest commit summary
3. If any FAIL exists, stop push and resolve blockers.
4. If only WARN exists, ask user for explicit confirmation.
5. Push only when checks are acceptable.

## Validation

- Report includes: untracked files, branch name, remote/upstream, and latest commit summary.
- Any push recommendation is grounded in script output.
- Final response clearly states `Ready to push: Yes/No`.

## Example Prompts

- Check pre-push safety for current branch and tell me if I can push now.
- Run pre-push checks against origin and explain any blockers.
- Validate branch and upstream, then summarize latest commit before push.
