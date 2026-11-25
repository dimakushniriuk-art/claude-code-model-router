#!/usr/bin/env python3
"""Estimate monthly savings from model routing and draw the README chart.

This is a MODEL, not a measurement. Every number below is an assumption you can
edit. Measure your own workload with extras/measure.sh.

Usage:
    python3 tools/estimate.py            # print the table, rewrite docs/*.svg
    python3 tools/estimate.py 250        # also print the estimate for $250/month
"""
import sys
from pathlib import Path

# --- Official API prices, USD per million tokens -----------------------------
# Source: https://platform.claude.com/docs/en/about-claude/pricing (checked 2026-11-25)
PRICES_CHECKED = "2026-11-25"
PRICES = {  # input, 5m cache write, cache read, output
    "opus":   {"input": 4.00, "cache_write": 5.00,  "cache_read": 0.20, "output": 20.00},  # Opus 5.5
    "sonnet": {"input": 2.00, "cache_write": 2.50,  "cache_read": 0.10, "output": 10.00},  # Sonnet 5.5
    "haiku":  {"input": 0.10, "cache_write": 0.125, "cache_read": 0.01, "output": 0.50},   # Haiku 5.5, prompts <=100K
}

# --- Assumption 1: token mix of an agentic coding session --------------------
# Share of all tokens by category. Agentic sessions re-send context, so cache
# reads dominate. Edit to match your /usage numbers.
TOKEN_MIX = {"cache_read": 0.85, "cache_write": 0.05, "input": 0.03, "output": 0.07}


def blended(model: str) -> float:
    """USD per million tokens of the mix above."""
    return sum(PRICES[model][k] * share for k, share in TOKEN_MIX.items())


REL = {m: blended(m) / blended("opus") for m in PRICES}  # cost relative to Opus

# --- Assumption 2: who does the work, and delegation overhead ----------------
# Baseline = everything on Opus (main session and any subagents).
# Shares are of the baseline's tokens. Overhead = extra tokens from subagent
# cold starts, briefs and summaries (the smaller main context it buys is ignored,
# which makes these estimates conservative on that side).
SCENARIOS = {
    "Conservative": {"sonnet": 0.60, "haiku": 0.10, "opus": 0.30, "overhead": 0.25},
    "Expected":     {"sonnet": 0.60, "haiku": 0.25, "opus": 0.15, "overhead": 0.15},
    "Optimistic":   {"sonnet": 0.60, "haiku": 0.35, "opus": 0.05, "overhead": 0.10},
}
# Plugin installed but main session left on Opus: only reading moves to Haiku.
OPUS_MAIN = {"opus": 0.75, "haiku": 0.25, "overhead": 0.15}

BASELINES = [100, 300, 1000]  # monthly spend on Opus, USD (API-equivalent)


def routed_factor(s: dict) -> float:
    work = sum(REL[m] * s.get(m, 0) for m in PRICES)
    return work * (1 + s["overhead"])


def savings(spend: float, s: dict) -> float:
    return spend * (1 - routed_factor(s))


# --- Chart (dependency-free SVG, light + dark) --------------------------------
THEMES = {
    "light": {"bg": "#ffffff", "ink": "#191919", "ink2": "#666666", "grid": "#e5e5e5",
              "series": ["#257de0", "#f47230", "#00b894"]},
    "dark":  {"bg": "#191919", "ink": "#efefef", "ink2": "#9c9c9c", "grid": "#333333",
              "series": ["#338ced", "#e76624", "#00a888"]},
}


def money(v: float) -> str:
    return f"${v:,.0f}"


def svg(theme: str) -> str:
    t = THEMES[theme]
    W, H = 760, 420
    L, R, T, B = 70, 20, 96, 56
    pw, ph = W - L - R, H - T - B
    names = list(SCENARIOS)
    vals = [[savings(b, SCENARIOS[n]) for n in names] for b in BASELINES]
    ymax = 700  # fixed nice max covering the optimistic $1,000 case
    y = lambda v: T + ph - v / ymax * ph
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" role="img" '
           f'aria-label="Estimated monthly savings with model-router">',
           f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
           f'<text x="{L}" y="30" font-size="18" font-weight="600" fill="{t["ink"]}">Estimated monthly savings</text>',
           f'<text x="{L}" y="52" font-size="13" fill="{t["ink2"]}">Main session on Sonnet + plugin vs. everything on Opus. '
           f'An estimate, not a measurement.</text>']
    # legend
    lx = L
    for i, n in enumerate(names):
        pct = (1 - routed_factor(SCENARIOS[n])) * 100
        label = f"{n} (−{pct:.0f}%)"
        out.append(f'<rect x="{lx}" y="68" width="12" height="12" rx="3" fill="{t["series"][i]}"/>')
        out.append(f'<text x="{lx + 18}" y="78.5" font-size="13" fill="{t["ink2"]}">{label}</text>')
        lx += 18 + len(label) * 7.4 + 22
    # grid + y axis
    for v in range(0, ymax + 1, 100):
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{t["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{L - 8}" y="{y(v) + 4:.1f}" font-size="12" text-anchor="end" fill="{t["ink2"]}">{money(v)}</text>')
    # bars
    gw = pw / len(BASELINES)
    bw, gap = 46, 2
    for gi, b in enumerate(BASELINES):
        cx = L + gw * gi + gw / 2
        x0 = cx - (bw * 3 + gap * 2) / 2
        for si, v in enumerate(vals[gi]):
            x = x0 + si * (bw + gap)
            top, h = y(v), y(0) - y(v)
            r = 4
            path = (f'M{x:.1f},{y(0):.1f} V{top + r:.1f} Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f} '
                    f'H{x + bw - r:.1f} Q{x + bw:.1f},{top:.1f} {x + bw:.1f},{top + r:.1f} V{y(0):.1f} Z')
            out.append(f'<path d="{path}" fill="{t["series"][si]}"><title>{names[si]}: save {money(v)}/month '
                       f'of {money(b)} (pay {money(b - v)})</title></path>')
            out.append(f'<text x="{x + bw / 2:.1f}" y="{top - 6:.1f}" font-size="12" text-anchor="middle" '
                       f'fill="{t["ink"]}">{money(v)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{y(0) + 22:.1f}" font-size="13" text-anchor="middle" fill="{t["ink"]}">'
                   f'{money(b)}/month on Opus</text>')
    out.append(f'<line x1="{L}" x2="{W - R}" y1="{y(0):.1f}" y2="{y(0):.1f}" stroke="{t["ink2"]}" stroke-width="1"/>')
    out.append(f'<text x="{L}" y="{H - 10}" font-size="11" fill="{t["ink2"]}">Assumptions and formula: tools/estimate.py. '
               f'API prices of {PRICES_CHECKED}. Measure your own work with extras/measure.sh.</text>')
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    print(f"Relative cost vs Opus for the assumed token mix: "
          + ", ".join(f"{m} {REL[m]:.3f}" for m in PRICES))
    print("\n| Scenario | Savings | " + " | ".join(f"{money(b)}/mo" for b in BASELINES) + " |")
    print("|---|---|" + "---|" * len(BASELINES))
    for n, s in list(SCENARIOS.items()) + [("Opus main + plugin", OPUS_MAIN)]:
        pct = (1 - routed_factor(s)) * 100
        print(f"| {n} | {pct:.0f}% | " + " | ".join(money(savings(b, s)) for b in BASELINES) + " |")
    if len(sys.argv) > 1:
        b = float(sys.argv[1])
        print(f"\nFor {money(b)}/month: " + ", ".join(f"{n} {money(savings(b, s))}" for n, s in SCENARIOS.items()))
    docs = Path(__file__).resolve().parent.parent / "docs"
    docs.mkdir(exist_ok=True)
    for theme in THEMES:
        (docs / f"savings-{theme}.svg").write_text(svg(theme), encoding="utf-8")


if __name__ == "__main__":
    main()
