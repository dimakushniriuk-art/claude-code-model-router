#!/usr/bin/env bash
# model-router installer for macOS and Linux.
#
# Computer (installs the plugin for your user):
#   curl -fsSL https://raw.githubusercontent.com/dimakushniriuk-art/claude-code-model-router/main/install.sh | bash
#     1. adds the marketplace and installs the plugin
#     2. sets Sonnet as the default main model in ~/.claude/settings.json   (skip: MR_SKIP_MODEL=1)
#     3. installs the status line, needs jq                                   (skip: MR_SKIP_STATUSLINE=1)
#
# Project mode (for phone / web / cloud sessions, which don't load plugins):
#   bash install.sh --project      run inside a git repository
#     copies the agents and the brief skill into ./.claude/ and adds the routing
#     policy to ./CLAUDE.md,
#     so every session on this repository (including ones started from the
#     Claude mobile app) has them once the change is committed and pushed.
#
# Any settings.json is backed up before it is changed.
set -euo pipefail
REPO="dimakushniriuk-art/claude-code-model-router"
RAW="https://raw.githubusercontent.com/$REPO/main"

# ---------------------------------------------------------------- project mode
if [ "${1:-}" = "--project" ]; then
  root=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "Run --project inside a git repository."; exit 1; }
  here="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
  if [ -n "$here" ] && [ -d "$here/plugins/model-router" ]; then
    src="$here/plugins/model-router"
  else
    tmp=$(mktemp -d); git clone -q --depth 1 "https://github.com/$REPO" "$tmp/mr"; src="$tmp/mr/plugins/model-router"
  fi
  command -v python3 >/dev/null || { echo "python3 is required for --project."; exit 1; }
  dst="$root/.claude"
  mkdir -p "$dst/agents" "$dst/skills/brief"
  cp "$src/agents/"*.md "$dst/agents/"
  cp "$src/skills/brief/SKILL.md" "$dst/skills/brief/SKILL.md"
  sed -i.bak 's/`model-router:reader`/`reader`/g' "$dst/skills/brief/SKILL.md" && rm -f "$dst/skills/brief/SKILL.md.bak"
  # The routing policy goes into the repo's CLAUDE.md (loaded by every session, also in the cloud),
  # between markers so re-running replaces it. Outside the plugin the agents have no "model-router:" prefix.
  policy=$(sed -e 's/model-router:brief skill/brief skill/g' -e 's/model-router://g' -e 's/ (model-router plugin)//' "$src/hooks/routing-policy.md")
  python3 - "$root/CLAUDE.md" "$policy" <<'PY'
import os, re, sys
p, policy = sys.argv[1], sys.argv[2].strip()
block = f"<!-- model-router:start -->\n{policy}\n<!-- model-router:end -->"
text = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
if "<!-- model-router:start -->" in text:
    text = re.sub(r"<!-- model-router:start -->.*?<!-- model-router:end -->", lambda m: block, text, flags=re.S)
else:
    text = (text.rstrip() + "\n\n" if text.strip() else "") + block + "\n"
open(p, "w", encoding="utf-8").write(text)
PY
  echo "Installed into $root:"
  echo "  .claude/agents/reader.md coder.md architect.md, .claude/skills/brief/, routing policy block in CLAUDE.md"
  echo "Commit and push them so new sessions on this repository use them. Use /model sonnet in a session."
  exit 0
fi

# --------------------------------------------------------------- computer mode
DIR="$HOME/.claude"; SETTINGS="$DIR/settings.json"
command -v claude >/dev/null || { echo "Claude Code ('claude') not found. Install it: https://code.claude.com/docs/en/setup"; exit 1; }

echo "1/3  Installing the model-router plugin..."
claude plugin marketplace add "$REPO" || echo "     Marketplace may already be added, continuing."
claude plugin install model-router@model-router || claude plugin update model-router@model-router

mkdir -p "$DIR"; [ -s "$SETTINGS" ] || echo '{}' > "$SETTINGS"
if ! command -v jq >/dev/null; then
  echo "jq not found: skipping steps 2-3. Set the model with /model sonnet inside Claude Code."; exit 0
fi
cp "$SETTINGS" "$SETTINGS.bak-$(date +%Y%m%d-%H%M%S)"
tmp=$(mktemp)
if [ "${MR_SKIP_MODEL:-0}" != "1" ]; then
  echo "2/3  Setting Sonnet as the main model..."
  jq '.model = "sonnet"' "$SETTINGS" > "$tmp" && cat "$tmp" > "$SETTINGS"
fi
if [ "${MR_SKIP_STATUSLINE:-0}" != "1" ]; then
  echo "3/3  Installing the status line..."
  curl -fsSL "$RAW/extras/statusline.sh" -o "$DIR/statusline.sh" && chmod +x "$DIR/statusline.sh"
  jq --arg c "$DIR/statusline.sh" '.statusLine = {type: "command", command: $c}' "$SETTINGS" > "$tmp" && cat "$tmp" > "$SETTINGS"
fi
rm -f "$tmp"
echo "Done. Restart Claude Code, then type /agents to see the model-router agents."
