"""PDF-отчёт «Зарплаты в IT в Узбекистане: осень 2026» – полная версия обзора для формы скачивания в статье.

Данные – агрегаты из tools/reports/it-salaries-2026-autumn.json (выгрузка из ATS, без ПДн).
Сборка: HTML (A4, шрифты Unbounded/Inter как на сайте) → PDF через headless Chrome:
    python3 tools/build_report.py
PDF НЕ публикуется на сайте (решение 30.10.2026: отчёт только по запросу – форма в статье создаёт
в Staffly сделку «Запрос отчёта (PDF)», менеджер отправляет файл на почту). Поэтому PDF пишется
вне репозитория – по умолчанию в ~/Downloads, путь можно передать аргументом:
    python3 tools/build_report.py ~/Desktop/report.pdf
HTML для проверки вёрстки остаётся рядом с PDF во временной папке (путь печатается).

Правила данных: срезы n < 30 не показываем; медианы и квантили; суммы – ожидания кандидатов на руки;
источник – «резюме, доступные агентству как работодателю на job-сайтах Узбекистана».
"""
import html
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "tools", "reports", "it-salaries-2026-autumn.json"), encoding="utf-8"))
OUT = os.path.abspath(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else
                                          "~/Downloads/Зарплаты в IT в Узбекистане – осень 2026 (Human and Capital).pdf"))
ARTICLE = "https://humancapital.uz/articles/zarplaty-v-it-v-uzbekistane-osen-2026-ed99d01e"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MIN_N = 30
RATE = DATA["rate"]
R = DATA["resumes"]
V = DATA["vacancies"]
FIELDS = DATA["_resumes_fields"]

GROUPS = [  # порядок – по медиане ожиданий, все уровни опыта
    ("it_lead", "Руководители IT", "CIO, CTO, тимлиды, руководители аналитики"),
    ("devops", "DevOps", "DevOps-инженеры"),
    ("ba_sa", "Бизнес- и системный анализ", "бизнес- и системные аналитики"),
    ("product", "Управление продуктом", "менеджеры продукта"),
    ("dev", "Разработка", "программисты, разработчики"),
    ("data", "Аналитика данных", "BI-, продуктовые аналитики, дата-сайентисты"),
    ("security", "Информационная безопасность", "специалисты по ИБ"),
    ("qa", "Тестирование (QA)", "тестировщики"),
    ("infra", "Сисадмины и сети", "системные администраторы, системные и сетевые инженеры"),
    ("support", "Техподдержка", "специалисты технической поддержки"),
]
NAME = {k: n for k, n, _ in GROUPS}
EXPS = [("0", "Без опыта"), ("1-2", "1–2 года"), ("3-5", "3–5 лет"), ("6+", "6+ лет")]
TOTAL_PAGES = 8


def row(grp, exp):
    return dict(zip(FIELDS, R[grp][exp]))


def e(s):
    return html.escape(str(s), quote=True)


def num(x):
    return f"{x:,.0f}".replace(",", " ")


def mln(x):
    return f"{x / 1e6:.1f}".replace(".", ",")


def usd(x):
    return "$" + num(round(x / RATE / 10) * 10)


def pct(a, b):
    return f"{round(100 * a / b)}%"


# --- компоненты ---
def head(no, title, lead=""):
    return (f'<header class="ph"><span class="ph-no">{e(no)}</span><h2>{e(title)}</h2>'
            + (f'<p class="ph-lead">{lead}</p>' if lead else "") + "</header>")


def page(n, body, cls=""):
    foot = ("" if n == 1 else
            f'<footer class="pf"><span>Human and Capital · Зарплаты в IT в Узбекистане: осень 2026</span>'
            f'<a href="https://humancapital.uz">humancapital.uz</a><span>{n} / {TOTAL_PAGES}</span></footer>')
    return f'<section class="page {cls}">{body}{foot}</section>'


def rng(r, top=60e6):
    """Полоса «разброс»: тонкая линия 10–90%, полоса 25–75%, точка – медиана."""
    p = lambda v: f"{min(v, top) / top * 100:.2f}%"
    return ('<div class="rng">'
            f'<i class="w" style="left:{p(r["p10"])};right:calc(100% - {p(r["p90"])})"></i>'
            f'<i class="b" style="left:{p(r["p25"])};right:calc(100% - {p(r["p75"])})"></i>'
            f'<i class="d" style="left:{p(r["p50"])}"></i></div>')


def heat(v):
    # 5 млн – светлый, 15 – горчичный, 30+ – тёмно-горчичный
    stops = [(5e6, (251, 246, 234)), (15e6, (227, 193, 114)), (30e6, (150, 112, 26))]
    v = max(stops[0][0], min(v, stops[-1][0]))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if v <= b:
            t = (v - a) / (b - a)
            c = tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))
            return f"rgb{c}", ("#fff" if v >= 22e6 else "#0e0e0d")


def bars(items, top, fmt, note=None):
    out = '<div class="bars">'
    for label, v, sub, hl in items:
        out += (f'<div class="bar{" hl" if hl else ""}"><span class="bl">{e(label)}</span>'
                f'<span class="bt"><i style="width:{v / top * 100:.1f}%"></i></span>'
                f'<span class="bv">{fmt(v)}{f" <em>{e(sub)}</em>" if sub else ""}</span></div>')
    return out + "</div>" + (f'<p class="note">{note}</p>' if note else "")


# --- данные для текста ---
it = {k: row("it_core", k) for k, _ in EXPS + [("all", "")]}
assert all(row(g, "all")["n"] >= MIN_N for g, *_ in GROUPS)
by_med = sorted(GROUPS, key=lambda g: -row(g[0], "all")["p50"])

# ---------- 1. Обложка ----------
p1 = f"""
<div class="cv-top"><img src="file://{ROOT}/logo-white.png" alt="Human and Capital"><span>Аналитика · Зарплатный обзор</span></div>
<div class="cv-mid">
  <p class="cv-kick">Полная версия обзора · осень 2026</p>
  <h1>Зарплаты в IT<br>в <span>Узбекистане</span></h1>
  <p class="cv-sub">Сколько просят IT-специалисты по 10 ролям и 4 уровням опыта, что предлагают работодатели и сколько стоит верхний сегмент</p>
</div>
<div class="cv-kf">
  <div><b>10 млн сум</b><span>медиана ожиданий IT-специалиста на руки (≈ {usd(it['all']['p50'])})</span></div>
  <div><b>×1,8</b><span>рост ожиданий от 1–2 к 3–5 годам опыта</span></div>
  <div><b>$5 000+</b><span>просят верхние 10% разработчиков с опытом 6+ лет</span></div>
  <div><b>{pct(it['all']['n_usd'], it['all']['n'])}</b><span>IT-специалистов называют зарплату в долларах</span></div>
</div>
<div class="cv-foot"><span>{num(it['all']['n'])} резюме · {V['total']} вакансий · данные на {DATA['snapshot']}</span><span>humancapital.uz</span></div>
"""

# --- таблица «опыт × квантили» для группы ---
def grp_table(g, name, desc, bare=False):
    a = row(g, "all")
    out = ('<div class="gt">' + ("" if bare else f'<div class="gt-h"><b>{e(name)}</b>'
           f'<em>{num(a["n"])} резюме · в USD {pct(a["n_usd"], a["n"])} · Ташкент {pct(a["n_tashkent"], a["n"])}</em></div>')
           + '<table class="t t2"><thead><tr><th>Опыт</th><th>Резюме</th><th>10%</th><th>25%</th><th>Медиана</th><th>75%</th><th>90%</th><th>≈ $ медиана</th><th>В USD</th></tr></thead><tbody>')
    for k, label in EXPS + [("all", "Все уровни")]:
        r = row(g, k)
        cls = ' class="tot"' if k == "all" else ""
        if r["n"] < MIN_N:
            out += f'<tr{cls}><td>{label}</td><td>{num(r["n"])}</td><td colspan="7" class="na">мало данных – срез меньше {MIN_N} резюме</td></tr>'
            continue
        out += (f'<tr{cls}><td>{label}</td><td>{num(r["n"])}</td><td>{mln(r["p10"])}</td><td>{mln(r["p25"])}</td><td><b>{mln(r["p50"])}</b></td>'
                f'<td>{mln(r["p75"])}</td><td>{mln(r["p90"])}</td><td>{usd(r["p50"])}</td><td>{pct(r["n_usd"], r["n"])}</td></tr>')
    return out + "</tbody></table></div>"


# ---------- 2. Главное ----------
p2 = head("", "Главное") + f"""
<ol class="key">
  <li><b>Медиана ожиданий IT-специалиста – {mln(it['all']['p50'])} млн сум на руки (≈ {usd(it['all']['p50'])}).</b>
      Средние 50% кандидатов просят от {mln(it['all']['p25'])} до {mln(it['all']['p75'])} млн, верхние 10% – от {mln(it['all']['p90'])} млн.</li>
  <li><b>Опыт решает больше, чем роль.</b> От 1–2 к 3–5 годам ожидания растут в 1,8 раза ({mln(it['1-2']['p50'])} → {mln(it['3-5']['p50'])} млн),
      к 6+ годам – ещё в 1,4 раза ({mln(it['6+']['p50'])} млн). Разброс растёт вместе с опытом.</li>
  <li><b>Самые дорогие роли</b> – руководители IT ({mln(row('it_lead','all')['p50'])} млн), DevOps ({mln(row('devops','all')['p50'])} млн),
      бизнес-анализ и продукт ({mln(row('ba_sa','all')['p50'])} млн). Дешевле всего – техподдержка ({mln(row('support','all')['p50'])} млн) и сисадмины ({mln(row('infra','all')['p50'])} млн).</li>
  <li><b>Вакансии не отстают от ожиданий.</b> Для опыта 1–3 года работодатели предлагают {mln(V['by_exp']['1-3'][2])} млн (просят {mln(it['1-2']['p50'])}),
      для 3–6 лет – {mln(V['by_exp']['3-6'][2])} млн (просят {mln(it['3-5']['p50'])}). Для 6+ лет вакансий с зарплатой почти нет.</li>
  <li><b>IT-рынок почти наполовину долларовый.</b> {pct(it['all']['n_usd'], it['all']['n'])} кандидатов называют сумму в USD, в DevOps – {pct(row('devops','all')['n_usd'], row('devops','all')['n'])},
      в разработке – {pct(row('dev','all')['n_usd'], row('dev','all')['n'])}. В вакансиях доллар – только у {V['usd_share']}%.</li>
  <li><b>Верхний сегмент – $5 000–6 000 и выше.</b> Столько просят верхние 10% кандидатов с опытом 6+ лет в разработке, DevOps, бизнес-анализе, продукте и среди руководителей IT.
      Офферы руководителям IT-направлений и C-level в проектах Human and Capital – $4 000–10 000 на руки.</li>
</ol>
<div class="how">
  <h3>Как читать таблицы</h3>
  <ul>
    <li>Все суммы – <b>ожидания кандидатов на руки</b>, млн сум в месяц, по резюме IT-специалистов, обновлённым за 90 дней до {DATA['snapshot']}.</li>
    <li><b>25% / медиана / 75% / 90%</b> – квантили: четверть кандидатов просит меньше первой цифры, половина – меньше медианы, 10% – больше последней.</li>
    <li><b>≈ $</b> – медиана по курсу {num(RATE)} сум за $1. <b>В USD</b> – доля кандидатов, назвавших сумму в долларах.</li>
    <li>Срезы меньше {MIN_N} резюме не показываем – в таблицах они отмечены «мало данных».</li>
  </ul>
</div>
<h3 class="sub">Все IT-роли: ожидания по опыту</h3>
""" + grp_table("it_core", "", "", bare=True) + """
<p class="toc">Дальше: <b>3</b> ожидания по ролям · <b>4–5</b> роль × опыт по 10 группам · <b>6</b> ожидания и вакансии, доллар или сум · <b>7</b> верхний сегмент и выводы · <b>8</b> методология и контакты</p>
"""

# ---------- 3. По ролям ----------
t = ('<table class="t"><thead><tr><th>Роль</th><th>Резюме</th><th>25%</th><th>Медиана</th><th>75%</th><th>90%</th>'
     '<th>≈ $</th><th>В USD</th><th class="rh">Разброс, млн сум<span class="sc"><i style="left:0">0</i><i style="left:33.3%">20</i><i style="left:66.6%">40</i><i style="left:100%">60</i></span></th></tr></thead><tbody>')
for g, name, _ in by_med + [("it_core", "Все IT-роли", "")]:
    r = row(g, "all")
    t += (f'<tr{" class=tot" if g == "it_core" else ""}><td>{e(name)}</td><td>{num(r["n"])}</td><td>{mln(r["p25"])}</td>'
          f'<td><b>{mln(r["p50"])}</b></td><td>{mln(r["p75"])}</td><td>{mln(r["p90"])}</td><td>{usd(r["p50"])}</td>'
          f'<td>{pct(r["n_usd"], r["n"])}</td><td class="rc">{rng(r)}</td></tr>')
t += "</tbody></table>"
hm = '<table class="hm"><thead><tr><th>Медиана, млн сум</th>' + "".join(f"<th>{e(x)}</th>" for _, x in EXPS) + "</tr></thead><tbody>"
for g, name, _ in by_med + [("it_core", "Все IT-роли", "")]:
    hm += f'<tr{" class=tot" if g == "it_core" else ""}><td>{e(name)}</td>'
    for k, _ in EXPS:
        r = row(g, k)
        if r["n"] < MIN_N:
            hm += '<td class="na">мало данных</td>'
        else:
            bg, fg = heat(r["p50"])
            hm += f'<td style="background:{bg};color:{fg}">{mln(r["p50"])}</td>'
    hm += "</tr>"
hm += "</tbody></table>"
p3 = head("1", "Ожидания по ролям",
          "Все уровни опыта. Роли отсортированы по медиане; на полосе – средние 50% кандидатов (25–75%), тонкая линия – от 10% до 90%, точка – медиана.") + t + f"""
<h3 class="sub">Медиана по роли и опыту</h3>
<p class="lead2">Цена роли почти целиком определяется опытом: без опыта почти все роли просят около 6 млн, а на 6+ годах руководители IT и DevOps просят почти втрое больше техподдержки.</p>
{hm}
"""

# ---------- 4–5. Роль × опыт ----------
ORDER = [g for g in GROUPS if g[0] in ("dev", "devops", "qa", "infra", "support")] + \
        [g for g in GROUPS if g[0] not in ("dev", "devops", "qa", "infra", "support")]
p4 = head("2", "Роль × опыт: полные таблицы", "Ожидания на руки, млн сум в месяц. Опыт – общий стаж из резюме; состав групп – на стр. 8.") + "".join(grp_table(*g) for g in ORDER[:5])
p5 = head("2", "Роль × опыт (продолжение)") + "".join(grp_table(*g) for g in ORDER[5:])

# ---------- 6. Вакансии и валюта ----------
VE = V["by_exp"]
vrows = [("Без опыта", "Без опыта", it["0"], VE["0"]), ("1–2 года", "1–3 года", it["1-2"], VE["1-3"]),
         ("3–5 лет", "3–6 лет", it["3-5"], VE["3-6"]), ("6+ лет", "6+ лет", it["6+"], VE["6+"]),
         ("Все уровни", "Все уровни", it["all"], VE["all"])]
vt = ('<table class="t vt"><thead><tr><th>Опыт в резюме</th><th>Просят, медиана</th><th>Средние 50%</th>'
      '<th>Опыт в вакансии</th><th>Вакансий</th><th>Предлагают, медиана</th><th>Средние 50%</th><th>Разница</th></tr></thead><tbody>')
for a, b, r, v in vrows:
    cls = ' class="tot"' if a == "Все уровни" else ""
    left = f'<td>{a}</td><td><b>{mln(r["p50"])}</b></td><td>{mln(r["p25"])}–{mln(r["p75"])}</td><td>{b}</td><td>{v[0]}</td>'
    if v[0] < MIN_N:
        vt += f'<tr{cls}>{left}<td colspan="3" class="na">мало данных – такие зарплаты обсуждают лично</td></tr>'
    else:
        d = round((v[2] / r["p50"] - 1) * 100)
        vt += (f'<tr{cls}>{left}<td><b>{mln(v[2])}</b></td><td>{mln(v[1])}–{mln(v[3])}</td>'
               f'<td class="{"pos" if d > 0 else "neg"}">{"+" if d > 0 else "−"}{abs(d)}%</td></tr>')
vt += "</tbody></table>"
VG = V["by_grp"]
roles_v = "".join(
    f'<div class="vs"><b>{NAME[g]}</b><span>просят <strong>{mln(row(g, "all")["p50"])}</strong> · предлагают <strong>{mln(VG[g][2])}</strong> млн</span>'
    f'<em>{num(row(g, "all")["n"])} резюме · {VG[g][0]} вакансий</em></div>' for g in ("dev", "support"))
usd_items = sorted(((NAME[g], row(g, "all")["n_usd"] / row(g, "all")["n"] * 100, None, g in ("dev", "devops")) for g, *_ in GROUPS),
                   key=lambda x: -x[1])
usd_items.append(("Все IT-роли", it["all"]["n_usd"] / it["all"]["n"] * 100, None, False))
p6 = head("3", "Ожидания и вакансии",
          f"Медианы ожиданий в резюме и зарплат в {V['total']} открытых IT-вакансиях с указанной суммой на {DATA['snapshot']}, млн сум в месяц.") + vt + f"""
<p class="note">В вакансиях опыт задан диапазонами 1–3 и 3–6 лет, в резюме – 1–2 и 3–5 года, поэтому сравнение по уровням приблизительное.
{V['gross_share']}% вакансий указывают сумму до налога, остальные – на руки; вилку «от – до» считаем по середине.</p>
<div class="vs-row">{roles_v}<p>По остальным ролям вакансий с зарплатой меньше {MIN_N} – сравнение не показываем.</p></div>
<header class="ph ph2"><span class="ph-no">4</span><h2>Доллар или сум</h2><p class="ph-lead">Доля кандидатов, назвавших ожидания в долларах, все уровни опыта.</p></header>
<div class="cols">
  <div>{bars(usd_items, 100, lambda v: f"{round(v)}%")}</div>
  <div class="aside">
    <p><b>По опыту:</b> без опыта – {pct(it['0']['n_usd'], it['0']['n'])}, 1–2 года – {pct(it['1-2']['n_usd'], it['1-2']['n'])}, 3–5 лет – {pct(it['3-5']['n_usd'], it['3-5']['n'])}, 6+ лет – {pct(it['6+']['n_usd'], it['6+']['n'])}.
       Чаще всего в долларах считают мидлы; у разработчиков с опытом 3–5 лет – {pct(row('dev','3-5')['n_usd'], row('dev','3-5')['n'])}.</p>
    <p><b>В вакансиях</b> доллар – редкость: {V['usd_share']}% IT-вакансий с зарплатой, в разработке – {V['dev_usd_share']}%.</p>
    <p><b>Что из этого следует:</b> вилку для разработчиков и DevOps удобнее называть в долларах, для сисадминов и техподдержки – в сумах: там в сумах считают больше 70% кандидатов.</p>
  </div>
</div>
"""

# ---------- 7. Верхний сегмент и выводы ----------
top_items = sorted(((NAME[g], row(g, "6+")["p90"], usd(row(g, "6+")["p90"]), g in ("it_lead", "devops", "dev")) for g, *_ in GROUPS
                    if row(g, "6+")["n"] >= MIN_N), key=lambda x: -x[1])
p75_6 = sorted(((NAME[g], row(g, "6+")["p75"]) for g, *_ in GROUPS), key=lambda x: -x[1])
p7 = head("5", "Верхний сегмент",
          "Сколько просят верхние 10% кандидатов с опытом 6+ лет: с этой суммы начинается «дорогой» сеньор, млн сум на руки.") + \
     bars(top_items, 75e6, lambda v: mln(v) + " млн") + f"""
<div class="offer"><b>$4 000–10 000 на руки</b><span>Офферы руководителям IT-направлений и C-level с опытом 6+ лет в проектах Human and Capital, сентябрь – октябрь 2026.
Верхняя граница выше всего, что видно в резюме: такие специалисты не ищут работу на job-сайтах – их находят через executive search.</span></div>
<header class="ph ph2"><span class="ph-no">6</span><h2>Что делать работодателю</h2></header>
<ol class="todo">
  <li><b>Хотите выбирать из лучших – ориентируйтесь на верхнюю четверть.</b> Вилка на уровне медианы отсекает половину рынка. Для разработчика с опытом 3–5 лет верхняя четверть начинается с {mln(row('dev','3-5')['p75'])} млн (≈ {usd(row('dev','3-5')['p75'])}), для DevOps – с {mln(row('devops','3-5')['p75'])} млн.</li>
  <li><b>Закладывайте скачок на переходе в мидлы.</b> От 1–2 к 3–5 годам опыта ожидания растут в 1,8 раза. Если не пересматривать зарплату вовремя, сотрудник уйдёт к тем, кто платит по рынку.</li>
  <li><b>Называйте вилку в той валюте, в которой считает кандидат.</b> Разработчики и DevOps – в долларах, сисадмины и техподдержка – в сумах.</li>
  <li><b>Сеньоров и руководителей не найти объявлением.</b> Вакансий с зарплатой для опыта 6+ лет почти нет, а офферы таким кандидатам – от $4 000 до $10 000: нужен прямой поиск.</li>
  <li><b>На массовых позициях не переплачивайте.</b> По итогам 2025 года на одну IT-вакансию на рынке приходилось около 11 резюме; техподдержка и джуниоры просят 6–8 млн, выбрать есть из кого.</li>
</ol>
"""

# ---------- 8. Методология и контакты ----------
p8 = head("7", "Методология") + f"""
<ul class="meth">
  <li><b>Ожидания</b> – резюме IT-специалистов с указанной зарплатой, доступные агентству как работодателю на job-сайтах Узбекистана и обновлённые за 90 дней до {DATA['snapshot']}: {num(it['all']['n'])} резюме. Цифры сверены с откликами на вакансии Human and Capital.</li>
  <li><b>Роли</b> – 18 профессиональных ролей, сведённых в 10 групп: {", ".join(f"{n if n == 'DevOps' else n[0].lower() + n[1:]} ({d})" for _, n, d in GROUPS)}.</li>
  <li><b>Опыт</b> – общий стаж из резюме. У четверти резюме стаж не указан: они входят только в итоги «Все уровни».</li>
  <li><b>Предложения</b> – {V['total']} открытых IT-вакансий с указанной зарплатой на {DATA['snapshot']}; вилка «от – до» – по середине; {V['gross_share']}% вакансий указывают сумму до налога.</li>
  <li><b>Валюта</b> – суммы в долларах пересчитаны в сумы по курсу {num(RATE)} сум за $1 на дату выгрузки.</li>
  <li><b>Статистика</b> – медианы и квантили, не средние; срезы меньше {MIN_N} наблюдений не публикуются; отсеяно 2% резюме с очевидными ошибками.</li>
  <li><b>Офферы агентства</b> – обобщённо, по проектам executive search Human and Capital (сентябрь – октябрь 2026), без данных отдельных компаний.</li>
  <li><b>Ограничения</b> – ожидание в резюме не равно фактической зарплате: работающий сеньор часто получает больше, чем пишет как стартовое ожидание. Рынок – в основном Ташкент ({pct(it['all']['n_tashkent'], it['all']['n'])} резюме).</li>
</ul>
<div class="cta">
  <div><h3>Нужна вилка под вашу позицию?</h3>
  <p>Подготовим срез зарплат по вашей роли, уровню и отрасли и найдём кандидатов – от массового подбора до executive search.</p>
  <a class="btn" href="https://humancapital.uz/recruitment.html#contact">Обсудить найм → humancapital.uz</a></div>
  <ul class="ct">
    <li><span>Телефон</span><a href="tel:+998903251336">+998 90 325 13 36</a></li>
    <li><span>Email</span><a href="mailto:akmal.s@human-capital.org">akmal.s@human-capital.org</a></li>
    <li><span>Telegram</span><a href="https://t.me/Djuanna555">t.me/Djuanna555</a></li>
    <li><span>Адрес</span>Ташкент, Фаргона йули, 94</li>
  </ul>
</div>
<div class="about"><img src="file://{ROOT}/logo.png" alt="Human and Capital">
<p><b>Human and Capital</b> – рекрутинговое и HR-агентство в Ташкенте: подбор персонала, IT-рекрутмент, executive search, аутстаффинг и HR-консалтинг.
Авторы обзора – Акмаль Саипов, коммерческий директор, и Анна Джу, генеральный директор, соучредители компании. Онлайн-версия с графиками: <a href="{ARTICLE}">humancapital.uz/articles</a>.</p></div>
<p class="legal">© Human and Capital, 2026. При цитировании ссылка на humancapital.uz обязательна.</p>
"""

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Inter,sans-serif;color:#0e0e0d;font-size:10pt;line-height:1.45;background:#fff}
a{color:#8a6a1c;text-decoration:none}
.page{width:210mm;height:297mm;padding:15mm 16mm 18mm;position:relative;overflow:hidden;page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.pf{position:absolute;left:16mm;right:16mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7.5pt;color:#8a8781;border-top:0.3mm solid #e5e3dd;padding-top:2.5mm}
.pf a{color:#8a8781}
.ph{margin-bottom:5mm}
.ph2{margin-top:7mm}
.ph-no{display:inline-block;font-family:Unbounded,sans-serif;font-weight:700;font-size:9pt;color:#c69a2e;margin-bottom:1.5mm}
.ph-no:empty{display:none}
h2{font-family:Unbounded,sans-serif;font-weight:700;font-size:19pt;line-height:1.15;letter-spacing:-0.01em}
.ph-lead{margin-top:2mm;color:#4a4844;font-size:9.5pt;max-width:165mm}
h3{font-family:Unbounded,sans-serif;font-weight:600;font-size:11pt;margin-bottom:2.5mm}
h3.sub{margin-top:7mm}
.lead2{color:#4a4844;font-size:9.5pt;margin-bottom:3mm}
.note{font-size:8pt;color:#6b6862;margin-top:2.5mm;line-height:1.45}

/* обложка */
.cover{background:#0e0e0d;color:#fff;padding:18mm 18mm 16mm;display:flex;flex-direction:column}
.cover:before{content:"";position:absolute;width:150mm;height:150mm;border-radius:50%;right:-55mm;top:-60mm;background:radial-gradient(circle,rgba(198,154,46,.32),rgba(198,154,46,0) 70%)}
.cv-top{display:flex;justify-content:space-between;align-items:center;position:relative}
.cv-top img{height:15mm}
.cv-top span{font-size:8.5pt;letter-spacing:.08em;text-transform:uppercase;color:#e3c172;font-weight:600}
.cv-mid{margin-top:42mm;position:relative}
.cv-kick{font-size:10pt;color:#c69a2e;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6mm}
.cover h1{font-family:Unbounded,sans-serif;font-weight:800;font-size:38pt;line-height:1.05;text-transform:uppercase;letter-spacing:-0.01em}
.cover h1 span{color:#c69a2e}
.cv-sub{margin-top:8mm;font-size:13pt;line-height:1.45;color:#d6d3cc;max-width:150mm}
.cv-kf{margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.cv-kf div{border:0.3mm solid rgba(255,255,255,.16);border-radius:4mm;padding:5mm 5.5mm;background:rgba(255,255,255,.04)}
.cv-kf b{display:block;font-family:Unbounded,sans-serif;font-weight:700;font-size:18pt;color:#e3c172;margin-bottom:2mm}
.cv-kf span{font-size:9pt;color:#d6d3cc;line-height:1.4}
.cv-foot{margin-top:9mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#8a8781;border-top:0.3mm solid rgba(255,255,255,.14);padding-top:4mm}

/* главное */
.key{list-style:none;counter-reset:k;display:grid;gap:2.4mm}
.key li{counter-increment:k;position:relative;padding:2.6mm 4mm 2.6mm 13mm;background:#f7f6f2;border-radius:3mm;font-size:9.5pt;color:#2b2a27}
.key li:before{content:counter(k);position:absolute;left:4mm;top:2.4mm;font-family:Unbounded,sans-serif;font-weight:700;color:#c69a2e;font-size:12pt}
.key b{color:#0e0e0d}
.how{margin-top:4.5mm;padding:3.5mm 5mm;border:0.3mm solid #e5e3dd;border-left:1mm solid #c69a2e;border-radius:2mm}
.how ul{padding-left:4.5mm;font-size:8.8pt;color:#4a4844;display:grid;gap:1.3mm}
.toc{margin-top:1mm;font-size:8.3pt;color:#6b6862}
.toc b{color:#c69a2e}

/* таблицы */
.t{width:100%;border-collapse:collapse;font-size:8.6pt;font-variant-numeric:tabular-nums}
.t th{font-weight:600;font-size:7.6pt;color:#6b6862;text-align:right;padding:1.6mm 1.8mm;border-bottom:0.4mm solid #0e0e0d;white-space:nowrap}
.t td{text-align:right;padding:1.55mm 1.8mm;border-bottom:0.25mm solid #e5e3dd;white-space:nowrap}
.t th:first-child,.t td:first-child{text-align:left;padding-left:0}
.t td:first-child{white-space:normal}
.t b{font-weight:700}
.t tr.tot td{background:#f7f6f2;font-weight:600;border-bottom:0.4mm solid #cfcbc2}
.t td.na{color:#a19d95;font-style:italic;text-align:center;font-size:8pt}
.t .rh{text-align:left;width:46mm}
.t .rh .sc{display:block;position:relative;width:44mm;height:3mm;margin-top:0.8mm;font-weight:400;color:#a19d95;font-size:6.5pt}
.t .rh .sc i{position:absolute;font-style:normal;transform:translateX(-50%)}
.t .rh .sc i:first-child{transform:none}
.rc{padding-right:0}
.rng{position:relative;height:3.2mm;width:44mm;background:repeating-linear-gradient(90deg,#efede8 0 0.2mm,transparent 0.2mm 14.66mm)}
.rng i{position:absolute;top:50%}
.rng .w{height:0.35mm;background:#b9b5ac;transform:translateY(-50%)}
.rng .b{height:2.6mm;background:#e8d7a8;border-radius:0.6mm;transform:translateY(-50%)}
.rng .d{width:2.4mm;height:2.4mm;border-radius:50%;background:#0e0e0d;transform:translate(-50%,-50%)}
.hm{width:100%;border-collapse:separate;border-spacing:0.8mm;font-size:8.8pt;font-variant-numeric:tabular-nums;margin-left:-0.8mm}
.hm th{font-size:7.6pt;font-weight:600;color:#6b6862;text-align:center;padding:1mm}
.hm th:first-child{text-align:left}
.hm td{text-align:center;padding:1.7mm 1mm;border-radius:1mm;font-weight:600}
.hm td:first-child{text-align:left;font-weight:500;padding-left:0;width:52mm}
.hm tr.tot td:first-child{font-weight:700}
.hm td.na{background:#f7f6f2;color:#a19d95;font-weight:400;font-style:italic;font-size:7.6pt}
.gt{margin-bottom:3.2mm;break-inside:avoid}
.gt-h{display:flex;align-items:baseline;gap:0 2.5mm;margin-bottom:0.6mm}
.gt-h b{font-family:Unbounded,sans-serif;font-weight:600;font-size:10pt}
.gt-h em{font-style:normal;font-size:7.8pt;color:#6b6862;margin-left:auto}
.t2 th{padding-top:1.2mm;padding-bottom:1.2mm}
.t2 td{padding-top:0.95mm;padding-bottom:0.95mm}
.vt th{white-space:normal;vertical-align:bottom}
.vt td.pos{color:#2f7d4f;font-weight:600}.vt td.neg{color:#a5452f;font-weight:600}
.vs-row{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:4mm}
.vs{padding:3.5mm 4mm;border:0.3mm solid #e5e3dd;border-radius:2.5mm;display:flex;flex-direction:column;gap:0.8mm}
.vs b{font-family:Unbounded,sans-serif;font-weight:600;font-size:9.5pt}
.vs span{font-size:9.5pt}
.vs strong{font-size:11pt}
.vs em{font-style:normal;font-size:7.8pt;color:#8a8781}
.vs-row p{grid-column:1/-1;font-size:8pt;color:#6b6862}

/* полосы */
.bars{display:grid;gap:1.6mm}
.bar{display:grid;grid-template-columns:52mm 1fr 30mm;align-items:center;gap:3mm;font-size:8.8pt}
.bt{height:4.2mm;background:#f2f0eb;border-radius:0.8mm;overflow:hidden}
.bt i{display:block;height:100%;background:#d9c799;border-radius:0.8mm}
.bar.hl .bt i{background:#c69a2e}
.bv{font-weight:600;font-variant-numeric:tabular-nums}
.bv em{font-style:normal;font-weight:400;color:#6b6862}
.cols{display:grid;grid-template-columns:1.4fr 1fr;gap:8mm}
.cols .bar{grid-template-columns:47mm 1fr 10mm}
.aside p{font-size:9pt;color:#2b2a27;margin-bottom:2.5mm}
.offer{margin-top:5mm;padding:5mm 6mm;background:#0e0e0d;color:#fff;border-radius:3mm;display:grid;grid-template-columns:58mm 1fr;gap:5mm;align-items:center}
.offer b{font-family:Unbounded,sans-serif;font-weight:700;font-size:15pt;color:#e3c172;line-height:1.2}
.offer span{font-size:9pt;color:#d6d3cc}
.todo{list-style:none;counter-reset:d;display:grid;gap:2.8mm}
.todo li{counter-increment:d;position:relative;padding-left:10mm;font-size:9.4pt;color:#2b2a27}
.todo li:before{content:counter(d);position:absolute;left:0;top:-0.4mm;width:6.5mm;height:6.5mm;border-radius:50%;background:#c69a2e;color:#0e0e0d;font-weight:700;font-size:9pt;display:flex;align-items:center;justify-content:center}
.todo b{color:#0e0e0d}

/* методология и контакты */
.meth{list-style:none;display:grid;gap:2.4mm;font-size:9pt;color:#2b2a27}
.meth li{padding-left:4mm;position:relative}
.meth li:before{content:"";position:absolute;left:0;top:1.9mm;width:1.6mm;height:1.6mm;background:#c69a2e;border-radius:50%}
.cta{margin-top:8mm;background:#0e0e0d;color:#fff;border-radius:4mm;padding:7mm;display:grid;grid-template-columns:1.2fr 1fr;gap:8mm}
.cta h3{font-size:14pt;line-height:1.25;margin-bottom:3mm}
.cta p{font-size:9.5pt;color:#d6d3cc;margin-bottom:5mm}
.btn{display:inline-block;background:#c69a2e;color:#0e0e0d;font-weight:700;padding:3mm 5mm;border-radius:2.5mm;font-size:9.5pt}
.ct{list-style:none;display:grid;gap:2.6mm;font-size:9.5pt;align-content:center}
.ct span{display:block;font-size:7.5pt;color:#8a8781;text-transform:uppercase;letter-spacing:.06em}
.ct a{color:#fff}
.about{margin-top:7mm;display:grid;grid-template-columns:38mm 1fr;gap:6mm;align-items:center}
.about img{width:38mm}
.about p{font-size:9pt;color:#4a4844}
.legal{margin-top:5mm;font-size:7.5pt;color:#a19d95}
"""

doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Зарплаты в IT в Узбекистане: осень 2026 – Human and Capital</title>
<meta name="author" content="Human and Capital">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Unbounded:wght@600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>
{page(1, p1, "cover")}{page(2, p2)}{page(3, p3)}{page(4, p4)}{page(5, p5)}{page(6, p6)}{page(7, p7)}{page(8, p8)}
</body></html>"""

doc = doc.replace("≈ ", "≈\u00a0")
tmp = tempfile.mkdtemp(prefix="hc-report-")
src = os.path.join(tmp, "report.html")
open(src, "w", encoding="utf-8").write(doc)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                "--virtual-time-budget=15000", "--print-to-pdf=" + OUT, "file://" + src],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("html:", src)
print("pdf: ", OUT, f"({os.path.getsize(OUT) // 1024} КБ)")
