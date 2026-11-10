#!/bin/bash

set -euo pipefail

REMOTE="${1:-origin}"
EXPECTED_PATTERN="${2:-}"

print_section() {
  echo
  echo "== $1 =="
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "FAIL: not inside a git repository"
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)"
LATEST_SUBJECT="$(git log -1 --pretty=%s 2>/dev/null || true)"
LATEST_ID="$(git rev-parse --short HEAD 2>/dev/null || true)"

print_section "Working Tree"
STATUS="$(git status --short)"
UNTRACKED="$(git ls-files --others --exclude-standard)"
if [ -n "$STATUS" ]; then
  echo "WARN: working tree is not clean"
  echo "$STATUS"
else
  echo "PASS: working tree clean"
fi

if [ -n "$UNTRACKED" ]; then
  echo "WARN: untracked files detected"
  echo "$UNTRACKED"
else
  echo "PASS: no untracked files"
fi

print_section "Branch"
echo "Current branch: $BRANCH"
if [ -n "$EXPECTED_PATTERN" ]; then
  case "$BRANCH" in
    $EXPECTED_PATTERN)
      echo "PASS: branch matches expected pattern '$EXPECTED_PATTERN'"
      ;;
    *)
      echo "WARN: branch does not match expected pattern '$EXPECTED_PATTERN'"
      ;;
  esac
fi

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "WARN: pushing directly from protected-like branch '$BRANCH'"
fi

print_section "Remote & Upstream"
if git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "PASS: remote '$REMOTE' exists"
  echo "Remote URL: $(git remote get-url "$REMOTE")"
else
  echo "FAIL: remote '$REMOTE' not found"
fi

if [ -n "$UPSTREAM" ]; then
  echo "PASS: upstream is set -> $UPSTREAM"
  AHEAD_BEHIND="$(git rev-list --left-right --count "$UPSTREAM"...HEAD 2>/dev/null || echo "0 0")"
  BEHIND_COUNT="$(echo "$AHEAD_BEHIND" | awk '{print $1}')"
  AHEAD_COUNT="$(echo "$AHEAD_BEHIND" | awk '{print $2}')"
  echo "Ahead: $AHEAD_COUNT, Behind: $BEHIND_COUNT"
  if [ "$BEHIND_COUNT" != "0" ]; then
    echo "WARN: branch is behind upstream"
  fi
else
  echo "WARN: no upstream configured for current branch"
fi

print_section "Latest Commit"
if [ -n "$LATEST_ID" ]; then
  echo "Latest commit: $LATEST_ID"
  echo "Summary: $LATEST_SUBJECT"
  git show --stat --oneline --no-patch HEAD
else
  echo "FAIL: cannot read latest commit"
fi

print_section "Recommendation"
HAS_FAIL=0
if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  HAS_FAIL=1
fi
if [ -z "$LATEST_ID" ]; then
  HAS_FAIL=1
fi

if [ "$HAS_FAIL" -eq 1 ]; then
  echo "Ready to push: NO"
  exit 1
fi

echo "Ready to push: CONDITIONAL"
echo "Proceed only after reviewing WARN entries above."
