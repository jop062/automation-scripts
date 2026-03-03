#!/bin/bash
# backup_dir.sh
# -------------
# Creates a timestamped .tar.gz backup of any directory.
# Optionally keeps only the last N backups.
#
# Usage:
#   ./backup_dir.sh --dir ./my_project
#   ./backup_dir.sh --dir ./my_project --output ./backups
#   ./backup_dir.sh --dir ./my_project --keep 5

set -euo pipefail

DIR=""
OUTPUT_DIR="./backups"
KEEP=0

# ── Parse arguments ───────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)    DIR="$2";        shift 2 ;;
    --output) OUTPUT_DIR="$2"; shift 2 ;;
    --keep)   KEEP="$2";       shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$DIR" ]]; then
  echo "❌ Usage: ./backup_dir.sh --dir <path> [--output <path>] [--keep <N>]"
  exit 1
fi

if [[ ! -d "$DIR" ]]; then
  echo "❌ Directory not found: $DIR"
  exit 1
fi

# ── Create backup ─────────────────────────────────────────────
mkdir -p "$OUTPUT_DIR"
DIRNAME=$(basename "$DIR")
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP="$OUTPUT_DIR/${DIRNAME}_${TIMESTAMP}.tar.gz"

echo "📂 Backing up: $DIR"
tar -czf "$BACKUP" -C "$(dirname "$DIR")" "$DIRNAME"

SIZE=$(du -sh "$BACKUP" | cut -f1)
echo "✅ Backup created: $BACKUP ($SIZE)"

# ── Trim old backups ──────────────────────────────────────────
if [[ "$KEEP" -gt 0 ]]; then
  EXISTING=$(ls -t "$OUTPUT_DIR/${DIRNAME}_"*.tar.gz 2>/dev/null | tail -n +"$((KEEP + 1))")
  if [[ -n "$EXISTING" ]]; then
    echo "$EXISTING" | xargs rm -f
    REMOVED=$(echo "$EXISTING" | wc -l | tr -d ' ')
    echo "🗑️  Removed $REMOVED old backup(s) (keeping last $KEEP)"
  fi
fi

echo "✅ Done."
