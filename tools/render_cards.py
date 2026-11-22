"""Рендер графики профиля: постеры флагманов, плитки студии, заголовки полок, схема агента.

    python tools/render_cards.py

Одна арт-система с hyperspace и терминалом: тёмная база #0d1117, один акцент (янтарь #d9a441),
Instrument Serif для заголовков, JetBrains Mono для меток. Скриншоты берутся из соседних репо
в ~/projects; выход: assets/shelf/*.webp и *.png.
"""
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT.parent
OUT = ROOT / "assets" / "shelf"
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", ink="#e6edf3", muted="#8b949e", line="#30363d", accent="#d9a441"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", ink="#1f2328", muted="#59636e", line="#d1d9e0", accent="#a86b0c"),
}
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
         '&family=JetBrains+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500&display=block" rel="stylesheet">')


def uri(p):
    return pathlib.Path(p).resolve().as_uri()


def base_css(t):
    return f"""
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{background:transparent;color:{t['ink']};font-family:'IBM Plex Sans',sans-serif;-webkit-font-smoothing:antialiased}}
    .card{{background:{t['bg']};overflow:hidden;position:relative}}
    .k{{font:600 15px/1 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:{t['accent']}}}
    .m{{font:400 15px/1.5 'JetBrains Mono',monospace;color:{t['muted']}}}
    .serif{{font-family:'Instrument Serif',serif;font-weight:400}}
    .tag{{display:inline-block;font:400 14px/1 'JetBrains Mono',monospace;color:{t['muted']};border:1px solid {t['line']};
          border-radius:4px;padding:7px 10px;margin:0 8px 8px 0}}
    """


# ---------- постер флагмана: 1600x760 ----------

def poster(t, kicker, title, big, caption, tags, art, num):
    tags_html = "".join(f'<span class="tag">{x}</span>' for x in tags)
    return f"""
    <div class="card" style="width:1600px;height:760px;border:1px solid {t['line']};border-radius:0">
      <div style="position:absolute;left:64px;top:60px;width:620px">
        <div class="k">{num} &nbsp;/&nbsp; {kicker}</div>
        <div class="serif" style="font-size:62px;line-height:1.02;margin-top:30px;letter-spacing:-.01em">{title}</div>
      </div>
      <div style="position:absolute;left:64px;bottom:150px;width:600px">
        <div class="serif" style="font-size:150px;line-height:.9;color:{t['accent']};letter-spacing:-.02em">{big}</div>
        <div class="m" style="font-size:17px;margin-top:18px;color:{t['ink']};opacity:.82">{caption}</div>
      </div>
      <div style="position:absolute;left:64px;bottom:44px;width:640px">{tags_html}</div>
      <div style="position:absolute;left:760px;top:60px;right:-2px;bottom:-2px;border:1px solid {t['line']};
                  border-radius:12px 0 0 0;overflow:hidden;background:{t['panel']}">{art}</div>
    </div>"""


def img_art(src, pos="left top", fit="cover", pad=0, bg=None):
    style = f"width:100%;height:100%;object-fit:{fit};object-position:{pos}"
    wrap = f"padding:{pad}px;width:100%;height:100%;" + (f"background:{bg};" if bg else "")
    return f'<div style="{wrap}"><img src="{uri(src)}" style="{style}"></div>'


def phones_art(t):
    shots = ["fill", "hunt", "combine", "choice"]
    imgs = "".join(
        f'<div style="flex:1;border:1px solid {t["line"]};border-radius:18px;overflow:hidden;height:{560 - (i % 2) * 40}px;'
        f'margin-top:{(i % 2) * 40}px"><img src="{uri(PROJ / "tutor-trainers/docs/shots" / (s + ".png"))}" '
        f'style="width:100%;height:100%;object-fit:cover;object-position:top"></div>'
        for i, s in enumerate(shots))
    return f'<div style="display:flex;gap:22px;padding:48px 48px 0 48px;height:100%">{imgs}</div>'


# ---------- плитка студии: 780x520 ----------

def tile(t, kicker, title, line, art):
    return f"""
    <div class="card" style="width:780px;height:520px;border:1px solid {t['line']};border-radius:0">
      <div style="position:absolute;inset:0 0 150px 0;overflow:hidden;border-bottom:1px solid {t['line']}">{art}</div>
      <div style="position:absolute;left:36px;right:36px;bottom:30px">
        <div class="k" style="font-size:13px">{kicker}</div>
        <div class="serif" style="font-size:44px;line-height:1;margin-top:12px">{title}</div>
        <div class="m" style="margin-top:10px;font-size:14px">{line}</div>
      </div>
    </div>"""


def brainrot_art(t):
    rows = ["BRAINROT-STRIKE  ·  2-8 players  ·  browser", "", "▸ slipper (auto-aim)      ▸ dumpling gun",
            "▸ aura blaster            ▸ trust-o-meter: ███████░░░", "",
            "streamer in your ear: «go left, trust me»", "chat: «DON'T»"]
    pre = "\n".join(rows)
    return (f'<pre style="font:500 19px/1.45 \'JetBrains Mono\',monospace;color:{t["accent"]};padding:34px 30px;'
            f'background:{t["panel"]};height:100%;white-space:pre">{pre}</pre>')


def vickrey_art(t):
    # числа из mechanism-design/vickrey/sim.py, 100 000 раундов, seed 7
    groups = [("rivals shade 20%", [11.63, 12.63, 12.19]), ("rivals honest", [7.41, 8.29, 7.59]),
              ("rivals overbid 20%", [5.12, 5.74, 4.96])]
    cols = []
    for name, vals in groups:
        bars = "".join(
            f'<div style="width:46px;height:{v / 13 * 210:.0f}px;background:{t["accent"] if i == 1 else t["line"]};'
            f'position:relative"><span style="position:absolute;top:-22px;left:0;right:0;text-align:center;'
            f'font:500 13px \'JetBrains Mono\';color:{t["ink"] if i == 1 else t["muted"]}">{v}</span></div>'
            for i, v in enumerate(vals))
        cols.append(f'<div style="text-align:center"><div style="display:flex;gap:6px;align-items:flex-end;height:240px">'
                    f'{bars}</div><div class="m" style="font-size:12px;margin-top:10px">{name}</div></div>')
    legend = (f'<div class="m" style="font-size:13px;position:absolute;top:24px;left:34px">'
              f'avg profit per round · <span style="color:{t["accent"]}">■ you bid honestly</span> · ■ you shade / overbid</div>')
    return (f'<div style="background:{t["panel"]};height:100%;position:relative;display:flex;gap:44px;'
            f'justify-content:center;align-items:flex-end;padding-bottom:26px">{legend}{"".join(cols)}</div>')


# ---------- заголовок полки: 1600x150, две темы ----------

def header(t, num, title, note):
    return f"""
    <div style="width:1600px;height:150px;position:relative;background:transparent">
      <div class="k" style="position:absolute;left:0;top:46px;font-size:18px">{num}</div>
      <div class="serif" style="position:absolute;left:70px;top:22px;font-size:76px;line-height:1">{title}</div>
      <div style="position:absolute;left:0;right:0;bottom:18px;height:1px;background:{t['line']}"></div>
      <div class="m" style="position:absolute;right:0;top:58px;font-size:17px;text-align:right">{note}</div>
    </div>"""


# ---------- схема агента: 1600x900, две темы ----------

def pipeline(t):
    def box(x, y, w, h, k, title, sub, hot=False):
        b = t['accent'] if hot else t['line']
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:1px solid {b};'
                f'border-radius:10px;background:{t["panel"]};padding:18px 20px">'
                f'<div class="k" style="font-size:15px">{k}</div>'
                f'<div class="serif" style="font-size:38px;line-height:1.05;margin-top:8px">{title}</div>'
                f'<div class="m" style="font-size:17px;margin-top:8px;line-height:1.4">{sub}</div></div>')

    def arrow(x1, y1, x2, y2, label="", dash=False):
        d = 'stroke-dasharray="6 6"' if dash else ""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        vert = x1 == x2
        lx, ly, anc = (mx + 12, my + 4, "start") if vert else (mx, my - 12, "middle")
        lab = (f'<text x="{lx}" y="{ly}" fill="{t["muted"]}" font-family="JetBrains Mono" font-size="17" '
               f'text-anchor="{anc}">{label}</text>') if label else ""
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["muted"]}" stroke-width="1.5" {d} '
                f'marker-end="url(#a)"/>{lab}')

    svg = f"""<svg width="1600" height="900" style="position:absolute;inset:0">
      <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="{t['muted']}"/></marker></defs>
      {arrow(270, 200, 352, 200, "")}
      {arrow(612, 200, 694, 200, "")}
      {arrow(954, 200, 1036, 200, "")}
      {arrow(1166, 280, 1166, 392, "spec")}
      {arrow(1036, 470, 954, 470, "diff")}
      {arrow(694, 470, 612, 470, "pass")}
      {arrow(482, 550, 482, 640, "accepted")}
      {arrow(612, 720, 694, 720, "")}
      {arrow(954, 720, 1036, 720, "weekly")}
      <path d="M1296 720 H1440 V200 H1302" fill="none" stroke="{t['accent']}" stroke-width="1.5" stroke-dasharray="6 6" marker-end="url(#a)"/>
      <text x="1452" y="470" fill="{t['accent']}" font-family="JetBrains Mono" font-size="17" transform="rotate(90 1452 470)" text-anchor="middle">next session starts warmer</text>
    </svg>"""
    nodes = "".join([
        box(40, 120, 230, 160, "you", "Course & goal", "what and why, the final call", True),
        box(352, 120, 260, 160, "hook", "Session start", "calendar, open loops, overdue sync"),
        box(694, 120, 260, 160, "router", "60-line index", "who, priority, pointers"),
        box(1036, 120, 260, 160, "hub", "Area hubs", "six areas of life, own state each"),
        box(1036, 392, 260, 160, "builders", "Code agents", "one codes to spec, one reads long files"),
        box(694, 392, 260, 160, "gate", "Acceptance", "red test or live API, never a report", True),
        box(352, 392, 260, 160, "lead", "Claude", "frames, specs, checks the run"),
        box(352, 640, 260, 160, "memory", "Checkpoint", "one line: where tomorrow starts"),
        box(694, 640, 260, 160, "sync", "Weekly sync", "checkpoints → hubs and timeline"),
        box(1036, 640, 260, 160, "ledger", "Dated decisions", "generated index, nothing re-argued"),
    ])
    title = (f'<div style="position:absolute;left:40px;top:34px"><span class="k" style="font-size:18px">how I build</span>'
             f'<span class="m" style="margin-left:18px;font-size:18px">plain files + hooks + three models, one human at the top</span></div>')
    return f'<div class="card" style="width:1600px;height:860px;background:{t["bg"]}">{svg}{title}{nodes}</div>'


def render(page, html, t, name, fmt="webp", transparent=False):
    tmp = OUT / "_render.html"
    tmp.write_text(f'<html><head><meta charset="utf-8">{FONTS}<style>{base_css(t)}</style></head><body>{html}</body></html>',
                   encoding="utf-8")
    page.goto(tmp.as_uri(), wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(400)
    el = page.locator("body > *").first
    png = OUT / f"{name}.png"
    el.screenshot(path=str(png), omit_background=transparent)
    if fmt == "webp":
        from PIL import Image
        Image.open(png).convert("RGB").save(OUT / f"{name}.webp", quality=86)
        png.unlink()
    tmp.unlink()
    print(name)


def main():
    d, l = THEMES["dark"], THEMES["light"]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1700, "height": 1000}, device_scale_factor=1)

        render(pg, poster(d, "product · bank hackathon · team captain",
                          "A credit agent that says what to fix, not just&nbsp;“no”", "N of M",
                          "bank conditions met, shown instead of an approval probability",
                          ["LLM workflow", "rule-based core", "golden exam 8/8", "3-vendor eval"],
                          img_art(PROJ / "alfa-credit-agent/docs/landing.png"), "01"), d, "p-alfa")
        render(pg, poster(d, "product · two real users",
                          "Homework trainers that learn from their own&nbsp;logs", "21 → 9",
                          "starts vs finishes: the log found the real bottleneck",
                          ["Telegram courier", "spaced repetition", "event log", "CI"],
                          phones_art(d), "02"), d, "p-trainers")
        render(pg, poster(d, "analytics · public data only",
                          "Forecasting the Bank of Russia key&nbsp;rate", "−16%",
                          "lower log loss than the market-implied baseline<br>83 meetings walk-forward · p&nbsp;=&nbsp;0.003",
                          ["1 739 hashed sources", "logit + LightGBM", "negative result kept"],
                          img_art(PROJ / "lampa/report/rate_forecast.png", "center", "contain", 34, "#ffffff"), "03"),
               d, "p-lampa")

        render(pg, tile(d, "design · generative art + auction", "ASSTRA · Nerven System",
                        "sealed bids, one clearing price for everyone",
                        img_art(PROJ / "alexregrets/assets/shelf/asstra.webp")), d, "t-asstra")
        render(pg, tile(d, "play · three.js, zero assets", "Omega Grand Prix",
                        "engine sound synthesised from firing order",
                        img_art(PROJ / "omega-gp/docs/shot.png", "center 70%")), d, "t-omega")
        render(pg, tile(d, "play · claude code mod", "hyperspace",
                        "a 3D rasterizer in terminal quarter-blocks",
                        img_art(PROJ / "alexregrets/assets/scene-falcon.webp", "center")), d, "t-hyperspace")
        render(pg, tile(d, "play · vibe-coding hackathon", "BRAINROT-STRIKE",
                        "browser multiplayer shooter · 24 of 32 commits mine", brainrot_art(d)), d, "t-brainrot")
        render(pg, tile(d, "study · mechanism design", "Why honest bidding wins",
                        "Vickrey auction, 100 000 simulated rounds", vickrey_art(d)), d, "t-vickrey")

        for name, t in THEMES.items():
            render(pg, header(t, "01", "Built &amp; shipped", "product and analytics, each with a case-study README"),
                   t, f"h-built-{name}", "png", True)
            render(pg, header(t, "02", "How I build", "an anonymised map of my agent setup"),
                   t, f"h-how-{name}", "png", True)
            render(pg, header(t, "03", "Learning in public", "theory first, then I build the thing"),
                   t, f"h-learn-{name}", "png", True)
            render(pg, header(t, "04", "Studio", "the creative side: art, games, toys"),
                   t, f"h-studio-{name}", "png", True)
            render(pg, pipeline(t), t, f"pipeline-{name}", "png")
        b.close()


if __name__ == "__main__":
    main()
