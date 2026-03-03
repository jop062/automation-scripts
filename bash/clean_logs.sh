#!/bin/bash
# clean_logs.sh
# -------------
# Finds log files older than N days, archives them into a .tar.gz,
# and optionally deletes the originals.
#
# Usage:
#   ./clean_logs.sh --dir /var/log --days 30
#   ./clean_logs.sh --dir ./logs --days 7 --delete
#   ./clean_logs.sh --dir ./logs --days 14 --dry-run

set -euo pipefail

DIR=""
DAYS=30
DELETE=false
DRY_RUN=false
ARCHIVE_DIR="./log_archives"

# ── Parse arguments ──────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)    DIR="$2";    shift 2 ;;
    --days)   DAYS="$2";  shift 2 ;;
    --delete) DELETE=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$DIR" ]]; then
  echo "❌ Usage: ./clean_logs.sh --dir <path> --days <N> [--delete] [--dry-run]"
  exit 1
fi

if [[ ! -d "$DIR" ]]; then
  echo "❌ Directory not found: $DIR"
  exit 1
fi

echo "🔍 Scanning: $DIR"
echo "📅 Files older than: $DAYS days"
[[ "$DRY_RUN" == true ]] && echo "🔍 DRY RUN — no changes will be made"

# ── Find old log files ────────────────────────────────────────
FILES=$(find "$DIR" -name "*.log" -mtime +"$DAYS" -type f)

if [[ -z "$FILES" ]]; then
  echo "✅ No log files older than $DAYS days found."
  exit 0
fi

COUNT=$(echo "$FILES" | wc -l | tr -d ' ')
echo "📋 Found $COUNT log file(s) to archive:"
echo "$FILES" | while read -r f; do echo "   $f"; done

if [[ "$DRY_RUN" == true ]]; then
  echo ""
  echo "✅ Dry run complete. $COUNT file(s) would be archived."
  exit 0
fi

# ── Create archive ────────────────────────────────────────────
mkdir -p "$ARCHIVE_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE="$ARCHIVE_DIR/logs_${TIMESTAMP}.tar.gz"

echo "$FILES" | xargs tar -czf "$ARCHIVE"
echo "📦 Archived to: $ARCHIVE"

# ── Optionally delete originals ───────────────────────────────
if [[ "$DELETE" == true ]]; then
  echo "$FILES" | xargs rm -f
  echo "🗑️  Original log files deleted."
fi

echo "✅ Done. $COUNT log file(s) processed."
