#!/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-shared/win-sync}"

echo "[sync] Fetching origin..."
git fetch origin

echo "[sync] Switching to $BRANCH ..."
git checkout -B "$BRANCH" "origin/$BRANCH" || git checkout -B "$BRANCH"

echo "[sync] Pulling..."
git pull --ff-only || true

echo "[done] origin -> server synced on branch: $BRANCH"
