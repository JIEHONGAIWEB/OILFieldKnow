---
name: targeted-commit
description: 'Safely create precise git commits with explicit include/exclude scope. Use for selective commits, ignored-file handling with explicit approval only, staged-scope verification, and Conventional Commits enforcement.'
user-invocable: false
---

# Targeted Commit

## What This Skill Produces

A safe, auditable commit that includes only requested files, excludes unrelated changes, and uses a valid Conventional Commit message.

## When To Use

- User asks to commit only selected files.
- Workspace contains unrelated modified files that must remain uncommitted.
- Some requested files may be ignored by `.gitignore`.
- User wants a clear proof of staged scope before commit.

## Required Inputs

- Include list: files that must be committed.
- Optional exclude list: files that must not be committed.
- Commit message in Conventional Commits format.

## Conventional Commit Rule

Message must follow:

- `feat(scope): summary`
- `fix(scope): summary`
- `chore(scope): summary`

If the message is not conventional, stop and ask for a corrected message before committing.

## Procedure

1. Inspect workspace state.
- Run `git status --short`.
- Identify unrelated changes that should remain uncommitted.

2. Stage only requested files.
- Use `git add <file...>` for normal files.
- If a requested file is ignored, run `git check-ignore -v <file>`.
- Use `git add -f <file>` only when the user explicitly requests including ignored files.

3. Verify staged scope before commit.
- Run `git diff --cached --name-only`.
- Confirm staged set exactly matches includes minus excludes.

4. Validate commit message format.
- Ensure message matches Conventional Commits before running commit.

5. Commit staged files.
- Run `git commit -m "<conventional-message>"`.
- If blocked by hooks or identity config, report blocker and next action.

6. Verify post-commit state.
- Run `git status --short`.
- Report remaining files explicitly as intentionally uncommitted or unexpected.

## Decision Logic

- If include list is empty: stop and request explicit files.
- If include path does not exist: stop and ask for correction.
- If file is ignored and there is no explicit approval for force add: stop and ask.
- If staged scope includes unrelated files: unstage only unrelated files, then re-verify.
- If commit message is not conventional: stop and request corrected message.

## Quality Checks

- Staged file list is exact and auditable before commit.
- Commit succeeds and returns a commit id.
- Final report includes commit id, committed files, excluded files, and remaining workspace changes.

## Safety Rules

- Do not use destructive commands such as `git reset --hard`.
- Do not amend commits unless explicitly requested.
- Do not include unrelated files even if modified.

## Example Prompts

- Commit only `.gitignore` and `libs/well-surveillance/src/lib/wpo/well-analysis/srp-new/components/dynacard-detail/config.ts`, exclude `docs/implementation/*`, use `chore(srp-new): include requested files only`.
- Stage selected files, show me staged scope, and commit only if message is a valid Conventional Commit.
