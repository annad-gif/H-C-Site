"""Графики обзора «Зарплаты в продажах в Узбекистане: осень 2026» на RU/EN/UZ.
Данные – hh_resume_stats, run_id 6 (снимок 29.10.2026), в сумах. Отрисовка – chart() из tools/it_salary_charts.py.

    python3 tools/sales_salary_charts.py <папка для html>
затем скриншоты headless Chrome шириной 1320 и печатаемой высотой (как в it_salary_charts.py).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from it_salary_charts import chart

D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

# p10, p25, p50, p75, p90 в сумах
ROLES = [("sales_head", (7150000, 11920000, 18000000, 29800000, 47680000)),
         ("sales_rep", (5000000, 6500000, 10000000, 12000000, 15000000)),
         ("sales_mgr", (4000000, 5000000, 8000000, 12000000, 20000000)),
         ("call_center", (3000000, 4000000, 5000000, 7000000, 10000000))]
EXP = {"sales_mgr": [("0", (4000000, 5000000, 5960000, 7150000, 10000000)),
                     ("1-2", (4770000, 5960000, 8000000, 10000000, 15000000)),
                     ("3-5", (5960000, 7150000, 10000000, 14300000, 20000000)),
                     ("6+", (7000000, 10000000, 15000000, 20630000, 29800000))],
       "sales_head": [("0", (4770000, 6000000, 8340000, 14000000, 20000000)),
                      ("1-2", (5000000, 7000000, 10000000, 14300000, 20000000)),
                      ("3-5", (7000000, 10000000, 15000000, 20000000, 29800000)),
                      ("6+", (11920000, 15000000, 23840000, 35760000, 57000000))],
       "call_center": [("0", (3500000, 4000000, 5000000, 6000000, 7150000)),
                       ("1-2", (3580000, 4770000, 5960000, 7150000, 10000000)),
                       ("3-5", (4000000, 5000000, 6000000, 8840000, 11920000)),
                       ("6+", (4000000, 5000000, 7000000, 10000000, 12000000))]}

T = {
 "ru": dict(
   dec=",",
   role_file="zarplaty-v-prodazhah-2026-po-rolyam", exp_file="zarplaty-v-prodazhah-2026-po-opytu",
   role_title="Руководители продаж просят больше всех, колл-центр – меньше всех",
   role_sub="Медиана: 18,0 против 5,0 млн сум (×3,6) · все уровни опыта",
   exp_title="С опытом менеджер и руководитель растут, колл-центр – почти нет",
   exp_sub="Медиана от «без опыта» до 6+ лет: менеджер ×2,5, руководитель ×2,9, колл-центр ×1,4",
   legend="Точка – медиана, серая полоса – средние 50%, тонкая линия – от 10% до 90%",
   axis="млн сум в месяц на руки",
   role={"sales_head": "Руководители продаж", "sales_rep": "Торговые представители",
         "sales_mgr": "Менеджеры по продажам", "call_center": "Операторы колл-центра"},
   grp={"sales_mgr": "Менеджер", "sales_head": "Руководитель", "call_center": "Колл-центр"},
   exp={"0": "без опыта", "1-2": "1–2 года", "3-5": "3–5 лет", "6+": "6+ лет"}),
 "en": dict(
   dec=".",
   role_file="sales-salaries-2026-by-role", exp_file="sales-salaries-2026-by-experience",
   role_title="Sales heads ask the most, call centre operators the least",
   role_sub="Median: UZS 18.0M vs 5.0M (×3.6) · all experience levels",
   exp_title="Managers and sales heads grow with experience, call centre staff barely do",
   exp_sub="Median from no experience to 6+ years: manager ×2.5, head ×2.9, call centre ×1.4",
   legend="Dot – median, grey band – middle 50%, thin line – 10th to 90th percentile",
   axis="UZS million per month, net",
   role={"sales_head": "Sales heads", "sales_rep": "Sales representatives",
         "sales_mgr": "Sales managers", "call_center": "Call centre operators"},
   grp={"sales_mgr": "Manager", "sales_head": "Sales head", "call_center": "Call centre"},
   exp={"0": "no experience", "1-2": "1–2 years", "3-5": "3–5 years", "6+": "6+ years"}),
 "uz": dict(
   dec=",",
   role_file="savdo-maoshlari-2026-rollar-boyicha", exp_file="savdo-maoshlari-2026-tajriba-boyicha",
   role_title="Savdo rahbarlari eng ko‘p, call-markaz operatorlari eng kam so‘raydi",
   role_sub="Mediana: 18,0 va 5,0 mln so‘m (×3,6) · barcha tajriba darajalari",
   exp_title="Tajriba bilan menejer va rahbar o‘sadi, call-markaz deyarli o‘smaydi",
   exp_sub="Tajribasizdan 6+ yilgacha mediana: menejer ×2,5, rahbar ×2,9, call-markaz ×1,4",
   legend="Nuqta – mediana, kulrang chiziq – o‘rtadagi 50%, ingichka chiziq – 10% dan 90% gacha",
   axis="mln so‘m oyiga, qo‘lga",
   role={"sales_head": "Savdo rahbarlari", "sales_rep": "Savdo vakillari",
         "sales_mgr": "Savdo menejerlari", "call_center": "Call-markaz operatorlari"},
   grp={"sales_mgr": "Menejer", "sales_head": "Rahbar", "call_center": "Call-markaz"},
   exp={"0": "tajribasiz", "1-2": "1–2 yil", "3-5": "3–5 yil", "6+": "6+ yil"}),
}

for lang, t in T.items():
    rows = [(t["role"][k], v) for k, v in ROLES]
    html, h = chart(t, t["role_title"], t["role_sub"], t["legend"], rows, 380, 92)
    open(os.path.join(D, t["role_file"] + ".html"), "w", encoding="utf-8").write(html); print(t["role_file"], h)
    rows = [(t["grp"][g] + " · " + t["exp"][e], v) for g in ("sales_mgr", "sales_head", "call_center") for e, v in EXP[g]]
    html, h = chart(t, t["exp_title"], t["exp_sub"], t["legend"], rows, 380, 66)
    open(os.path.join(D, t["exp_file"] + ".html"), "w", encoding="utf-8").write(html); print(t["exp_file"], h)
