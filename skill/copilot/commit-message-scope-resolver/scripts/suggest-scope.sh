#!/bin/bash

set -euo pipefail

MODE="${1:-staged}"
TOP_N="${2:-5}"

collect_files() {
  if [ "$MODE" = "staged" ]; then
    git diff --cached --name-only
  elif [ "$MODE" = "working" ]; then
    git diff --name-only
  else
    echo "Error: mode must be 'staged' or 'working'" >&2
    exit 1
  fi
}

extract_scope_candidates() {
  awk -F'/' '
    NF == 0 {next}
    {
      # Priority 1: srp-new under well analysis path
      for (i = 1; i <= NF; i++) {
        if ($i == "srp-new") {
          print "srp-new"
          if (i + 2 <= NF && $(i+1) == "components") {
            print $(i+2)
          }
          next
        }
      }

      # Priority 2: components/<name>
      for (i = 1; i <= NF; i++) {
        if ($i == "components" && i + 1 <= NF) {
          print $(i+1)
          next
        }
      }

      # Priority 3: feature folders in libs/src
      for (i = 1; i <= NF; i++) {
        if (($i == "lib" || $i == "src") && i + 1 <= NF) {
          print $(i+1)
          next
        }
      }

      # Fallback: top-level folder
      print $1
    }
  '
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository"
  exit 1
fi

FILES="$(collect_files)"
if [ -z "$FILES" ]; then
  echo "No changed files detected for mode: $MODE"
  exit 0
fi

echo "Changed files ($MODE):"
echo "$FILES"

echo
echo "Scope candidates:"
echo "$FILES" | extract_scope_candidates | sed '/^$/d' | sort | uniq -c | sort -nr | head -n "$TOP_N" | awk '{
  count=$1
  $1=""
  sub(/^ /, "")
  printf("- %s (%d)\n", $0, count)
}'

TOP_SCOPE="$(echo "$FILES" | extract_scope_candidates | sed '/^$/d' | sort | uniq -c | sort -nr | head -n 1 | awk '{$1=""; sub(/^ /, ""); print}')"

if [ -n "$TOP_SCOPE" ]; then
  echo
  echo "Recommended scope: $TOP_SCOPE"
  echo "Template: chore($TOP_SCOPE): <summary>"
fi
