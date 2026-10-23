"""SEO-расширение страниц аутстаффинга (RU/EN/UZ): мета, H1, новые блоки, FAQ и JSON-LD.

Повторный запуск безопасен: блоки между маркерами OS-SEO заменяются, а не дублируются.
Запуск из корня сайта: python3 tools/build_outstaffing_seo.py
"""
import json, re

MARK_B, MARK_E = "<!-- OS-SEO:BEGIN -->", "<!-- OS-SEO:END -->"
CSS_B, CSS_E = "/* OS-SEO:CSS:BEGIN */", "/* OS-SEO:CSS:END */"
LD_B, LD_E = "<!-- OS-SEO:LD:BEGIN -->", "<!-- OS-SEO:LD:END -->"

CSS = CSS_B + """
  #os-scope{background:var(--grey-50);}
  .oss-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}
  .oss-card{background:var(--white);border:1px solid var(--grey-100);border-radius:18px;padding:26px 24px;}
  .oss-card h3{font-family:var(--ff-display);font-weight:600;font-size:17px;line-height:1.35;margin-bottom:10px;color:var(--black);}
  .oss-card p{font-size:15px;line-height:1.65;color:var(--grey-700);}
  #os-compare{background:var(--white);}
  .oss-table-wrap{overflow-x:auto;border:1px solid var(--grey-100);border-radius:18px;}
  .oss-table{width:100%;border-collapse:collapse;min-width:720px;font-size:15px;}
  .oss-table th,.oss-table td{padding:16px 20px;text-align:left;vertical-align:top;border-bottom:1px solid var(--grey-100);line-height:1.55;}
  .oss-table thead th{font-family:var(--ff-display);font-weight:600;font-size:15px;background:var(--grey-50);}
  .oss-table tbody th{font-weight:600;color:var(--black);width:22%;}
  .oss-table td{color:var(--grey-700);}
  .oss-table .oss-hl{background:rgba(198,154,46,0.08);color:var(--black);}
  .oss-table thead .oss-hl{background:var(--mustard);color:var(--black);}
  .oss-table tr:last-child th,.oss-table tr:last-child td{border-bottom:none;}
  .oss-note{margin-top:18px;font-size:15px;color:var(--grey-700);line-height:1.7;max-width:820px;}
  #os-fit{background:var(--grey-50);}
  .oss-fit{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:14px 40px;max-width:980px;}
  .oss-fit li{display:flex;gap:12px;font-size:16px;line-height:1.6;color:var(--grey-700);}
  .oss-fit li::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--mustard);flex-shrink:0;margin-top:9px;}
  #os-steps{background:var(--black);color:var(--white);}
  #os-steps .sec-title{color:var(--white);}
  #os-steps .sec-eyebrow{color:var(--mustard-light);}
  .oss-steps{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;counter-reset:oss;}
  .oss-steps li{border:1px solid rgba(255,255,255,0.10);border-radius:16px;padding:24px 22px;background:rgba(255,255,255,0.03);}
  .oss-steps li::before{counter-increment:oss;content:counter(oss,decimal-leading-zero);display:block;font-family:var(--ff-display);font-weight:700;font-size:22px;color:var(--mustard);margin-bottom:12px;}
  .oss-steps h3{font-size:16px;font-weight:600;margin-bottom:8px;color:var(--white);}
  .oss-steps p{font-size:14px;line-height:1.6;color:var(--grey-300);}
  .oss-links{margin-top:28px;font-size:15px;color:var(--grey-300);}
  .oss-links a{color:var(--mustard-light);font-weight:600;}
  #os-faq{background:var(--white);}
  .oss-faq{max-width:860px;display:flex;flex-direction:column;gap:12px;}
  .oss-faq details{border:1px solid var(--grey-100);border-radius:14px;background:var(--grey-50);}
  .oss-faq summary{cursor:pointer;list-style:none;padding:20px 56px 20px 22px;font-family:var(--ff-display);font-weight:600;font-size:16px;line-height:1.4;position:relative;}
  .oss-faq summary::-webkit-details-marker{display:none;}
  .oss-faq summary::after{content:'+';position:absolute;right:22px;top:50%;transform:translateY(-50%);font-size:22px;color:var(--mustard-dim);transition:transform .2s;}
  .oss-faq details[open] summary::after{transform:translateY(-50%) rotate(45deg);}
  .oss-faq details p{padding:0 22px 20px;font-size:15px;line-height:1.7;color:var(--grey-700);}
  @media (max-width:1080px){.oss-grid,.oss-steps{grid-template-columns:1fr 1fr;}}
  @media (max-width:720px){
    .oss-grid,.oss-steps,.oss-fit{grid-template-columns:1fr;}
    .oss-table-wrap{border:none;overflow:visible;}
    .oss-table{min-width:0;display:block;}
    .oss-table thead{display:none;}
    .oss-table tbody{display:flex;flex-direction:column;gap:14px;}
    .oss-table tr{display:block;border:1px solid var(--grey-100);border-radius:14px;overflow:hidden;}
    .oss-table tbody th{display:block;width:auto;background:var(--grey-50);padding:14px 16px;border-bottom:1px solid var(--grey-100);}
    .oss-table td{display:grid;grid-template-columns:42% 1fr;gap:12px;padding:12px 16px;}
    .oss-table td::before{content:attr(data-label);font-weight:600;color:var(--grey-500);font-size:13px;}
    .oss-table tr:last-child td{border-bottom:1px solid var(--grey-100);}
    .oss-table td:last-child{border-bottom:none !important;}
  }
""" + CSS_E

L = {}

L["ru"] = dict(
    file="outstaffing.html", url="https://humancapital.uz/outstaffing.html", home="https://humancapital.uz/", home_name="Главная",
    title="Аутстаффинг персонала в Узбекистане – аутстаффинговая компания Human and Capital",
    desc="Услуги аутстаффинга в Узбекистане: оформление сотрудников, расчёт зарплаты и отчётность, подбор и сопровождение. Команды для BPO и международных компаний.",
    h1="Аутстаффинг персонала в Узбекистане",
    service_name="Аутстаффинг персонала в Узбекистане",
    scope_eyebrow="Состав услуги", scope_title="Что входит в аутстаффинг",
    scope=[
        ("Подбор и оценка", "Ищем специалистов под ваши требования и проверяем навыки, опыт и уровень иностранных языков."),
        ("Легальное оформление", "Трудоустраиваем сотрудников в нашей компании в соответствии с трудовым законодательством Республики Узбекистан."),
        ("Расчёт заработной платы", "Ежемесячно начисляем и выплачиваем зарплату, рассчитываем налоги и обязательные взносы."),
        ("Кадровый учёт и отчётность", "Ведём кадровые документы и сдаём отчётность вовремя – без нагрузки на вашу бухгалтерию."),
        ("Мониторинг и отчёты", "Отслеживаем эффективность сотрудников и регулярно отчитываемся перед вами."),
        ("Гибкое масштабирование", "Увеличиваем или сокращаем команду по вашему запросу – в том числе под пиковые нагрузки."),
    ],
    cmp_eyebrow="Сравнение моделей", cmp_title="Аутстаффинг, аутсорсинг или свой штат",
    cmp_head=("", "Свой штат", "Аутстаффинг", "Аутсорсинг"),
    cmp_rows=[
        ("Кто работодатель", "Ваша компания", "Human and Capital", "Компания-подрядчик"),
        ("Кто ставит задачи и управляет работой", "Вы", "Вы", "Подрядчик"),
        ("Кто ведёт кадры, зарплату и отчётность", "Ваши HR и бухгалтерия", "Human and Capital", "Подрядчик"),
        ("За что вы платите", "Зарплата, налоги и содержание HR и бухгалтерии", "Услуга провайдера, включая фонд оплаты труда", "Результат – выполненная функция"),
        ("Когда подходит", "Долгосрочные ключевые роли, есть юрлицо и HR-отдел", "Нужна команда под вашим управлением без расширения штата или без юрлица в Узбекистане", "Нужно передать функцию целиком и получать результат"),
    ],
    cmp_note="Human and Capital работает по модели аутстаффинга: сотрудники выполняют ваши задачи под вашим руководством, а мы берём на себя их трудоустройство, зарплату, кадровый учёт и отчётность.",
    fit_eyebrow="Кому подходит", fit_title="Когда выбирают аутстаффинг",
    fit=[
        "Международным компаниям, которым нужна команда в Узбекистане без открытия собственного юрлица и HR-отдела",
        "BPO-проектам: контакт-центрам, переводческим проектам, клиентской и технической поддержке",
        "Бизнесу с сезонными пиками и проектами, где команду нужно быстро нарастить или сократить",
        "Компаниям, которые хотят снять с себя кадровое администрирование и расчёт зарплаты",
        "Проектам, где нужны специалисты со знанием английского, немецкого, арабского, турецкого, корейского, французского и других языков",
        "Тем, кому важен прозрачный бюджет и регулярная отчётность по команде",
    ],
    steps_eyebrow="Как начать", steps_title="Запуск аутстаффинга за 6 шагов",
    steps=[
        ("Заявка", "Вы описываете задачу: роли, количество сотрудников, языки, график работы."),
        ("Анализ и предложение", "Согласовываем состав команды, требования к специалистам и условия."),
        ("Договор", "Фиксируем объём услуг, сроки и порядок отчётности."),
        ("Подбор и оценка", "Находим и проверяем специалистов, вы утверждаете кандидатов."),
        ("Оформление", "Трудоустраиваем сотрудников в нашей компании по законодательству РУз."),
        ("Работа и сопровождение", "Сотрудники работают на ваших задачах, мы ведём кадры, зарплату и отчётность."),
    ],
    links='Нужен только подбор? – <a href="recruitment.html">Рекрутмент</a>. Хотите выстроить HR-процессы? – <a href="consulting.html">HR-консалтинг</a>.',
    faq_eyebrow="Вопросы и ответы", faq_title="Частые вопросы об аутстаффинге",
    faq=[
        ("Что такое аутстаффинг простыми словами?", "Сотрудники официально оформлены в аутстаффинговой компании, а работают на задачах и под руководством клиента. Провайдер отвечает за трудоустройство, расчёт зарплаты, кадровый учёт и отчётность, а клиент – за постановку задач и результат работы."),
        ("Чем аутстаффинг отличается от аутсорсинга?", "При аутстаффинге вы сами управляете работой сотрудников, а провайдер берёт на себя только оформление и администрирование. При аутсорсинге вы передаёте подрядчику функцию целиком и получаете готовый результат, не управляя людьми."),
        ("Может ли иностранная компания нанять сотрудников в Узбекистане через аутстаффинг?", "Да, это один из основных сценариев, с которыми к нам приходят международные клиенты. Сотрудники оформляются в нашей компании по законодательству Республики Узбекистан и работают над вашими задачами."),
        ("Сотрудники оформляются официально?", "Да. Мы трудоустраиваем сотрудников в соответствии с трудовым законодательством Республики Узбекистан, начисляем зарплату, рассчитываем налоги и взносы и своевременно сдаём отчётность."),
        ("Каких специалистов можно получить по аутстаффингу?", "Наша специализация – BPO: операторы контакт-центров, переводчики, специалисты клиентской и технической поддержки, в том числе со знанием иностранных языков. Если вам нужен другой профиль, опишите задачу – мы предложим решение."),
        ("Можно ли увеличить или сократить команду?", "Да. Мы масштабируем команду по вашему запросу, в том числе под сезонные и пиковые нагрузки."),
        ("Сколько стоит аутстаффинг?", "Стоимость рассчитывается индивидуально: она зависит от количества сотрудников, их квалификации и условий работы. Оставьте заявку – мы подготовим предложение в течение рабочего дня."),
        ("Что даёт резидентство IT Park?", "Мы работаем в рамках льготного правового и налогового режима IT Park. Это делает сотрудничество прозрачным, безопасным и экономически выгодным для клиента."),
    ],
)

L["en"] = dict(
    file="outstaffing-en.html", url="https://humancapital.uz/outstaffing-en.html", home="https://humancapital.uz/index-en.html", home_name="Home",
    title="Outstaffing Services in Uzbekistan – Outstaffing Company Human and Capital",
    desc="Outstaffing services in Uzbekistan: legal employment, payroll and reporting, sourcing and support of staff. Work-ready teams for BPO and international companies.",
    h1="Outstaffing Services in Uzbekistan",
    service_name="Outstaffing services in Uzbekistan",
    scope_eyebrow="What's included", scope_title="What our outstaffing service covers",
    scope=[
        ("Sourcing & assessment", "We find specialists to your requirements and verify their skills, experience and language level."),
        ("Legal employment", "Staff are employed by our company in full compliance with the labour law of the Republic of Uzbekistan."),
        ("Payroll", "We calculate and pay salaries every month, including taxes and mandatory contributions."),
        ("HR records & reporting", "We keep HR documentation and file reports on time – with no load on your accounting team."),
        ("Monitoring & reports", "We track staff performance and report to you on a regular basis."),
        ("Flexible scaling", "We scale the team up or down on request, including for peak loads."),
    ],
    cmp_eyebrow="Compare the models", cmp_title="Outstaffing vs outsourcing vs in-house",
    cmp_head=("", "In-house staff", "Outstaffing", "Outsourcing"),
    cmp_rows=[
        ("Legal employer", "Your company", "Human and Capital", "The contractor"),
        ("Who sets tasks and manages the work", "You", "You", "The contractor"),
        ("Who handles HR, payroll and reporting", "Your HR and accounting", "Human and Capital", "The contractor"),
        ("What you pay for", "Salaries, taxes and the cost of HR and accounting", "The provider's service, including the payroll fund", "The result – a function performed"),
        ("Best for", "Long-term key roles when you have a local entity and HR", "A team under your management without growing headcount or without a legal entity in Uzbekistan", "Handing over a whole function and paying for the outcome"),
    ],
    cmp_note="Human and Capital works on the outstaffing model: the employees do your work under your management, while we take care of their employment, payroll, HR records and reporting.",
    fit_eyebrow="Who it's for", fit_title="When companies choose outstaffing",
    fit=[
        "International companies that need a team in Uzbekistan without setting up a local entity and HR department",
        "BPO projects: contact centres, translation projects, customer and technical support",
        "Businesses with seasonal peaks or projects where the team must grow or shrink quickly",
        "Companies that want to offload HR administration and payroll",
        "Projects that need specialists with English, German, Arabic, Turkish, Korean, French and other languages",
        "Teams that need a transparent budget and regular reporting",
    ],
    steps_eyebrow="How to start", steps_title="Launching outstaffing in 6 steps",
    steps=[
        ("Request", "You describe the task: roles, number of employees, languages and working schedule."),
        ("Analysis & proposal", "We agree on the team structure, requirements and terms."),
        ("Contract", "We fix the scope of services, timelines and reporting."),
        ("Sourcing & assessment", "We find and vet specialists; you approve the candidates."),
        ("Employment", "Employees are hired by our company under Uzbek law."),
        ("Work & support", "Staff work on your tasks while we handle HR, payroll and reporting."),
    ],
    links='Need recruitment only? – <a href="recruitment-en.html">Recruitment</a>. All our services – <a href="hr-services-uzbekistan.html">HR services in Uzbekistan</a>.',
    faq_eyebrow="FAQ", faq_title="Outstaffing in Uzbekistan: frequently asked questions",
    faq=[
        ("What is outstaffing?", "Employees are formally employed by an outstaffing company but work on the client's tasks under the client's management. The provider is responsible for employment, payroll, HR records and reporting, while the client sets the tasks and owns the results."),
        ("What is the difference between outstaffing and outsourcing?", "With outstaffing you manage the employees' work yourself, and the provider only handles employment and administration. With outsourcing you hand over an entire function to a contractor and receive a finished result without managing the people."),
        ("Can a foreign company hire employees in Uzbekistan through outstaffing?", "Yes – this is one of the most common reasons international clients come to us. Employees are hired by our company under the laws of the Republic of Uzbekistan and work on your tasks."),
        ("Are employees hired officially?", "Yes. We employ staff in compliance with the labour law of the Republic of Uzbekistan, run payroll, calculate taxes and contributions and file reports on time."),
        ("Which specialists are available through outstaffing?", "We specialise in BPO: contact centre agents, translators, customer and technical support specialists, including multilingual staff. If you need another profile, describe your task and we will propose a solution."),
        ("Can the team be scaled up or down?", "Yes. We scale the team on request, including for seasonal and peak loads."),
        ("How much does outstaffing cost?", "The cost is calculated individually and depends on the number of employees, their qualifications and working conditions. Send us a request and we will prepare a proposal within one business day."),
        ("What does IT Park residency give?", "We operate within the IT Park preferential legal and tax regime, which makes cooperation transparent, secure and cost-effective for the client."),
    ],
)

L["uz"] = dict(
    file="outstaffing-uz.html", url="https://humancapital.uz/outstaffing-uz.html", home="https://humancapital.uz/index-uz.html", home_name="Bosh sahifa",
    title="O‘zbekistonda xodimlar autstaffingi – autstaffing kompaniyasi Human and Capital",
    desc="O‘zbekistonda autstaffing xizmatlari: xodimlarni qonuniy rasmiylashtirish, ish haqini hisoblash va hisobotlar, tanlash va kuzatib borish. BPO va xalqaro kompaniyalar uchun jamoalar.",
    h1="O‘zbekistonda xodimlar autstaffingi",
    service_name="O‘zbekistonda autstaffing xizmatlari",
    scope_eyebrow="Xizmat tarkibi", scope_title="Autstaffing nimalarni o‘z ichiga oladi",
    scope=[
        ("Tanlash va baholash", "Talablaringizga mos mutaxassislarni topamiz, ularning ko‘nikmalari, tajribasi va chet tili darajasini tekshiramiz."),
        ("Qonuniy rasmiylashtirish", "Xodimlarni O‘zbekiston Respublikasi mehnat qonunchiligiga muvofiq kompaniyamizga ishga rasmiylashtiramiz."),
        ("Ish haqini hisoblash", "Har oy ish haqini hisoblaymiz va to‘laymiz, soliqlar va majburiy badallarni hisoblaymiz."),
        ("Kadrlar hisobi va hisobotlar", "Kadrlar hujjatlarini yuritamiz va hisobotlarni o‘z vaqtida topshiramiz – buxgalteriyangizga yuklamasiz."),
        ("Monitoring va hisobotlar", "Xodimlar samaradorligini kuzatamiz va sizga muntazam hisobot beramiz."),
        ("Moslashuvchan kengaytirish", "So‘rovingiz bo‘yicha jamoani kengaytiramiz yoki qisqartiramiz, shu jumladan yuqori yuklama davrlarida."),
    ],
    cmp_eyebrow="Modellarni taqqoslash", cmp_title="Autstaffing, autsorsing yoki o‘z shtatingiz",
    cmp_head=("", "O‘z shtatingiz", "Autstaffing", "Autsorsing"),
    cmp_rows=[
        ("Ish beruvchi kim", "Sizning kompaniyangiz", "Human and Capital", "Pudratchi kompaniya"),
        ("Vazifalarni kim qo‘yadi va ishni boshqaradi", "Siz", "Siz", "Pudratchi"),
        ("Kadrlar, ish haqi va hisobotlarni kim yuritadi", "HR va buxgalteriyangiz", "Human and Capital", "Pudratchi"),
        ("Nima uchun to‘laysiz", "Ish haqi, soliqlar va HR hamda buxgalteriya xarajatlari", "Provayder xizmati, ish haqi fondi bilan birga", "Natija – bajarilgan funksiya"),
        ("Qachon mos keladi", "Uzoq muddatli asosiy lavozimlar, yuridik shaxs va HR bo‘limi mavjud bo‘lsa", "Shtatni kengaytirmasdan yoki O‘zbekistonda yuridik shaxssiz o‘z boshqaruvingizdagi jamoa kerak bo‘lsa", "Funksiyani to‘liq topshirib, natija olish kerak bo‘lsa"),
    ],
    cmp_note="Human and Capital autstaffing modeli bo‘yicha ishlaydi: xodimlar sizning rahbarligingiz ostida vazifalaringizni bajaradi, biz esa ularni ishga rasmiylashtirish, ish haqi, kadrlar hisobi va hisobotlarni o‘z zimmamizga olamiz.",
    fit_eyebrow="Kimlar uchun", fit_title="Qachon autstaffing tanlanadi",
    fit=[
        "O‘zbekistonda yuridik shaxs va HR bo‘limi ochmasdan jamoaga ega bo‘lishni istagan xalqaro kompaniyalar",
        "BPO loyihalari: kontakt-markazlar, tarjima loyihalari, mijozlarni qo‘llab-quvvatlash va texnik yordam",
        "Mavsumiy cho‘qqilar yoki jamoani tez kengaytirish va qisqartirish kerak bo‘lgan loyihalar",
        "Kadrlar ma’muriyati va ish haqini hisoblash yukidan xalos bo‘lishni istagan kompaniyalar",
        "Ingliz, nemis, arab, turk, koreys, fransuz va boshqa tillarni biladigan mutaxassislar kerak bo‘lgan loyihalar",
        "Shaffof byudjet va jamoa bo‘yicha muntazam hisobot muhim bo‘lganlar",
    ],
    steps_eyebrow="Qanday boshlash", steps_title="Autstaffingni 6 bosqichda ishga tushirish",
    steps=[
        ("Ariza", "Vazifani tasvirlaysiz: lavozimlar, xodimlar soni, tillar va ish jadvali."),
        ("Tahlil va taklif", "Jamoa tarkibi, mutaxassislarga talablar va shartlarni kelishamiz."),
        ("Shartnoma", "Xizmatlar hajmi, muddatlar va hisobot tartibini belgilaymiz."),
        ("Tanlash va baholash", "Mutaxassislarni topamiz va tekshiramiz, nomzodlarni siz tasdiqlaysiz."),
        ("Rasmiylashtirish", "Xodimlarni O‘zbekiston qonunchiligiga muvofiq kompaniyamizga ishga olamiz."),
        ("Ish va kuzatib borish", "Xodimlar vazifalaringiz ustida ishlaydi, biz kadrlar, ish haqi va hisobotlarni yuritamiz."),
    ],
    links='Faqat xodim tanlash kerakmi? – <a href="recruitment-uz.html">Rekruting</a>. HR jarayonlarini yo‘lga qo‘ymoqchimisiz? – <a href="consulting-uz.html">HR-konsalting</a>.',
    faq_eyebrow="Savol-javoblar", faq_title="Autstaffing haqida ko‘p beriladigan savollar",
    faq=[
        ("Autstaffing nima?", "Xodimlar autstaffing kompaniyasida rasman ishga rasmiylashtiriladi, lekin mijozning vazifalari ustida va uning rahbarligi ostida ishlaydi. Provayder ishga rasmiylashtirish, ish haqi, kadrlar hisobi va hisobotlar uchun javob beradi, mijoz esa vazifalarni qo‘yadi va natijaga ega bo‘ladi."),
        ("Autstaffing autsorsingdan nimasi bilan farq qiladi?", "Autstaffingda xodimlar ishini o‘zingiz boshqarasiz, provayder esa faqat rasmiylashtirish va ma’muriy ishlarni bajaradi. Autsorsingda funksiyani pudratchiga to‘liq topshirasiz va odamlarni boshqarmasdan tayyor natija olasiz."),
        ("Xorijiy kompaniya autstaffing orqali O‘zbekistonda xodim yollay oladimi?", "Ha, bu xalqaro mijozlar bizga murojaat qiladigan asosiy holatlardan biri. Xodimlar O‘zbekiston Respublikasi qonunchiligiga muvofiq kompaniyamizga rasmiylashtiriladi va sizning vazifalaringiz ustida ishlaydi."),
        ("Xodimlar rasman rasmiylashtiriladimi?", "Ha. Xodimlarni O‘zbekiston Respublikasi mehnat qonunchiligiga muvofiq ishga olamiz, ish haqini hisoblaymiz, soliq va badallarni hisoblaymiz hamda hisobotlarni o‘z vaqtida topshiramiz."),
        ("Autstaffing orqali qanday mutaxassislarni olish mumkin?", "Bizning ixtisosligimiz – BPO: kontakt-markaz operatorlari, tarjimonlar, mijozlarni qo‘llab-quvvatlash va texnik yordam mutaxassislari, shu jumladan chet tillarini biladiganlar. Boshqa profil kerak bo‘lsa, vazifani tasvirlang – yechim taklif qilamiz."),
        ("Jamoani kengaytirish yoki qisqartirish mumkinmi?", "Ha. So‘rovingiz bo‘yicha jamoani kengaytiramiz yoki qisqartiramiz, shu jumladan mavsumiy va yuqori yuklama davrlarida."),
        ("Autstaffing qancha turadi?", "Narx individual hisoblanadi va xodimlar soni, ularning malakasi hamda ish sharoitlariga bog‘liq. Ariza qoldiring – bir ish kuni ichida taklif tayyorlaymiz."),
        ("IT Park rezidentligi nima beradi?", "Biz IT Parkning imtiyozli huquqiy va soliq rejimi doirasida ishlaymiz. Bu hamkorlikni mijoz uchun shaffof, xavfsiz va iqtisodiy jihatdan foydali qiladi."),
    ],
)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def sections(d):
    scope = "\n".join(f'      <div class="oss-card reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in d["scope"])
    HL = ' class="oss-hl"'
    head = "".join(f'<th{HL if i == 2 else ""}>{h}</th>' for i, h in enumerate(d["cmp_head"]))
    rows = "\n".join(
        "          <tr><th>" + r[0] + "</th>" + "".join(f'<td{HL if i == 1 else ""} data-label="{d["cmp_head"][i + 1]}">{c}</td>' for i, c in enumerate(r[1:])) + "</tr>"
        for r in d["cmp_rows"])
    fit = "\n".join(f"      <li>{x}</li>" for x in d["fit"])
    steps = "\n".join(f'      <li class="reveal"><h3>{t}</h3><p>{p}</p></li>' for t, p in d["steps"])
    faq = "\n".join(f"      <details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in d["faq"])
    return f"""{MARK_B}
<section id="os-scope">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['scope_eyebrow']}</p>
      <h2 class="sec-title">{d['scope_title']}</h2>
    </div>
    <div class="oss-grid">
{scope}
    </div>
  </div>
</section>

<section id="os-compare">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['cmp_eyebrow']}</p>
      <h2 class="sec-title">{d['cmp_title']}</h2>
    </div>
    <div class="oss-table-wrap reveal">
      <table class="oss-table">
        <thead><tr>{head}</tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
    <p class="oss-note reveal">{d['cmp_note']}</p>
  </div>
</section>

<section id="os-fit">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['fit_eyebrow']}</p>
      <h2 class="sec-title">{d['fit_title']}</h2>
    </div>
    <ul class="oss-fit reveal">
{fit}
    </ul>
  </div>
</section>

<section id="os-steps">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">{d['steps_eyebrow']}</p>
      <h2 class="sec-title">{d['steps_title']}</h2>
    </div>
    <ol class="oss-steps">
{steps}
    </ol>
    <p class="oss-links reveal">{d['links']}</p>
  </div>
</section>

<section id="os-faq">
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
{MARK_E}

"""


def jsonld(d):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": d["service_name"], "serviceType": "Outstaffing", "description": d["desc"], "url": d["url"],
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


for lang, d in L.items():
    p = d["file"]
    s = open(p, encoding="utf-8").read()
    s = strip_between(s, MARK_B, MARK_E)
    s = strip_between(s, LD_B, LD_E)
    i = s.find(CSS_B)
    if i >= 0:
        s = s[:i] + s[s.index(CSS_E) + len(CSS_E):]

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
