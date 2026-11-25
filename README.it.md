# model-router per Claude Code

**Stessa chat, conto più basso.** Haiku legge, Sonnet scrive codice, Opus ragiona.

[English](README.md) · [Tutti i dettagli](docs/DETAILS.it.md) · MIT

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/money-it-dark.svg"><img alt="Fino al 60 per cento in meno, massimo stimato per fatturazione API ed Enterprise a consumo: con 100, 300 e 1000 dollari al mese su Opus risparmi fino a 60, 181 e 605 dollari; stima prudente 25 per cento" src="docs/img/money-it-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/plans-it-dark.svg"><img alt="Abbonamenti, stesso prezzo, fino a 2,5 volte più lavoro prima dei limiti: Pro 20 dollari da 1x a 2,5x, Max 100 dollari da 5x a 12,6x, Ultra 200 dollari settimanale da 10x a 25,3x; posti Team stesso moltiplicatore; se usi già Sonnet l'intervallo è da 0,7x a 1,3x" src="docs/img/plans-it-light.svg" width="900"></picture>

## Come funziona

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/flow-it-dark.svg"><img alt="Flusso: scrivi in una sola chat; per i compiti più grandi una fase brief fa al massimo 3 domande; la sessione principale su Sonnet fa da sola i passi piccoli e affida la lettura a reader su Haiku, il codice a coder su Sonnet, piani e bug difficili ad architect su Opus; se un risultato non basta sale di un livello" src="docs/img/flow-it-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/brief-it-dark.svg"><img alt="Fase brief: per una richiesta vaga come rendi più sicuri gli account utente, Claude prima guarda il codice, poi chiede solo ciò che cambia il risultato con un'opzione consigliata, poi scrive un brief compatto diviso tra gli agenti" src="docs/img/brief-it-light.svg" width="900"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/agents-it-dark.svg"><img alt="I tre agenti: reader su Haiku a circa il 3 per cento del prezzo di Opus, coder su Sonnet al 50 per cento, architect su Opus al 100 per cento" src="docs/img/agents-it-light.svg" width="900"></picture>

## Installazione

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/install-pc-it-dark.svg"><img alt="Installazione dal computer: comando unico per Windows PowerShell, comando unico per il terminale di macOS o Linux, oppure i comandi del plugin dentro Claude Code; poi riavvia e scrivi /agents" src="docs/img/install-pc-it-light.svg" width="900"></picture>

```powershell
# Windows · PowerShell
irm https://raw.githubusercontent.com/dimakushniriuk-art/claude-code-model-router/main/install.ps1 | iex
```

```bash
# macOS / Linux · Terminale
curl -fsSL https://raw.githubusercontent.com/dimakushniriuk-art/claude-code-model-router/main/install.sh | bash
```

<picture><source media="(prefers-color-scheme: dark)" srcset="docs/img/install-phone-it-dark.svg"><img alt="Installazione dal cellulare: nell'app Claude apri Code e scegli il tuo repository, invia il messaggio di installazione, e le sessioni successive su quel repository usano gli agenti" src="docs/img/install-phone-it-light.svg" width="900"></picture>

```text
Installa model-router in questo repo: git clone --depth 1 https://github.com/dimakushniriuk-art/claude-code-model-router /tmp/mr && bash /tmp/mr/install.sh --project, poi fai commit e push.
```

> Tutti i risparmi sono stime, non garanzie. [Come sono calcolati](docs/DETAILS.it.md#come-è-calcolata-la-stima) · [Misura il tuo risparmio](docs/DETAILS.it.md#misura-il-tuo-risparmio) · Progetto della community, non affiliato ad Anthropic.
