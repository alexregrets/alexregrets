"""Графика для README флагманов в арт-системе профиля: постер-хиро и полоса цифр (две темы).

    python tools/render_repos.py

Пишет в ~/projects/<repo>/docs/brand/: hero.webp, stats-dark.png, stats-light.png.
Постеры alfa, trainers, lampa берутся готовыми из assets/shelf, asstra и omega рисуются здесь.
"""
import shutil

from playwright.sync_api import sync_playwright

import render_cards as rc

STATS = {
    "alfa-credit-agent": [("N из M", "условий банка вместо процента одобрения"), ("8 / 8", "golden-экзамен ядра"),
                          ("8 из 14", "мутаций правил поймал экзамен"), ("136", "синтетических клиентов с метками")],
    "tutor-trainers": [("21 → 9", "стартов против завершений"), ("43", "события в журнале за неделю"),
                       ("4/13", "чтение против 19/21 грамматики"), ("0/1/3/7/16", "дней в коробках Лейтнера")],
    "lampa": [("0.692", "log loss ансамбля против 0.824 рынка"), ("0.771", "accuracy на 83 заседаниях"),
              ("p = 0.003", "перестановочный тест"), ("0.46", "ROC-AUC SVB-скора: не подтверждено")],
    "asstra": [("k + 1", "цена: одна для всех победителей"), ("7", "пластин в дропе по единой цене"),
               ("120 + 6", "тестов: сервер и рендер"), ("10", "строк клиринга в auction.py")],
    "omega-gp": [("0", "файлов ассетов: всё считается кодом"), ("1/120 с", "шаг симуляции в автотесте"),
                 ("3 462 м", "трасса, четыре поворота"), ("5", "соперников с характером")],
}


def stats(t, items):
    cells = "".join(
        f'<div style="flex:1;padding:0 34px;border-left:1px solid {t["line"]}">'
        f'<div class="serif" style="font-size:64px;line-height:1;color:{t["accent"]};white-space:nowrap">{big}</div>'
        f'<div class="m" style="font-size:17px;margin-top:14px;line-height:1.35">{cap}</div></div>'
        for big, cap in items)
    return (f'<div style="width:1600px;height:210px;display:flex;align-items:center;'
            f'border-top:1px solid {t["line"]};border-bottom:1px solid {t["line"]};margin-left:-1px">{cells}</div>')


def main():
    d = rc.THEMES["dark"]
    P = rc.PROJ
    for src, repo in [("p-alfa", "alfa-credit-agent"), ("p-trainers", "tutor-trainers"), ("p-lampa", "lampa")]:
        (P / repo / "docs/brand").mkdir(parents=True, exist_ok=True)
        shutil.copy(rc.OUT / f"{src}.webp", P / repo / "docs/brand/hero.webp")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1700, "height": 1000})
        rc.render(pg, rc.poster(d, "design · generative art + mechanism",
                                "An art drop where honest bidding is the safe&nbsp;move", "k + 1",
                                "uniform-price sealed-bid auction: every winner pays the first losing bid",
                                ["ink + generated plates", "stdlib Python", "120 + 6 tests"],
                                rc.img_art(rc.OUT / "asstra.webp"), "04"), d, "p-asstra")
        rc.render(pg, rc.poster(d, "play · three.js, zero assets",
                                "A racer where even the engine sound is&nbsp;code", "0",
                                "asset files: geometry, music and the engine are all generated",
                                ["tyre friction circle", "WebAudio synth", "headless autotest", "CI"],
                                rc.img_art(P / "omega-gp/docs/shot.png", "center 60%"), "05"), d, "p-omega")
        for src, repo in [("p-asstra", "asstra"), ("p-omega", "omega-gp")]:
            (P / repo / "docs/brand").mkdir(parents=True, exist_ok=True)
            shutil.copy(rc.OUT / f"{src}.webp", P / repo / "docs/brand/hero.webp")
        for repo, items in STATS.items():
            for name, t in rc.THEMES.items():
                rc.render(pg, stats(t, items), t, f"_stats-{name}", "png", True)
                shutil.move(rc.OUT / f"_stats-{name}.png", P / repo / f"docs/brand/stats-{name}.png")
        b.close()


if __name__ == "__main__":
    main()
