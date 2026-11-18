"""Графики обзора «Зарплаты в финансах в Узбекистане: осень 2026» на RU/EN/UZ.
Данные – hh_resume_stats, run_id 7 (снимок 29.10.2026), в сумах. Отрисовка – chart() из tools/it_salary_charts.py.

    python3 tools/finance_salary_charts.py <папка для html>
затем скриншоты headless Chrome шириной 1320 и печатаемой высотой (как в it_salary_charts.py).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from it_salary_charts import chart

D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

# p10, p25, p50, p75, p90 в сумах
ROLES = [("cfo", (10000000, 15000000, 29800000, 47680000, 59600000)),
         ("audit", (5000000, 7000000, 11920000, 23840000, 35760000)),
         ("fin_analysis", (4770000, 6000000, 10000000, 20000000, 35000000)),
         ("credit", (5000000, 6000000, 9000000, 15000000, 20000000)),
         ("accounting", (4000000, 5000000, 8000000, 12000000, 20000000)),
         ("economist", (4000000, 5000000, 8000000, 12000000, 20000000))]
EXP = {"accounting": [("0", (3000000, 4000000, 5000000, 7000000, 9540000)),
                      ("1-2", (4000000, 5000000, 7000000, 10000000, 12000000)),
                      ("3-5", (5000000, 6000000, 10000000, 12000000, 19930000)),
                      ("6+", (6000000, 10000000, 14300000, 20000000, 30000000))],
       "fin_analysis": [("0", (3000000, 4600000, 5960000, 8000000, 11920000)),
                        ("1-2", (4770000, 5960000, 8000000, 11920000, 16000000)),
                        ("3-5", (5000000, 8000000, 12000000, 20000000, 30000000)),
                        ("6+", (8000000, 11920000, 20000000, 30000000, 47680000))],
       "audit": [("0", (3000000, 4770000, 5960000, 8000000, 11920000)),
                 ("1-2", (5000000, 6000000, 9000000, 12000000, 20000000)),
                 ("3-5", (6000000, 8340000, 14300000, 24000000, 35000000)),
                 ("6+", (9000000, 13220000, 20000000, 35760000, 53640000))]}

T = {
 "ru": dict(
   dec=",",
   role_file="zarplaty-v-finansah-2026-po-rolyam", exp_file="zarplaty-v-finansah-2026-po-opytu",
   role_title="Финансовые директора просят почти вчетверо больше бухгалтеров",
   role_sub="Медиана: 29,8 против 8,0 млн сум (×3,7) · все уровни опыта",
   exp_title="Аудит и финансовый анализ дорожают с опытом быстрее бухгалтерии",
   exp_sub="Медиана от «без опыта» до 6+ лет: аудитор ×3,4, финансовый аналитик ×3,4, бухгалтер ×2,9",
   legend="Точка – медиана, серая полоса – средние 50%, тонкая линия – от 10% до 90%",
   axis="млн сум в месяц на руки",
   role={"cfo": "Финансовые директора", "audit": "Аудиторы и комплаенс",
         "fin_analysis": "Финансовые аналитики и менеджеры", "credit": "Кредитные специалисты",
         "accounting": "Бухгалтеры", "economist": "Экономисты"},
   grp={"accounting": "Бухгалтер", "fin_analysis": "Фин. аналитик", "audit": "Аудитор"},
   exp={"0": "без опыта", "1-2": "1–2 года", "3-5": "3–5 лет", "6+": "6+ лет"}),
 "en": dict(
   dec=".",
   role_file="finance-salaries-2026-by-role", exp_file="finance-salaries-2026-by-experience",
   role_title="Finance directors ask almost four times as much as accountants",
   role_sub="Median: UZS 29.8M vs 8.0M (×3.7) · all experience levels",
   exp_title="Audit and financial analysis grow faster with experience than accounting",
   exp_sub="Median from no experience to 6+ years: auditor ×3.4, financial analyst ×3.4, accountant ×2.9",
   legend="Dot – median, grey band – middle 50%, thin line – 10th to 90th percentile",
   axis="UZS million per month, net",
   role={"cfo": "Finance directors (CFO)", "audit": "Auditors & compliance",
         "fin_analysis": "Financial analysts & managers", "credit": "Credit specialists",
         "accounting": "Accountants", "economist": "Economists"},
   grp={"accounting": "Accountant", "fin_analysis": "Fin. analyst", "audit": "Auditor"},
   exp={"0": "no experience", "1-2": "1–2 years", "3-5": "3–5 years", "6+": "6+ years"}),
 "uz": dict(
   dec=",",
   role_file="moliya-maoshlari-2026-rollar-boyicha", exp_file="moliya-maoshlari-2026-tajriba-boyicha",
   role_title="Moliya direktorlari buxgalterlardan deyarli to‘rt baravar ko‘p so‘raydi",
   role_sub="Mediana: 29,8 va 8,0 mln so‘m (×3,7) · barcha tajriba darajalari",
   exp_title="Audit va moliyaviy tahlil tajriba bilan buxgalteriyadan tezroq qimmatlashadi",
   exp_sub="Tajribasizdan 6+ yilgacha mediana: auditor ×3,4, moliyaviy tahlilchi ×3,4, buxgalter ×2,9",
   legend="Nuqta – mediana, kulrang chiziq – o‘rtadagi 50%, ingichka chiziq – 10% dan 90% gacha",
   axis="mln so‘m oyiga, qo‘lga",
   role={"cfo": "Moliya direktorlari", "audit": "Auditorlar va komplayens",
         "fin_analysis": "Moliyaviy tahlilchilar va menejerlar", "credit": "Kredit mutaxassislari",
         "accounting": "Buxgalterlar", "economist": "Iqtisodchilar"},
   grp={"accounting": "Buxgalter", "fin_analysis": "Moliyaviy tahlilchi", "audit": "Auditor"},
   exp={"0": "tajribasiz", "1-2": "1–2 yil", "3-5": "3–5 yil", "6+": "6+ yil"}),
}

if __name__ == "__main__":
  for lang, t in T.items():
    rows = [(t["role"][k], v) for k, v in ROLES]
    html, h = chart(t, t["role_title"], t["role_sub"], t["legend"], rows, 430, 92)
    open(os.path.join(D, t["role_file"] + ".html"), "w", encoding="utf-8").write(html); print(t["role_file"], h)
    rows = [(t["grp"][g] + " · " + t["exp"][e], v) for g in ("accounting", "fin_analysis", "audit") for e, v in EXP[g]]
    html, h = chart(t, t["exp_title"], t["exp_sub"], t["legend"], rows, 430, 66)
    open(os.path.join(D, t["exp_file"] + ".html"), "w", encoding="utf-8").write(html); print(t["exp_file"], h)
