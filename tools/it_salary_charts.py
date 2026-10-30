"""Графики обзора «Зарплаты в IT в Узбекистане: осень 2026» на английском и узбекском
(русские – img/articles/zarplaty-v-it-2026-po-*.png). Данные – hh_resume_stats, run_id 2 (снимок 29.10.2026), в сумах.

    python3 tools/it_salary_charts.py <папка для html>
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
      --window-size=1320,<высота> --virtual-time-budget=6000 --screenshot=<имя>.png file://<папка>/<имя>.html
Высота печатается для каждого файла.
"""
import os, sys
D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
# chart() используется и в tools/sales_salary_charts.py

# p10, p25, p50, p75, p90 в сумах
EXP = [("0", (3575718, 4767624, 5959530, 8000000, 10727155)),
       ("1-2", (4767624, 6000000, 8343342, 11919061, 17878591)),
       ("3-5", (5959530, 9535249, 15000000, 23838121, 35757182)),
       ("6+", (8000000, 11919061, 21454309, 35757182, 56019585))]
ROLES = [("it_lead", (8343342, 13000000, 23838121, 41716712, 59595303)),
         ("devops", (5959530, 10000000, 17878591, 30000000, 47676243)),
         ("product", (5959530, 8343342, 15000000, 29797652, 47676243)),
         ("ba_sa", (5000000, 8000000, 15000000, 25000000, 41716712)),
         ("dev", (4000000, 5959530, 10000000, 20000000, 35757182)),
         ("data", (4120170, 5959530, 10000000, 17878591, 30000000)),
         ("security", (5000000, 6000000, 10000000, 17439295, 29797652)),
         ("qa", (4767624, 6000000, 9535249, 17878591, 29797652)),
         ("infra", (4767624, 5959530, 9000000, 15000000, 23838121)),
         ("support", (4421733, 5959530, 8000000, 12000000, 17878591))]

T = {
 "en": dict(
   dec=".",
   exp_file="it-salaries-2026-by-experience", role_file="it-salaries-2026-by-role",
   exp_title="With 3–5 years of experience, IT specialists ask almost twice as much as with 1–2 years",
   exp_sub="Median expectation: UZS 8.3M → 15.0M (×1.8) · 10,505 CVs with stated experience",
   exp_legend="Dot – median, grey band – middle 50% (25th to 75th percentile), thin line – 10th to 90th percentile",
   role_title="IT heads and DevOps ask the most, tech support the least",
   role_sub="Median: UZS 23.8M vs 8.0M (×3.0) · all experience levels",
   role_legend="Dot – median, grey band – middle 50%, thin line – 10th to 90th percentile",
   axis="UZS million per month, net",
   exp={"0": "No experience", "1-2": "1–2 years", "3-5": "3–5 years", "6+": "6+ years"},
   role={"it_lead": "IT management", "devops": "DevOps", "product": "Product management",
         "ba_sa": "Business & systems analysis", "dev": "Development", "data": "Data analytics",
         "security": "Information security", "qa": "Testing (QA)", "infra": "System & network admins",
         "support": "Tech support"}),
 "uz": dict(
   dec=",",
   exp_file="it-maoshlari-2026-tajriba-boyicha", role_file="it-maoshlari-2026-rollar-boyicha",
   exp_title="3–5 yillik tajribada IT mutaxassislari 1–2 yillikka nisbatan deyarli ikki baravar ko‘p so‘raydi",
   exp_sub="Kutilmalar medianasi: 8,3 → 15,0 mln so‘m (×1,8) · tajribasi ko‘rsatilgan 10 505 ta rezyume",
   exp_legend="Nuqta – mediana, kulrang chiziq – o‘rtadagi 50% (25% dan 75% gacha), ingichka chiziq – 10% dan 90% gacha",
   role_title="IT rahbarlari va DevOps eng ko‘p, texnik yordam eng kam so‘raydi",
   role_sub="Mediana: 23,8 va 8,0 mln so‘m (×3,0) · barcha tajriba darajalari",
   role_legend="Nuqta – mediana, kulrang chiziq – o‘rtadagi 50%, ingichka chiziq – 10% dan 90% gacha",
   axis="mln so‘m oyiga, qo‘lga",
   exp={"0": "Tajribasiz", "1-2": "1–2 yil", "3-5": "3–5 yil", "6+": "6+ yil"},
   role={"it_lead": "IT rahbarlari", "devops": "DevOps", "product": "Mahsulotni boshqarish",
         "ba_sa": "Biznes va tizim tahlili", "dev": "Dasturlash", "data": "Ma’lumotlar tahlili",
         "security": "Axborot xavfsizligi", "qa": "Testlash (QA)", "infra": "Tizim va tarmoq administratorlari",
         "support": "Texnik yordam"}),
}

W, PAD_R, MAX = 1320, 48, 60  # ширина, правое поле, ось до 60 млн


def chart(t, title, sub, legend, rows, label_w, row_h):
    top = 150
    x0, x1 = label_w, W - 72 - PAD_R // 2
    sx = lambda v: x0 + (v / 1e6) / MAX * (x1 - x0)
    h = top + row_h * len(rows) + 100
    svg = []
    for g in range(0, MAX + 1, 10):
        x = sx(g * 1e6)
        svg.append(f'<line x1="{x:.1f}" y1="{top - 10}" x2="{x:.1f}" y2="{top + row_h * len(rows)}" stroke="#e6e6e3" stroke-width="2"/>')
        svg.append(f'<text x="{x:.1f}" y="{top + row_h * len(rows) + 32}" text-anchor="middle" class="tick">{g}</text>')
    for i, (name, (p10, p25, p50, p75, p90)) in enumerate(rows):
        y = top + row_h * i + row_h / 2
        svg.append(f'<text x="0" y="{y + 7:.1f}" class="lbl">{name}</text>')
        svg.append(f'<rect x="{sx(p25):.1f}" y="{y - 16:.1f}" width="{sx(p75) - sx(p25):.1f}" height="32" rx="4" fill="#dcdbd5"/>')
        svg.append(f'<line x1="{sx(p10):.1f}" y1="{y:.1f}" x2="{sx(p90):.1f}" y2="{y:.1f}" stroke="#c4c3b8" stroke-width="3.5"/>')
        svg.append(f'<circle cx="{sx(p50):.1f}" cy="{y:.1f}" r="11" fill="#2b74d8"/>')
        v = f"{p50 / 1e6:.1f}".replace(".", t["dec"])
        svg.append(f'<text x="{sx(p50):.1f}" y="{y - 24:.1f}" text-anchor="middle" class="val">{v}</text>')
    svg.append(f'<text x="{x1}" y="{top + row_h * len(rows) + 72}" text-anchor="end" class="tick">{t["axis"]}</text>')
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=block" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{h}px;overflow:hidden;background:#fff}}
body{{font-family:Inter,sans-serif;color:#111;padding:0 36px}}
h1{{font-size:28px;font-weight:700;letter-spacing:-.2px;padding-top:24px;white-space:nowrap}}
.sub{{font-size:20px;color:#555;margin-top:14px}}.leg{{font-size:17px;color:#555;margin-top:14px}}
svg{{position:absolute;left:36px;top:0;overflow:visible}}
.lbl{{font-size:21px;fill:#111}}.val{{font-size:19px;font-weight:600;fill:#111}}.tick{{font-size:19px;fill:#555}}</style></head>
<body><h1>{title}</h1><p class="sub">{sub}</p><p class="leg">{legend}</p>
<svg width="{W - 72}" height="{h}" viewBox="0 0 {W - 72} {h}">{''.join(svg)}</svg></body></html>"""
    return html, h


if __name__ == "__main__":
  for lang, t in T.items():
    for kind in ("exp", "role"):
        rows = [(t[kind][k], v) for k, v in (EXP if kind == "exp" else ROLES)]
        label_w = 230 if kind == "exp" else 400
        html, h = chart(t, t[kind + "_title"], t[kind + "_sub"], t[kind + "_legend"], rows, label_w, 113 if kind == "exp" else 81)
        name = t[kind + "_file"]
        open(os.path.join(D, name + ".html"), "w", encoding="utf-8").write(html)
        print(name, h)
