#!/usr/bin/env bash
# Sync know-skills core skills into the local Agent skills directory.
#
# Default target: $HOME/.agents/skills  (override with SKILLS_ROOT)
# Usage:
#   ./scripts/sync-skills.sh              # copy css-professor + agent-loop
#   ./scripts/sync-skills.sh --dry-run    # print actions only
#   ./scripts/sync-skills.sh --symlink    # prefer symlink when filesystem allows
#   SKILLS_ROOT=/custom/path ./scripts/sync-skills.sh

set -euo pipefail

DRY_RUN=0
USE_SYMLINK=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --symlink) USE_SYMLINK=1 ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS_ROOT="${SKILLS_ROOT:-$HOME/.agents/skills}"

CORE_SKILLS=(css-professor agent-loop)

if [[ ! -d "$SKILLS_SRC/css-professor" ]]; then
  echo "ERROR: expected skill dir missing: $SKILLS_SRC/css-professor" >&2
  exit 1
fi

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "DRY: $*"
  else
    "$@"
  fi
}

echo "Source: $SKILLS_SRC"
echo "Target: $SKILLS_ROOT"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "(dry-run)"
fi

run mkdir -p "$SKILLS_ROOT"

for name in "${CORE_SKILLS[@]}"; do
  src="$SKILLS_SRC/$name"
  dst="$SKILLS_ROOT/$name"
  if [[ ! -d "$src" ]]; then
    echo "SKIP  missing source: $src" >&2
    continue
  fi

  if [[ "$USE_SYMLINK" -eq 1 ]]; then
    if [[ -e "$dst" || -L "$dst" ]]; then
      run rm -rf "$dst"
    fi
    # Relative symlink when possible so moves of HOME still resolve poorly;
    # absolute is clearer for Agent hosts that resolve once.
    run ln -s "$src" "$dst"
    echo "LINK  $name -> $src"
  else
    run mkdir -p "$dst"
    # Portable recursive copy; replace contents.
    if [[ "$DRY_RUN" -eq 1 ]]; then
      echo "DRY: cp -R $src/. $dst/"
    else
      rm -rf "$dst"
      mkdir -p "$dst"
      cp -R "$src/." "$dst/"
    fi
    echo "COPY  $name -> $dst"
  fi
done

echo
echo "Done. Reload Agent skills / start a new session if the host caches skill files."
