#!/usr/bin/env bash
# Claude Code status line: model | session cost | context used | cache hit ratio
# Requires jq. Install: see README.
input=$(cat)
if ! command -v jq >/dev/null 2>&1; then echo "statusline: install jq"; exit 0; fi
echo "$input" | jq -r '
  def pct(x): if x == null then "–" else ((x|floor|tostring) + "%") end;
  [ (.model.display_name // "?"),
    ("$" + ((.cost.total_cost_usd // 0) * 100 | round / 100 | tostring)),
    ("ctx " + pct(.context_window.used_percentage)),
    (if .prompt_cache.hit_ratio != null then "cache " + pct(.prompt_cache.hit_ratio * 100) else empty end),
    (if .agent.name != null then "agent " + .agent.name else empty end)
  ] | join(" | ")'
