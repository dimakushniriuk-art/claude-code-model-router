Model routing policy (model-router plugin). Delegate subtasks to the cheapest agent that keeps quality:
- Do it yourself when it is small: about 3 tool calls or fewer, or the needed files are already in context. Delegation has a cold-start cost, so never delegate trivial steps.
- model-router:reader (Haiku): read-only exploration across several files, searches, summaries of code/logs/docs. Ask for conclusions + file:line only.
- model-router:coder (Sonnet): implementing a clearly specified change and its tests.
- model-router:architect (Opus): design, trade-offs, multi-file plans, hard bugs after a failed attempt, security. Then hand its plan to coder.
- Give every agent a self-contained brief (goal, relevant paths, constraints, expected output). Run independent reader tasks in parallel.
- If an agent's result is wrong or incomplete, escalate one level (reader -> coder/you -> architect) instead of retrying the same agent more than once.
- Keep your own replies concise; do not paste large files or diffs back into the conversation.
