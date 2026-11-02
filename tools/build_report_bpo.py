"""PDF-отчёт «Сколько стоит оператор поддержки в Узбекистане» (BPO / контакт-центры) – полная версия обзора, RU и EN.

Данные – агрегаты tools/reports/bpo-2026-11.json (hh_resume_stats run 8, резерв по языкам run 9, вакансии КЦ, страны).
Вёрстка и стили – те же, что у tools/build_report.py (CSS берётся оттуда). Сборка: HTML → PDF через headless Chrome:
    python3 tools/build_report_bpo.py            # RU и EN в ~/Downloads
    python3 tools/build_report_bpo.py en [путь]  # один язык
PDF НЕ публикуется на сайте: отчёт выдаётся по запросу (как IT-отчёт). Правила данных: срезы n < 30 не показываем;
медианы и квантили; суммы – ожидания кандидатов на руки; стоимость команды – без ставки агентства.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "tools", "reports", "bpo-2026-11.json"), encoding="utf-8"))
CSS = re.search(r'CSS = """(.*?)"""', open(os.path.join(ROOT, "tools", "build_report.py"), encoding="utf-8").read(), re.S).group(1)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MIN_N, RATE, F = 30, D["rate"], D["fields"]
TOTAL = 9
ARTICLE = {"ru": "https://humancapital.uz/articles/skolko-stoit-operator-podderzhki-v-uzbekistane-v-2026-godu-378c6170",
           "en": "https://humancapital.uz/articles/hiring-in-uzbekistan-what-a-support-agent-costs-in-2026-375b57d2"}
OUTS = {"ru": "~/Downloads/Сколько стоит оператор поддержки в Узбекистане – 2026 (Human and Capital).pdf",
        "en": "~/Downloads/Hiring in Uzbekistan – what a support agent costs, 2026 (Human and Capital).pdf"}

T = {
 "ru": dict(
   foot="Human and Capital · Сколько стоит оператор поддержки в Узбекистане, 2026",
   cv_top="Аналитика · BPO и контакт-центры", cv_kick="Полная версия обзора · ноябрь 2026",
   cv_h1="Сколько стоит<br><span>оператор поддержки</span><br>в Узбекистане",
   cv_sub="Ожидания операторов колл-центра, техподдержки и переводчиков по языку, опыту и региону, кадровый резерв, стоимость команды для работодателя и сравнение со странами",
   exps=[("0", "Без опыта"), ("1-2", "1–2 года"), ("3-5", "3–5 лет"), ("6+", "6+ лет")], all="Все уровни",
   few=f"мало данных – срез меньше {MIN_N} резюме", mln="млн", sum="сум", cvs="резюме",
   th=["Опыт", "Резюме", "10%", "25%", "Медиана", "75%", "90%", "≈ $ медиана", "В USD"],
   grp={"cc": ("Оператор колл-центра", "все операторы КЦ и контакт-центров"), "cc_eng_b1": ("Оператор, английский B1+", ""),
        "cc_eng_b2": ("Оператор, английский B2+", ""), "cc_eng_c1": ("Оператор, английский C1+", ""),
        "cc_rus_c1": ("Оператор, русский C1+", ""), "cc_regions": ("Оператор, регионы", "все города, кроме Ташкента"),
        "cc_eng_b2_regions": ("Оператор, английский B2+, регионы", ""), "support": ("Техподдержка", "специалисты технической поддержки"),
        "support_eng_b2": ("Техподдержка, английский B2+", ""), "translator": ("Переводчик", "письменные и устные переводчики"),
        "translator_eng_c1": ("Переводчик, английский C1+", ""), "bpo_core": ("Все роли BPO", "")},
   lang={"eng.b1": "Английский B1+", "eng.b2": "Английский B2+", "eng.c1": "Английский C1+", "rus.c1": "Русский C1+",
         "tur.b2": "Турецкий B2+", "kor.b2": "Корейский B2+", "deu.b2": "Немецкий B2+", "zho.b2": "Китайский B2+",
         "ara.b2": "Арабский B2+", "fra.b2": "Французский B2+"},
   country={"ph": "Филиппины", "eg": "Египет (Каир)", "ge": "Грузия (Тбилиси)", "kz": "Казахстан (Алматы)"},
   basis={"gross": "до налогов", "net": "на руки", "mixed": "до и после налогов"},
 ),
 "en": dict(
   foot="Human and Capital · Hiring in Uzbekistan: what a support agent costs, 2026",
   cv_top="Insights · BPO and contact centres", cv_kick="Full report · November 2026",
   cv_h1="Hiring in Uzbekistan:<br><span>what a support agent</span><br>costs",
   cv_sub="Expectations of contact-centre agents, tech support and translators by language, experience and region, the talent pool, team cost for the employer and a country comparison",
   exps=[("0", "No experience"), ("1-2", "1–2 years"), ("3-5", "3–5 years"), ("6+", "6+ years")], all="All levels",
   few=f"not enough data – fewer than {MIN_N} CVs", mln="M", sum="UZS", cvs="CVs",
   th=["Experience", "CVs", "10%", "25%", "Median", "75%", "90%", "≈ $ median", "In USD"],
   grp={"cc": ("Contact-centre agent", "all contact-centre agents"), "cc_eng_b1": ("Agent, English B1+", ""),
        "cc_eng_b2": ("Agent, English B2+", ""), "cc_eng_c1": ("Agent, English C1+", ""),
        "cc_rus_c1": ("Agent, Russian C1+", ""), "cc_regions": ("Agent, regions", "all cities except Tashkent"),
        "cc_eng_b2_regions": ("Agent, English B2+, regions", ""), "support": ("Tech support", "technical support specialists"),
        "support_eng_b2": ("Tech support, English B2+", ""), "translator": ("Translator", "written and oral translators"),
        "translator_eng_c1": ("Translator, English C1+", ""), "bpo_core": ("All BPO roles", "")},
   lang={"eng.b1": "English B1+", "eng.b2": "English B2+", "eng.c1": "English C1+", "rus.c1": "Russian C1+",
         "tur.b2": "Turkish B2+", "kor.b2": "Korean B2+", "deu.b2": "German B2+", "zho.b2": "Chinese B2+",
         "ara.b2": "Arabic B2+", "fra.b2": "French B2+"},
   country={"ph": "Philippines", "eg": "Egypt (Cairo)", "ge": "Georgia (Tbilisi)", "kz": "Kazakhstan (Almaty)"},
   basis={"gross": "gross", "net": "net", "mixed": "gross and net mixed"},
 ),
}


def e(s):
    return html.escape(str(s), quote=True)


def build(L, out):
    t = T[L]
    ru = L == "ru"
    dec, thou = ("," , " ") if ru else (".", ",")
    num = lambda x: f"{x:,.0f}".replace(",", thou)
    mln = lambda x: f"{x / 1e6 + 1e-9:.1f}".replace(".", dec)
    usd = lambda x: "$" + num(round(x / RATE / 5) * 5)
    pct = lambda a, b: f"{round(100 * a / b)}%"
    row = lambda g, k: dict(zip(F, D["resumes"][g][k]))
    P = D["pool"]
    G = lambda g: t["grp"][g][0]

    def page(n, body, cls=""):
        foot = "" if n == 1 else (f'<footer class="pf"><span>{e(t["foot"])}</span><a href="https://humancapital.uz">humancapital.uz</a>'
                                  f'<span>{n} / {TOTAL}</span></footer>')
        return f'<section class="page {cls}">{body}{foot}</section>'

    def head(no, title, lead=""):
        return (f'<header class="ph"><span class="ph-no">{e(no)}</span><h2>{e(title)}</h2>'
                + (f'<p class="ph-lead">{lead}</p>' if lead else "") + "</header>")

    def rng(r, top=25e6):
        p = lambda v: f"{min(v, top) / top * 100:.2f}%"
        return ('<div class="rng" style="background:repeating-linear-gradient(90deg,#efede8 0 0.2mm,transparent 0.2mm 8.8mm)">'
                f'<i class="w" style="left:{p(r["p10"])};right:calc(100% - {p(r["p90"])})"></i>'
                f'<i class="b" style="left:{p(r["p25"])};right:calc(100% - {p(r["p75"])})"></i>'
                f'<i class="d" style="left:{p(r["p50"])}"></i></div>')

    def bars(items, top, fmt):
        o = '<div class="bars">'
        for label, v, hl in items:
            o += (f'<div class="bar{" hl" if hl else ""}"><span class="bl">{e(label)}</span>'
                  f'<span class="bt"><i style="width:{max(v / top * 100, 0.6):.1f}%"></i></span><span class="bv">{fmt(v)}</span></div>')
        return o + "</div>"

    def grp_table(g):
        a = row(g, "all")
        name, desc = t["grp"][g]
        o = (f'<div class="gt"><div class="gt-h"><b>{e(name)}</b><em>{num(a["n"])} {t["cvs"]} · USD {pct(a["n_usd"], a["n"])}'
             + (f' · {"Ташкент" if ru else "Tashkent"} {pct(a["n_tashkent"], a["n"])}' if a["n_tashkent"] else "")
             + '</em></div><table class="t t2"><thead><tr>' + "".join(f"<th>{x}</th>" for x in t["th"]) + "</tr></thead><tbody>")
        for k, label in t["exps"] + [("all", t["all"])]:
            r = row(g, k)
            cls = ' class="tot"' if k == "all" else ""
            if r["n"] < MIN_N:
                o += f'<tr{cls}><td>{label}</td><td>{num(r["n"])}</td><td colspan="7" class="na">{t["few"]}</td></tr>'
                continue
            o += (f'<tr{cls}><td>{label}</td><td>{num(r["n"])}</td><td>{mln(r["p10"])}</td><td>{mln(r["p25"])}</td><td><b>{mln(r["p50"])}</b></td>'
                  f'<td>{mln(r["p75"])}</td><td>{mln(r["p90"])}</td><td>{usd(r["p50"])}</td><td>{pct(r["n_usd"], r["n"])}</td></tr>')
        return o + "</tbody></table></div>"

    cc, b2, c1, rus = (row(g, "all") for g in ("cc", "cc_eng_b2", "cc_eng_c1", "cc_rus_c1"))
    sup, tr = row("support_eng_b2", "all"), row("translator_eng_c1", "all")
    fd = D["found"]
    # стоимость для работодателя: на руки → начислено (НДФЛ 7,5% / 12%) + соцналог (0% / 12%)
    net = cc["p50"]
    res_cost, reg_gross = net / 0.925, net / 0.88
    reg_cost = reg_gross * 1.12
    team = 30
    V = D["vacancies_cc"]

    # ---------- 1. Обложка ----------
    p1 = f"""
<div class="cv-top"><img src="file://{ROOT}/logo-white.png" alt="Human and Capital"><span>{e(t['cv_top'])}</span></div>
<div class="cv-mid"><p class="cv-kick">{e(t['cv_kick'])}</p><h1>{t['cv_h1']}</h1><p class="cv-sub">{e(t['cv_sub'])}</p></div>
<div class="cv-kf">
  <div><b>≈ {usd(b2['p50'])}</b><span>{"медиана ожиданий оператора с английским B2+ на руки – как и без английского" if ru else "median net ask of an agent with English B2+ – the same as without English"}</span></div>
  <div><b>≈ {usd(res_cost)}</b><span>{"в месяц обходится оператор работодателю – резиденту IT Park" if ru else "monthly cost of an agent for an IT Park resident employer"}</span></div>
  <div><b>{num(round(P['eng.b2@97'], -2))}</b><span>{"резюме с английским B2+ за год" if ru else "CVs with English B2+ in the last year"}</span></div>
  <div><b>−{round((1 - res_cost / reg_cost) * 100)}%</b><span>{"фонд оплаты труда у резидента IT Park против обычной компании" if ru else "payroll cost for an IT Park resident vs a regular company"}</span></div>
</div>
<div class="cv-foot"><span>{num(fd['bpo_core'])} {"резюме BPO-ролей" if ru else "BPO CVs"} · {num(P['all@97'])} {"резюме в резерве" if ru else "CVs in the talent pool"} · {D['snapshot']}</span><span>humancapital.uz</span></div>
"""

    # ---------- 2. Главное ----------
    if ru:
        keys = [
            f"<b>Оператор с английским B2+ просит {mln(b2['p50'])} млн сум на руки (≈ {usd(b2['p50'])}) – столько же, сколько любой оператор.</b> Средние 50% – от {mln(b2['p25'])} до {mln(b2['p75'])} млн. С русским C1+ – {mln(rus['p50'])} млн.",
            f"<b>Опыт важнее языка.</b> Медиана оператора с B2+ растёт с {mln(row('cc_eng_b2','1-2')['p50'])} млн при 1–2 годах до {mln(row('cc_eng_b2','3-5')['p50'])} млн при 3–5 годах; язык поднимает только верх: верхняя четверть при 3–5 годах – {mln(row('cc_eng_b2','3-5')['p75'])} млн против {mln(row('cc','3-5')['p75'])} млн у всех операторов.",
            f"<b>Поддержка и переводчики дороже.</b> Техподдержка с английским B2+ – {mln(sup['p50'])} млн (≈ {usd(sup['p50'])}), переводчик с английским C1+ – {mln(tr['p50'])} млн (≈ {usd(tr['p50'])}).",
            f"<b>Резерв – английский и русский.</b> {num(P['eng.b2@97'])} резюме с английским B2+ и {num(P['rus.c1@97'])} с русским C1+ за год; турецкий, корейский, немецкий – единицы тысяч.",
            f"<b>Работодатели предлагают больше, чем просят.</b> Медиана {V['all'][0]} вакансий операторов с зарплатой – {mln(V['all'][2])} млн против {mln(cc['p50'])} млн в резюме; почти половина вакансий – без опыта.",
            f"<b>Оператор обходится резиденту IT Park в ≈ {usd(res_cost)} в месяц</b> против ≈ {usd(reg_cost)} у обычной компании (−{round((1 - res_cost / reg_cost) * 100)}%). По стоимости Узбекистан сопоставим с Филиппинами и Египтом, дешевле Грузии и Казахстана – и говорит по-русски.",
        ]
        how = [f"Все суммы – <b>ожидания кандидатов на руки</b>, млн сум в месяц, по резюме, обновлённым за 90 дней до {D['snapshot']}; только кандидаты, которые живут в Узбекистане.",
               "<b>25% / медиана / 75% / 90%</b> – квантили: четверть кандидатов просит меньше первой цифры, половина – меньше медианы, 10% – больше последней.",
               f"<b>≈ $</b> – по курсу {num(RATE)} сум за $1. <b>В USD</b> – доля кандидатов, назвавших сумму в долларах.",
               "Уровень языка – как указан в резюме, фильтр «не ниже указанного». Срезы меньше 30 резюме не показываем."]
        toc = "Дальше: <b>3</b> кадровый резерв · <b>4</b> ожидания по ролям · <b>5–6</b> полные таблицы · <b>7</b> регионы, вакансии и стоимость команды · <b>8</b> страны и выводы · <b>9</b> методология и контакты"
    else:
        keys = [
            f"<b>An agent with English B2+ asks UZS {mln(b2['p50'])}M net (≈ {usd(b2['p50'])}) – the same as any agent.</b> The middle 50% ask UZS {mln(b2['p25'])}–{mln(b2['p75'])}M. With Russian C1+ – UZS {mln(rus['p50'])}M.",
            f"<b>Experience matters more than language.</b> The median for B2+ agents grows from UZS {mln(row('cc_eng_b2','1-2')['p50'])}M at 1–2 years to {mln(row('cc_eng_b2','3-5')['p50'])}M at 3–5 years; English lifts only the top: the upper quartile at 3–5 years is UZS {mln(row('cc_eng_b2','3-5')['p75'])}M vs {mln(row('cc','3-5')['p75'])}M for all agents.",
            f"<b>Support and translators cost more.</b> Tech support with English B2+ – UZS {mln(sup['p50'])}M (≈ {usd(sup['p50'])}), translator with English C1+ – UZS {mln(tr['p50'])}M (≈ {usd(tr['p50'])}).",
            f"<b>The pool is English and Russian.</b> {num(P['eng.b2@97'])} CVs with English B2+ and {num(P['rus.c1@97'])} with Russian C1+ in a year; Turkish, Korean, German – a few thousand.",
            f"<b>Employers offer more than candidates ask.</b> The median of {V['all'][0]} agent vacancies with a salary is UZS {mln(V['all'][2])}M vs {mln(cc['p50'])}M in CVs; almost half of the vacancies are entry-level.",
            f"<b>An agent costs an IT Park resident ≈ {usd(res_cost)} a month</b> vs ≈ {usd(reg_cost)} for a regular company (−{round((1 - res_cost / reg_cost) * 100)}%). On cost Uzbekistan is comparable to the Philippines and Egypt, cheaper than Georgia and Kazakhstan – and it speaks Russian.",
        ]
        how = [f"All amounts are <b>candidates’ net expectations</b>, UZS million per month, from CVs updated within 90 days before {D['snapshot']}; candidates living in Uzbekistan only.",
               "<b>25% / median / 75% / 90%</b> are percentiles: a quarter of candidates ask less than the first figure, half less than the median, 10% more than the last.",
               f"<b>≈ $</b> – at UZS {num(RATE)} per $1. <b>In USD</b> – share of candidates who stated their salary in dollars.",
               "Language level as stated in the CV, filter “level or higher”. Slices with fewer than 30 CVs are not shown."]
        toc = "Next: <b>3</b> talent pool · <b>4</b> expectations by role · <b>5–6</b> full tables · <b>7</b> regions, vacancies and team cost · <b>8</b> countries and takeaways · <b>9</b> methodology and contacts"
    p2 = head("", "Главное" if ru else "Key findings") + '<ol class="key">' + "".join(f"<li>{k}</li>" for k in keys) + "</ol>" + \
        f'<div class="how"><h3>{"Как читать таблицы" if ru else "How to read the tables"}</h3><ul>' + "".join(f"<li>{h}</li>" for h in how) + \
        f'</ul></div><p class="toc" style="margin-top:5mm">{toc}</p>'

    # ---------- 3. Кадровый резерв ----------
    langs = ["eng.b1", "eng.b2", "eng.c1", "rus.c1", "tur.b2", "kor.b2", "deu.b2", "zho.b2", "ara.b2", "fra.b2"]
    pool_bars = bars([(t["lang"][k], P[k + "@97"], k == "eng.b2") for k in langs], P["rus.c1@97"], num)
    pt = ('<table class="t"><thead><tr><th>' + ("Язык и уровень" if ru else "Language and level") + "</th><th>"
          + ("Резюме, Узбекистан" if ru else "CVs, Uzbekistan") + "</th><th>" + ("Из них Ташкент" if ru else "Of which Tashkent")
          + "</th><th>" + ("Доля Ташкента" if ru else "Tashkent share") + "</th></tr></thead><tbody>")
    for k in langs:
        a, b = P[k + "@97"], P[k + "@2759"]
        pt += f"<tr><td>{t['lang'][k]}</td><td>{num(a)}</td><td>{num(b)}</td><td>{pct(b, a)}</td></tr>"
    pt += (f'<tr class="tot"><td>{"Все резюме" if ru else "All CVs"}</td><td>{num(P["all@97"])}</td><td>{num(P["all@2759"])}</td>'
           f'<td>{pct(P["all@2759"], P["all@97"])}</td></tr></tbody></table>')
    share = [(G(g), fd[g] / fd["cc"] * 100, g == "cc_eng_b2") for g in ("cc_rus_c1", "cc_eng_b1", "cc_eng_b2", "cc_eng_c1")]
    p3 = head("1", "Кадровый резерв по языкам" if ru else "Talent pool by language",
              ("Резюме, обновлённые за год, авторы живут в Узбекистане; уровень – не ниже указанного. Один человек может разместить несколько резюме."
               if ru else "CVs updated within a year, candidates living in Uzbekistan; level or higher. One person may post several CVs.")) + pool_bars + \
        f'<h3 class="sub">{"Узбекистан и Ташкент" if ru else "Uzbekistan and Tashkent"}</h3>' + pt + \
        f'<h3 class="sub">{"Сколько операторов колл-центра указывают язык" if ru else "How many contact-centre agents state a language"}</h3>' + \
        bars(share, 100, lambda v: f"{round(v)}%") + \
        (f'<p class="note">Доля от {num(fd["cc"])} резюме операторов колл-центра с указанной зарплатой за 90 дней. Русский C1+ указывают не все носители – часть отмечает «родной».</p>'
         if ru else f'<p class="note">Share of {num(fd["cc"])} contact-centre CVs with a stated salary in 90 days. Not all native Russian speakers tick C1+ – some mark “native”.</p>')

    # ---------- 4. Ожидания по ролям ----------
    order = ["translator_eng_c1", "translator", "support_eng_b2", "support", "cc_rus_c1", "cc_eng_c1", "cc_eng_b2", "cc_eng_b1", "cc"]
    head_r = ("<th>Роль</th><th>Резюме</th><th>25%</th><th>Медиана</th><th>75%</th><th>90%</th><th>≈ $</th><th>В USD</th>" if ru else
              "<th>Role</th><th>CVs</th><th>25%</th><th>Median</th><th>75%</th><th>90%</th><th>≈ $</th><th>In USD</th>")
    tt = ('<table class="t"><thead><tr>' + head_r + '<th class="rh">' + ("Разброс, млн сум" if ru else "Range, UZS M")
          + '<span class="sc"><i style="left:0">0</i><i style="left:40%">10</i><i style="left:80%">20</i></span></th></tr></thead><tbody>')
    for g in order + ["bpo_core"]:
        r = row(g, "all")
        tt += (f'<tr{" class=tot" if g == "bpo_core" else ""}><td>{e(G(g))}</td><td>{num(r["n"])}</td><td>{mln(r["p25"])}</td><td><b>{mln(r["p50"])}</b></td>'
               f'<td>{mln(r["p75"])}</td><td>{mln(r["p90"])}</td><td>{usd(r["p50"])}</td><td>{pct(r["n_usd"], r["n"])}</td><td class="rc">{rng(r)}</td></tr>')
    tt += "</tbody></table>"

    def heat(v):
        stops = [(4e6, (251, 246, 234)), (8e6, (227, 193, 114)), (15e6, (150, 112, 26))]
        v = max(stops[0][0], min(v, stops[-1][0]))
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if v <= b:
                k = (v - a) / (b - a)
                return f"rgb{tuple(round(x + (y - x) * k) for x, y in zip(ca, cb))}", ("#fff" if v >= 11e6 else "#0e0e0d")
    hm = f'<table class="hm"><thead><tr><th>{"Медиана, млн сум" if ru else "Median, UZS M"}</th>' + "".join(f"<th>{x}</th>" for _, x in t["exps"]) + "</tr></thead><tbody>"
    for g in order:
        hm += f"<tr><td>{e(G(g))}</td>"
        for k, _ in t["exps"]:
            r = row(g, k)
            if r["n"] < MIN_N:
                hm += f'<td class="na">{"мало данных" if ru else "n/a"}</td>'
            else:
                bg, fg = heat(r["p50"])
                hm += f'<td style="background:{bg};color:{fg}">{mln(r["p50"])}</td>'
        hm += "</tr>"
    hm += "</tbody></table>"
    p4 = head("2", "Ожидания по ролям" if ru else "Expectations by role",
              ("Все уровни опыта. На полосе – средние 50% кандидатов (25–75%), тонкая линия – от 10% до 90%, точка – медиана."
               if ru else "All experience levels. Band – middle 50% (25–75%), thin line – 10th to 90th percentile, dot – median.")) + tt + \
        f'<h3 class="sub">{"Медиана по роли и опыту" if ru else "Median by role and experience"}</h3>' + \
        (f'<p class="lead2">Без опыта все роли просят 5–6 млн; к 6+ годам переводчики и поддержка с английским уходят к 12–15 млн, а операторы остаются около 7 млн.</p>'
         if ru else '<p class="lead2">Without experience every role asks UZS 5–6M; by 6+ years translators and English-speaking support reach 12–15M, while agents stay around 7M.</p>') + hm

    # ---------- 5–6. Полные таблицы ----------
    p5 = head("3", "Роль × опыт: полные таблицы" if ru else "Role × experience: full tables",
              ("Ожидания на руки, млн сум в месяц. Опыт – общий стаж из резюме." if ru else "Net expectations, UZS million per month. Experience is total work experience from the CV.")) + \
        "".join(grp_table(g) for g in ("cc", "cc_eng_b1", "cc_eng_b2", "cc_eng_c1", "cc_rus_c1"))
    p6 = head("3", "Роль × опыт (продолжение)" if ru else "Role × experience (continued)") + \
        "".join(grp_table(g) for g in ("support", "support_eng_b2", "translator", "translator_eng_c1"))

    # ---------- 7. Регионы и вакансии ----------
    rt = ('<table class="t"><thead><tr><th>' + ("Срез" if ru else "Slice") + "</th><th>" + ("Резюме в hh за 90 дней" if ru else "CVs found, 90 days")
          + "</th><th>25%</th><th>" + ("Медиана" if ru else "Median") + "</th><th>75%</th><th>90%</th></tr></thead><tbody>")
    for g in ("cc", "cc_regions", "cc_eng_b2", "cc_eng_b2_regions"):
        r = row(g, "all")
        rt += f"<tr><td>{e(G(g))}</td><td>{num(fd[g])}</td><td>{mln(r['p25'])}</td><td><b>{mln(r['p50'])}</b></td><td>{mln(r['p75'])}</td><td>{mln(r['p90'])}</td></tr>"
    rt += "</tbody></table>"
    vt = ('<table class="t vt"><thead><tr><th>' + ("Опыт в вакансии" if ru else "Experience in vacancy") + "</th><th>"
          + ("Вакансий" if ru else "Vacancies") + "</th><th>25%</th><th>" + ("Предлагают, медиана" if ru else "Offered, median")
          + "</th><th>75%</th></tr></thead><tbody>")
    for k, lbl in (("no_exp", "Без опыта" if ru else "No experience"), ("1-3", "1–3 года" if ru else "1–3 years"),
                   ("3-6", "3–6 лет" if ru else "3–6 years"), ("all", t["all"])):
        n, a, m, b = V[k]
        cls = ' class="tot"' if k == "all" else ""
        if n < MIN_N:
            vt += f'<tr{cls}><td>{lbl}</td><td>{n}</td><td colspan="3" class="na">{"мало данных" if ru else "not enough data"}</td></tr>'
        else:
            vt += f"<tr{cls}><td>{lbl}</td><td>{n}</td><td>{mln(a)}</td><td><b>{mln(m)}</b></td><td>{mln(b)}</td></tr>"
    vt += "</tbody></table>"
    if ru:
        reg_txt = (f"<p class='lead2'>{pct(fd['cc_regions'], fd['cc'])} резюме операторов – из регионов. Медиана там та же, {mln(row('cc_regions','all')['p50'])} млн; "
                   f"разница в верхней части: у операторов с английским B2+ верхняя четверть в регионах – {mln(row('cc_eng_b2_regions','all')['p75'])} млн, "
                   f"по всей стране – {mln(b2['p75'])} млн. Резюме с английским B2+ в регионах – {num(fd['cc_eng_b2_regions'])} из {num(fd['cc_eng_b2'])}.</p>")
        vac_txt = (f"<p class='note'>{V['all'][0]} открытых вакансий операторов колл-центра с указанной зарплатой на {V['snapshot']}; вилка «от – до» – по середине; "
                   f"{V['gross_pct']}% вакансий указывают сумму до налога, в долларах – {V['usd_pct']}%, в Ташкенте – {V['tash_pct']}%. "
                   f"Вакансий для 6+ лет с зарплатой почти нет. Работодатели платят за скорость найма: медиана предложения выше медианы ожиданий ({mln(cc['p50'])} млн).</p>")
    else:
        reg_txt = (f"<p class='lead2'>{pct(fd['cc_regions'], fd['cc'])} of agent CVs come from outside Tashkent. The median there is the same, UZS {mln(row('cc_regions','all')['p50'])}M; "
                   f"the difference is at the top: for agents with English B2+ the upper quartile is UZS {mln(row('cc_eng_b2_regions','all')['p75'])}M in the regions vs "
                   f"{mln(b2['p75'])}M nationwide. Regional CVs with English B2+ – {num(fd['cc_eng_b2_regions'])} of {num(fd['cc_eng_b2'])}.</p>")
        vac_txt = (f"<p class='note'>{V['all'][0]} open contact-centre vacancies with a stated salary as of {V['snapshot']}; ranges taken at the midpoint; "
                   f"{V['gross_pct']}% state the amount gross, {V['usd_pct']}% in dollars, {V['tash_pct']}% are in Tashkent. "
                   f"There are almost no 6+ year vacancies with a salary. Employers pay for hiring speed: the median offer is above the median ask (UZS {mln(cc['p50'])}M).</p>")
    p7 = head("4", "Ташкент или регионы" if ru else "Tashkent or the regions") + reg_txt + rt + \
        f'<header class="ph ph2"><span class="ph-no">5</span><h2>{"Что предлагают работодатели" if ru else "What employers offer"}</h2>' + \
        f'<p class="ph-lead">{"Зарплаты в вакансиях операторов колл-центра, млн сум в месяц." if ru else "Salaries in contact-centre vacancies, UZS million per month."}</p></header>' + vt + vac_txt

    # ---------- 8. Стоимость, страны, выводы, контакты ----------
    ct = ('<table class="t"><thead><tr><th></th><th>' + ("Резидент IT Park" if ru else "IT Park resident") + "</th><th>"
          + ("Обычная компания" if ru else "Regular company") + "</th></tr></thead><tbody>"
          + f"<tr><td>{'На руки (медиана оператора)' if ru else 'Net (agent median)'}</td><td>{mln(net)} {t['mln']}</td><td>{mln(net)} {t['mln']}</td></tr>"
          + f"<tr><td>{'Начислено' if ru else 'Gross'}</td><td>{mln(res_cost)} {t['mln']} ({'НДФЛ' if ru else 'income tax'} 7,5%)</td><td>{mln(reg_gross)} {t['mln']} ({'НДФЛ' if ru else 'income tax'} 12%)</td></tr>".replace("7,5", "7,5" if ru else "7.5")
          + f"<tr><td>{'Социальный налог' if ru else 'Social tax'}</td><td>0%</td><td>12%</td></tr>"
          + f"<tr class='tot'><td>{'Стоимость в месяц' if ru else 'Monthly cost'}</td><td>{mln(res_cost)} {t['mln']} ≈ {usd(res_cost)}</td><td>{mln(reg_cost)} {t['mln']} ≈ {usd(reg_cost)}</td></tr>"
          + f"<tr class='tot'><td>{'Команда из 30 операторов' if ru else 'Team of 30 agents'}</td><td>≈ {usd(res_cost * team)}</td><td>≈ {usd(reg_cost * team)}</td></tr>"
          + "</tbody></table>")
    cr = ('<table class="t"><thead><tr><th>' + ("Страна" if ru else "Country") + "</th><th>" + ("Оператор с английским, в месяц" if ru else "Agent with English, per month")
          + "</th><th>≈ $</th><th>" + ("Источник" if ru else "Source") + "</th></tr></thead><tbody>"
          + f"<tr class='tot'><td>{'Узбекистан' if ru else 'Uzbekistan'}</td><td>{mln(b2['p50'])} {t['mln']} {t['sum']}, {t['basis']['net']}</td><td>{usd(b2['p50'])}</td><td>{'наши данные' if ru else 'our data'}</td></tr>")
    for code, val, cur, fx, basis, url, src in D["countries"]["rows"]:
        lo, hi = (val, val) if isinstance(val, (int, float)) else val
        usd_c = f"${num(round(lo / fx / 10) * 10)}" + ("" if lo == hi else f"–{num(round(hi / fx / 10) * 10)}")
        loc = f"{num(lo)}" + ("" if lo == hi else f"–{num(hi)}") + f" {cur}"
        cr += f"<tr><td>{t['country'][code]}</td><td>{loc}, {t['basis'][basis]}</td><td>{usd_c}</td><td><a href='{url}'>{src}</a></td></tr>"
    cr += "</tbody></table>"
    todo = ([("Проверяйте язык на отборе.", "Уровень в резюме кандидаты указывают сами; реальный B2 подтверждают интервью на английском и тестовый звонок."),
             ("Платите за опыт, а не за строчку «английский».", f"Медиана одинакова, но лучшие операторы с языком и опытом 3+ лет просят от {mln(row('cc_eng_b2','3-5')['p75'])} млн – закладывайте это в вилку тимлидов и ключевых ролей."),
             ("Двуязычная команда – главное преимущество рынка.", "Английский и русский на одной линии без надбавки."),
             ("Рассмотрите регион для массовой линии.", "Медиана та же, верх вилки ниже, конкуренция за людей меньше."),
             ("Оформляйте через резидента IT Park.", f"Около {round((1 - res_cost / reg_cost) * 100)}% экономии на фонде оплаты труда без своего юрлица – например, через аутстаффинг Human and Capital.")]
            if ru else
            [("Test language during selection.", "Candidates self-report their level; a real B2 is confirmed by an interview in English and a test call."),
             ("Pay for experience, not for the word “English”.", f"The median is the same, but the best agents with language and 3+ years ask from UZS {mln(row('cc_eng_b2','3-5')['p75'])}M – budget for that in team leads and key roles."),
             ("A bilingual team is the market’s main advantage.", "English and Russian on one line at no premium."),
             ("Consider a regional site for volume lines.", "Same median, lower top of the range, less competition for people."),
             ("Employ through an IT Park resident.", f"About {round((1 - res_cost / reg_cost) * 100)}% payroll savings without your own legal entity – for example, through Human and Capital outstaffing.")])
    p7 += (f'<header class="ph ph2"><span class="ph-no">6</span><h2>{"Стоимость команды" if ru else "Team cost"}</h2>'
           f'<p class="ph-lead">{"Типовой расчёт по налогам; без ставки агентства, расходов на офис и оборудование." if ru else "Typical tax calculation; excluding agency fee, office and equipment."}</p></header>' + ct)
    p8 = head("7", "Узбекистан и другие страны" if ru else "Uzbekistan vs other countries") + cr + \
        (f'<p class="note">Источники и методы различаются – ориентир, а не точное сравнение; курсы на {D["countries"]["fx_date"]}.</p>' if ru else
         f'<p class="note">Sources and methods differ – a guide, not an exact comparison; exchange rates as of {D["countries"]["fx_date"]}.</p>') + \
        f'<header class="ph ph2"><span class="ph-no">8</span><h2>{"Что делать компании" if ru else "What to do"}</h2></header><ol class="todo">' + \
        "".join(f"<li><b>{a}</b> {b}</li>" for a, b in todo) + "</ol>"

    meth = ([f"<b>Ожидания</b> – резюме операторов колл-центра (роль hh 83), техподдержки (121) и переводчиков (93) с указанной зарплатой, доступные агентству как работодателю на job-сайтах Узбекистана и обновлённые за 90 дней до {D['snapshot']}; только живущие в Узбекистане. Расчёт по выборке свежих резюме в каждом срезе с поправкой на размер.",
             "<b>Резерв</b> – число резюме за год по фильтру «язык не ниже уровня»; один человек может разместить несколько резюме.",
             f"<b>Налоги</b> – по данным IT Park: НДФЛ сотрудников резидента 7,5%, социальный налог 0%; у обычной компании 12% и 12%. Курс {num(RATE)} сум за $1."]
            if ru else
            [f"<b>Expectations</b> – CVs of contact-centre agents, tech support and translators with a stated salary, available to the agency as an employer on Uzbekistan’s job sites and updated within 90 days before {D['snapshot']}; candidates living in Uzbekistan only. Calculated on a sample of recent CVs in each slice, weighted by size.",
             "<b>Talent pool</b> – number of CVs updated within a year with the language at or above the level; one person may post several CVs.",
             f"<b>Taxes</b> – per IT Park: employee income tax 7.5% and social tax 0% for residents; 12% and 12% for a regular company. Rate UZS {num(RATE)} per $1."])
    p9 = head("9", "Методология" if ru else "Methodology") + '<ul class="meth">' + "".join(f"<li>{m}</li>" for m in meth) + "</ul>"
    p9 += (f"""<div class="cta"><div><h3>{"Соберём команду под ваш проект" if ru else "We will build your team"}</h3>
<p>{"Подбор, оформление через резидента IT Park и сопровождение операторов, поддержки и переводчиков – в Ташкенте и регионах." if ru else "Recruitment, employment through an IT Park resident and ongoing support of agents, tech support and translators – in Tashkent and the regions."}</p>
<a class="btn" href="https://humancapital.uz/{"outstaffing.html" if ru else "outstaffing-en.html"}">{"Обсудить команду → humancapital.uz" if ru else "Discuss your team → humancapital.uz"}</a></div>
<ul class="ct"><li><span>{"Телефон" if ru else "Phone"}</span><a href="tel:+998903251336">+998 90 325 13 36</a></li>
<li><span>Email</span><a href="mailto:akmal.s@human-capital.org">akmal.s@human-capital.org</a></li>
<li><span>Telegram</span><a href="https://t.me/Djuanna555">t.me/Djuanna555</a></li>
<li><span>{"Онлайн-версия" if ru else "Online version"}</span><a href="{ARTICLE[L]}">humancapital.uz/articles</a></li></ul></div>
<div class="about"><img src="file://{ROOT}/logo.png" alt="Human and Capital"><p>{"<b>Human and Capital</b> – рекрутинговое и HR-агентство в Ташкенте, резидент IT Park: подбор персонала, аутстаффинг и Employer of Record, executive search, HR-консалтинг. Авторы обзора – Акмаль Саипов, коммерческий директор, и Анна Джу, генеральный директор, соучредители компании." if ru else "<b>Human and Capital</b> is a recruitment and HR agency in Tashkent and an IT Park resident: recruitment, outstaffing and Employer of Record, executive search, HR consulting. Authors – Akmal Saipov, Commercial Director, and Anna Dju, CEO, co-founders of the company."}</p></div>
<p class="legal">© Human and Capital, 2026. {"При цитировании ссылка на humancapital.uz обязательна." if ru else "Please credit humancapital.uz when quoting."}</p>""")

    css = CSS + ".cover h1{font-size:30pt}.cv-mid{margin-top:30mm}.cv-kf{margin-top:16mm !important}.meth{font-size:8.6pt}.cta{padding:5.5mm}.todo li{font-size:9pt}"
    doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{e(t["foot"])}</title><meta name="author" content="Human and Capital">'
           '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Unbounded:wght@600;700;800&display=block" rel="stylesheet">'
           f"<style>{css}</style></head><body>"
           + page(1, p1, "cover") + page(2, p2) + page(3, p3) + page(4, p4) + page(5, p5) + page(6, p6) + page(7, p7) + page(8, p8) + page(9, p9)
           + "</body></html>").replace("≈ ", "≈ ")
    tmp = tempfile.mkdtemp(prefix="hc-bpo-")
    src = os.path.join(tmp, "report.html")
    open(src, "w", encoding="utf-8").write(doc)
    out = os.path.abspath(os.path.expanduser(out))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    "--virtual-time-budget=15000", "--print-to-pdf=" + out, "file://" + src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("html:", src)
    print("pdf: ", out, f"({os.path.getsize(out) // 1024} КБ)")


if __name__ == "__main__":
    langs = [sys.argv[1]] if len(sys.argv) > 1 else ["ru", "en"]
    for L in langs:
        build(L, sys.argv[2] if len(sys.argv) > 2 else OUTS[L])
