"""PDF-отчёт «Зарплаты в финансах в Узбекистане: осень 2026» – полная версия обзора, RU и EN.

Данные – агрегаты tools/reports/fin-2026-11.json (hh_resume_stats run 7, вакансии финансов на 01.11.2026).
Вёрстка и стили – те же, что у tools/build_report.py (CSS берётся оттуда). Сборка: HTML → PDF через headless Chrome:
    python3 tools/build_report_fin.py            # RU и EN в ~/Downloads
    python3 tools/build_report_fin.py en [путь]  # один язык
PDF НЕ публикуется на сайте: отчёт выдаётся по запросу (форма «Запросить отчёт» в статье, менеджер присылает файл).
Правила данных: срезы n < 30 не показываем; медианы и квантили; суммы – ожидания кандидатов на руки;
офферы агентства – только обобщённый диапазон C-level.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "tools", "reports", "fin-2026-11.json"), encoding="utf-8"))
CSS = re.search(r'CSS = """(.*?)"""', open(os.path.join(ROOT, "tools", "build_report.py"), encoding="utf-8").read(), re.S).group(1)
CSS += """
.pos-t td.mid{color:#6b6862}.pos-t td.top{color:#a5452f;font-weight:600}.pos-t td.low{color:#2f7d4f;font-weight:600}
.cmp{display:grid;grid-template-columns:repeat(5,1fr);gap:2.5mm;margin-top:3mm}
.cmp div{border:0.3mm solid #e5e3dd;border-radius:2.5mm;padding:3mm;display:flex;flex-direction:column;gap:1mm}
.cmp div.hl{background:#0e0e0d;color:#fff;border-color:#0e0e0d}
.cmp b{font-family:Unbounded,sans-serif;font-weight:700;font-size:12pt}
.cmp div.hl b{color:#e3c172}
.cmp span{font-size:8pt;line-height:1.35}
.cmp em{font-style:normal;font-size:7.6pt;color:#8a8781}
.cmp div.hl em{color:#b9b5ac}
"""
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MIN_N, RATE, F = 30, D["rate"], D["_resumes_fields"]
R, V = D["resumes"], D["vacancies"]
TOTAL = 8
ARTICLE = {"ru": "https://humancapital.uz/articles/zarplaty-v-finansakh-v-uzbekistane-osen-2026-7948aacf",
           "en": "https://humancapital.uz/articles/finance-salaries-in-uzbekistan-autumn-2026-5c4d34c3"}
OUTS = {"ru": "~/Downloads/Зарплаты в финансах в Узбекистане – осень 2026 (Human and Capital).pdf",
        "en": "~/Downloads/Finance salaries in Uzbekistan – autumn 2026 (Human and Capital).pdf"}
GROUPS = ["cfo", "audit", "fin_analysis", "credit", "accounting", "economist"]  # по медиане, все уровни

T = {
 "ru": dict(
   title="Зарплаты в финансах в Узбекистане: осень 2026",
   foot="Human and Capital · Зарплаты в финансах в Узбекистане: осень 2026",
   cv_top="Аналитика · Зарплатный обзор", cv_kick="Полная версия обзора · осень 2026",
   cv_h1="Зарплаты в финансах<br>в <span>Узбекистане</span>",
   cv_sub="Сколько просят финансисты по 6 ролям и 4 уровням опыта – от бухгалтера до финансового директора, что предлагают работодатели и сколько стоит CFO",
   exps=[("0", "Без опыта"), ("1-2", "1–2 года"), ("3-5", "3–5 лет"), ("6+", "6+ лет")], all="Все уровни",
   few=f"мало данных – срез меньше {MIN_N} резюме", few_s="мало данных", mln="млн", sum="сум", cvs="резюме",
   th=["Опыт", "Резюме", "10%", "25%", "Медиана", "75%", "90%", "≈ $ медиана", "В USD"],
   grp={"cfo": ("Финансовые директора", "финансовые директора (CFO)"),
        "audit": ("Аудиторы и комплаенс", "аудиторы, специалисты по комплаенсу"),
        "fin_analysis": ("Финансовые аналитики и менеджеры", "финансовые менеджеры, аналитики, контролёры, казначеи"),
        "credit": ("Кредитные специалисты", "кредитные специалисты"),
        "accounting": ("Бухгалтеры", "бухгалтеры, включая главных"),
        "economist": ("Экономисты", "экономисты"),
        "fin_core": ("Все финансовые роли", "")},
 ),
 "en": dict(
   title="Finance salaries in Uzbekistan: autumn 2026",
   foot="Human and Capital · Finance salaries in Uzbekistan: autumn 2026",
   cv_top="Insights · Salary review", cv_kick="Full report · autumn 2026",
   cv_h1="Finance salaries<br>in <span>Uzbekistan</span>",
   cv_sub="What finance professionals ask across 6 roles and 4 experience levels – from accountant to finance director, what employers offer and what a CFO costs",
   exps=[("0", "No experience"), ("1-2", "1–2 years"), ("3-5", "3–5 years"), ("6+", "6+ years")], all="All levels",
   few=f"not enough data – fewer than {MIN_N} CVs", few_s="not enough data", mln="M", sum="UZS", cvs="CVs",
   th=["Experience", "CVs", "10%", "25%", "Median", "75%", "90%", "≈ $ median", "In USD"],
   grp={"cfo": ("Finance directors", "finance directors (CFO)"),
        "audit": ("Auditors & compliance", "auditors, compliance specialists"),
        "fin_analysis": ("Financial analysts & managers", "financial managers, analysts, controllers, treasurers"),
        "credit": ("Credit specialists", "credit specialists"),
        "accounting": ("Accountants", "accountants, including chief accountants"),
        "economist": ("Economists", "economists"),
        "fin_core": ("All finance roles", "")},
 ),
}


def e(s):
    return html.escape(str(s), quote=True)


def row(g, x):
    return dict(zip(F, R[g][x]))


def build(L, out):
    t = T[L]
    ru = L == "ru"
    dec, thou = (",", " ") if ru else (".", ",")
    num = lambda x: f"{x:,.0f}".replace(",", thou)
    mln = lambda x: f"{x / 1e6 + 1e-9:.1f}".replace(".", dec)
    usd = lambda x: "$" + num(round(x / RATE / 10) * 10)
    pct = lambda a, b: f"{round(100 * a / b)}%"
    xx = lambda a, b: "×" + f"{b / a:.1f}".replace(".", dec)
    G = lambda g: t["grp"][g][0]
    fc = {k: row("fin_core", k) for k, _ in t["exps"] + [("all", "")]}
    cfo = {k: row("cfo", k) for k, _ in t["exps"] + [("all", "")]}
    for g in GROUPS:
        assert row(g, "all")["n"] >= MIN_N

    def head(no, title, lead=""):
        return (f'<header class="ph"><span class="ph-no">{e(no)}</span><h2>{e(title)}</h2>'
                + (f'<p class="ph-lead">{lead}</p>' if lead else "") + "</header>")

    def page(n, body, cls=""):
        foot = ("" if n == 1 else f'<footer class="pf"><span>{e(t["foot"])}</span>'
                f'<a href="https://humancapital.uz">humancapital.uz</a><span>{n} / {TOTAL}</span></footer>')
        return f'<section class="page {cls}">{body}{foot}</section>'

    def rng(r, top=60e6):
        p = lambda v: f"{min(v, top) / top * 100:.2f}%"
        return ('<div class="rng">'
                f'<i class="w" style="left:{p(r["p10"])};right:calc(100% - {p(r["p90"])})"></i>'
                f'<i class="b" style="left:{p(r["p25"])};right:calc(100% - {p(r["p75"])})"></i>'
                f'<i class="d" style="left:{p(r["p50"])}"></i></div>')

    def heat(v):
        stops = [(5e6, (251, 246, 234)), (15e6, (227, 193, 114)), (30e6, (150, 112, 26))]
        v = max(stops[0][0], min(v, stops[-1][0]))
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if v <= b:
                k = (v - a) / (b - a)
                c = tuple(round(x + (y - x) * k) for x, y in zip(ca, cb))
                return f"rgb{c}", ("#fff" if v >= 22e6 else "#0e0e0d")

    def bars(items, top, fmt):
        out = '<div class="bars">'
        for label, v, sub, hl in items:
            out += (f'<div class="bar{" hl" if hl else ""}"><span class="bl">{e(label)}</span>'
                    f'<span class="bt"><i style="width:{v / top * 100:.1f}%"></i></span>'
                    f'<span class="bv">{fmt(v)}{f" <em>{e(sub)}</em>" if sub else ""}</span></div>')
        return out + "</div>"

    def grp_table(g, bare=False):
        a = row(g, "all")
        meta = (f'{num(a["n"])} {t["cvs"]} · {"в USD" if ru else "in USD"} {pct(a["n_usd"], a["n"])} · '
                f'{"Ташкент" if ru else "Tashkent"} {pct(a["n_tashkent"], a["n"])}')
        out = ('<div class="gt">' + ("" if bare else f'<div class="gt-h"><b>{e(G(g))}</b><em>{meta}</em></div>')
               + '<table class="t t2"><thead><tr>' + "".join(f"<th>{x}</th>" for x in t["th"]) + "</tr></thead><tbody>")
        for k, label in t["exps"] + [("all", t["all"])]:
            r = row(g, k)
            cls = ' class="tot"' if k == "all" else ""
            if r["n"] < MIN_N:
                out += f'<tr{cls}><td>{label}</td><td>{num(r["n"])}</td><td colspan="7" class="na">{t["few"]}</td></tr>'
                continue
            out += (f'<tr{cls}><td>{label}</td><td>{num(r["n"])}</td><td>{mln(r["p10"])}</td><td>{mln(r["p25"])}</td>'
                    f'<td><b>{mln(r["p50"])}</b></td><td>{mln(r["p75"])}</td><td>{mln(r["p90"])}</td>'
                    f'<td>{usd(r["p50"])}</td><td>{pct(r["n_usd"], r["n"])}</td></tr>')
        return out + "</tbody></table></div>"

    by_med = sorted(GROUPS, key=lambda g: -row(g, "all")["p50"])
    au, fa, ac, cr = (lambda g: (row(g, "0"), row(g, "6+")))("audit"), (lambda g: (row(g, "0"), row(g, "6+")))("fin_analysis"), \
        (lambda g: (row(g, "0"), row(g, "6+")))("accounting"), (lambda g: (row(g, "0"), row(g, "6+")))("credit")
    VG = V["by_grp"]

    # ---------- 1. Обложка ----------
    kf = [(f'{mln(row("accounting","all")["p50"])} {t["mln"]} {t["sum"]}' if ru else f'UZS {mln(row("accounting","all")["p50"])}M',
           f'медиана ожиданий бухгалтера на руки (≈ {usd(row("accounting","all")["p50"])})' if ru else
           f'median net expectation of an accountant (≈ {usd(row("accounting","all")["p50"])})'),
          ("≈ " + usd(cfo["6+"]["p50"]), "медиана финансового директора с опытом 6+ лет" if ru else "median of a finance director with 6+ years"),
          (xx(au[0]["p50"], au[1]["p50"]), "рост ожиданий аудитора и финансового аналитика от «без опыта» до 6+ лет" if ru
           else "growth of auditors’ and analysts’ expectations from no experience to 6+ years"),
          (pct(cfo["all"]["n_usd"], cfo["all"]["n"]), "финансовых директоров называют зарплату в долларах" if ru else "of finance directors state their salary in dollars")]
    p1 = (f'<div class="cv-top"><img src="file://{ROOT}/logo-white.png" alt="Human and Capital"><span>{t["cv_top"]}</span></div>'
          f'<div class="cv-mid"><p class="cv-kick">{t["cv_kick"]}</p><h1>{t["cv_h1"]}</h1><p class="cv-sub">{t["cv_sub"]}</p></div>'
          '<div class="cv-kf">' + "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in kf) + "</div>"
          f'<div class="cv-foot"><span>{num(D["found"])} {t["cvs"]} · {V["with_salary"]} {"вакансий с зарплатой" if ru else "vacancies with a stated salary"} · '
          f'{"данные на" if ru else "data as of"} {D["snapshot"]}</span><span>humancapital.uz</span></div>')

    # ---------- 2. Главное ----------
    fv = VG["fin_core"]
    if ru:
        key = [
          f"<b>Медиана ожиданий финансиста – {mln(fc['all']['p50'])} млн сум на руки (≈ {usd(fc['all']['p50'])}).</b> Средние 50% просят от {mln(fc['all']['p25'])} до {mln(fc['all']['p75'])} млн, верхние 10% – от {mln(fc['all']['p90'])} млн.",
          f"<b>Роли.</b> Финансовые директора – {mln(row('cfo','all')['p50'])} млн, аудиторы – {mln(row('audit','all')['p50'])} млн, финансовые аналитики – {mln(row('fin_analysis','all')['p50'])} млн, кредитные специалисты – {mln(row('credit','all')['p50'])} млн, бухгалтеры и экономисты – по {mln(row('accounting','all')['p50'])} млн.",
          f"<b>Быстрее всего с опытом дорожают аудит и финансовый анализ</b> – {xx(au[0]['p50'], au[1]['p50'])} от «без опыта» до 6+ лет; бухгалтеры – {xx(ac[0]['p50'], ac[1]['p50'])}, кредитные специалисты – {xx(cr[0]['p50'], cr[1]['p50'])}. У аудиторов главный скачок – между 1–2 и 3–5 годами ({mln(row('audit','1-2')['p50'])} → {mln(row('audit','3-5')['p50'])} млн).",
          f"<b>Финансовый директор с опытом 6+ лет просит {mln(cfo['6+']['p50'])} млн (≈ {usd(cfo['6+']['p50'])}),</b> верхние 10% – от {mln(cfo['6+']['p90'])} млн (≈ {usd(cfo['6+']['p90'])}). Офферы C-level в проектах Human and Capital – $4 000–10 000 на руки.",
          f"<b>Зарплату указывают {V['salary_share']['fin']}% вакансий в финансах</b> (в продажах {V['salary_share']['sales']}%, в IT {V['salary_share']['it']}%). С опытом от 3 лет кандидаты просят у верхней границы вилки: при 3–5 годах вакансии дают {mln(fv['3-5'][1])}–{mln(fv['3-5'][2])} млн, кандидаты просят {mln(fc['3-5']['p50'])}.",
          f"<b>Доллар – у руководителей.</b> В долларах считают {pct(fc['all']['n_usd'], fc['all']['n'])} финансистов, но {pct(cfo['all']['n_usd'], cfo['all']['n'])} финансовых директоров; в вакансиях доллар – у {V['usd_share']}%."]
        how = [f"Все суммы – <b>ожидания кандидатов на руки</b>, млн сум в месяц, по резюме финансистов, обновлённым за 90 дней до {D['snapshot']}.",
               "<b>25% / медиана / 75% / 90%</b> – квантили: четверть кандидатов просит меньше первой цифры, половина – меньше медианы, 10% – больше последней.",
               f"<b>≈ $</b> – медиана по курсу {num(RATE)} сум за $1. <b>В USD</b> – доля кандидатов, назвавших сумму в долларах.",
               f"Срезы меньше {MIN_N} резюме не показываем – в таблицах они отмечены «мало данных»."]
        toc = "Дальше: <b>3</b> ожидания по ролям · <b>4–5</b> роль × опыт по 6 группам · <b>6</b> ожидания и вакансии, доллар или сум · <b>7</b> финансовый директор и выводы · <b>8</b> методология и контакты"
    else:
        key = [
          f"<b>The median finance professional asks for UZS {mln(fc['all']['p50'])}M net (≈ {usd(fc['all']['p50'])}).</b> The middle 50% ask for UZS {mln(fc['all']['p25'])}–{mln(fc['all']['p75'])}M, the top 10% from {mln(fc['all']['p90'])}M.",
          f"<b>Roles.</b> Finance directors – UZS {mln(row('cfo','all')['p50'])}M, auditors – {mln(row('audit','all')['p50'])}M, financial analysts – {mln(row('fin_analysis','all')['p50'])}M, credit specialists – {mln(row('credit','all')['p50'])}M, accountants and economists – {mln(row('accounting','all')['p50'])}M each.",
          f"<b>Audit and financial analysis grow fastest with experience</b> – {xx(au[0]['p50'], au[1]['p50'])} from no experience to 6+ years; accountants – {xx(ac[0]['p50'], ac[1]['p50'])}, credit specialists – {xx(cr[0]['p50'], cr[1]['p50'])}. For auditors the main jump is between 1–2 and 3–5 years ({mln(row('audit','1-2')['p50'])} → {mln(row('audit','3-5')['p50'])}M).",
          f"<b>A finance director with 6+ years asks for UZS {mln(cfo['6+']['p50'])}M (≈ {usd(cfo['6+']['p50'])}),</b> the top 10% from {mln(cfo['6+']['p90'])}M (≈ {usd(cfo['6+']['p90'])}). C-level offers in Human and Capital projects are $4,000–10,000 net.",
          f"<b>{V['salary_share']['fin']}% of finance vacancies state a salary</b> ({V['salary_share']['sales']}% in sales, {V['salary_share']['it']}% in IT). From 3 years of experience, candidates ask near the top of the range: at 3–5 years vacancies offer UZS {mln(fv['3-5'][1])}–{mln(fv['3-5'][2])}M, candidates ask for {mln(fc['3-5']['p50'])}M.",
          f"<b>Dollars are for leaders.</b> {pct(fc['all']['n_usd'], fc['all']['n'])} of finance professionals state salary in dollars, but {pct(cfo['all']['n_usd'], cfo['all']['n'])} of finance directors; in vacancies – {V['usd_share']}%."]
        how = [f"All amounts are <b>candidates’ net expectations</b>, UZS million per month, from CVs of finance professionals updated within 90 days before {D['snapshot']}.",
               "<b>25% / median / 75% / 90%</b> are percentiles: a quarter of candidates ask less than the first figure, half less than the median, 10% more than the last.",
               f"<b>≈ $</b> – the median at UZS {num(RATE)} per $1. <b>In USD</b> – share of candidates who stated their salary in dollars.",
               f"Slices with fewer than {MIN_N} CVs are not shown – they are marked “not enough data”."]
        toc = "Next: <b>3</b> expectations by role · <b>4–5</b> role × experience for 6 groups · <b>6</b> expectations vs vacancies, dollars or sums · <b>7</b> finance director and takeaways · <b>8</b> methodology and contacts"
    p2 = (head("", "Главное" if ru else "Key findings") + '<ol class="key">' + "".join(f"<li>{x}</li>" for x in key) + "</ol>"
          + f'<div class="how"><h3>{"Как читать таблицы" if ru else "How to read the tables"}</h3><ul>' + "".join(f"<li>{x}</li>" for x in how) + "</ul></div>"
          + f'<h3 class="sub">{"Все финансовые роли: ожидания по опыту" if ru else "All finance roles: expectations by experience"}</h3>'
          + grp_table("fin_core", bare=True) + f'<p class="toc">{toc}</p>')

    # ---------- 3. По ролям ----------
    th = ["Роль", "Резюме", "25%", "Медиана", "75%", "90%", "≈ $", "В USD", "Разброс, млн сум"] if ru else \
         ["Role", "CVs", "25%", "Median", "75%", "90%", "≈ $", "In USD", "Spread, UZS M"]
    tb = ('<table class="t"><thead><tr>' + "".join(f"<th>{x}</th>" for x in th[:-1])
          + f'<th class="rh">{th[-1]}<span class="sc"><i style="left:0">0</i><i style="left:33.3%">20</i><i style="left:66.6%">40</i><i style="left:100%">60</i></span></th></tr></thead><tbody>')
    for g in by_med + ["fin_core"]:
        r = row(g, "all")
        tb += (f'<tr{" class=tot" if g == "fin_core" else ""}><td>{e(G(g))}</td><td>{num(r["n"])}</td><td>{mln(r["p25"])}</td>'
               f'<td><b>{mln(r["p50"])}</b></td><td>{mln(r["p75"])}</td><td>{mln(r["p90"])}</td><td>{usd(r["p50"])}</td>'
               f'<td>{pct(r["n_usd"], r["n"])}</td><td class="rc">{rng(r)}</td></tr>')
    tb += "</tbody></table>"
    hm = f'<table class="hm"><thead><tr><th>{"Медиана, млн сум" if ru else "Median, UZS M"}</th>' + "".join(f"<th>{x}</th>" for _, x in t["exps"]) + "</tr></thead><tbody>"
    for g in by_med + ["fin_core"]:
        hm += f'<tr{" class=tot" if g == "fin_core" else ""}><td>{e(G(g))}</td>'
        for k, _ in t["exps"]:
            r = row(g, k)
            if r["n"] < MIN_N:
                hm += f'<td class="na">{t["few_s"]}</td>'
            else:
                bg, fg = heat(r["p50"])
                hm += f'<td style="background:{bg};color:{fg}">{mln(r["p50"])}</td>'
        hm += "</tr>"
    hm += "</tbody></table>"
    p3 = (head("1", "Ожидания по ролям" if ru else "Expectations by role",
               "Все уровни опыта. Роли отсортированы по медиане; на полосе – средние 50% кандидатов (25–75%), тонкая линия – от 10% до 90%, точка – медиана." if ru else
               "All experience levels. Roles are sorted by median; the band is the middle 50% of candidates (25–75%), the thin line 10% to 90%, the dot the median.")
          + tb + f'<h3 class="sub">{"Медиана по роли и опыту" if ru else "Median by role and experience"}</h3>'
          + f'<p class="lead2">{"Без опыта почти все роли просят 5–6 млн. К 6+ годам бухгалтер выходит на " + mln(ac[1]["p50"]) + " млн, аудитор и финансовый аналитик – на " + mln(au[1]["p50"]) + " млн, а финансовый директор – на " + mln(cfo["6+"]["p50"]) + " млн." if ru else "With no experience almost every role asks UZS 5–6M. By 6+ years an accountant reaches " + mln(ac[1]["p50"]) + "M, an auditor and a financial analyst " + mln(au[1]["p50"]) + "M, and a finance director " + mln(cfo["6+"]["p50"]) + "M."}</p>'
          + hm)

    # ---------- 4–5. Роль × опыт ----------
    lead45 = ("Ожидания на руки, млн сум в месяц. Опыт – общий стаж из резюме; состав групп – на стр. 8." if ru else
              "Net expectations, UZS million per month. Experience is total work experience from the CV; group composition on p. 8.")
    p4 = head("2", "Роль × опыт: полные таблицы" if ru else "Role × experience: full tables", lead45) + "".join(grp_table(g) for g in ("cfo", "audit", "fin_analysis", "credit"))
    tash = sorted(((G(g), row(g, "all")["n_tashkent"] / row(g, "all")["n"] * 100, None, g == "cfo") for g in GROUPS), key=lambda x: -x[1])
    p5 = (head("2", "Роль × опыт (продолжение)" if ru else "Role × experience (continued)") + "".join(grp_table(g) for g in ("accounting", "economist"))
          + f'<h3 class="sub">{"Доля резюме из Ташкента" if ru else "Share of CVs from Tashkent"}</h3>'
          + bars(tash, 100, lambda v: f"{round(v)}%")
          + f'<p class="note">{"Чем выше позиция, тем больше кандидатов – в столице. Кредитных специалистов и экономистов почти половина – в регионах, их проще нанять на месте." if ru else "The more senior the role, the more candidates are in the capital. Almost half of credit specialists and economists are in the regions and are easier to hire locally."}</p>')

    # ---------- 6. Вакансии и валюта ----------
    def place(ask, f, to):
        k = (ask - f) / (to - f)
        if k >= 0.9: return ("top", "у верхней границы" if ru else "at the top")
        if k >= 0.6: return ("top", "ближе к верхней" if ru else "upper part")
        if k >= 0.4: return ("mid", "середина" if ru else "middle")
        return ("low", "ближе к нижней" if ru else "lower part")
    vth = (["Группа", "Опыт", "Просят, медиана", "Вакансий", "Вилка в вакансиях", "Где просьба в вилке"] if ru else
           ["Group", "Experience", "Candidates ask", "Vacancies", "Range in vacancies", "Ask within range"])
    vt = '<table class="t vt pos-t"><thead><tr>' + "".join(f"<th>{x}</th>" for x in vth) + "</tr></thead><tbody>"
    lab = dict(t["exps"] + [("all", t["all"])])
    for g in ("fin_core", "accounting", "fin_analysis"):
        for k, v in VG[g].items():
            r = row(g, k)
            c, w = place(r["p50"], v[1], v[2])
            vt += (f'<tr{" class=tot" if k == "all" else ""}><td>{e(G(g))}</td><td>{lab[k]}</td><td><b>{mln(r["p50"])}</b></td><td>{v[0]}</td>'
                   f'<td>{mln(v[1])}–{mln(v[2])}</td><td class="{c}">{w}</td></tr>')
    vt += "</tbody></table>"
    usd_items = sorted(((G(g), row(g, "all")["n_usd"] / row(g, "all")["n"] * 100, None, g == "cfo") for g in GROUPS), key=lambda x: -x[1])
    usd_items.append((G("fin_core"), fc["all"]["n_usd"] / fc["all"]["n"] * 100, None, False))
    if ru:
        vnote = (f"Вилка – медианы нижней и верхней границы в {V['with_salary']} вакансиях финансов с указанной зарплатой на {D['vac_snapshot']}; {V['gross_share']}% вакансий указывают сумму до налога – она пересчитана на руки. "
                 f"В вакансиях опыт задан диапазонами 1–3 и 3–6 лет, в резюме – 1–2 и 3–5, поэтому сравнение по уровням приблизительное. Строки с числом вакансий меньше {MIN_N} не показаны – вакансий финансовых директоров с зарплатой почти нет.")
        aside = (f"<p><b>По опыту у финансовых директоров:</b> 3–5 лет – {pct(cfo['3-5']['n_usd'], cfo['3-5']['n'])}, 6+ лет – {pct(cfo['6+']['n_usd'], cfo['6+']['n'])} называют сумму в долларах.</p>"
                 f"<p><b>В вакансиях</b> доллар – редкость: {V['usd_share']}% вакансий финансов с зарплатой.</p>"
                 "<p><b>Что из этого следует:</b> вилку финансовому директору и опытному аналитику удобнее обсуждать в долларах, бухгалтеру, экономисту и кредитному специалисту – в сумах: в сумах считают больше 80% этих кандидатов.</p>")
    else:
        vnote = (f"The range is the median of the lower and upper bounds in {V['with_salary']} finance vacancies with a stated salary as of {D['vac_snapshot']}; {V['gross_share']}% of vacancies state a gross figure – converted to net. "
                 f"Vacancies set experience as 1–3 and 3–6 years, CVs as 1–2 and 3–5, so the comparison by level is approximate. Rows with fewer than {MIN_N} vacancies are not shown – there are almost no finance director vacancies with a salary.")
        aside = (f"<p><b>Finance directors by experience:</b> {pct(cfo['3-5']['n_usd'], cfo['3-5']['n'])} at 3–5 years and {pct(cfo['6+']['n_usd'], cfo['6+']['n'])} at 6+ years state the amount in dollars.</p>"
                 f"<p><b>In vacancies</b> the dollar is rare: {V['usd_share']}% of finance vacancies with a salary.</p>"
                 "<p><b>What follows:</b> discuss pay with a finance director or a senior analyst in dollars, and with an accountant, economist or credit specialist in sums – more than 80% of them think in sums.</p>")
    p6 = (head("3", "Ожидания и вакансии" if ru else "Expectations vs vacancies",
               "Медиана ожиданий в резюме против вилки в открытых вакансиях, млн сум в месяц на руки." if ru else
               "Median expectation in CVs against the range in open vacancies, UZS million per month, net.")
          + vt + f'<p class="note">{vnote}</p>'
          + f'<header class="ph ph2"><span class="ph-no">4</span><h2>{"Доллар или сум" if ru else "Dollars or sums"}</h2><p class="ph-lead">{"Доля кандидатов, назвавших ожидания в долларах, все уровни опыта." if ru else "Share of candidates who stated expectations in dollars, all experience levels."}</p></header>'
          + f'<div class="cols"><div>{bars(usd_items, 100, lambda v: f"{round(v)}%")}</div><div class="aside">{aside}</div></div>')

    # ---------- 7. Финансовый директор и выводы ----------
    cmp = [("accounting", "6+", False), ("fin_analysis", "6+", False), ("audit", "6+", False), ("cfo", "3-5", False), ("cfo", "6+", True)]
    lab_e = dict(t["exps"])
    cmp_h = '<div class="cmp">' + "".join(
        f'<div{" class=hl" if hl else ""}><em>{e(G(g))} · {lab_e[k].lower() if ru else lab_e[k]}</em><b>{usd(row(g, k)["p50"])}</b>'
        f'<span>{mln(row(g, k)["p50"])} {t["mln"]} {t["sum"]}</span></div>' for g, k, hl in cmp) + "</div>"
    if ru:
        cfo_lead = (f"Ожидания финансовых директоров растут с опытом сильнее, чем у любой другой роли: {mln(cfo['1-2']['p50'])} млн при 1–2 годах, {mln(cfo['3-5']['p50'])} млн при 3–5 и {mln(cfo['6+']['p50'])} млн при 6+. "
                    "Нижняя часть вилки – в основном финансовые директора небольших компаний, где роль совмещена с главным бухгалтером.")
        when = ("<p class=\"lead2\" style=\"margin-top:3mm\"><b>Финансовый директор или сильный специалист?</b> На ранней стадии IT-компании или стартапа отчётность и юнит-экономику закрывает "
                "финансовый аналитик или главный бухгалтер с опытом 6+ лет. Финансовый директор нужен, когда компания привлекает инвестиции, работает через несколько юрлиц или строит отношения с банками.</p>")
        offer = ("<div class=\"offer\"><b>$4 000–10 000 на руки</b><span>Офферы руководителям и C-level с опытом 6+ лет в проектах Human and Capital, осень 2026. "
                 "Сильные финансовые директора редко ищут работу на job-сайтах – их находят через executive search.</span></div>")
        todo = [f"<b>Закладывайте запас в верхнюю часть вилки для опытных.</b> С 3 лет опыта кандидаты просят у верхней границы вакансии: при 3–5 годах – {mln(fc['3-5']['p50'])} млн при вилке {mln(fv['3-5'][1])}–{mln(fv['3-5'][2])}. Бюджет на середине вилки отсекает сильных на первом разговоре.",
                f"<b>Указывайте зарплату в вакансии.</b> Её называют только {V['salary_share']['fin']}% вакансий в финансах – вакансия с понятной вилкой заметнее.",
                f"<b>Удерживайте аудиторов и аналитиков к 3–5 годам.</b> В этот момент их ожидания растут быстрее всего: у аудитора – с {mln(row('audit','1-2')['p50'])} до {mln(row('audit','3-5')['p50'])} млн.",
                "<b>Финансового директора ищите прямым поиском.</b> Вакансий CFO с зарплатой почти нет, половина кандидатов считает в долларах, а офферы – от $4 000."]
    else:
        cfo_lead = (f"Finance directors’ expectations grow with experience more than any other role: UZS {mln(cfo['1-2']['p50'])}M at 1–2 years, {mln(cfo['3-5']['p50'])}M at 3–5 and {mln(cfo['6+']['p50'])}M at 6+. "
                    "The lower part of the range is mostly finance directors of small companies, where the role is combined with that of chief accountant.")
        when = ("<p class=\"lead2\" style=\"margin-top:3mm\"><b>A finance director or a strong specialist?</b> At an early stage of an IT company or a startup, reporting and unit economics are covered by "
                "a financial analyst or chief accountant with 6+ years. A finance director is needed when the company raises investment, operates through several legal entities or builds relationships with banks.</p>")
        offer = ("<div class=\"offer\"><b>$4,000–10,000 net</b><span>Offers to heads and C-level executives with 6+ years in Human and Capital projects, autumn 2026. "
                 "Strong finance directors rarely look for jobs on job sites – they are found through executive search.</span></div>")
        todo = [f"<b>Leave room at the top of the range for experienced hires.</b> From 3 years, candidates ask near the top of a vacancy’s range: at 3–5 years, UZS {mln(fc['3-5']['p50'])}M against {mln(fv['3-5'][1])}–{mln(fv['3-5'][2])}M. A budget at the middle of the range loses strong candidates at the first conversation.",
                f"<b>State the salary in the vacancy.</b> Only {V['salary_share']['fin']}% of finance vacancies do – a clear range stands out.",
                f"<b>Retain auditors and analysts as they reach 3–5 years.</b> That is when their expectations grow fastest: an auditor goes from UZS {mln(row('audit','1-2')['p50'])}M to {mln(row('audit','3-5')['p50'])}M.",
                "<b>Find a finance director through direct search.</b> There are almost no CFO vacancies with a salary, half of candidates think in dollars, and offers start at $4,000."]
    p7 = (head("5", "Финансовый директор: сколько стоит CFO" if ru else "Finance director: what a CFO costs", cfo_lead)
          + grp_table("cfo", bare=True)
          + f'<h3 class="sub">{"Медиана ожиданий: финансовый директор и сильные специалисты" if ru else "Median expectation: finance director vs strong specialists"}</h3>' + cmp_h + when + offer
          + f'<header class="ph ph2"><span class="ph-no">6</span><h2>{"Что делать работодателю" if ru else "What employers should do"}</h2></header>'
          + '<ol class="todo">' + "".join(f"<li>{x}</li>" for x in todo) + "</ol>")

    # ---------- 8. Методология и контакты ----------
    groups_txt = "; ".join(t["grp"][g][1] for g in by_med)
    if ru:
        meth = [f"<b>Ожидания</b> – резюме финансистов с указанной зарплатой, доступные агентству как работодателю на job-сайтах Узбекистана и обновлённые за 90 дней до {D['snapshot']}: {num(D['found'])} резюме. Расчёт – по выборке самых свежих резюме в каждом сочетании роли и стажа, с поправкой на размер сочетания; размер выборки – в столбце «Резюме».",
                f"<b>Роли</b> – 10 профессиональных ролей, сведённых в 6 групп: {groups_txt}.",
                "<b>Опыт</b> – общий стаж из резюме. Резюме без указанного стажа входят только в итоги «Все уровни».",
                f"<b>Предложения</b> – {V['with_salary']} из {V['total']} открытых вакансий финансов с указанной зарплатой на {D['vac_snapshot']}; вилка – медианы нижней и верхней границы; суммы до налога ({V['gross_share']}% вакансий) пересчитаны на руки.",
                f"<b>Валюта</b> – суммы в долларах пересчитаны в сумы по курсу {num(RATE)} сум за $1 на дату выгрузки.",
                f"<b>Статистика</b> – медианы и квантили, не средние; срезы меньше {MIN_N} наблюдений не публикуются; резюме с очевидными ошибками в сумме отсеяны.",
                "<b>Офферы агентства</b> – обобщённо, по проектам executive search Human and Capital, без данных отдельных компаний.",
                f"<b>Ограничения</b> – ожидание в резюме не равно фактической зарплате; рынок – в основном Ташкент ({pct(fc['all']['n_tashkent'], fc['all']['n'])} резюме)."]
        cta = ("Нужна вилка под вашу позицию?", "Подготовим срез зарплат по вашей роли, уровню и отрасли и найдём кандидатов – от бухгалтера до финансового директора.", "Обсудить найм → humancapital.uz")
        about = (f"<b>Human and Capital</b> – рекрутинговое и HR-агентство в Ташкенте: подбор персонала, executive search, аутстаффинг и HR-консалтинг. "
                 f"Авторы обзора – Акмаль Саипов, коммерческий директор, и Анна Джу, генеральный директор, соучредители компании. Онлайн-версия с графиками: <a href=\"{ARTICLE['ru']}\">humancapital.uz/articles</a>.")
        legal = "© Human and Capital, 2026. При цитировании ссылка на humancapital.uz обязательна."
        lbl = ("Телефон", "WhatsApp", "Email", "Telegram", "Адрес", "Ташкент, Фаргона йули, 94")
    else:
        meth = [f"<b>Expectations</b> – CVs of finance professionals with a stated salary, available to the agency as an employer on Uzbekistan’s job sites and updated within 90 days before {D['snapshot']}: {num(D['found'])} CVs. Calculated on a sample of the most recent CVs in each role-and-experience combination, weighted by its size; the sample size is in the “CVs” column.",
                f"<b>Roles</b> – 10 professional roles grouped into 6: {groups_txt}.",
                "<b>Experience</b> – total work experience from the CV. CVs without stated experience count only in “All levels”.",
                f"<b>Offers</b> – {V['with_salary']} of {V['total']} open finance vacancies with a stated salary as of {D['vac_snapshot']}; the range is the median of the lower and upper bounds; gross amounts ({V['gross_share']}% of vacancies) are converted to net.",
                f"<b>Currency</b> – dollar amounts converted to sums at UZS {num(RATE)} per $1 on the date of the data pull.",
                f"<b>Statistics</b> – medians and percentiles, not averages; slices with fewer than {MIN_N} observations are not published; CVs with obvious errors in the amount are excluded.",
                "<b>Agency offers</b> – aggregated from Human and Capital executive search projects, without data on individual companies.",
                f"<b>Limitations</b> – an expectation in a CV is not an actual salary; the market is mostly Tashkent ({pct(fc['all']['n_tashkent'], fc['all']['n'])} of CVs)."]
        cta = ("Need a range for your role?", "We will prepare a salary benchmark for your role, level and industry and find candidates – from accountant to finance director.", "Discuss hiring → humancapital.uz")
        about = (f"<b>Human and Capital</b> is a recruitment and HR agency in Tashkent: recruitment, executive search, outstaffing and HR consulting. "
                 f"The review is by Akmal Saipov, Commercial Director, and Anna Dju, CEO, co-founders of the company. Online version with charts: <a href=\"{ARTICLE['en']}\">humancapital.uz/articles</a>.")
        legal = "© Human and Capital, 2026. Please cite humancapital.uz when quoting."
        lbl = ("Phone", "WhatsApp", "Email", "Telegram", "Address", "94 Fargona yuli, Tashkent")
    p8 = (head("7", "Методология" if ru else "Methodology") + '<ul class="meth">' + "".join(f"<li>{x}</li>" for x in meth) + "</ul>"
          + f'<div class="cta"><div><h3>{cta[0]}</h3><p>{cta[1]}</p><a class="btn" href="https://humancapital.uz/{"recruitment.html" if ru else "recruitment-en.html"}#contact">{cta[2]}</a></div>'
          + f'<ul class="ct"><li><span>{lbl[0]}</span><a href="tel:+998903251336">+998 90 325 13 36</a></li>'
          + f'<li><span>{lbl[1]}</span><a href="https://wa.me/998958631199">+998 95 863 11 99</a></li>'
          + f'<li><span>{lbl[2]}</span><a href="mailto:akmal.s@human-capital.org">akmal.s@human-capital.org</a></li>'
          + f'<li><span>{lbl[3]}</span><a href="https://t.me/Djuanna555">t.me/Djuanna555</a></li>'
          + f'<li><span>{lbl[4]}</span>{lbl[5]}</li></ul></div>'
          + f'<div class="about"><img src="file://{ROOT}/logo.png" alt="Human and Capital"><p>{about}</p></div><p class="legal">{legal}</p>')

    doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{e(t["title"])} – Human and Capital</title>'
           '<meta name="author" content="Human and Capital">'
           '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Unbounded:wght@600;700;800&display=block" rel="stylesheet">'
           f'<style>{CSS}</style></head><body>'
           + page(1, p1, "cover") + page(2, p2) + page(3, p3) + page(4, p4) + page(5, p5) + page(6, p6) + page(7, p7) + page(8, p8)
           + "</body></html>").replace("≈ ", "≈ ")
    tmp = tempfile.mkdtemp(prefix=f"hc-report-fin-{L}-")
    src = os.path.join(tmp, "report.html")
    open(src, "w", encoding="utf-8").write(doc)
    out = os.path.abspath(os.path.expanduser(out))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    "--virtual-time-budget=15000", "--print-to-pdf=" + out, "file://" + src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("html:", src)
    print("pdf: ", out, f"({os.path.getsize(out) // 1024} КБ)")


if __name__ == "__main__":
    langs = [sys.argv[1]] if len(sys.argv) > 1 else ["ru", "en"]
    for L in langs:
        build(L, sys.argv[2] if len(sys.argv) > 2 else OUTS[L])
