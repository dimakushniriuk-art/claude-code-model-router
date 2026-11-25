<!-- Optional. Paste into ~/.claude/CLAUDE.md (all projects) or a project's CLAUDE.md.
     The plugin already injects the delegation policy; these are general token-saving habits. -->
## Token economy
- Be concise; don't restate what I just wrote or summarize what you just did at length.
- Search with Grep/Glob before reading, and read only the relevant line ranges, not whole files.
- Don't paste long files or diffs into the chat: point to `file:line`.
- After a failing test run, re-run only the failing tests, not the whole suite.
- Suggest `/clear` when I switch to an unrelated task.

# Compact instructions
When compacting, keep: current goal, decisions made, files changed, failing tests. Drop command output and file contents already read.
