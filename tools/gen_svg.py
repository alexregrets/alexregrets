"""Генерит анимированные SVG профиля в assets/ (тёмная и светлая версии).

    python tools/gen_svg.py

Анимации только на CSS внутри SVG: GitHub отдаёт картинки через camo, JS там не живёт.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", ink="#e6edf3", muted="#8b949e",
                 line="#30363d", accent="#d9a441", accent2="#58a6ff"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", ink="#1f2328", muted="#59636e",
                  line="#d1d9e0", accent="#b7791f", accent2="#0969da"),
}


def reduced_motion(*rules):
    return "@media (prefers-reduced-motion: reduce) { " + " ".join(rules) + " }"


# ---------- терминал: печатает строки по очереди ----------

LINES = [
    ("cmd", "whoami"),
    ("out", "alexander sotnik · economics, Financial University '28"),
    ("cmd", "cat direction.txt"),
    ("out", "incentive design for agentic economies, measured causally"),
    ("cmd", "ls now/"),
    ("hi",  "cournot-x-llm-agents/   hh-agent/   claude-code-mods/"),
]
CHAR = 7.83   # ширина символа 13px моноширинного, с запасом
CPS = 34      # символов в секунду


def terminal(t):
    top, lh, x0 = 58, 24, 28
    rows, styles, at = [], [], 0.6
    for i, (kind, text) in enumerate(LINES):
        y = top + i * lh
        shown = ("$ " + text) if kind == "cmd" else text
        n = len(shown)
        dur = n / CPS if kind == "cmd" else 0.35
        steps = n if kind == "cmd" else 1
        cls = {"cmd": "tc", "out": "to", "hi": "th"}[kind]
        rows.append(
            f'<text class="{cls}" x="{x0}" y="{y}">'
            + (f'<tspan class="p">$</tspan> {text}' if kind == "cmd" else text)
            + "</text>"
            + f'<rect class="cv c{i}" x="{x0 - 2}" y="{y - 15}" width="{n * CHAR + 12:.0f}" height="21"/>'
        )
        styles.append(
            f".c{i} {{ animation: type{i} {dur:.2f}s steps({steps}, end) {at:.2f}s forwards; }}"
            f"@keyframes type{i} {{ to {{ transform: translateX({n * CHAR + 12:.0f}px); }} }}"
        )
        at += dur + (0.35 if kind == "cmd" else 0.55)
    cy = top + len(LINES) * lh
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 236" width="760" height="236" role="img" aria-label="Terminal: whoami prints Alexander Sotnik, economics at Financial University, class of 2028; direction: incentive design for agentic economies, measured causally; now: Cournot with LLM agents, hh-agent, Claude Code mods">
  <style>
    .win {{ fill: {t["panel"]}; stroke: {t["line"]}; }}
    .bar {{ fill: {t["bg"]}; }}
    .tc, .to, .th, .tt {{ font-family: {MONO}; font-size: 13px; white-space: pre; }}
    .tc {{ fill: {t["ink"]}; }}
    .p  {{ fill: {t["accent"]}; }}
    .to {{ fill: {t["muted"]}; }}
    .th {{ fill: {t["accent2"]}; }}
    .tt {{ fill: {t["muted"]}; font-size: 12px; }}
    .cv {{ fill: {t["panel"]}; }}
    .cur {{ fill: {t["accent"]}; opacity: 0; animation: on 0s {at:.2f}s forwards, cur 1.05s steps(1) {at:.2f}s infinite; }}
    @keyframes on {{ to {{ opacity: 1; }} }}
    @keyframes cur {{ 50% {{ opacity: 0; }} }}
    {" ".join(styles)}
    {reduced_motion(".cv { display: none; }", ".cur { animation: none; opacity: 1; }")}
  </style>
  <rect class="win" x="0.5" y="0.5" width="759" height="235" rx="10"/>
  <path class="bar" d="M1 11 a10 10 0 0 1 10 -10 h738 a10 10 0 0 1 10 10 v19 h-758z"/>
  <circle cx="20" cy="16" r="5" fill="#ff5f57"/>
  <circle cx="38" cy="16" r="5" fill="#febc2e"/>
  <circle cx="56" cy="16" r="5" fill="#28c840"/>
  <text class="tt" x="380" y="20" text-anchor="middle">~/alexregrets</text>
  <clipPath id="screen"><rect x="1" y="31" width="758" height="204"/></clipPath>
  <g clip-path="url(#screen)">{"".join(rows)}</g>
  <text class="tc" x="{x0}" y="{cy}"><tspan class="p">$</tspan></text>
  <rect class="cur" x="{x0 + 2 * CHAR:.0f}" y="{cy - 13}" width="8" height="16"/>
</svg>
'''


if __name__ == "__main__":
    for name, fn in [("terminal", terminal)]:
        for theme, tokens in THEMES.items():
            out = ASSETS / f"{name}-{theme}.svg"
            out.write_text(fn(tokens), encoding="utf-8")
            print(out.name)
