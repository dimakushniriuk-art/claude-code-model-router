# model-router for Claude Code

**Same single chat, lower bill.** Haiku reads, Sonnet codes, Opus thinks.

[Italiano](README.it.md) · [Full details](docs/DETAILS.md) · MIT

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/flow-en-dark.svg"><img alt="Flow: you write in one chat; the main session on Sonnet does small steps itself and hands reading to reader on Haiku, coding to coder on Sonnet, planning and hard bugs to architect on Opus; if a result is not good enough it escalates one level" src="docs/img/flow-en-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/brief-en-dark.svg"><img alt="Brief step: for a vague request like make user accounts more secure, Claude first looks in the code, then asks only the questions that change the result with a recommended option, then writes a compact brief with goal, done-when, out of scope and steps split across agents" src="docs/img/brief-en-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/agents-en-dark.svg"><img alt="The three agents: reader on Haiku finds code and returns answer plus file:line at about 3% of Opus price; coder on Sonnet implements changes and tests at 50%; architect on Opus designs and plans at 100%" src="docs/img/agents-en-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/install-en-dark.svg"><img alt="Install in three steps: add the marketplace, install the plugin, switch to Sonnet" src="docs/img/install-en-light.svg" width="900"></picture>

```bash
claude plugin marketplace add dimakushniriuk-art/claude-code-model-router
claude plugin install model-router@model-router
```

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/savings-en-dark.svg"><img alt="Estimated saving: 47 percent in the expected scenario, range 25 to 60 percent; about 47, 142 and 475 dollars per month at 100, 300 and 1000 dollars of monthly Opus spend" src="docs/img/savings-en-light.svg" width="900"></picture>

> Estimate, not a measurement. [How it is computed](docs/DETAILS.md#how-the-estimate-is-computed) · [Measure your own](docs/DETAILS.md#measure-your-own-savings) · On Pro/Max plans the saving means more usage before limits, not money back.
