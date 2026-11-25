# model-router for Claude Code

**Same single chat, lower bill.** Haiku reads, Sonnet codes, Opus thinks.

[Italiano](README.it.md) · [Full details](docs/DETAILS.md) · MIT

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/money-en-dark.svg"><img alt="Up to 60 percent cheaper, estimated maximum for API and usage-based Enterprise billing: at 100, 300 and 1000 dollars a month on Opus you save up to 60, 181 and 605 dollars; cautious estimate 25 percent" src="docs/img/money-en-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/plans-en-dark.svg"><img alt="Subscriptions, same price, up to 2.5 times more work before limits: Pro 20 dollars from 1x to 2.5x, Max 100 dollars from 5x to 12.6x, Ultra 200 dollars weekly from 10x to 25.3x; Team seats same multiplier; if you already use Sonnet the range is 0.7x to 1.3x" src="docs/img/plans-en-light.svg" width="900"></picture>

## How it works

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/flow-en-dark.svg"><img alt="Flow: you write in one chat; a brief step asks at most 3 questions for bigger tasks; the main session on Sonnet does small steps itself and hands reading to reader on Haiku, coding to coder on Sonnet, planning and hard bugs to architect on Opus; if a result is not good enough it escalates one level" src="docs/img/flow-en-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/brief-en-dark.svg"><img alt="Brief step: for a vague request like make user accounts more secure, Claude first looks in the code, then asks only the questions that change the result with a recommended option, then writes a compact brief with goal, done-when, out of scope and steps split across agents" src="docs/img/brief-en-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/agents-en-dark.svg"><img alt="The three agents: reader on Haiku at about 3 percent of Opus price, coder on Sonnet at 50 percent, architect on Opus at 100 percent" src="docs/img/agents-en-light.svg" width="900"></picture>

## Install

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/install-pc-en-dark.svg"><img alt="Install on a computer: Windows PowerShell one-liner, macOS or Linux terminal one-liner, or the plugin commands inside Claude Code; then restart and type /agents" src="docs/img/install-pc-en-light.svg" width="900"></picture>

```powershell
# Windows · PowerShell
irm https://raw.githubusercontent.com/dimakushniriuk-art/claude-code-model-router/main/install.ps1 | iex
```

```bash
# macOS / Linux · Terminal
curl -fsSL https://raw.githubusercontent.com/dimakushniriuk-art/claude-code-model-router/main/install.sh | bash
```

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/install-phone-en-dark.svg"><img alt="Install from a phone: in the Claude app open Code and pick your repository, send the install message, and next sessions on that repository use the agents" src="docs/img/install-phone-en-light.svg" width="900"></picture>

```text
Install model-router in this repo: git clone --depth 1 https://github.com/dimakushniriuk-art/claude-code-model-router /tmp/mr && bash /tmp/mr/install.sh --project, then commit and push.
```

> All savings are estimates, not guarantees. [How they are computed](docs/DETAILS.md#how-the-estimate-is-computed) · [Measure your own](docs/DETAILS.md#measure-your-own-savings) · Community project, not affiliated with Anthropic.
