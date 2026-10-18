#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
INFO_FILE="$PROJECT_DIR/Marchenko_Danil_info.txt"

printf '%s\n' '==============================' 'Student Information' '=============================='
printf 'Name: %s\n' 'Danil'
printf 'Surname: %s\n' 'Marchenko'
printf 'Group: %s\n' 'IT2-2303'
printf 'Student ID: %s\n' '41587'
printf '\n%s\n' '==============================' 'System Information' '=============================='
printf 'Username: %s\n' "$(whoami)"
printf 'Hostname: %s\n' "$(hostname)"
printf 'Current Date: %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
printf 'Operating System: %s\n' "$(uname -srmo)"
printf 'Disk Usage:\n'
df -h "$PROJECT_DIR" | awk 'NR == 1 || NR == 2'
printf 'Memory Usage:\n'
free -h

if [[ -f "$INFO_FILE" ]]; then
  printf '\n%s\n' 'Student information file exists.'
else
  printf '\n%s\n' 'Student information file does not exist.'
fi
