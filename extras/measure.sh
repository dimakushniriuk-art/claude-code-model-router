#!/usr/bin/env bash
# A/B cost measurement: run the same task with and without routing, each in a
# clean git worktree (your working tree is never touched).
# Usage:  bash extras/measure.sh "task description" [RUNS]
# Optional env vars:
#   BASE_MODEL   main model for the baseline   (default: opus)
#   ROUTED_MODEL main model with routing        (default: sonnet)
#   PERM         permission mode for -p         (default: acceptEdits; Bash commands
#                that are not allowed get denied - use PERM=auto for tasks that run tests)
#   PLUGIN_DIR   plugin folder                  (default: ../plugins/model-router)
set -euo pipefail
TASK="${1:?Usage: measure.sh \"task\" [RUNS]}"; RUNS="${2:-1}"
BASE_MODEL="${BASE_MODEL:-opus}"; ROUTED_MODEL="${ROUTED_MODEL:-sonnet}"; PERM="${PERM:-acceptEdits}"
PLUGIN_DIR="${PLUGIN_DIR:-$(cd "$(dirname "$0")/../plugins/model-router" && pwd)}"
command -v jq >/dev/null || { echo "jq is required"; exit 1; }
git rev-parse --show-toplevel >/dev/null 2>&1 || { echo "Run this inside a git repository"; exit 1; }

# Don't load the plugin twice if it is already installed.
EXTRA=(); claude plugin list 2>/dev/null | grep -q "model-router" || EXTRA=(--plugin-dir "$PLUGIN_DIR")

run() { # $1=label, rest=command
  local label=$1; shift
  local wt; wt=$(mktemp -d); git worktree add -q --detach "$wt" HEAD
  local out; out=$( cd "$wt" && "$@" -p "$TASK" --output-format json --permission-mode "$PERM" 2>/dev/null || true )
  git worktree remove --force "$wt"
  echo "$out" | jq -r --arg l "$label" '
    "\($l)\t$\(.total_cost_usd // 0 | . * 10000 | round / 10000)\t\(.num_turns // "?")\t\((.duration_ms // 0) / 1000 | floor)s\t" +
    ((.modelUsage // {}) | to_entries | map("\(.key): $\(.value.costUSD // 0 | . * 10000 | round / 10000)") | join(", "))' \
    || echo "$label	error: output was not JSON"
}

echo -e "variant\tcost\tturns\ttime\tper model"
for i in $(seq 1 "$RUNS"); do
  # Baseline: every subagent forced onto the main model = no routing.
  run "baseline#$i" env CLAUDE_CODE_SUBAGENT_MODEL="$BASE_MODEL" CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 claude --model "$BASE_MODEL"
  run "routed#$i"   claude --model "$ROUTED_MODEL" "${EXTRA[@]}"
done
echo
echo "Compare QUALITY too, not just cost. One run is noisy: use at least 3."
