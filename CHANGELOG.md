# Changelog

## 1.2.0 (2026-11-25)

- One-line installers: `install.ps1` (Windows PowerShell) and `install.sh` (macOS/Linux): plugin + Sonnet as main model + status line, with a settings backup.
- `install.sh --project`: puts the agents, the brief skill and the routing policy into a repository, for phone/web (cloud) sessions, which don't load plugins.
- PowerShell status line (`extras/statusline.ps1`).
- New visuals: "up to 60%" for pay-as-you-go billing, more work before limits for Pro/Max/Ultra/Team, illustrated install for computer and phone.

## 1.1.0 (2026-11-25)

- New `brief` skill: for medium/large or vague requests, looks in the code first, asks at most 3 decisive questions in one round (with a recommended option), then writes a compact brief whose STEPS are split across the agents. Skipped for small or clear requests.
- Routing policy now triggers the brief step.
- README is now visual: routing flow, agent cards, install steps and savings at a glance (EN/IT, light/dark). Long text moved to `docs/DETAILS.md`.

## 1.0.0 (2026-11-25)

- First release: `reader` (Haiku), `coder` (Sonnet) and `architect` (Opus) subagents.
- SessionStart hook that injects the delegation policy at startup, after `/clear` and after compaction.
- Extras: status line, A/B cost measurement script, CLAUDE.md snippet.
- Savings estimator and chart (`tools/estimate.py`) using API prices checked on 2026-11-25.
