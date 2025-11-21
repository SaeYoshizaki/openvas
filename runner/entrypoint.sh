#!/bin/bash
set -e

echo "[INFO] Configuring GitHub Actions runner..."

# Run the GitHub Actions runner configuration
/actions-runner/config.sh \
  --url "$REPO_URL" \
  --token "$RUNNER_TOKEN" \
  --name "docker-openvas-runner" \
  --work _work

echo "[INFO] Runner configured. Starting runner..."

# Check socket share
ls -l /run/gvmd || echo "[WARN] /run/gvmd not found"

# Start GitHub runner
/actions-runner/run.sh