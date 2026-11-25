# model-router per Claude Code

**Stessa chat, conto più basso.** Haiku legge, Sonnet scrive codice, Opus ragiona.

[English](README.md) · [Tutti i dettagli](docs/DETAILS.it.md) · MIT

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/flow-it-dark.svg"><img alt="Flusso: scrivi in una sola chat; la sessione principale su Sonnet fa da sola i passi piccoli e affida la lettura a reader su Haiku, il codice a coder su Sonnet, piani e bug difficili ad architect su Opus; se un risultato non basta sale di un livello" src="docs/img/flow-it-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/brief-it-dark.svg"><img alt="Fase brief: per una richiesta vaga come rendi più sicuri gli account utente, Claude prima guarda il codice, poi chiede solo ciò che cambia il risultato con un'opzione consigliata, poi scrive un brief compatto con obiettivo, criteri di fatto, fuori ambito e passi divisi tra gli agenti" src="docs/img/brief-it-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/agents-it-dark.svg"><img alt="I tre agenti: reader su Haiku trova il codice e restituisce risposta più file:riga a circa il 3% del prezzo di Opus; coder su Sonnet implementa modifiche e test al 50%; architect su Opus progetta e pianifica al 100%" src="docs/img/agents-it-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/install-it-dark.svg"><img alt="Installazione in tre passi: aggiungi il marketplace, installa il plugin, passa a Sonnet" src="docs/img/install-it-light.svg" width="900"></picture>

```bash
claude plugin marketplace add dimakushniriuk-art/claude-code-model-router
claude plugin install model-router@model-router
```

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/savings-it-dark.svg"><img alt="Risparmio stimato: 47 per cento nello scenario atteso, intervallo dal 25 al 60 per cento; circa 47, 142 e 475 dollari al mese con 100, 300 e 1000 dollari di spesa mensile su Opus" src="docs/img/savings-it-light.svg" width="900"></picture>

> Stima, non misura. [Come è calcolata](docs/DETAILS.it.md#come-è-calcolata-la-stima) · [Misura il tuo risparmio](docs/DETAILS.it.md#misura-il-tuo-risparmio) · Con i piani Pro/Max il risparmio significa più utilizzo prima dei limiti, non denaro.
