"""Генерит анимированные SVG профиля в assets/ (тёмная и светлая версии).

    python tools/gen_svg.py

Анимации только на CSS внутри SVG: GitHub отдаёт картинки через camo, JS там не живёт.
"""
import random
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


# ---------- баннер: Курно, агенты отвечают друг другу и сходятся к Нэшу ----------

def br1(y):  # q1 как ответ на q2: прямая (340,250) → (70,40)
    return 340 - 270 * (250 - y) / 210


def br2(x):  # q2 как ответ на q1: прямая (70,145) → (610,250)
    return 145 + 105 * (x - 70) / 540


def staircase(y0=56, steps=6):
    pts, y = [], y0
    x = br1(y)
    pts.append((x, y))
    for _ in range(steps):
        y = br2(x)
        pts.append((x, y))
        x = br1(y)
        pts.append((x, y))
    return pts


def cournot(t):
    pts = staircase()
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    # доля длины пути до каждой точки: точка загорается, когда до неё дошла линия
    seg = [abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in zip(pts, pts[1:])]
    total, run, node_css = sum(seg), 0.0, []
    for i in range(8):
        pct = 45 * run / total
        node_css.append(f".n{i} {{ animation-name: blink{i}; }}"
                        f"@keyframes blink{i} {{ 0%, {pct:.1f}% {{ opacity: 0; }} {pct + 2:.1f}%, 85% {{ opacity: .9; }} 100% {{ opacity: 0; }} }}")
        if i < len(seg):
            run += seg[i]
    nodes = "".join(
        f'<circle class="node n{i}" cx="{x:.1f}" cy="{y:.1f}" r="2.6"/>' for i, (x, y) in enumerate(pts[:8])
    )
    path_len = total + 20
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 300" width="760" height="300" role="img" aria-label="Cournot best-response diagram: two firms keep best-responding to each other and the path converges to the Nash equilibrium">
  <style>
    .ink    {{ stroke: {t["ink"]}; }}
    .muted  {{ stroke: {t["line"]}; }}
    .accent {{ stroke: {t["accent"]}; }}
    .t   {{ fill: {t["ink"]}; font-family: {MONO}; font-size: 13px; }}
    .tb  {{ fill: {t["ink"]}; font-family: {MONO}; font-size: 15px; font-weight: 600; }}
    .tm  {{ fill: {t["muted"]}; font-family: {MONO}; font-size: 12px; }}
    .ta  {{ fill: {t["accent"]}; font-family: {MONO}; font-size: 13px; }}
    .dot {{ fill: {t["accent"]}; }}

    .br {{ stroke-width: 1.6; fill: none; stroke-linecap: round;
          stroke-dasharray: 620; stroke-dashoffset: 620;
          animation: draw 1.5s cubic-bezier(.4,0,.2,1) forwards; }}
    .br2 {{ animation-delay: .35s; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}

    .path {{ fill: none; stroke: {t["accent2"]}; stroke-width: 1.3; stroke-linejoin: round;
            stroke-dasharray: {path_len:.0f}; stroke-dashoffset: {path_len:.0f};
            animation: walk 9s ease-in-out 1.9s infinite; }}
    @keyframes walk {{
      0%   {{ stroke-dashoffset: {path_len:.0f}; opacity: 1; }}
      45%  {{ stroke-dashoffset: 0;   opacity: 1; }}
      85%  {{ stroke-dashoffset: 0;   opacity: 1; }}
      100% {{ stroke-dashoffset: 0;   opacity: 0; }}
    }}
    .node {{ fill: {t["accent2"]}; opacity: 0; animation: blink0 9s linear 1.9s infinite; }}
    {" ".join(node_css)}

    .pop {{ opacity: 0; animation: pop .5s ease-out 1.7s forwards; }}
    @keyframes pop {{ to {{ opacity: 1; }} }}

    .pulse {{ animation: pulse 3.5s ease-in-out 2.2s infinite; }}
    @keyframes pulse {{ 0%,100% {{ r: 5; }} 50% {{ r: 7.5; }} }}

    {reduced_motion(
        ".br { animation: none; stroke-dashoffset: 0; }",
        ".path { animation: none; stroke-dashoffset: 0; }",
        ".node { animation: none; opacity: .9; }",
        ".pop { animation: none; opacity: 1; }",
        ".pulse { animation: none; }")}
  </style>

  <g class="muted pop" stroke-width="1" stroke-dasharray="3 4">
    <line x1="70" y1="180" x2="250" y2="180"/>
    <line x1="250" y1="250" x2="250" y2="180"/>
  </g>

  <g class="ink" stroke-width="1.4" stroke-linecap="round">
    <line x1="70" y1="250" x2="618" y2="250"/>
    <line x1="70" y1="250" x2="70" y2="34"/>
  </g>

  <line class="br accent" x1="340" y1="250" x2="70"  y2="40"/>
  <line class="br br2 accent" x1="70"  y1="145" x2="610" y2="250" opacity=".55"/>

  <path class="path" d="{path}"/>
  {nodes}

  <g class="pop">
    <circle class="dot pulse" cx="250" cy="180" r="5"/>
  </g>

  <text class="tm" x="60"  y="268" text-anchor="middle">0</text>
  <text class="t"  x="628" y="255">q₁</text>
  <text class="t"  x="62"  y="28"  text-anchor="middle">q₂</text>

  <text class="tm" x="352" y="222" transform="rotate(-38 352 222)">BR₁(q₂)</text>
  <text class="tm" x="470" y="228">BR₂(q₁)</text>

  <g class="pop">
    <text class="ta" x="264" y="172">Nash</text>
    <text class="tm" x="264" y="188">q* = (a − c) / 3b</text>
  </g>

  <text class="tb" x="440" y="70">Alexander Sotnik</text>
  <text class="tm" x="440" y="92">economics × agents</text>
  <text class="t"  x="440" y="128">two firms best-respond</text>
  <text class="t"  x="440" y="146">until nobody moves.</text>
  <text class="tm" x="440" y="172">swap the students for LLMs:</text>
  <text class="ta" x="440" y="190">Nash, collusion, or Berge?</text>
</svg>
'''


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


# ---------- hyperspace: звёзды в три слоя и истребитель ----------

def hyperspace(t):
    rnd = random.Random(7)
    layers = []
    for k, (n, r, op, dur) in enumerate([(26, .8, .35, 18), (16, 1.1, .6, 10), (8, 1.5, .9, 5)]):
        stars = "".join(
            f'<circle cx="{rnd.uniform(0, 380):.0f}" cy="{rnd.uniform(6, 114):.0f}" r="{r}"/>'
            for _ in range(n)
        )
        # два одинаковых куска подряд дают бесшовную прокрутку
        layers.append(
            f'<g class="s{k}" opacity="{op}"><g>{stars}</g><g transform="translate(380 0)">{stars}</g></g>'
        )
        layers.append(f".s{k} {{ animation: drift {dur}s linear infinite; }}")
    groups = "".join(x for x in layers if x.startswith("<g"))
    css = " ".join(x for x in layers if x.startswith("."))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 120" width="380" height="120" role="img" aria-label="An X-wing flies through a parallax starfield and fires laser volleys">
  <style>
    .bg {{ fill: {t["panel"]}; stroke: {t["line"]}; }}
    .stars circle {{ fill: {t["ink"]}; }}
    @keyframes drift {{ to {{ transform: translateX(-380px); }} }}
    {css}
    .hull {{ fill: {t["ink"]}; }}
    .cockpit {{ fill: {t["accent2"]}; }}
    .engine {{ fill: #ff8a3d; animation: glow .4s ease-in-out infinite alternate; }}
    @keyframes glow {{ to {{ opacity: .45; }} }}
    .bob {{ animation: bob 3s ease-in-out infinite; }}
    @keyframes bob {{ 50% {{ transform: translateY(-4px); }} }}
    .laser {{ stroke: #ff4d4d; stroke-width: 2; stroke-linecap: round; opacity: 0;
             animation: shoot 2.4s linear infinite; }}
    .l2 {{ animation-delay: .18s; }}
    @keyframes shoot {{
      0%   {{ transform: translateX(0);     opacity: 1; }}
      30%  {{ transform: translateX(220px); opacity: 1; }}
      31%, 100% {{ opacity: 0; }}
    }}
    .cap {{ font-family: {MONO}; font-size: 10px; fill: {t["muted"]}; }}
    {reduced_motion("g[class^=s], .bob, .engine { animation: none; }", ".laser { animation: none; }")}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="379" height="119" rx="8"/>
  <svg x="1" y="1" width="378" height="118" viewBox="0 0 378 118"><g class="stars">{groups}</g></svg>
  <g class="bob">
    <g class="hull">
      <path d="M24 58 L44 52 L118 55 L136 60 L118 65 L44 68 L24 62 Z"/>
      <path class="cockpit" d="M66 55 L84 53.5 L92 56 L66 57 Z"/>
      <path d="M40 54 L58 34 L66 34 L58 54 Z"/>
      <path d="M40 66 L58 86 L66 86 L58 66 Z"/>
      <rect x="58" y="32" width="84" height="3" rx="1.5"/>
      <rect x="58" y="85" width="84" height="3" rx="1.5"/>
      <rect x="18" y="55" width="8" height="10" rx="2" class="engine"/>
    </g>
    <line class="laser"    x1="144" y1="33.5" x2="164" y2="33.5"/>
    <line class="laser l2" x1="144" y1="86.5" x2="164" y2="86.5"/>
  </g>
  <text class="cap" x="14" y="108">✧ Calculating the jump to hyperspace… (12s)</text>
</svg>
'''


if __name__ == "__main__":
    for name, fn in [("cournot", cournot), ("terminal", terminal), ("hyperspace", hyperspace)]:
        for theme, tokens in THEMES.items():
            out = ASSETS / f"{name}-{theme}.svg"
            out.write_text(fn(tokens), encoding="utf-8")
            print(out.name)
