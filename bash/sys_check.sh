#!/bin/bash
# sys_check.sh
# ------------
# Prints a quick system health snapshot:
#   - CPU usage
#   - Memory usage
#   - Disk usage
#   - Uptime
#   - Top 5 processes by CPU
#
# Usage:
#   ./sys_check.sh
#   ./sys_check.sh --watch   (refresh every 5 seconds)

set -euo pipefail

WATCH=false
[[ "${1:-}" == "--watch" ]] && WATCH=true

print_report() {
  clear
  echo "════════════════════════════════════════"
  echo "  🖥️  SYSTEM HEALTH CHECK"
  echo "  $(date '+%Y-%m-%d %H:%M:%S')"
  echo "════════════════════════════════════════"

  # Uptime
  echo ""
  echo "⏱️  Uptime"
  uptime | awk -F'( up |,  [0-9]+ user)' '{print "   " $2}'

  # CPU
  echo ""
  echo "🔥 CPU Usage"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    CPU=$(top -l 1 | grep "CPU usage" | awk '{print $3}')
    echo "   User: $CPU"
  else
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    echo "   Used: ${CPU}%"
  fi

  # Memory
  echo ""
  echo "💾 Memory Usage"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    vm_stat | awk '
      /Pages free/     { free=$3 }
      /Pages active/   { active=$3 }
      /Pages inactive/ { inactive=$3 }
      /Pages wired/    { wired=$4 }
      END {
        total=(free+active+inactive+wired)*4096/1024/1024/1024
        used=(active+wired)*4096/1024/1024/1024
        printf "   Used: %.1f GB / Total: %.1f GB\n", used, total
      }'
  else
    free -h | awk '/^Mem:/ {printf "   Used: %s / Total: %s\n", $3, $2}'
  fi

  # Disk
  echo ""
  echo "💿 Disk Usage"
  df -h / | awk 'NR==2 {printf "   Used: %s / Total: %s (%s used)\n", $3, $2, $5}'

  # Top processes
  echo ""
  echo "📋 Top 5 Processes (by CPU)"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    ps aux | sort -rk3 | head -6 | tail -5 | awk '{printf "   %-25s %5s%%\n", $11, $3}'
  else
    ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "   %-25s %5s%%\n", $11, $3}'
  fi

  echo ""
  echo "════════════════════════════════════════"
  [[ "$WATCH" == true ]] && echo "  Refreshing every 5s — Ctrl+C to exit"
}

if [[ "$WATCH" == true ]]; then
  while true; do
    print_report
    sleep 5
  done
else
  print_report
fi
