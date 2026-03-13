#!/bin/bash
# Deploy expertpack.ai site to 165.245.136.51
# Usage: ./deploy.sh [--dry-run]
#
# Deploys all files from this directory (except deploy.sh and backups)
# to /var/www/expertpack/ on the expertpack.ai server.

set -euo pipefail

REMOTE="root@165.245.136.51"
REMOTE_DIR="/var/www/expertpack"
SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
DRY_RUN=""

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN="--dry-run"
    echo "DRY RUN — no files will be transferred"
fi

echo "Deploying expertpack.ai from $SITE_DIR..."

# Backup current index.html on remote
ssh "$REMOTE" "cp $REMOTE_DIR/index.html $REMOTE_DIR/index.html.bak.\$(date +%Y%m%d%H%M) 2>/dev/null || true"

# Sync site files (exclude deploy script, backups, and .git)
rsync -avz --delete \
    --exclude 'deploy.sh' \
    --exclude '*.bak.*' \
    --exclude '.git' \
    --exclude '.DS_Store' \
    $DRY_RUN \
    "$SITE_DIR/" "$REMOTE:$REMOTE_DIR/"

echo "✅ Deploy complete: https://expertpack.ai"
