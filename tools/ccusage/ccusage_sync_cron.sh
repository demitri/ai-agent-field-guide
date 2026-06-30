#!/bin/bash
# ccusage_sync_cron.sh — cron wrapper that loads nvm before syncing.
# Cron environment lacks nvm, so we source it explicitly here.
# Extra args are passed through to ccusage_sync.py (e.g. --db, --stale-days).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load nvm if present; fall back gracefully to whatever npx is on PATH.
# shellcheck source=/dev/null
if [ -s "$HOME/.nvm/nvm.sh" ]; then
    export NVM_DIR="$HOME/.nvm"
    . "$NVM_DIR/nvm.sh" --no-use
    nvm use default --silent 2>/dev/null || true
fi

exec npx ccusage --json | python3 "$SCRIPT_DIR/ccusage_sync.py" "$@"
