"""График обзора «Дефицитные IT-роли в Узбекистане» на RU/EN/UZ: резюме на одну открытую вакансию по 10 IT-ролям.
Данные: hh_resume_runs id 2 (found – резюме с указанной зарплатой за 90 дней до 29.10.2026) / hh_market_vacancies
на 01.11.2026 (открытые вакансии тех же групп ролей).

    python3 tools/it_deficit_charts.py <папка для html>
затем скриншот headless Chrome шириной 1320 и печатаемой высотой (как в it_salary_charts.py).
"""
import os, sys

D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
W = 1320
# группа: (резюме, вакансии)
DATA = [("devops", 355, 44), ("product", 939, 86), ("qa", 618, 41), ("ba_sa", 1129, 70), ("support", 1921, 114),
        ("security", 943, 48), ("data", 1739, 79), ("infra", 2418, 105), ("it_lead", 1146, 40), ("dev", 6149, 164)]
AVG = 14381 / 791
SCARCE = {"devops", "product", "qa", "ba_sa"}

T = {
 "ru": dict(dec=",", file="deficitnye-it-roli-2026-rezyume-na-vakansiyu",
   title="DevOps – 8 резюме на вакансию, разработка – 37",
   sub="Свежие резюме с зарплатой на одну открытую вакансию · пунктир – среднее по IT (18)",
   avg="среднее 18",
   role={"devops": "DevOps", "product": "Управление продуктом", "qa": "Тестирование (QA)", "ba_sa": "Бизнес- и системный анализ",
         "support": "Техподдержка", "security": "Информационная безопасность", "data": "Аналитика данных",
         "infra": "Сисадмины и сети", "it_lead": "Руководители IT", "dev": "Разработка"}),
 "en": dict(dec=".", file="scarce-it-roles-2026-cvs-per-vacancy",
   title="DevOps: 8 CVs per vacancy, development: 37",
   sub="Recent CVs with a stated salary per open vacancy · dashed line – IT average (18)",
   avg="average 18",
   role={"devops": "DevOps", "product": "Product management", "qa": "Testing (QA)", "ba_sa": "Business & systems analysis",
         "support": "Tech support", "security": "Information security", "data": "Data analytics",
         "infra": "System & network admins", "it_lead": "IT management", "dev": "Development"}),
 "uz": dict(dec=",", file="taqchil-it-rollar-2026-vakansiyaga-rezyume",
   title="DevOps – vakansiyaga 8 ta rezyume, dasturlash – 37",
   sub="Bitta ochiq vakansiyaga maoshi ko‘rsatilgan yangi rezyumelar · punktir – IT bo‘yicha o‘rtacha (18)",
   avg="o‘rtacha 18",
   role={"devops": "DevOps", "product": "Mahsulotni boshqarish", "qa": "Testlash (QA)", "ba_sa": "Biznes va tizim tahlili",
         "support": "Texnik yordam", "security": "Axborot xavfsizligi", "data": "Ma’lumotlar tahlili",
         "infra": "Tizim va tarmoq administratorlari", "it_lead": "IT rahbarlari", "dev": "Dasturlash"}),
}


def chart(t, label_w=400, row_h=62):
    top, x0, x1 = 150, label_w, W - 72 - 110
    mx = 40
    sx = lambda v: x0 + (x1 - x0) * v / mx
    n = len(DATA)
    h = top + row_h * n + 60
    ax = sx(AVG)  # пунктир среднего – под столбиками
    svg = [f'<line x1="{ax:.1f}" y1="{top - 6}" x2="{ax:.1f}" y2="{top + row_h * n + 6}" stroke="#111" stroke-width="2" stroke-dasharray="7 6"/>']
    for i, (g, cv, vac) in enumerate(DATA):
        v = cv / vac
        y = top + row_h * i
        col = "#2b74d8" if g in SCARCE else "#b9c9df"
        svg.append(f'<text x="0" y="{y + row_h / 2 + 7:.1f}" class="lbl">{t["role"][g]}</text>')
        svg.append(f'<rect x="{x0}" y="{y + 12}" width="{sx(v) - x0:.1f}" height="{row_h - 24}" rx="4" fill="{col}"/>')
        svg.append(f'<text x="{sx(v) + 12:.1f}" y="{y + row_h / 2 + 7:.1f}" class="val">{round(v)}</text>')
    svg.append(f'<text x="{ax + 8:.1f}" y="{top + row_h * n + 34}" class="tick">{t["avg"]}</text>')
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=block" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{h}px;overflow:hidden;background:#fff}}
body{{font-family:Inter,sans-serif;color:#111;padding:0 36px}}
h1{{font-size:28px;font-weight:700;letter-spacing:-.2px;padding-top:24px;white-space:nowrap}}
.sub{{font-size:20px;color:#555;margin-top:14px}}
svg{{position:absolute;left:36px;top:0;overflow:visible}}
.lbl{{font-size:21px;fill:#111}}.val{{font-size:20px;font-weight:600;fill:#111;paint-order:stroke;stroke:#fff;stroke-width:8px;stroke-linejoin:round}}.tick{{font-size:18px;fill:#555}}</style></head>
<body><h1>{t["title"]}</h1><p class="sub">{t["sub"]}</p>
<svg width="{W - 72}" height="{h}" viewBox="0 0 {W - 72} {h}">{''.join(svg)}</svg></body></html>"""
    return html, h


if __name__ == "__main__":
    for lang, t in T.items():
        html, h = chart(t)
        open(os.path.join(D, t["file"] + ".html"), "w", encoding="utf-8").write(html)
        print(t["file"], h)
