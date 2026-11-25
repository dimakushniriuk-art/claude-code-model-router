#!/usr/bin/env python3
"""Draw the README visuals (routing flow, agent cards, install steps, savings).

Dependency-free SVG, light + dark, English + Italian.
Savings numbers come from tools/estimate.py, so the picture always matches the model.

Usage: python3 tools/visuals.py
"""
from pathlib import Path
import estimate as est

OUT = Path(__file__).resolve().parent.parent / "docs" / "img"
FONT = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
MONO = "SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "light": dict(bg="#ffffff", card="#f6f7f9", line="#d9dce1", ink="#191919", ink2="#5f6368",
                  haiku="#257de0", sonnet="#00a383", opus="#6a4ce2", accent="#f47230", muted="#c9ccd1",
                  code="#eef0f3"),
    "dark":  dict(bg="#0d1117", card="#161b22", line="#30363d", ink="#efefef", ink2="#9c9c9c",
                  haiku="#338ced", sonnet="#00a888", opus="#9887ef", accent="#e76624", muted="#3a4048",
                  code="#1f262e"),
}

T = {
    "en": dict(
        you="You", one_chat="one chat",
        brief="Brief", brief_1="≤3 questions", brief_2="→ clear plan",
        brief_skip="small task: skipped",
        main="Main session", main_m="Sonnet",
        policy="decides who does each step",
        small="Small step? Done right here",
        reader_do="Reads & searches", coder_do="Writes code", arch_do="Plans & hard bugs",
        escalate="Not good enough? Next level up",
        cards=[("reader", "Haiku", "haiku", ["Finds code", "Traces flows", "Summarizes files & logs"],
                "Answer + file:line", "≈3%"),
               ("coder", "Sonnet", "sonnet", ["Implements changes", "Writes tests", "Runs checks"],
                "What changed + tests", "50%"),
               ("architect", "Opus", "opus", ["Designs & plans", "Root-causes hard bugs", "Security review"],
                "Decision + plan", "100%")],
        does="Does", returns="Returns", price="Price vs Opus",
        steps=[("Add", "claude plugin marketplace add\ndimakushniriuk-art/\nclaude-code-model-router"),
               ("Install", "claude plugin install\nmodel-router@model-router"),
               ("Use Sonnet", "/model sonnet\nthen restart Claude Code")],
        sav_title="Estimated saving per month",
        sav_sub="Sonnet main session + plugin, compared with everything on Opus",
        sav_range="range", sav_cons="cautious", sav_opt="optimistic",
        sav_spend="If you spend on Opus", sav_save="you save about",
        sav_note="Estimate from official API prices ({d}) and stated assumptions. Measure yours: extras/measure.sh",
        per_month="/mo",
        b_req="Your request", b_req_txt="\u201cmake user accounts more secure\u201d",
        b_look="1 · Looks in the code first", b_look_txt="finds app/users.py, plaintext passwords",
        b_ask="2 · Asks only what changes the result", b_q="Scope?", b_opts=["Hashing + validation (Recommended)", "Also 2FA and lockout"],
        b_brief="3 · Compact brief → split across agents",
        b_lines=[("GOAL", "hash passwords, validate input"), ("DONE WHEN", "tests pass, no plaintext stored"),
                 ("OUT OF SCOPE", "2FA, sessions"), ("STEPS", "1 coder: users.py + tests")],
        b_why="A few hundred tokens up front, so the expensive work runs once on the right target",
    ),
    "it": dict(
        you="Tu", one_chat="una sola chat",
        brief="Brief", brief_1="≤3 domande", brief_2="→ piano chiaro",
        brief_skip="compito piccolo: saltato",
        main="Sessione principale", main_m="Sonnet",
        policy="decide chi fa ogni passo",
        small="Passo piccolo? Lo fa subito qui",
        reader_do="Legge e cerca", coder_do="Scrive codice", arch_do="Piani e bug difficili",
        escalate="Non basta? Sale di livello",
        cards=[("reader", "Haiku", "haiku", ["Trova il codice", "Segue i flussi", "Riassume file e log"],
                "Risposta + file:riga", "≈3%"),
               ("coder", "Sonnet", "sonnet", ["Implementa modifiche", "Scrive i test", "Lancia i controlli"],
                "Modifiche + test", "50%"),
               ("architect", "Opus", "opus", ["Progetta e pianifica", "Trova la causa dei bug", "Revisione sicurezza"],
                "Decisione + piano", "100%")],
        does="Fa", returns="Restituisce", price="Prezzo vs Opus",
        steps=[("Aggiungi", "claude plugin marketplace add\ndimakushniriuk-art/\nclaude-code-model-router"),
               ("Installa", "claude plugin install\nmodel-router@model-router"),
               ("Usa Sonnet", "/model sonnet\npoi riavvia Claude Code")],
        sav_title="Risparmio mensile stimato",
        sav_sub="Sessione principale su Sonnet + plugin, rispetto a tutto su Opus",
        sav_range="intervallo", sav_cons="prudente", sav_opt="ottimista",
        sav_spend="Se spendi su Opus", sav_save="risparmi circa",
        sav_note="Stima da prezzi API ufficiali ({d}) e ipotesi dichiarate. Misura il tuo: extras/measure.sh",
        per_month="/mese",
        b_req="La tua richiesta", b_req_txt="\u201crendi più sicuri gli account utente\u201d",
        b_look="1 · Prima guarda il codice", b_look_txt="trova app/users.py, password in chiaro",
        b_ask="2 · Chiede solo ciò che cambia il risultato", b_q="Ambito?", b_opts=["Hash + validazione (Consigliato)", "Anche 2FA e blocco"],
        b_brief="3 · Brief compatto → diviso tra gli agenti",
        b_lines=[("OBIETTIVO", "hash password, validare input"), ("FATTO QUANDO", "test ok, niente in chiaro"),
                 ("FUORI AMBITO", "2FA, sessioni"), ("PASSI", "1 coder: users.py + test")],
        b_why="Poche centinaia di token all'inizio, così il lavoro costoso si fa una volta sola, sull'obiettivo giusto",
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(w, h, c, label):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}" role="img" aria-label="{esc(label)}">',
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c["ink2"]}"/></marker></defs>',
            f'<rect width="{w}" height="{h}" rx="16" fill="{c["bg"]}"/>']


def text(x, y, s, size=14, fill="#000", weight=400, anchor="start", family=None):
    fam = f' font-family="{family}"' if family else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{fam}>{esc(s)}</text>')


def pill(x, y, w, h, fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/>'


# --- 1. Routing flow -----------------------------------------------------------
def flow(c, t):
    W, H = 900, 400
    o = head(W, H, c, "How model-router routes work")
    # you
    o.append(f'<rect x="20" y="150" width="130" height="100" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>')
    o.append(text(85, 192, t["you"], 22, c["ink"], 700, "middle"))
    o.append(text(85, 218, t["one_chat"], 12.5, c["ink2"], 400, "middle"))
    o.append(f'<line x1="152" y1="200" x2="176" y2="200" stroke="{c["ink2"]}" stroke-width="2" marker-end="url(#a)"/>')
    # brief
    o.append(f'<rect x="180" y="150" width="120" height="100" rx="14" fill="{c["card"]}" stroke="{c["accent"]}" stroke-width="2" stroke-dasharray="6 4"/>')
    o.append(text(240, 184, t["brief"], 17, c["ink"], 700, "middle"))
    o.append(text(240, 208, t["brief_1"], 12.5, c["ink2"], 400, "middle"))
    o.append(text(240, 228, t["brief_2"], 12.5, c["ink2"], 400, "middle"))
    o.append(text(240, 272, t["brief_skip"], 11, c["ink2"], 400, "middle"))
    o.append(f'<line x1="302" y1="200" x2="324" y2="200" stroke="{c["ink2"]}" stroke-width="2" marker-end="url(#a)"/>')
    # main
    o.append(f'<rect x="328" y="130" width="196" height="140" rx="14" fill="{c["card"]}" stroke="{c["sonnet"]}" stroke-width="2"/>')
    o.append(text(426, 172, t["main"], 16, c["ink"], 700, "middle"))
    o.append(pill(386, 186, 80, 26, c["sonnet"]))
    o.append(text(426, 204, t["main_m"], 14, "#ffffff", 600, "middle"))
    o.append(text(426, 240, t["policy"], 12, c["ink2"], 400, "middle"))
    # small step loop
    o.append(f'<path d="M380,272 C380,330 472,330 472,272" fill="none" stroke="{c["ink2"]}" stroke-width="2" '
             f'stroke-dasharray="5 4" marker-end="url(#a)"/>')
    o.append(text(426, 352, t["small"], 13, c["ink2"], 400, "middle"))
    # agents
    rows = [("reader", "Haiku", "haiku", t["reader_do"], 50),
            ("coder", "Sonnet", "sonnet", t["coder_do"], 160),
            ("architect", "Opus", "opus", t["arch_do"], 270)]
    for name, model, key, does, y in rows:
        o.append(f'<path d="M526,200 C575,200 575,{y + 40} 618,{y + 40}" fill="none" stroke="{c[key]}" '
                 f'stroke-width="2.5" marker-end="url(#a)"/>')
        o.append(f'<rect x="622" y="{y}" width="232" height="80" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>')
        o.append(f'<rect x="622" y="{y}" width="8" height="80" rx="4" fill="{c[key]}"/>')
        o.append(text(646, y + 32, name, 18, c["ink"], 700))
        o.append(pill(766, y + 14, 76, 24, c[key]))
        o.append(text(804, y + 31, model, 13, "#ffffff", 600, "middle"))
        o.append(text(646, y + 60, does, 14, c["ink2"]))
    # escalation
    o.append(f'<line x1="868" y1="96" x2="868" y2="296" stroke="{c["accent"]}" stroke-width="2" marker-end="url(#a)"/>')
    o.append(f'<text x="0" y="0" font-size="12" fill="{c["accent"]}" text-anchor="middle" '
             f'transform="translate(888,196) rotate(-90)" font-weight="600">{esc(t["escalate"])}</text>')
    o.append("</svg>")
    return "\n".join(o)


# --- 2. Agent cards ----------------------------------------------------------
def cards(c, t):
    W, H = 900, 300
    o = head(W, H, c, "The three agents")
    cw, gap = 276, 18
    for i, (name, model, key, does, ret, price) in enumerate(t["cards"]):
        x = 24 + i * (cw + gap)
        o.append(f'<rect x="{x}" y="20" width="{cw}" height="260" rx="16" fill="{c["card"]}" stroke="{c["line"]}"/>')
        o.append(f'<rect x="{x}" y="20" width="{cw}" height="8" rx="4" fill="{c[key]}"/>')
        o.append(text(x + 20, 64, name, 22, c["ink"], 700))
        o.append(pill(x + cw - 96, 44, 76, 26, c[key]))
        o.append(text(x + cw - 58, 62, model, 14, "#ffffff", 600, "middle"))
        o.append(text(x + 20, 96, t["does"].upper(), 11, c["ink2"], 600))
        for j, d in enumerate(does):
            yy = 120 + j * 24
            o.append(f'<circle cx="{x + 26}" cy="{yy - 5}" r="3.5" fill="{c[key]}"/>')
            o.append(text(x + 38, yy, d, 14, c["ink"]))
        o.append(f'<line x1="{x + 20}" x2="{x + cw - 20}" y1="202" y2="202" stroke="{c["line"]}"/>')
        o.append(text(x + 20, 226, t["returns"].upper(), 11, c["ink2"], 600))
        o.append(text(x + 20, 248, ret, 14, c["ink"]))
        o.append(text(x + cw - 20, 226, t["price"].upper(), 11, c["ink2"], 600, "end"))
        o.append(text(x + cw - 20, 256, price, 24, c[key], 700, "end"))
    o.append("</svg>")
    return "\n".join(o)


# --- 3. Install steps --------------------------------------------------------
def install(c, t):
    W, H = 900, 210
    o = head(W, H, c, "Install in three steps")
    cw, gap = 276, 18
    for i, (title, cmd) in enumerate(t["steps"]):
        x = 24 + i * (cw + gap)
        o.append(f'<rect x="{x}" y="20" width="{cw}" height="172" rx="16" fill="{c["card"]}" stroke="{c["line"]}"/>')
        o.append(f'<circle cx="{x + 36}" cy="56" r="18" fill="{c["sonnet"]}"/>')
        o.append(text(x + 36, 62, str(i + 1), 17, "#ffffff", 700, "middle"))
        o.append(text(x + 66, 63, title, 19, c["ink"], 700))
        o.append(f'<rect x="{x + 16}" y="88" width="{cw - 32}" height="88" rx="10" fill="{c["code"]}"/>')
        for j, line in enumerate(cmd.split("\n")):
            o.append(text(x + 28, 112 + j * 22, line, 11.5, c["ink"], 400, family=MONO))
        if i < 2:
            o.append(f'<line x1="{x + cw + 2}" y1="95" x2="{x + cw + gap - 2}" y2="95" stroke="{c["ink2"]}" '
                     f'stroke-width="2" marker-end="url(#a)"/>')
    o.append("</svg>")
    return "\n".join(o)


# --- 4. Savings --------------------------------------------------------------
def savings(c, t):
    W, H = 900, 330
    o = head(W, H, c, t["sav_title"])
    sc = {n: (1 - est.routed_factor(s)) * 100 for n, s in est.SCENARIOS.items()}
    lo, mid, hi = sc["Conservative"], sc["Expected"], sc["Optimistic"]
    o.append(text(32, 50, t["sav_title"], 22, c["ink"], 700))
    o.append(text(32, 76, t["sav_sub"], 14, c["ink2"]))
    # hero number
    o.append(text(32, 168, f"−{mid:.0f}%", 72, c["accent"], 800))
    # range bar 0..100%
    bx, bw, by = 300, 560, 128
    X = lambda p: bx + p / 100 * bw
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="14" rx="7" fill="{c["muted"]}"/>')
    o.append(f'<rect x="{X(lo):.1f}" y="{by}" width="{X(hi) - X(lo):.1f}" height="14" rx="7" fill="{c["accent"]}" opacity="0.45"/>')
    o.append(f'<circle cx="{X(mid):.1f}" cy="{by + 7}" r="10" fill="{c["accent"]}" stroke="{c["bg"]}" stroke-width="3"/>')
    for p in (0, 25, 50, 75, 100):
        o.append(text(X(p), by + 36, f"{p}%", 12, c["ink2"], 400, "middle"))
    o.append(text(X(lo), by - 14, f"{t['sav_cons']} {lo:.0f}%", 12, c["ink2"], 600, "middle"))
    o.append(text(X(hi), by - 14, f"{t['sav_opt']} {hi:.0f}%", 12, c["ink2"], 600, "middle"))
    # chips
    cw, gap = 276, 18
    for i, b in enumerate(est.BASELINES):
        x = 24 + i * (cw + gap)
        s = est.savings(b, est.SCENARIOS["Expected"])
        o.append(f'<rect x="{x}" y="196" width="{cw}" height="92" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>')
        o.append(text(x + 18, 222, f'{t["sav_spend"]} {est.money(b)}{t["per_month"]}', 13, c["ink2"]))
        o.append(text(x + 18, 246, t["sav_save"], 13, c["ink2"]))
        o.append(text(x + cw - 18, 274, f'{est.money(s)}{t["per_month"]}', 30, c["ink"], 700, "end"))
    o.append(text(32, 314, t["sav_note"].format(d=est.PRICES_CHECKED), 12, c["ink2"]))
    o.append("</svg>")
    return "\n".join(o)


# --- 5. Brief step -----------------------------------------------------------
def brief(c, t):
    W, H = 900, 300
    o = head(W, H, c, t["b_brief"])
    # request
    o.append(text(32, 44, t["b_req"].upper(), 11, c["ink2"], 600))
    o.append(text(32, 70, t["b_req_txt"], 17, c["ink"], 600))
    cw, gap, y0 = 276, 18, 96
    xs = [24 + i * (cw + gap) for i in range(3)]
    for i, x in enumerate(xs):
        o.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="160" rx="16" fill="{c["card"]}" stroke="{c["line"]}"/>')
        if i < 2:
            o.append(f'<line x1="{x + cw + 2}" y1="{y0 + 80}" x2="{x + cw + gap - 2}" y2="{y0 + 80}" stroke="{c["ink2"]}" stroke-width="2" marker-end="url(#a)"/>')
    # 1 look
    x = xs[0]
    o.append(text(x + 18, y0 + 30, t["b_look"], 14, c["ink"], 700))
    o.append(f'<rect x="{x + 18}" y="{y0 + 50}" width="{cw - 36}" height="34" rx="8" fill="{c["code"]}"/>')
    o.append(text(x + 30, y0 + 72, "grep password app/", 12, c["ink"], 400, family=MONO))
    o.append(text(x + 18, y0 + 112, t["b_look_txt"], 12.5, c["ink2"]))
    # 2 ask
    x = xs[1]
    o.append(text(x + 18, y0 + 30, t["b_ask"], 14 if len(t["b_ask"]) < 34 else 12.5, c["ink"], 700))
    o.append(text(x + 18, y0 + 58, t["b_q"], 13, c["ink2"], 600))
    for j, opt in enumerate(t["b_opts"]):
        yy = y0 + 72 + j * 38
        stroke = c["accent"] if j == 0 else c["line"]
        o.append(f'<rect x="{x + 18}" y="{yy}" width="{cw - 36}" height="30" rx="8" fill="{c["bg"]}" stroke="{stroke}" stroke-width="{2 if j == 0 else 1}"/>')
        o.append(text(x + 28, yy + 20, opt, 11.5, c["ink"], 600 if j == 0 else 400))
    # 3 brief
    x = xs[2]
    o.append(text(x + 18, y0 + 30, t["b_brief"], 13 if len(t["b_brief"]) < 40 else 12, c["ink"], 700))
    for j, (k, v) in enumerate(t["b_lines"]):
        yy = y0 + 54 + j * 27
        o.append(text(x + 18, yy, k, 10.5, c["accent"], 700, family=MONO))
        o.append(text(x + 18, yy + 13, v, 12, c["ink"]))
    o.append(text(32, 284, t["b_why"], 13, c["ink2"]))
    o.append("</svg>")
    return "\n".join(o)


# --- Extra strings for the plan / install visuals -------------------------------
T["en"].update(
    hero_title="Up to 60% cheaper", hero_sub="estimated maximum · API and usage-based Enterprise billing",
    m_title="Pay-as-you-go (API, usage-based Enterprise): lower bill",
    m_spend="Spend on Opus today", m_save="save up to", m_scale="saving",
    m_note="Estimate, not a guarantee: cautious {lo:.0f}% · upper end {hi:.0f}%. Official API prices of {d}. Measure yours: extras/measure.sh",
    p_title="Subscriptions: same price, up to {x:.1f}× more work before limits",
    p_today="today", p_with="with model-router (up to)", p_unit="× Pro usage",
    p_weekly="weekly", p_team="Team (Standard $25 · Premium $125 per seat): same up to {x:.1f}× per seat",
    p_note1="Assumes limits are used up in proportion to API price (Anthropic: “Opus costs several times more per turn than Sonnet”)",
    p_note2="and that you used Opus for everything. Already on Sonnet? From {a:.1f}× to {b:.1f}×: it can cost more if Opus is called often.",
    pc_title="On a computer", pc_win="Windows · PowerShell", pc_mac="macOS / Linux · Terminal", pc_cc="Inside Claude Code",
    pc_win_cmd="irm \nhttps://raw.githubusercontent.com/\ndimakushniriuk-art/\nclaude-code-model-router/main/\ninstall.ps1 | iex",
    pc_mac_cmd="curl -fsSL \nhttps://raw.githubusercontent.com/\ndimakushniriuk-art/\nclaude-code-model-router/main/\ninstall.sh | bash",
    pc_cc_cmd="/plugin marketplace add\n  dimakushniriuk-art/\n  claude-code-model-router\n/plugin install\n  model-router@model-router",
    pc_does="installs plugin + Sonnet + status line", pc_does_cc="then /model sonnet",
    pc_end="Restart Claude Code → type /agents → you see reader, coder, architect",
    ph_title="On a phone (Claude app → Code)",
    ph_1="Open Code and pick your repository", ph_2="Send this message", ph_3="Next sessions on that repo use the agents",
    ph_msg="Install model-router in this repo:\ngit clone --depth 1 https://github.com/\ndimakushniriuk-art/claude-code-model-router\n/tmp/mr && bash /tmp/mr/install.sh --project\nthen commit and push.",
    ph_3b="Then type /model sonnet in a session",
    ph_note="Why: plugins installed on a computer don't load in phone/web sessions (official docs). This puts the agents inside your repository instead.",
)
T["it"].update(
    hero_title="Fino al 60% in meno", hero_sub="massimo stimato · fatturazione API ed Enterprise a consumo",
    m_title="A consumo (API, Enterprise a consumo): conto più basso",
    m_spend="Spesa su Opus oggi", m_save="risparmi fino a", m_scale="risparmio",
    m_note="Stima, non garanzia: prudente {lo:.0f}% · massimo {hi:.0f}%. Prezzi API ufficiali del {d}. Misura il tuo: extras/measure.sh",
    p_title="Abbonamenti: stesso prezzo, fino a {x:.1f}× più lavoro prima dei limiti",
    p_today="oggi", p_with="con model-router (fino a)", p_unit="× uso Pro",
    p_weekly="settimanale", p_team="Team (Standard 25 $ · Premium 125 $ a posto): stesso fino a {x:.1f}× per posto",
    p_note1="Ipotesi: i limiti si consumano in proporzione al prezzo API (Anthropic: “Opus costa diverse volte più di Sonnet per turno”)",
    p_note2="e prima usavi Opus per tutto. Usi già Sonnet? Da {a:.1f}× a {b:.1f}×: può costare di più se Opus viene chiamato spesso.",
    pc_title="Dal computer", pc_win="Windows · PowerShell", pc_mac="macOS / Linux · Terminale", pc_cc="Dentro Claude Code",
    pc_win_cmd="irm \nhttps://raw.githubusercontent.com/\ndimakushniriuk-art/\nclaude-code-model-router/main/\ninstall.ps1 | iex",
    pc_mac_cmd="curl -fsSL \nhttps://raw.githubusercontent.com/\ndimakushniriuk-art/\nclaude-code-model-router/main/\ninstall.sh | bash",
    pc_cc_cmd="/plugin marketplace add\n  dimakushniriuk-art/\n  claude-code-model-router\n/plugin install\n  model-router@model-router",
    pc_does="installa plugin + Sonnet + status line", pc_does_cc="poi /model sonnet",
    pc_end="Riavvia Claude Code → scrivi /agents → vedi reader, coder, architect",
    ph_title="Dal cellulare (app Claude → Code)",
    ph_1="Apri Code e scegli il tuo repository", ph_2="Invia questo messaggio", ph_3="Le sessioni successive su quel repo usano gli agenti",
    ph_msg="Installa model-router in questo repo:\ngit clone --depth 1 https://github.com/\ndimakushniriuk-art/claude-code-model-router\n/tmp/mr && bash /tmp/mr/install.sh --project\npoi fai commit e push.",
    ph_3b="Poi scrivi /model sonnet in una sessione",
    ph_note="Perché: i plugin installati sul computer non si caricano nelle sessioni da cellulare/web (documentazione ufficiale). Così gli agenti stanno nel tuo repository.",
)


def _scen():
    sc = {n: (1 - est.routed_factor(s)) * 100 for n, s in est.SCENARIOS.items()}
    return sc["Conservative"], sc["Optimistic"]


# --- Money: pay-as-you-go ----------------------------------------------------
def money_chart(c, t):
    W, H = 900, 330
    o = head(W, H, c, t["hero_title"])
    lo, hi = _scen()
    o.append(text(32, 92, t["hero_title"], 52, c["accent"], 800))
    o.append(text(34, 122, t["hero_sub"], 14, c["ink2"]))
    o.append(text(32, 158, t["m_title"], 15, c["ink"], 700))
    # chips
    cw, gap = 276, 18
    for i, b in enumerate(est.BASELINES):
        x = 24 + i * (cw + gap)
        s = est.savings(b, est.SCENARIOS["Optimistic"])
        o.append(f'<rect x="{x}" y="176" width="{cw}" height="104" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>')
        o.append(text(x + 18, 202, t["m_spend"], 12.5, c["ink2"]))
        o.append(text(x + 18, 226, f'{est.money(b)}{t["per_month"]}', 20, c["ink"], 700))
        o.append(text(x + cw - 18, 202, t["m_save"], 12.5, c["ink2"], 400, "end"))
        o.append(text(x + cw - 18, 266, f'{est.money(s)}', 34, c["accent"], 800, "end"))
        # mini bar: pay vs save
        bx, bw = x + 18, 120
        pay = bw * (1 - hi / 100)
        o.append(f'<rect x="{bx}" y="252" width="{pay:.1f}" height="12" rx="6" fill="{c["muted"]}"/>')
        o.append(f'<rect x="{bx + pay + 2:.1f}" y="252" width="{bw - pay - 2:.1f}" height="12" rx="6" fill="{c["accent"]}"/>')
    o.append(text(32, 308, t["m_note"].format(lo=lo, hi=hi, d=est.PRICES_CHECKED), 12, c["ink2"]))
    o.append("</svg>")
    return "\n".join(o)


# --- Subscriptions -------------------------------------------------------------
def plans_chart(c, t):
    W, H = 900, 350
    xmax = est.work_multiplier(est.SCENARIOS["Optimistic"])
    a = est.sonnet_baseline_multiplier(est.SCENARIOS["Conservative"])
    b = est.sonnet_baseline_multiplier(est.SCENARIOS["Optimistic"])
    o = head(W, H, c, t["p_title"].format(x=xmax))
    o.append(text(32, 48, t["p_title"].format(x=xmax), 19, c["ink"], 700))
    # legend
    o.append(f'<rect x="32" y="64" width="14" height="12" rx="3" fill="{c["muted"]}"/>')
    o.append(text(52, 75, t["p_today"], 12.5, c["ink2"]))
    o.append(f'<rect x="120" y="64" width="14" height="12" rx="3" fill="{c["sonnet"]}"/>')
    o.append(text(140, 75, t["p_with"], 12.5, c["ink2"]))
    bx, bw = 200, 520
    top = max(u for _, _, u in est.PLANS) * xmax
    X = lambda v: bw * v / top
    for i, (name, price, units) in enumerate(est.PLANS):
        y = 100 + i * 58
        o.append(text(32, y + 18, name, 18, c["ink"], 700))
        o.append(text(32, y + 38, price + (f' · {t["p_weekly"]}' if name == "Ultra" else ""), 12.5, c["ink2"]))
        today, up = X(units), X(units * xmax)
        o.append(f'<rect x="{bx}" y="{y + 6}" width="{up:.1f}" height="28" rx="6" fill="{c["sonnet"]}"/>')
        o.append(f'<rect x="{bx}" y="{y + 6}" width="{today:.1f}" height="28" rx="6" fill="{c["muted"]}"/>')
        o.append(text(bx + up + 10, y + 26, f'{units}× → {units * xmax:.1f}×', 14, c["ink"], 600))
    o.append(text(32, 290, t["p_team"].format(x=xmax), 13, c["ink"], 600))
    o.append(text(32, 314, t["p_note1"], 11.5, c["ink2"]))
    o.append(text(32, 332, t["p_note2"].format(a=a, b=b), 11.5, c["ink2"]))
    o.append("</svg>")
    return "\n".join(o)


# --- Install: computer ------------------------------------------------------
def install_pc(c, t):
    W, H = 900, 350
    o = head(W, H, c, t["pc_title"])
    o.append(text(32, 44, t["pc_title"], 20, c["ink"], 700))
    cw, gap = 276, 18
    cards_ = [(t["pc_win"], t["pc_win_cmd"], t["pc_does"], c["haiku"]),
              (t["pc_mac"], t["pc_mac_cmd"], t["pc_does"], c["ink2"]),
              (t["pc_cc"], t["pc_cc_cmd"], t["pc_does_cc"], c["sonnet"])]
    for i, (title, cmd, does, col) in enumerate(cards_):
        x = 24 + i * (cw + gap)
        o.append(f'<rect x="{x}" y="62" width="{cw}" height="236" rx="16" fill="{c["card"]}" stroke="{c["line"]}"/>')
        o.append(f'<rect x="{x}" y="62" width="{cw}" height="6" rx="3" fill="{col}"/>')
        o.append(text(x + 18, 96, title, 15, c["ink"], 700))
        o.append(f'<rect x="{x + 14}" y="110" width="{cw - 28}" height="138" rx="10" fill="{c["code"]}"/>')
        for j, line in enumerate(cmd.split("\n")):
            o.append(text(x + 24, 132 + j * 24, line, 11, c["ink"], 400, family=MONO))
        o.append(f'<circle cx="{x + 24}" cy="273" r="5" fill="{c["sonnet"]}"/>')
        o.append(text(x + 36, 278, does, 12.5, c["ink2"]))
    o.append(f'<rect x="24" y="308" width="852" height="32" rx="10" fill="{c["card"]}" stroke="{c["sonnet"]}"/>')
    o.append(text(450, 329, t["pc_end"], 13.5, c["ink"], 600, "middle"))
    o.append("</svg>")
    return "\n".join(o)


# --- Install: phone -----------------------------------------------------------
def install_phone(c, t):
    W, H = 900, 400
    o = head(W, H, c, t["ph_title"])
    o.append(text(32, 44, t["ph_title"], 20, c["ink"], 700))
    # step column
    steps = [t["ph_1"], t["ph_2"], t["ph_3"]]
    for i, s in enumerate(steps):
        y = 92 + i * 78
        o.append(f'<circle cx="52" cy="{y}" r="18" fill="{c["sonnet"]}"/>')
        o.append(text(52, y + 6, str(i + 1), 16, "#ffffff", 700, "middle"))
        o.append(text(82, y + 6, s, 14.5, c["ink"], 600))
        if i < 2:
            o.append(f'<line x1="52" y1="{y + 22}" x2="52" y2="{y + 56}" stroke="{c["line"]}" stroke-width="2"/>')
    o.append(text(82, 92 + 2 * 78 + 26, t["ph_3b"], 12.5, c["ink2"]))
    # phone mockup
    px, py, pw, ph = 520, 58, 340, 320
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="28" fill="{c["card"]}" stroke="{c["line"]}" stroke-width="2"/>')
    o.append(f'<rect x="{px + pw / 2 - 30}" y="{py + 10}" width="60" height="6" rx="3" fill="{c["line"]}"/>')
    o.append(text(px + 20, py + 44, "Code · your-repo", 12, c["ink2"], 600))
    # chat bubble
    bx, by, bw2 = px + 20, py + 58, pw - 40
    lines = t["ph_msg"].split("\n")
    bh = 20 + len(lines) * 19
    o.append(f'<rect x="{bx}" y="{by}" width="{bw2}" height="{bh}" rx="14" fill="{c["code"]}" stroke="{c["sonnet"]}"/>')
    for j, line in enumerate(lines):
        o.append(text(bx + 12, by + 24 + j * 19, line, 10.5, c["ink"], 400, family=MONO))
    o.append(f'<rect x="{px + 20}" y="{py + ph - 48}" width="{pw - 40}" height="32" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>')
    o.append(f'<circle cx="{px + pw - 38}" cy="{py + ph - 32}" r="11" fill="{c["sonnet"]}"/>')
    o.append(f'<path d="M{px + pw - 43},{py + ph - 32} L{px + pw - 33},{py + ph - 32} M{px + pw - 37},{py + ph - 36} L{px + pw - 33},{py + ph - 32} L{px + pw - 37},{py + ph - 28}" stroke="#ffffff" stroke-width="2" fill="none"/>')
    # note
    words, line, out_lines = t["ph_note"].split(" "), "", []
    for w_ in words:
        if len(line) + len(w_) > 66:
            out_lines.append(line); line = w_
        else:
            line = (line + " " + w_).strip()
    out_lines.append(line)
    for j, l_ in enumerate(out_lines):
        o.append(text(32, 316 + j * 18, l_, 12, c["ink2"]))
    o.append("</svg>")
    return "\n".join(o)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, strings in T.items():
        for theme, colors in THEMES.items():
            for name, fn in (("flow", flow), ("agents", cards), ("brief", brief), ("money", money_chart),
                             ("plans", plans_chart), ("install-pc", install_pc), ("install-phone", install_phone)):
                (OUT / f"{name}-{lang}-{theme}.svg").write_text(fn(colors, strings), encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
