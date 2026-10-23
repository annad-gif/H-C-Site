"""Блок «Статьи по теме» на страницах HR-консалтинга (RU/EN/UZ) – внутренняя перелинковка.

Повторный запуск безопасен: блок между маркерами RL-SEO заменяется, а не дублируется.
Запуск из корня сайта: python3 tools/build_related_links.py
"""
MARK_B, MARK_E = "<!-- RL-SEO:BEGIN -->", "<!-- RL-SEO:END -->"
A = "/articles/"

PAGES = {
    "consulting.html": ("Полезно знать", "Статьи по теме", [
        (A + "sovremennye-metody-otsenki-kandidatov-ca76824c", "Современные методы оценки кандидатов", "Ключевые подходы к оценке"),
        (A + "dvukhfaktornaya-teoriya-motivatsii-gertsberga-90ce2867", "Двухфакторная теория мотивации Герцберга", "Что удерживает сотрудников в компании"),
        (A + "kpi-rekrutera-6109c26b", "KPI рекрутера", "Как понять, эффективно ли работает подбор"),
        (A + "intervyu-po-kompetentsiyam-119bd224", "Интервью по компетенциям", "Как оценивать кандидатов на собеседовании"),
    ]),
    "consulting-en.html": ("Further reading", "Related guides", [
        ("/hr-services-uzbekistan.html", "HR services in Uzbekistan", "Recruitment, outstaffing and HR consulting in one place"),
        (A + "hiring-in-uzbekistan-d0f28979", "Hiring in Uzbekistan", "A practical guide for foreign companies"),
        ("/recruitment-en.html", "Recruitment agency in Uzbekistan", "Specialists, executives, IT and mass recruitment"),
        ("/outstaffing-en.html", "Outstaffing in Uzbekistan", "Legal employment, payroll and reporting"),
    ]),
    "consulting-uz.html": ("Foydali", "Mavzuga oid materiallar", [
        ("/recruitment-uz.html", "Toshkentda xodimlarni tanlash", "Mutaxassislar, rahbarlar, IT va ommaviy tanlov"),
        ("/outstaffing-uz.html", "O‘zbekistonda xodimlar autstaffingi", "Rasmiylashtirish, ish haqi va hisobotlar"),
        (A + "sovremennye-metody-otsenki-kandidatov-ca76824c", "Современные методы оценки кандидатов", "rus tilida"),
        (A + "toshkentda-kadrlar-agentligini-qanday-tanlash-kerak-1f022de9", "Toshkentda kadrlar agentligini qanday tanlash kerak", "Shartnomadan oldin beriladigan 10 ta savol"),
    ]),
}

STYLE = """<style>
  #rl-read{background:var(--grey-50);}
  .rl-list{list-style:none;display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:980px;}
  .rl-list a{display:flex;flex-direction:column;gap:6px;padding:20px 22px;border-radius:16px;background:var(--white);border:1px solid var(--grey-100);text-decoration:none;color:var(--black);transition:border-color .2s, transform .2s;}
  .rl-list a:hover{border-color:var(--mustard);transform:translateY(-2px);}
  .rl-list b{font-family:var(--ff-display);font-weight:600;font-size:16px;line-height:1.35;}
  .rl-list span{font-size:14px;color:var(--grey-500);}
  @media (max-width:720px){.rl-list{grid-template-columns:1fr;}}
</style>"""


def block(eyebrow, title, items):
    lis = "\n".join(f'      <li><a href="{u}"><b>{t}</b><span>{s}</span></a></li>' for u, t, s in items)
    return f"""{MARK_B}
{STYLE}
<section id="rl-read">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{eyebrow}</p>
      <h2 class="sec-title">{title}</h2>
    </div>
    <ul class="rl-list reveal">
{lis}
    </ul>
  </div>
</section>
{MARK_E}

"""


def main():
    for p, (eyebrow, title, items) in PAGES.items():
        s = open(p, encoding="utf-8").read()
        i = s.find(MARK_B)
        if i >= 0:
            s = s[:i] + s[s.index(MARK_E) + len(MARK_E):].lstrip("\n")
        assert s.count('<section id="contact">') == 1, p
        s = s.replace('<section id="contact">', block(eyebrow, title, items) + '<section id="contact">', 1)
        open(p, "w", encoding="utf-8").write(s)
        print("ok", p)


if __name__ == "__main__":
    main()
