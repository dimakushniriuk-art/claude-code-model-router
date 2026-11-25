# Changelog

## Unreleased

- README is now visual: routing flow, agent cards, install steps and savings at a glance (EN/IT, light/dark). Long text moved to `docs/DETAILS.md`.

## 1.0.0 (2026-11-25)

- First release: `reader` (Haiku), `coder` (Sonnet) and `architect` (Opus) subagents.
- SessionStart hook that injects the delegation policy at startup, after `/clear` and after compaction.
- Extras: status line, A/B cost measurement script, CLAUDE.md snippet.
- Savings estimator and chart (`tools/estimate.py`) using API prices checked on 2026-11-25.
