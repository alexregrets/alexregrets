"""Графика профиля и README флагманов: постеры, плитки, заголовки полок, схема агента, полосы цифр.

    python tools/render_cards.py            # всё: профиль + docs/brand/ в репо флагманов

Система v3 (22.11): одна гарнитура Manrope, синий акцент, две темы под <picture>.
Перед рендером аудит падает, если пара цвет/фон ниже WCAG (4.5 текст) или кегль меньше MIN_PX:
GitHub ужимает картинку 1600 px до ~888, то есть в 0.555 раза.
"""
import pathlib
import re
import shutil

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT.parent
OUT = ROOT / "assets" / "shelf"
OUT.mkdir(parents=True, exist_ok=True)

SCALE = 888 / 1600          # ширина колонки README на github.com / ширина исходника
MIN_PX = 24                 # 24 * 0.555 ≈ 13.3 px на экране
MIN_PX_TILE = 26            # плитки стоят по две в ряд: 780 → ~420 px

THEMES = {
    "light": dict(paper="#f4f6fb", surface="#ffffff", ink="#0e1a2f", muted="#4a5770", line="#d5dcea",
                  accent="#1c54f4", accent_soft="#e3ebff"),
    "dark": dict(paper="#0b1324", surface="#121d33", ink="#eaf0fb", muted="#a3b1cb", line="#26344f",
                 accent="#7aa5ff", accent_soft="#17284a"),
}
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800'
         '&display=block" rel="stylesheet">')


# ---------- аудит ----------

def _lum(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def audit_colors():
    """Каждая пара текст/фон из системы: печать и падение ниже порога."""
    bad = []
    for name, t in THEMES.items():
        for fg, bg, need in [("ink", "paper", 7), ("muted", "paper", 4.5), ("muted", "surface", 4.5),
                             ("accent", "paper", 4.5), ("accent", "surface", 4.5), ("ink", "accent_soft", 4.5)]:
            r = contrast(t[fg], t[bg])
            print(f"  {name:5} {fg:6} на {bg:11} {r:5.2f}  {'ok' if r >= need else 'FAIL'} (нужно {need})")
            if r < need:
                bad.append((name, fg, bg, r))
    assert not bad, bad


def audit_sizes(html, name, min_px):
    sizes = [int(x) for x in re.findall(r"font-size:\s*(\d+)px", html)]
    small = [s for s in sizes if s < min_px]
    assert not small, f"{name}: кегль {small} меньше {min_px}px (на экране {min(small) * SCALE:.1f}px)"


# ---------- общий CSS ----------

def css(t):
    return f"""
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{background:transparent;color:{t['ink']};font-family:'Manrope',sans-serif;
         -webkit-font-smoothing:antialiased;font-feature-settings:'tnum' 1}}
    .card{{background:{t['paper']};border:2px solid {t['line']};border-radius:24px;overflow:hidden;position:relative}}
    .kick{{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{t['accent']}}}
    .muted{{color:{t['muted']}}}
    .tag{{display:inline-block;font-weight:600;color:{t['ink']};background:{t['accent_soft']};
          border-radius:999px;padding:10px 20px;margin:0 12px 12px 0}}
    """


def uri(p):
    return pathlib.Path(p).resolve().as_uri()


def shot(src, pos="left top", fit="cover", bg=None, pad=0):
    return (f'<div style="width:100%;height:100%;padding:{pad}px;{f"background:{bg};" if bg else ""}">'
            f'<img src="{uri(src)}" style="width:100%;height:100%;object-fit:{fit};object-position:{pos};display:block"></div>')


# ---------- постер флагмана 1600x800 ----------

def poster(t, kicker, title, big, caption, tags, art):
    tags_html = "".join(f'<span class="tag" style="font-size:24px">{x}</span>' for x in tags)
    return f"""
    <div class="card" style="width:1600px;height:800px">
      <div style="position:absolute;left:80px;top:72px;bottom:60px;width:620px;display:flex;flex-direction:column">
        <div class="kick" style="font-size:24px">{kicker}</div>
        <div style="font-size:56px;font-weight:700;line-height:1.08;letter-spacing:-.02em;margin-top:24px">{title}</div>
        <div style="margin-top:auto;font-size:136px;font-weight:800;line-height:1;letter-spacing:-.04em;color:{t['accent']}">{big}</div>
        <div class="muted" style="font-size:28px;line-height:1.35;margin-top:16px;font-weight:500">{caption}</div>
        <div style="margin-top:32px">{tags_html}</div>
      </div>
      <div style="position:absolute;left:776px;top:72px;right:72px;bottom:72px;border-radius:16px;overflow:hidden;
                  border:2px solid {t['line']};background:{t['surface']}">{art}</div>
    </div>"""


def phones(t):
    names = ["fill", "hunt", "combine", "choice"]
    cells = "".join(
        f'<div style="flex:1;border-radius:14px;overflow:hidden;border:2px solid {t["line"]};margin-top:{(i % 2) * 36}px;'
        f'height:{560 - (i % 2) * 36}px"><img src="{uri(PROJ / "tutor-trainers/docs/shots" / (n + ".png"))}" '
        f'style="width:100%;height:100%;object-fit:cover;object-position:top"></div>' for i, n in enumerate(names))
    return f'<div style="display:flex;gap:20px;padding:40px 40px 0">{cells}</div>'


# ---------- плитка 780x560 ----------

def tile(t, kicker, title, line, art):
    return f"""
    <div class="card" style="width:780px;height:560px">
      <div style="position:absolute;left:0;right:0;top:0;height:330px;overflow:hidden;border-bottom:2px solid {t['line']};
                  background:{t['surface']}">{art}</div>
      <div style="position:absolute;left:48px;right:48px;top:362px">
        <div class="kick" style="font-size:26px">{kicker}</div>
        <div style="font-size:48px;font-weight:700;letter-spacing:-.02em;line-height:1.1;margin-top:10px">{title}</div>
        <div class="muted" style="font-size:28px;margin-top:10px;font-weight:500;line-height:1.3">{line}</div>
      </div>
    </div>"""


def brainrot_art(t):
    rows = [("BRAINROT-STRIKE", t["ink"]), ("2–8 players · browser · no install", t["muted"]), ("", ""),
            ("slipper with auto-aim · dumpling gun", t["ink"]), ("a streamer in your ear: “go left, trust me”", t["accent"])]
    body = "".join(f'<div style="font-size:30px;font-weight:{800 if i == 0 else 600};color:{c};margin-top:{6 if i else 0}px">'
                   f'{s or "&nbsp;"}</div>' for i, (s, c) in enumerate(rows))
    return f'<div style="padding:48px">{body}</div>'


def vickrey_art(t):
    # mechanism-design/vickrey/sim.py: 100 000 раундов, seed 7; средняя прибыль за раунд
    groups = [("rivals shade", [11.63, 12.63, 12.19]), ("rivals honest", [7.41, 8.29, 7.59]),
              ("rivals overbid", [5.12, 5.74, 4.96])]
    cols = ""
    for name, vals in groups:
        bars = "".join(
            f'<div style="width:52px;height:{v / 13 * 190:.0f}px;border-radius:6px 6px 0 0;'
            f'background:{t["accent"] if i == 1 else t["line"]}"></div>' for i, v in enumerate(vals))
        cols += (f'<div style="text-align:center"><div style="font-size:26px;font-weight:800;color:{t["accent"]}">{vals[1]}</div>'
                 f'<div style="display:flex;gap:6px;align-items:flex-end;height:200px;margin-top:6px">{bars}</div>'
                 f'<div class="muted" style="font-size:26px;margin-top:10px;font-weight:600">{name}</div></div>')
    return f'<div style="display:flex;justify-content:center;gap:56px;padding-top:34px">{cols}</div>'


# ---------- заголовок полки 1600x170 ----------

def header(t, num, title, note):
    return f"""
    <div style="width:1600px;height:170px;position:relative">
      <div style="position:absolute;left:0;top:34px;display:flex;align-items:baseline;gap:28px">
        <span style="font-size:40px;font-weight:800;color:{t['accent']}">{num}</span>
        <span style="font-size:80px;font-weight:800;letter-spacing:-.03em;line-height:1">{title}</span>
      </div>
      <div class="muted" style="position:absolute;right:0;top:66px;font-size:30px;font-weight:600">{note}</div>
      <div style="position:absolute;left:0;right:0;bottom:12px;height:3px;background:{t['line']}"></div>
    </div>"""


# ---------- схема агента 1600x1160 ----------

def pipeline(t):
    W, H = 316, 224
    X = [40, 434, 828, 1222]
    Y = [150, 490, 830]

    def box(c, r, k, title, sub, hot=False):
        return (f'<div style="position:absolute;left:{X[c]}px;top:{Y[r]}px;width:{W}px;height:{H}px;border-radius:18px;'
                f'border:2px solid {t["accent"] if hot else t["line"]};'
                f'background:{t["accent_soft"] if hot else t["surface"]};padding:26px 28px">'
                f'<div class="kick" style="font-size:24px">{k}</div>'
                f'<div style="font-size:40px;font-weight:800;letter-spacing:-.02em;line-height:1.1;margin-top:10px">{title}</div>'
                f'<div class="muted" style="font-size:26px;font-weight:600;line-height:1.3;margin-top:10px">{sub}</div></div>')

    def arrow(x1, y1, x2, y2, label=""):
        lab = ""
        if label:
            if x1 == x2:
                lab = f'<text x="{x1 + 16}" y="{(y1 + y2) / 2 + 9}" class="al">{label}</text>'
            else:
                lab = f'<text x="{(x1 + x2) / 2}" y="{y1 - 16}" text-anchor="middle" class="al">{label}</text>'
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["muted"]}" stroke-width="3" marker-end="url(#a)"/>{lab}'

    cy = [y + H / 2 for y in Y]
    cx = [x + W / 2 for x in X]
    svg = f"""<svg width="1600" height="1160" style="position:absolute;inset:0">
      <style>.al{{font:600 24px Manrope;fill:{t['muted']}}}</style>
      <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="{t['muted']}"/></marker></defs>
      {arrow(X[0] + W, cy[0], X[1] - 4, cy[0])}{arrow(X[1] + W, cy[0], X[2] - 4, cy[0])}{arrow(X[2] + W, cy[0], X[3] - 4, cy[0])}
      {arrow(cx[3], Y[0] + H, cx[3], Y[1] - 4, "spec")}
      {arrow(X[3], cy[1], X[2] + W + 4, cy[1], "diff")}{arrow(X[2], cy[1], X[1] + W + 4, cy[1], "pass")}
      {arrow(cx[1], Y[1] + H, cx[1], Y[2] - 4, "accepted")}
      {arrow(X[1] + W, cy[2], X[2] - 4, cy[2])}{arrow(X[2] + W, cy[2], X[3] - 4, cy[2])}
      <path d="M{X[3] + W / 2} {Y[2] + H} V{Y[2] + H + 40} H{X[0] + W / 2} V{Y[0] + H + 4}" fill="none"
            stroke="{t['accent']}" stroke-width="3" stroke-dasharray="10 10" marker-end="url(#a)"/>
      <text x="{X[0] + W / 2 + 18}" y="{Y[2] + H + 32}" class="al" style="fill:{t['accent']}">the next session starts from here</text>
    </svg>"""
    nodes = "".join([
        box(0, 0, "you", "Course", "what, why, the final call", True),
        box(1, 0, "hook", "Session start", "calendar, open loops"),
        box(2, 0, "router", "60-line index", "who, priority, pointers"),
        box(3, 0, "hubs", "Areas of life", "six areas, own state"),
        box(3, 1, "builders", "Code agents", "code to spec, long reads"),
        box(2, 1, "gate", "Acceptance", "a red test, not a report", True),
        box(1, 1, "lead", "Claude", "frames, specs, checks"),
        box(1, 2, "memory", "Checkpoint", "where tomorrow starts"),
        box(2, 2, "sync", "Weekly sync", "checkpoints → hubs"),
        box(3, 2, "ledger", "Decisions", "dated, never re-argued"),
    ])
    title = (f'<div style="position:absolute;left:40px;top:48px;font-size:30px;font-weight:600" class="muted">'
             f'Plain files, a few hooks, three models. One human sets the course.</div>')
    return f'<div class="card" style="width:1600px;height:1160px">{svg}{title}{nodes}</div>'


# ---------- полоса цифр 1600x250 (README репо, по-русски) ----------

def stats(t, items):
    cells = "".join(
        f'<div style="flex:1;padding:0 36px;{"border-left:2px solid " + t["line"] if i else ""}">'
        f'<div style="font-size:60px;font-weight:800;letter-spacing:-.03em;line-height:1;color:{t["accent"]};white-space:nowrap">{big}</div>'
        f'<div class="muted" style="font-size:26px;font-weight:600;line-height:1.3;margin-top:14px">{cap}</div></div>'
        for i, (big, cap) in enumerate(items))
    return f'<div class="card" style="width:1600px;height:250px;display:flex;align-items:center">{cells}</div>'


# ---------- рендер ----------

def render(page, html, t, path, min_px=MIN_PX):
    audit_sizes(html, path.name, min_px)
    tmp = OUT / "_render.html"
    tmp.write_text(f'<html><head><meta charset="utf-8">{FONTS}<style>{css(t)}</style></head><body>{html}</body></html>',
                   encoding="utf-8")
    page.goto(tmp.as_uri(), wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(300)
    png = path.with_suffix(".png")
    page.locator("body > *").first.screenshot(path=str(png), omit_background=True)
    tmp.unlink()
    if path.suffix == ".webp":
        Image.open(png).save(path, quality=90)
        png.unlink()
    print("  ", path.relative_to(PROJ))


POSTERS = {
    "alfa": ("alfa-credit-agent", "Product · bank hackathon · captain", "A credit agent that says what to fix",
             "N of M", "bank conditions met, shown instead of an approval probability",
             ["LLM workflow", "rule-based core", "golden exam 8/8"], lambda t: shot(PROJ / "alfa-credit-agent/docs/landing.png")),
    "trainers": ("tutor-trainers", "Product · two real users", "Homework trainers that learn from logs",
                 "21 → 9", "starts vs finishes: the log found the real bottleneck",
                 ["Telegram courier", "spaced repetition", "event log"], phones),
    "lampa": ("lampa", "Analytics · public data only", "Forecasting the Bank of Russia key rate",
              "−16%", "log loss vs the market-implied baseline, 83 meetings, p = 0.003",
              ["1 739 hashed sources", "logit + LightGBM"],
              lambda t: shot(PROJ / "lampa/report/rate_forecast.png", "center", "contain", "#ffffff", 28)),
    "asstra": ("asstra", "Design · art + mechanism", "An art drop where honest bidding is the safe move",
               "k + 1", "sealed bids: every winner pays the first losing bid",
               ["generated plates", "stdlib Python"], lambda t: shot(OUT / "src-asstra.png")),
    "omega": ("omega-gp", "Play · three.js, zero assets", "A racer where even the engine sound is code",
              "0", "asset files: geometry, music and the engine are generated",
              ["tyre physics", "WebAudio synth", "autotest in CI"], lambda t: shot(PROJ / "omega-gp/docs/shot.png", "center 60%")),
}

STATS = {
    "alfa-credit-agent": [("N из M", "условий вместо процента"), ("8 / 8", "golden-экзамен ядра"),
                          ("8 из 14", "мутаций поймал экзамен"), ("136", "синтетических клиентов")],
    "tutor-trainers": [("21 → 9", "стартов против завершений"), ("43", "события за неделю"),
                       ("4 / 13", "чтение против 19 / 21"), ("5", "коробок Лейтнера")],
    "lampa": [("0.692", "log loss против 0.824 рынка"), ("0.771", "accuracy, 83 заседания"),
              ("p = 0.003", "перестановочный тест"), ("0.46", "SVB-скор: не подтверждён")],
    "asstra": [("k + 1", "единая цена для всех"), ("7", "пластин в дропе"),
               ("120 + 6", "тестов: сервер и рендер"), ("10", "строк клиринга")],
    "omega-gp": [("0", "файлов ассетов"), ("1/120 с", "шаг симуляции"),
                 ("3 462 м", "трасса, 4 поворота"), ("5", "соперников с характером")],
}


def main():
    print("контраст:")
    audit_colors()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1700, "height": 1200})
        for th, t in THEMES.items():
            print(th)
            for key, (repo, k, title, big, cap, tags, art) in POSTERS.items():
                render(pg, poster(t, k, title, big, cap, tags, art(t)), t, OUT / f"p-{key}-{th}.webp")
                brand = PROJ / repo / "docs/brand"
                brand.mkdir(parents=True, exist_ok=True)
                shutil.copy(OUT / f"p-{key}-{th}.webp", brand / f"hero-{th}.webp")
                render(pg, stats(t, STATS[repo]), t, brand / f"stats-{th}.png")
            render(pg, tile(t, "Design · art + auction", "ASSTRA", "one clearing price for everyone",
                            shot(OUT / "src-asstra.png")), t, OUT / f"t-asstra-{th}.webp", MIN_PX_TILE)
            render(pg, tile(t, "Play · three.js", "Omega Grand Prix", "the engine sound is synthesised",
                            shot(PROJ / "omega-gp/docs/shot.png", "center 70%")), t, OUT / f"t-omega-{th}.webp", MIN_PX_TILE)
            render(pg, tile(t, "Play · Claude Code mod", "hyperspace", "3D in terminal quarter-blocks",
                            shot(ROOT / "assets/scene-falcon.webp", "center")), t, OUT / f"t-hyperspace-{th}.webp", MIN_PX_TILE)
            render(pg, tile(t, "Play · hackathon game", "BRAINROT-STRIKE", "24 of 32 commits mine",
                            brainrot_art(t)), t, OUT / f"t-brainrot-{th}.webp", MIN_PX_TILE)
            render(pg, tile(t, "Study · mechanism design", "Honest bidding wins", "Vickrey, 100 000 rounds",
                            vickrey_art(t)), t, OUT / f"t-vickrey-{th}.webp", MIN_PX_TILE)
            for key, num, title, note in [("built", "01", "Built & shipped", "product and analytics"),
                                          ("how", "02", "How I build", "my agent setup, anonymised"),
                                          ("learn", "03", "Learning in public", "theory first, then the build"),
                                          ("studio", "04", "Studio", "art, games, toys")]:
                render(pg, header(t, num, title, note), t, OUT / f"h-{key}-{th}.png")
            render(pg, pipeline(t), t, OUT / f"pipeline-{th}.png")
        extras(pg)
        b.close()


# ---------- интро 1600x640 ----------

def about(t):
    toc = "".join(
        f'<div style="display:flex;gap:20px;padding:22px 0;{"border-top:2px solid " + t["line"] if i else ""}">'
        f'<span style="font-size:28px;font-weight:800;color:{t["accent"]};width:44px">{n}</span>'
        f'<span><span style="font-size:30px;font-weight:700">{a}</span><br>'
        f'<span class="muted" style="font-size:26px;font-weight:600">{b}</span></span></div>'
        for i, (n, a, b) in enumerate([("01", "Built & shipped", "product and analytics, as case studies"),
                                       ("02", "How I build", "my agent setup, anonymised"),
                                       ("03", "Learning in public", "theory first, then the build"),
                                       ("04", "Studio", "art, games, toys")]))
    return f"""
    <div class="card" style="width:1600px;height:640px">
      <div style="position:absolute;left:80px;top:72px;width:860px">
        <div class="kick" style="font-size:24px">Alexander Sotnik · Moscow · Financial University ’28</div>
        <div style="font-size:72px;font-weight:800;letter-spacing:-.03em;line-height:1.05;margin-top:24px">I study economics<br>and I build.</div>
        <div class="muted" style="font-size:30px;font-weight:500;line-height:1.4;margin-top:28px">Products with real users, models on public data,
          and the occasional thing that exists only because it was fun to make.</div>
        <div style="font-size:30px;font-weight:600;line-height:1.4;margin-top:28px;padding-left:24px;border-left:4px solid {t['accent']}">
          Heading to <span style="color:{t['accent']}">mechanism design for economies where the players are AI agents</span>,
          and causal inference to check what they actually do.</div>
      </div>
      <div style="position:absolute;left:1020px;right:72px;top:72px;bottom:72px;border-radius:16px;background:{t['surface']};
                  border:2px solid {t['line']};padding:20px 36px">{toc}</div>
    </div>"""


# ---------- мини-карточка 780x250 ----------

def mini(t, kicker, title, line, link=True):
    arrow = f'<div style="position:absolute;right:40px;top:30px;font-size:36px;font-weight:700;color:{t["accent"]}">↗</div>' if link else ""
    return f"""
    <div class="card" style="width:780px;height:250px">
      {arrow}
      <div style="position:absolute;left:44px;right:44px;top:36px">
        <div class="kick" style="font-size:24px">{kicker}</div>
        <div style="font-size:42px;font-weight:800;letter-spacing:-.02em;line-height:1.1;margin-top:10px">{title}</div>
        <div class="muted" style="font-size:26px;margin-top:10px;font-weight:600;line-height:1.3">{line}</div>
      </div>
    </div>"""


# ---------- учёба 1600x700 ----------

def learning(t):
    notes = "".join(
        f'<div style="margin-top:{0 if i == 0 else 34}px"><div class="kick" style="font-size:24px">{k}</div>'
        f'<div style="font-size:28px;font-weight:500;line-height:1.42;margin-top:8px">{x}</div></div>'
        for i, (k, x) in enumerate([
            ("Mechanism design", "Self-taught from Roughgarden’s CS364A. Write down a prediction, then simulate. "
                                 "Weeks later the same rule cleared the ASSTRA art drop."),
            ("Finance, out loud", "A talk on compute-for-equity: a cloud paying a startup in GPUs is a venture investor, "
                                  "and the deal pays only while utilisation stays under ~86%."),
            ("Next", "The same auction with LLM bidders. Do they find the dominant strategy, or talk themselves out of it?")]))
    return f"""
    <div class="card" style="width:1600px;height:700px">
      <div style="position:absolute;left:72px;top:72px;width:660px;bottom:72px;border-radius:16px;background:{t['surface']};
                  border:2px solid {t['line']}">
        <div style="padding:36px 40px 0"><div class="kick" style="font-size:24px">Vickrey auction · 100 000 rounds</div>
          <div style="font-size:40px;font-weight:800;letter-spacing:-.02em;margin-top:10px">Honest bidding wins</div>
          <div class="muted" style="font-size:24px;font-weight:600;margin-top:6px">mean profit per round; blue = bid your value</div></div>
        {vickrey_art(t)}
      </div>
      <div style="position:absolute;left:800px;right:80px;top:80px">{notes}</div>
    </div>"""


# ---------- подвал 1600x300 ----------

def footer(t):
    return f"""
    <div class="card" style="width:1600px;height:300px">
      <div style="position:absolute;left:80px;top:64px">
        <div class="kick" style="font-size:24px">Say hi</div>
        <div style="font-size:64px;font-weight:800;letter-spacing:-.03em;margin-top:14px">Telegram <span style="color:{t['accent']}">@alexeval</span></div>
      </div>
      <div class="muted" style="position:absolute;right:80px;bottom:70px;font-size:30px;font-weight:600;text-align:right">
        Moscow<br>sanek2OO6@mail.ru</div>
    </div>"""


ALSO = [("econ", "Course tournament · 450+ tests", "Econometrics Championship", "students regress on a market they played"),
        ("hh", "Experiment · job search", "hh-agent", "cover letters assigned by coin flip"),
        ("kapi", "T-Bank hackathon · team KAPI", "MCP investing scenario", "two PRs, 11 new tests, teammate’s repo"),
        ("uni", "Econometrics · 14.5k obs", "university-analysis", "OLS and diff-in-diff on the COVID shock")]


def extras(pg):
    for th, t in THEMES.items():
        render(pg, about(t), t, OUT / f"about-{th}.png")
        render(pg, learning(t), t, OUT / f"learn-{th}.png")
        render(pg, footer(t), t, OUT / f"footer-{th}.png")
        render(pg, header(t, "05", "Recently shipped", "updated daily from public repos"), t, OUT / f"h-recent-{th}.png")
        for key, k, title, line in ALSO:
            render(pg, mini(t, k, title, line, key != "kapi"), t, OUT / f"m-{key}-{th}.png", MIN_PX_TILE - 2)


if __name__ == "__main__":
    main()
