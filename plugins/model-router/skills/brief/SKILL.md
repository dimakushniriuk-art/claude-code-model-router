---
name: brief
description: Use BEFORE starting a medium or large task (several files or steps) or a vague request, to ask at most 3 decisive questions and rewrite the request into a compact brief split across the model-router agents. Skip for small, clear or follow-up requests.
argument-hint: "[request to clarify]"
---

# Brief: clarify once, then route

Goal: spend a few hundred tokens up front so the expensive part (exploration, code, tests) runs once, on the right target. A brief that does not change what gets built is waste, so keep this short.

## 1. Decide if a brief is needed (no output for this step)

Skip the whole skill and just do the work when ANY is true:
- The request is small: about 3 tool calls or fewer, or a single obvious edit.
- It is a follow-up inside a task that already has a brief.
- The request already states goal, scope and how to check it is done.
- The user said "just do it", "no questions", or similar.

## 2. Look before you ask (max 2-3 quick searches)

Answer from the repository whatever it can answer: framework, existing patterns, test commands, file locations. Use Grep/Glob directly, or `model-router:reader` if it needs more than a few lookups. Never ask the user something the code already tells you.

## 3. Ask only decisive questions (0-3, one round)

A question is allowed only if its answer **changes what gets built or how it is verified**, and a wrong guess would be costly to undo: scope, behavior visible to users, data or API contracts, security, irreversible operations.

- Use the AskUserQuestion tool: all questions in ONE call, 2-4 options each, your recommended option first and marked "(Recommended)".
- No questions about style, naming or details you can decide reversibly. Decide them and list them as assumptions.
- If you cannot ask (non-interactive run, `-p`, or the tool is unavailable), do not stop: pick the recommended options and list them as assumptions.

## 4. Write the brief (max ~12 lines, no prose)

```
GOAL: <one sentence, the outcome, not the activity>
CONTEXT: <relevant paths/symbols found in step 2>
CONSTRAINTS: <must / must not, incl. answers from step 3>
DONE WHEN: <checkable criteria: tests/commands/behaviors>
OUT OF SCOPE: <what not to touch>
ASSUMPTIONS: <decisions you made without asking>
STEPS:
  1. reader | coder | architect | self: <subtask>   (cheapest agent that can do it)
  2. ...
```

Rules for STEPS:
- `self` for tiny steps; `reader` for exploration; `coder` for clearly specified edits; `architect` only for real design or a bug whose cause is unknown.
- Mark steps that can run in parallel with `||`.
- Each agent gets the brief's GOAL, CONSTRAINTS and DONE WHEN plus its own step, so it does not re-derive context.

## 5. Show it, then go

- Always print the brief before executing it, also in non-interactive runs (it is the user's chance to spot a wrong target).
- Medium task: then start immediately.
- Large task (many files, migrations, anything hard to undo) and the brief contains ASSUMPTIONS: put "Proceed with this brief?" as the last question in the step 3 call, or ask it alone if there were no other questions. Recommended option: "Proceed".
- Then execute the STEPS. At the end, check every DONE WHEN item and report which pass.

$ARGUMENTS
