"""Графики обзора «Сколько стоит оператор поддержки в Узбекистане» (BPO / контакт-центры) на RU/EN/UZ.
Данные – hh_resume_stats run_id 8 (ожидания, 2.11.2026) и hh_resume_runs id 9 (резерв по языкам, found).
Ожидания – chart() из tools/it_salary_charts.py; резерв – горизонтальные столбики.

    python3 tools/bpo_charts.py <папка для html>
затем скриншоты headless Chrome шириной 1320 и печатаемой высотой (как в it_salary_charts.py).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from it_salary_charts import chart, W

D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

# p10, p25, p50, p75, p90 в сумах, все уровни опыта
ROLES = [("translator_eng_c1", (4000000, 6000000, 9000000, 15000000, 24130000)),
         ("support_eng_b2", (4500000, 6000000, 8450000, 12070000, 20000000)),
         ("cc_rus_c1", (3500000, 4500000, 5500000, 7240000, 10000000)),
         ("cc_eng_c1", (3000000, 4000000, 5000000, 7240000, 10000000)),
         ("cc_eng_b2", (3000000, 4000000, 5000000, 7000000, 9650000)),
         ("cc", (3000000, 4000000, 5000000, 7240000, 10000000))]
# резюме за год, живущие в Узбекистане (found)
POOL = [("eng.b1", 147844), ("eng.b2", 105849), ("eng.c1", 43870), ("rus.c1", 197924), ("tur.b2", 12376),
        ("kor.b2", 2132), ("deu.b2", 1440), ("zho.b2", 1428), ("ara.b2", 795), ("fra.b2", 435)]

T = {
 "ru": dict(dec=",", thou=" ",
   role_file="operator-podderzhki-2026-po-rolyam", pool_file="operator-podderzhki-2026-yazyki",
   role_title="Английский не меняет медиану оператора – дороже стоят поддержка и переводчики",
   role_sub="Ожидания на руки, все уровни опыта · резюме за 90 дней до 2.11.2026",
   legend="Точка – медиана, серая полоса – средние 50%, тонкая линия – от 10% до 90%",
   axis="млн сум в месяц на руки",
   role={"translator_eng_c1": "Переводчик, английский C1+", "support_eng_b2": "Техподдержка, английский B2+",
         "cc_rus_c1": "Оператор КЦ, русский C1+", "cc_eng_c1": "Оператор КЦ, английский C1+",
         "cc_eng_b2": "Оператор КЦ, английский B2+", "cc": "Оператор КЦ, все"},
   pool_title="Кадровый резерв: английский и русский – массово, остальные языки – тысячи",
   pool_sub="Резюме за год, авторы живут в Узбекистане · уровень не ниже указанного",
   pool={"eng.b1": "Английский B1+", "eng.b2": "Английский B2+", "eng.c1": "Английский C1+", "rus.c1": "Русский C1+",
         "tur.b2": "Турецкий B2+", "kor.b2": "Корейский B2+", "deu.b2": "Немецкий B2+", "zho.b2": "Китайский B2+",
         "ara.b2": "Арабский B2+", "fra.b2": "Французский B2+"},
   pool_unit="резюме"),
 "en": dict(dec=".", thou=",",
   role_file="support-agent-cost-2026-by-role", pool_file="support-agent-cost-2026-languages",
   role_title="English doesn’t change an agent’s median – support and translators cost more",
   role_sub="Net expectations, all experience levels · CVs updated within 90 days before 2.11.2026",
   legend="Dot – median, grey band – middle 50%, thin line – 10th to 90th percentile",
   axis="UZS million per month, net",
   role={"translator_eng_c1": "Translator, English C1+", "support_eng_b2": "Tech support, English B2+",
         "cc_rus_c1": "Contact centre, Russian C1+", "cc_eng_c1": "Contact centre, English C1+",
         "cc_eng_b2": "Contact centre, English B2+", "cc": "Contact centre, all"},
   pool_title="Talent pool: English and Russian at scale, other languages in the thousands",
   pool_sub="CVs updated within a year, candidates living in Uzbekistan · level or higher",
   pool={"eng.b1": "English B1+", "eng.b2": "English B2+", "eng.c1": "English C1+", "rus.c1": "Russian C1+",
         "tur.b2": "Turkish B2+", "kor.b2": "Korean B2+", "deu.b2": "German B2+", "zho.b2": "Chinese B2+",
         "ara.b2": "Arabic B2+", "fra.b2": "French B2+"},
   pool_unit="CVs"),
 "uz": dict(dec=",", thou=" ",
   role_file="operator-narxi-2026-rollar-boyicha", pool_file="operator-narxi-2026-tillar",
   role_title="Ingliz tili operator medianasini o‘zgartirmaydi, tarjimonlar qimmatroq",
   role_sub="Qo‘lga kutilmalar, barcha tajriba darajalari · 2.11.2026 gacha 90 kunlik rezyumelar",
   legend="Nuqta – mediana, kulrang chiziq – o‘rtadagi 50%, ingichka chiziq – 10% dan 90% gacha",
   axis="mln so‘m oyiga, qo‘lga",
   role={"translator_eng_c1": "Tarjimon, ingliz C1+", "support_eng_b2": "Texnik yordam, ingliz B2+",
         "cc_rus_c1": "Call-markaz, rus C1+", "cc_eng_c1": "Call-markaz, ingliz C1+",
         "cc_eng_b2": "Call-markaz, ingliz B2+", "cc": "Call-markaz, barchasi"},
   pool_title="Kadrlar zaxirasi: ingliz va rus – ommaviy, boshqa tillar – minglab",
   pool_sub="Bir yillik rezyumelar, O‘zbekistonda yashovchilar · ko‘rsatilgan darajadan past emas",
   pool={"eng.b1": "Ingliz B1+", "eng.b2": "Ingliz B2+", "eng.c1": "Ingliz C1+", "rus.c1": "Rus C1+",
         "tur.b2": "Turk B2+", "kor.b2": "Koreys B2+", "deu.b2": "Nemis B2+", "zho.b2": "Xitoy B2+",
         "ara.b2": "Arab B2+", "fra.b2": "Fransuz B2+"},
   pool_unit="rezyume"),
}


def bars(t, rows, label_w=300, row_h=58):
    top, x0, x1 = 150, label_w, W - 72 - 170
    mx = max(v for _, v in rows)
    h = top + row_h * len(rows) + 40
    svg = []
    for i, (name, v) in enumerate(rows):
        y = top + row_h * i
        w = max((x1 - x0) * v / mx, 3)
        num = f"{v:,}".replace(",", t["thou"])
        svg.append(f'<text x="0" y="{y + row_h / 2 + 7:.1f}" class="lbl">{name}</text>')
        svg.append(f'<rect x="{x0}" y="{y + 12}" width="{w:.1f}" height="{row_h - 24}" rx="4" fill="#2b74d8"/>')
        svg.append(f'<text x="{x0 + w + 12:.1f}" y="{y + row_h / 2 + 7:.1f}" class="val">{num}</text>')
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=block" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{h}px;overflow:hidden;background:#fff}}
body{{font-family:Inter,sans-serif;color:#111;padding:0 36px}}
h1{{font-size:28px;font-weight:700;letter-spacing:-.2px;padding-top:24px;white-space:nowrap}}
.sub{{font-size:20px;color:#555;margin-top:14px}}
svg{{position:absolute;left:36px;top:0;overflow:visible}}
.lbl{{font-size:21px;fill:#111}}.val{{font-size:19px;font-weight:600;fill:#111}}</style></head>
<body><h1>{t["pool_title"]}</h1><p class="sub">{t["pool_sub"]}</p>
<svg width="{W - 72}" height="{h}" viewBox="0 0 {W - 72} {h}">{''.join(svg)}</svg></body></html>"""
    return html, h


for lang, t in T.items():
    rows = [(t["role"][k], v) for k, v in ROLES]
    html, h = chart(t, t["role_title"], t["role_sub"], t["legend"], rows, 400, 92, max_m=25)
    open(os.path.join(D, t["role_file"] + ".html"), "w", encoding="utf-8").write(html); print(t["role_file"], h)
    html, h = bars(t, [(t["pool"][k], v) for k, v in POOL])
    open(os.path.join(D, t["pool_file"] + ".html"), "w", encoding="utf-8").write(html); print(t["pool_file"], h)
