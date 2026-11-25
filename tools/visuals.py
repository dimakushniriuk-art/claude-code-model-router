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
        you="You", one_chat="one chat, as usual",
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
    ),
    "it": dict(
        you="Tu", one_chat="una sola chat, come sempre",
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
    o.append(f'<rect x="20" y="150" width="200" height="100" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>')
    o.append(text(120, 192, t["you"], 22, c["ink"], 700, "middle"))
    o.append(text(120, 218, t["one_chat"], 12.5, c["ink2"], 400, "middle"))
    o.append(f'<line x1="222" y1="200" x2="262" y2="200" stroke="{c["ink2"]}" stroke-width="2" marker-end="url(#a)"/>')
    # main
    o.append(f'<rect x="266" y="130" width="230" height="140" rx="14" fill="{c["card"]}" stroke="{c["sonnet"]}" stroke-width="2"/>')
    o.append(text(381, 172, t["main"], 18, c["ink"], 700, "middle"))
    o.append(pill(341, 186, 80, 26, c["sonnet"]))
    o.append(text(381, 204, t["main_m"], 14, "#ffffff", 600, "middle"))
    o.append(text(381, 240, t["policy"], 13, c["ink2"], 400, "middle"))
    # small step loop
    o.append(f'<path d="M330,272 C330,330 432,330 432,272" fill="none" stroke="{c["ink2"]}" stroke-width="2" '
             f'stroke-dasharray="5 4" marker-end="url(#a)"/>')
    o.append(text(381, 352, t["small"], 13, c["ink2"], 400, "middle"))
    # agents
    rows = [("reader", "Haiku", "haiku", t["reader_do"], 50),
            ("coder", "Sonnet", "sonnet", t["coder_do"], 160),
            ("architect", "Opus", "opus", t["arch_do"], 270)]
    for name, model, key, does, y in rows:
        o.append(f'<path d="M498,200 C560,200 560,{y + 40} 618,{y + 40}" fill="none" stroke="{c[key]}" '
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, strings in T.items():
        for theme, colors in THEMES.items():
            for name, fn in (("flow", flow), ("agents", cards), ("install", install), ("savings", savings)):
                (OUT / f"{name}-{lang}-{theme}.svg").write_text(fn(colors, strings), encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
