"""SEO-расширение страниц рекрутмента (RU/EN/UZ): мета, H1, новые блоки, FAQ, ссылки на статьи и JSON-LD.

Стили блоков общие со страницами аутстаффинга (tools/build_outstaffing_seo.py, классы oss-*).
Повторный запуск безопасен: блоки между маркерами RC-SEO заменяются, а не дублируются.
Запуск из корня сайта: python3 tools/build_recruitment_seo.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_outstaffing_seo import CSS as OSS_CSS, esc  # noqa: E402

MARK_B, MARK_E = "<!-- RC-SEO:BEGIN -->", "<!-- RC-SEO:END -->"
CSS_B, CSS_E = "/* RC-SEO:CSS:BEGIN */", "/* RC-SEO:CSS:END */"
LD_B, LD_E = "<!-- RC-SEO:LD:BEGIN -->", "<!-- RC-SEO:LD:END -->"

# стили oss-* берём из генератора аутстаффинга (на страницах рекрутмента их нет) + свои мелочи
CSS = CSS_B + "\n" + OSS_CSS.replace("/* OS-SEO:CSS:BEGIN */", "").replace("/* OS-SEO:CSS:END */", "").replace("#os-", "#rc-") + """
  .oss-tags{display:flex;flex-wrap:wrap;gap:10px;max-width:980px;}
  .oss-tags span{border:1px solid var(--grey-100);background:var(--white);border-radius:999px;padding:9px 16px;font-size:14px;color:var(--grey-700);}
  #rc-read{background:var(--grey-50);}
  .oss-read{list-style:none;display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:980px;}
  .oss-read a{display:flex;flex-direction:column;gap:6px;padding:20px 22px;border-radius:16px;background:var(--white);border:1px solid var(--grey-100);text-decoration:none;color:var(--black);transition:border-color .2s, transform .2s;}
  .oss-read a:hover{border-color:var(--mustard);transform:translateY(-2px);}
  .oss-read b{font-family:var(--ff-display);font-weight:600;font-size:16px;line-height:1.35;}
  .oss-read span{font-size:14px;color:var(--grey-500);}
  @media (max-width:720px){.oss-read{grid-template-columns:1fr;}}
""" + CSS_E

A = "/articles/"
L = {}

L["ru"] = dict(
    file="recruitment.html", url="https://humancapital.uz/recruitment.html", home="https://humancapital.uz/", home_name="Главная",
    title="Подбор персонала в Ташкенте – рекрутинговое агентство Human and Capital",
    desc="Рекрутинговое агентство в Ташкенте: подбор специалистов и руководителей, executive search, IT-рекрутинг и массовый подбор. Гарантия замены, бесплатный пробный день кандидата.",
    h1="Подбор персонала в Ташкенте",
    service_name="Подбор персонала в Ташкенте и Узбекистане",
    fmt_eyebrow="Форматы подбора", fmt_title="Кого мы подбираем",
    fmt=[
        ("Специалисты", "Поиск и отбор специалистов уровня middle и senior в продажи, финансы, маркетинг, логистику и другие направления."),
        ("Руководители – executive search", "Прямой поиск топ-менеджеров и редких специалистов, которые не ищут работу активно."),
        ("IT-рекрутинг", "Разработчики, инженеры, QA, аналитики и системные администраторы для IT-компаний и IT-отделов."),
        ("Массовый подбор", "Десятки однотипных позиций в сжатые сроки – для ритейла, BPO и контакт-центров, производства."),
        ("Языковые позиции", "Специалисты со знанием английского, немецкого, французского, корейского и других языков с проверкой уровня."),
        ("Подбор из базы резюме", "Выбор кандидата из нашей базы – оплата фиксированная, только если кандидат вышел на работу."),
    ],
    ind_eyebrow="Отрасли", ind_title="С какими отраслями работаем",
    ind=["IT", "Финансы", "Госсектор", "Туризм и авиация", "Недвижимость и строительство", "HORECA", "Производство", "Дистрибуция", "Фарма и медицина", "Ритейл", "BPO и контакт-центры", "и многие другие"],
    steps_eyebrow="Как проходит подбор", steps_title="8 шагов от заявки до адаптации",
    steps=[
        ("Заявка", "Вы описываете вакансию и требования к кандидату."),
        ("Анализ задачи", "Разбираем требования и строим стратегию поиска."),
        ("Договор", "Фиксируем условия, сроки и гарантии."),
        ("Поиск", "Ищем кандидатов, проводим интервью и отбираем лучших."),
        ("Оценка", "Оцениваем кандидатов прозрачно и по международным методикам."),
        ("Встречи с вами", "Представляем шорт-лист с полной информацией по каждому кандидату."),
        ("Выход на работу", "Сопровождаем кандидата до первого рабочего дня."),
        ("Адаптация", "Остаёмся на связи с сотрудником и с вами на испытательном сроке."),
    ],
    faq_eyebrow="Вопросы и ответы", faq_title="Частые вопросы о подборе персонала",
    faq=[
        ("Сколько времени занимает подбор?", "Срок зависит от позиции, ситуации на рынке труда и условий, которые предлагает работодатель. Мы согласуем сроки до старта поиска и регулярно держим вас в курсе."),
        ("Сколько стоит подбор персонала?", "Стоимость зависит от уровня позиции и формата работы. Базовые условия указаны выше на этой странице, точный расчёт подготовим после брифа по вакансии."),
        ("Какие гарантии вы даёте?", "Одна бесплатная замена специалиста в оговорённый срок, бесплатный пробный день кандидата и возврат предоплаты, если в согласованный срок мы не представим как минимум трёх подходящих кандидатов. Также мы сопровождаем сотрудника и работодателя на испытательном сроке."),
        ("Ищете ли вы топ-менеджеров?", "Да. Для руководителей и редких специалистов мы используем прямой поиск – executive search, потому что такие кандидаты обычно не откликаются на вакансии."),
        ("Беретесь ли вы за массовый подбор?", "Да, закрываем десятки однотипных позиций в сжатые сроки для ритейла, BPO и контакт-центров, производства."),
        ("Можно ли нанять кандидата из вашей базы резюме?", "Да. Вы выбираете кандидата в банке резюме, а агентство получает фиксированное вознаграждение, только если кандидат вышел на работу."),
        ("Работаете ли вы с иностранными компаниями?", "Да. Подбираем сотрудников для местных и международных компаний, а если нужно оформить команду в Узбекистане без собственного юрлица – предлагаем аутстаффинг."),
        ("Используете ли вы AI при подборе?", "Да. Современные инструменты помогают быстрее анализировать резюме, а решения о кандидатах принимают опытные рекрутеры."),
    ],
    read_eyebrow="Полезно знать", read_title="Статьи о подборе персонала",
    read=[
        (A + "kak-vybrat-kadrovoe-agentstvo-v-tashkente-fcdacdb7", "Как выбрать кадровое агентство в Ташкенте", "10 вопросов до подписания договора"),
        (A + "massovyy-podbor-personala-v-uzbekistane-37157357", "Массовый подбор персонала в Узбекистане", "Как закрыть десятки вакансий в сжатые сроки"),
        (A + "rekrutingovoe-agentstvo-ili-vnutrenniy-hr-e9bef7f5", "Рекрутинговое агентство или внутренний HR", "Что выбрать компании"),
        (A + "intervyu-po-kompetentsiyam-119bd224", "Интервью по компетенциям", "Как оценивать кандидатов на собеседовании"),
    ],
)

L["en"] = dict(
    file="recruitment-en.html", url="https://humancapital.uz/recruitment-en.html", home="https://humancapital.uz/index-en.html", home_name="Home",
    title="Recruitment Agency in Tashkent, Uzbekistan – Human and Capital",
    desc="Recruitment agency in Tashkent: specialists and managers, executive search, IT and mass recruitment for local and international companies. Free replacement guarantee.",
    h1="Recruitment Agency in Uzbekistan",
    service_name="Recruitment services in Uzbekistan",
    fmt_eyebrow="Recruitment formats", fmt_title="Who we hire for you",
    fmt=[
        ("Specialists", "Search and selection of middle and senior specialists in sales, finance, marketing, logistics and other functions."),
        ("Executive search", "Direct search for top managers and rare specialists who are not actively looking for a job."),
        ("IT recruitment", "Developers, engineers, QA, analysts and system administrators for IT companies and IT departments."),
        ("Mass recruitment", "Dozens of similar roles in tight timelines – for retail, BPO and contact centres, manufacturing."),
        ("Language roles", "Specialists with English, German, French, Korean and other languages, with a verified language level."),
        ("Hiring from our CV database", "Pick a candidate from our database – a fixed fee, paid only if the candidate starts work."),
    ],
    ind_eyebrow="Industries", ind_title="Industries we work with",
    ind=["IT", "Finance", "Government", "Tourism & Aviation", "Real Estate & Construction", "HORECA", "Manufacturing", "Distribution", "Pharma & Medicine", "Retail", "BPO & contact centres", "and many more"],
    steps_eyebrow="How it works", steps_title="8 steps from request to adaptation",
    steps=[
        ("Request", "You describe the role and the requirements for the candidate."),
        ("Needs analysis", "We analyse the requirements and build a search strategy."),
        ("Contract", "We fix the terms, timelines and guarantees."),
        ("Sourcing", "We search for candidates, run interviews and shortlist the best."),
        ("Assessment", "We assess candidates objectively using international methodologies."),
        ("Client interviews", "You meet the shortlist with full information on every candidate."),
        ("Onboarding", "We support the candidate up to their first working day."),
        ("Adaptation", "We stay in touch with the employee and with you during probation."),
    ],
    faq_eyebrow="FAQ", faq_title="Recruitment in Uzbekistan: frequently asked questions",
    faq=[
        ("How long does recruitment take?", "It depends on the role, the labour market and the conditions the employer offers. We agree on the timeline before the search starts and keep you updated."),
        ("How much does recruitment cost?", "The cost depends on the level of the role and the format. The basic terms are listed above on this page; we prepare an exact quote after a brief on the vacancy."),
        ("What guarantees do you give?", "One free replacement within the agreed terms, a free trial day for the candidate, and a refund of the prepayment if we do not present at least three suitable candidates within the agreed timeframe. We also support the employee and the employer during probation."),
        ("Do you search for top managers?", "Yes. For executives and rare specialists we use direct search, because such candidates rarely respond to job ads."),
        ("Do you handle mass recruitment?", "Yes, we fill dozens of similar roles in tight timelines for retail, BPO and contact centres, and manufacturing."),
        ("Can I hire a candidate from your CV database?", "Yes. You choose a candidate from our CV database, and the agency receives a fixed fee only if the candidate starts work."),
        ("Do you work with international companies?", "Yes. We recruit for local and international companies, and if you need to employ a team in Uzbekistan without your own legal entity, we offer outstaffing."),
        ("Do you use AI in recruitment?", "Yes. Modern tools help us analyse CVs faster, while experienced recruiters make every decision about candidates."),
    ],
    read_eyebrow="Further reading", read_title="Guides for employers",
    read=[
        (A + "hiring-in-uzbekistan-d0f28979", "Hiring in Uzbekistan", "A practical guide for foreign companies"),
        ("/hr-services-uzbekistan.html", "HR services in Uzbekistan", "Recruitment, outstaffing and HR consulting in one place"),
        ("/outstaffing-en.html", "Outstaffing in Uzbekistan", "Legal employment, payroll and reporting for your team"),
        ("/consulting-en.html", "HR consulting", "HR audit, assessment and onboarding systems"),
    ],
)

L["uz"] = dict(
    file="recruitment-uz.html", url="https://humancapital.uz/recruitment-uz.html", home="https://humancapital.uz/index-uz.html", home_name="Bosh sahifa",
    title="Toshkentda xodimlarni tanlash – Human and Capital rekruting agentligi",
    desc="Toshkentdagi rekruting agentligi: mutaxassis va rahbarlarni tanlash, executive search, IT-rekrutment va ommaviy tanlov. Almashtirish kafolati, nomzodning bepul sinov kuni.",
    h1="Toshkentda xodimlarni tanlash",
    service_name="Toshkent va O‘zbekistonda xodimlarni tanlash",
    fmt_eyebrow="Tanlash formatlari", fmt_title="Kimlarni tanlaymiz",
    fmt=[
        ("Mutaxassislar", "Savdo, moliya, marketing, logistika va boshqa yo‘nalishlar uchun middle va senior darajadagi mutaxassislarni qidirish va tanlash."),
        ("Rahbarlar – executive search", "Faol ish qidirmayotgan top-menejerlar va noyob mutaxassislarni to‘g‘ridan-to‘g‘ri qidirish."),
        ("IT-rekrutment", "IT-kompaniyalar va IT-bo‘limlar uchun dasturchilar, muhandislar, QA, tahlilchilar va tizim administratorlari."),
        ("Ommaviy tanlov", "Qisqa muddatda o‘nlab bir xil lavozimlar – chakana savdo, BPO va kontakt-markazlar, ishlab chiqarish uchun."),
        ("Til biladigan mutaxassislar", "Ingliz, nemis, fransuz, koreys va boshqa tillarni biladigan mutaxassislar, til darajasi tekshiriladi."),
        ("Rezyume bazasidan tanlash", "Bazamizdan nomzod tanlash – qat’iy to‘lov, faqat nomzod ishga chiqsa."),
    ],
    ind_eyebrow="Sohalar", ind_title="Qaysi sohalar bilan ishlaymiz",
    ind=["IT", "Moliya", "Davlat sektori", "Turizm va aviatsiya", "Ko‘chmas mulk va qurilish", "HORECA", "Ishlab chiqarish", "Distributsiya", "Farmatsevtika va tibbiyot", "Chakana savdo", "BPO va kontakt-markazlar", "va boshqalar"],
    steps_eyebrow="Tanlash qanday o‘tadi", steps_title="Arizadan moslashuvgacha 8 bosqich",
    steps=[
        ("Ariza", "Vakansiya va nomzodga talablarni tasvirlaysiz."),
        ("Vazifani tahlil qilish", "Talablarni tahlil qilamiz va qidiruv strategiyasini tuzamiz."),
        ("Shartnoma", "Shartlar, muddatlar va kafolatlarni belgilaymiz."),
        ("Qidiruv", "Nomzodlarni qidiramiz, suhbatlar o‘tkazamiz va eng yaxshilarini tanlaymiz."),
        ("Baholash", "Nomzodlarni xalqaro uslublar asosida shaffof baholaymiz."),
        ("Siz bilan uchrashuvlar", "Har bir nomzod bo‘yicha to‘liq ma’lumot bilan qisqa ro‘yxatni taqdim etamiz."),
        ("Ishga chiqish", "Nomzodni birinchi ish kunigacha kuzatib boramiz."),
        ("Moslashuv", "Sinov muddatida xodim va siz bilan aloqada bo‘lamiz."),
    ],
    faq_eyebrow="Savol-javoblar", faq_title="Xodimlarni tanlash haqida ko‘p beriladigan savollar",
    faq=[
        ("Tanlash qancha vaqt oladi?", "Muddat lavozimga, mehnat bozoridagi vaziyatga va ish beruvchi taklif qilayotgan shartlarga bog‘liq. Qidiruv boshlanishidan oldin muddatlarni kelishamiz va sizni muntazam xabardor qilib turamiz."),
        ("Xodimlarni tanlash qancha turadi?", "Narx lavozim darajasi va ish formatiga bog‘liq. Asosiy shartlar ushbu sahifada yuqorida ko‘rsatilgan, aniq hisobni vakansiya bo‘yicha brifdan keyin tayyorlaymiz."),
        ("Qanday kafolatlar berasiz?", "Kelishilgan muddatda mutaxassisni bir marta bepul almashtirish, nomzodning bepul sinov kuni va kelishilgan muddatda kamida uchta mos nomzod taqdim etilmasa, oldindan to‘lovni qaytarish. Shuningdek, sinov muddatida xodim va ish beruvchini kuzatib boramiz."),
        ("Top-menejerlarni qidirasizmi?", "Ha. Rahbarlar va noyob mutaxassislar uchun to‘g‘ridan-to‘g‘ri qidiruv – executive search usulini qo‘llaymiz, chunki bunday nomzodlar odatda vakansiyalarga javob bermaydi."),
        ("Ommaviy tanlov bilan shug‘ullanasizmi?", "Ha, chakana savdo, BPO va kontakt-markazlar, ishlab chiqarish uchun qisqa muddatda o‘nlab bir xil lavozimlarni yopamiz."),
        ("Rezyume bazangizdan nomzodni ishga olsa bo‘ladimi?", "Ha. Siz rezyume bankidan nomzod tanlaysiz, agentlik esa faqat nomzod ishga chiqsa qat’iy haq oladi."),
        ("Xorijiy kompaniyalar bilan ishlaysizmi?", "Ha. Mahalliy va xalqaro kompaniyalar uchun xodim tanlaymiz, O‘zbekistonda o‘z yuridik shaxsisiz jamoani rasmiylashtirish kerak bo‘lsa – autstaffingni taklif qilamiz."),
        ("Tanlashda AI dan foydalanasizmi?", "Ha. Zamonaviy vositalar rezyumelarni tezroq tahlil qilishga yordam beradi, nomzodlar bo‘yicha qarorlarni esa tajribali rekruterlar qabul qiladi."),
    ],
    read_eyebrow="Foydali", read_title="Xodim tanlash haqida maqolalar",
    read=[
        (A + "toshkentda-kadrlar-agentligini-qanday-tanlash-kerak-1f022de9", "Toshkentda kadrlar agentligini qanday tanlash kerak", "Shartnomadan oldin beriladigan 10 ta savol"),
        (A + "massovyy-podbor-personala-v-uzbekistane-37157357", "Массовый подбор персонала в Узбекистане", "rus tilida"),
        ("/outstaffing-uz.html", "O‘zbekistonda xodimlar autstaffingi", "Rasmiylashtirish, ish haqi va hisobotlar"),
        ("/consulting-uz.html", "HR-konsalting", "HR-audit, baholash va moslashuv tizimlari"),
    ],
)


def sections(d):
    fmt = "\n".join(f'      <div class="oss-card reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in d["fmt"])
    ind = "\n".join(f"      <span>{x}</span>" for x in d["ind"])
    steps = "\n".join(f'      <li class="reveal"><h3>{t}</h3><p>{p}</p></li>' for t, p in d["steps"])
    faq = "\n".join(f"      <details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in d["faq"])
    read = "\n".join(f'      <li><a href="{u}"><b>{t}</b><span>{s}</span></a></li>' for u, t, s in d["read"])
    return f"""{MARK_B}
<section id="rc-scope">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['fmt_eyebrow']}</p>
      <h2 class="sec-title">{d['fmt_title']}</h2>
    </div>
    <div class="oss-grid">
{fmt}
    </div>
  </div>
</section>

<section id="rc-compare">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['ind_eyebrow']}</p>
      <h2 class="sec-title">{d['ind_title']}</h2>
    </div>
    <div class="oss-tags reveal">
{ind}
    </div>
  </div>
</section>

<section id="rc-steps">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['steps_eyebrow']}</p>
      <h2 class="sec-title">{d['steps_title']}</h2>
    </div>
    <ol class="oss-steps">
{steps}
    </ol>
  </div>
</section>

<section id="rc-faq">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['faq_eyebrow']}</p>
      <h2 class="sec-title">{d['faq_title']}</h2>
    </div>
    <div class="oss-faq">
{faq}
    </div>
  </div>
</section>

<section id="rc-read">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['read_eyebrow']}</p>
      <h2 class="sec-title">{d['read_title']}</h2>
    </div>
    <ul class="oss-read reveal">
{read}
    </ul>
  </div>
</section>
{MARK_E}

"""


def jsonld(d):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": d["service_name"], "serviceType": "Recruitment", "description": d["desc"], "url": d["url"],
         "areaServed": {"@type": "Country", "name": "Uzbekistan"},
         "provider": {"@type": ["Organization", "EmploymentAgency"], "@id": "https://humancapital.uz/#organization", "name": "Human and Capital",
                      "url": "https://humancapital.uz/", "telephone": "+998903251336",
                      "address": {"@type": "PostalAddress", "streetAddress": "Farg‘ona yo‘li, 94", "addressLocality": "Tashkent", "addressCountry": "UZ"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": d["home_name"], "item": d["home"]},
            {"@type": "ListItem", "position": 2, "name": d["h1"], "item": d["url"]}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]},
    ]}
    return f'{LD_B}\n<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=2)}\n</script>\n{LD_E}\n'


def strip_between(s, a, b):
    i = s.find(a)
    if i < 0:
        return s
    j = s.index(b, i) + len(b)
    return s[:i] + s[j:].lstrip("\n")


def main():
    for lang, d in L.items():
        p = d["file"]
        s = open(p, encoding="utf-8").read()
        s = strip_between(s, MARK_B, MARK_E)
        s = strip_between(s, LD_B, LD_E)
        i = s.find(CSS_B)
        if i >= 0:
            j = s.index(CSS_E) + len(CSS_E)
            s = s[:i] + s[j + 1 if s[j:j + 1] == "\n" else j:]

        s, n = re.subn(r"<title>[^<]*</title>", f"<title>{d['title']}</title>", s, count=1); assert n
        for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            s, n = re.subn(r'(<meta ' + attr + r' content=")[^"]*(")', lambda m: m.group(1) + esc(d["desc"]) + m.group(2), s, count=1); assert n, attr
        for attr in ('property="og:title"', 'name="twitter:title"'):
            s, n = re.subn(r'(<meta ' + attr + r' content=")[^"]*(")', lambda m: m.group(1) + esc(d["title"]) + m.group(2), s, count=1); assert n, attr
        s, n = re.subn(r'(<section class="rec-hero" id="home">.*?<h1>)[^<]*(</h1>)', lambda m: m.group(1) + d["h1"] + m.group(2), s, count=1, flags=re.S); assert n

        s = s.replace("</style>", CSS + "\n</style>", 1)
        s = s.replace("</head>", jsonld(d) + "</head>", 1)
        assert s.count('<section id="contact">') == 1
        s = s.replace('<section id="contact">', sections(d) + '<section id="contact">', 1)
        open(p, "w", encoding="utf-8").write(s)
        print("ok", p)


if __name__ == "__main__":
    main()
