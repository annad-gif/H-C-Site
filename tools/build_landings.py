"""Посадочные страницы под отдельные поисковые запросы: Executive search (RU/EN/UZ) и Employer of Record (EN).

Оболочка (стили, меню, форма, подвал, скрипты) берётся из consulting*.html нужного языка,
контент – из PAGES ниже. Цены услуг не указываем (см. «стоимость рассчитывается индивидуально»).
Запуск из корня сайта: python3 tools/build_landings.py
"""
import json, re

SITE = "https://humancapital.uz"
A = "/articles/"
ARROW = '<svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'

ES_ALT = {"ru": "executive-search.html", "en": "executive-search-en.html", "uz": "executive-search-uz.html"}

PAGES = []

# ---------------------------------------------------------------- Executive search RU
PAGES.append(dict(
    file="executive-search.html", shell="consulting.html", lang="ru", locale="ru_RU", alt=ES_ALT,
    home=("Главная", SITE + "/"), parent=("Подбор персонала", SITE + "/recruitment.html"),
    title="Executive search в Ташкенте – подбор топ-менеджеров и руководителей | Human and Capital",
    short="Executive search в Ташкенте – Human and Capital",
    desc="Executive search и хедхантинг в Ташкенте: прямой поиск топ-менеджеров, руководителей и редких специалистов по всему Узбекистану. Конфиденциально, с гарантией замены.",
    service="Executive search – подбор топ-менеджеров в Узбекистане",
    eyebrow="Executive search · Ташкент",
    h1='Executive search и подбор <span class="accent">топ-менеджеров</span> в Ташкенте',
    lead="Находим руководителей и редких специалистов, которые не ищут работу активно: прямой поиск, глубокая оценка и полная конфиденциальность на каждом этапе.",
    cta=("Обсудить позицию", "Как мы ищем", "#lp-process"),
    stats=[("5+", "лет на HR-рынке Узбекистана"), ("500+", "закрытых позиций для клиентов"), ("20+", "HR-специалистов в команде")],
    marquee=["Executive search", "Хедхантинг", "Топ-менеджмент", "Руководители направлений", "Редкие специалисты", "Конфиденциальный поиск"],
    intro=("Что такое executive search", "Прямой поиск вместо ожидания откликов", [
        "<strong>Executive search</strong> – это подбор руководителей и ключевых специалистов методом прямого поиска. Сильные топ-менеджеры почти никогда не откликаются на вакансии: они уже работают и ценятся в своих компаниях. Поэтому мы не ждём резюме, а сами находим людей с нужным опытом и лично предлагаем им вашу позицию.",
        "Такой поиск называют ещё <strong>хедхантингом</strong>. Он требует знания рынка: кто и где сейчас работает, какие команды сильны в вашей отрасли, сколько стоят такие специалисты и что может их заинтересовать, кроме денег.",
        "Human and Capital ведёт executive search в Ташкенте и по всему Узбекистану для местных и международных компаний. Если вы ещё выбираете подрядчика, прочитайте статью <a href=\"" + A + "kak-vybrat-kadrovoe-agentstvo-v-tashkente-fcdacdb7\">Как выбрать кадровое агентство в Ташкенте</a>.",
    ]),
    svc=("Кого ищем", "Позиции для executive search", "Беремся за роли, от которых зависит результат бизнеса и где ошибка найма стоит дорого.", [
        ("01 / ТОП-МЕНЕДЖМЕНТ", "Первые лица и C-level", "Руководители, которые отвечают за стратегию и результат компании.",
         ["Генеральный и исполнительный директор", "Финансовый директор (CFO)", "Операционный директор (COO)", "Коммерческий директор", "Директор по персоналу (HRD)"]),
        ("02 / РУКОВОДИТЕЛИ", "Руководители направлений", "Те, кто строит и ведёт команды внутри бизнеса.",
         ["Руководители продаж и маркетинга", "IT-директора и руководители разработки", "Руководители производства и логистики", "Руководители филиалов и региональные менеджеры", "Руководители контакт-центров и BPO"]),
        ("03 / РЕДКИЕ ЭКСПЕРТЫ", "Узкие специалисты", "Эксперты с редким сочетанием опыта, которых на рынке единицы.",
         ["Специалисты с отраслевой экспертизой", "Руководители проектов запуска", "Специалисты со знанием иностранных языков", "Эксперты для выхода на рынок Узбекистана", "Позиции, которые не удалось закрыть другим способом"]),
    ]),
    who=("Когда нужен executive search", "Типичные задачи", "Типичные запросы", [
        "Нужен руководитель, а на вакансию откликаются не те люди",
        "Позицию нужно закрыть конфиденциально, пока на ней работает другой человек",
        "Компания запускает новое направление или выходит на рынок Узбекистана",
        "Нужен кандидат из конкретной отрасли или из конкретных компаний",
        "Прошлый найм на эту роль не сработал, и ошибку нельзя повторить",
    ], "Отрасли", ["IT", "Финансы и банки", "Ритейл", "Производство", "Дистрибуция", "Фарма и медицина", "Недвижимость и строительство", "Туризм и авиация", "HORECA", "BPO и контакт-центры", "Госсектор", "и многие другие"]),
    process=("Как мы ищем", "8 шагов executive search", "Каждый этап согласуем с вами заранее – от брифа до выхода кандидата и испытательного срока.", [
        ("Бриф", "Разбираем задачи позиции, ожидаемые результаты, команду и условия."),
        ("Профиль кандидата", "Фиксируем обязательные требования, компетенции и список целевых компаний."),
        ("Карта рынка", "Изучаем, где работают подходящие люди, и составляем длинный список."),
        ("Прямой выход", "Лично связываемся с кандидатами и конфиденциально презентуем позицию."),
        ("Оценка", "Проводим интервью по компетенциям, проверяем опыт и рекомендации."),
        ("Шорт-лист", "Представляем лучших кандидатов с подробным отчётом по каждому."),
        ("Оффер", "Помогаем согласовать условия и довести кандидата до выхода."),
        ("Адаптация", "Остаёмся на связи с руководителем и сотрудником на испытательном сроке."),
    ]),
    why=("Почему Human and Capital", "Гарантии и преимущества", [
        ("Конфиденциальность", "Не раскрываем название компании без вашего согласия и готовы подписать NDA."),
        ("Гарантия замены", "Одна бесплатная замена специалиста в оговорённый срок."),
        ("Гарантия поиска", "Если в согласованный срок не представим минимум 3 подходящих кандидата, вернём предоплату."),
        ("Глубокая оценка", "Интервью по компетенциям, проверка опыта и рекомендаций до того, как вы увидите кандидата."),
        ("Знание рынка", "Постоянно отслеживаем рынок труда и ожидания руководителей по доходу в Узбекистане."),
        ("Опытная команда", "Каждый специалист команды работает в своей области больше 2 лет."),
    ]),
    reviews=("Отзывы клиентов", "Что говорят о нас", "index.html"),
    faq=("Вопросы и ответы", "Executive search: частые вопросы", [
        ("Чем executive search отличается от обычного подбора?", "При обычном подборе вакансию размещают на сайтах и работают с откликами. При executive search мы сами находим кандидатов, которые сейчас работают и не ищут новое место, и лично предлагаем им вашу позицию. Так ищут руководителей и редких специалистов."),
        ("Сколько длится поиск руководителя?", "Срок зависит от позиции, требований к кандидату, ситуации на рынке и условий, которые вы предлагаете. Мы согласуем срок до начала поиска и держим вас в курсе на каждом этапе."),
        ("Как вы обеспечиваете конфиденциальность?", "Мы не раскрываем название компании кандидатам без вашего согласия, презентуем позицию в обезличенном виде и готовы подписать NDA. Это особенно важно, когда вы ищете замену действующему руководителю."),
        ("Как вы оцениваете кандидатов?", "Проводим интервью по компетенциям, проверяем профессиональный опыт и рекомендации, при необходимости – кейсы и тесты. Вы получаете шорт-лист с подробным отчётом по каждому кандидату."),
        ("Есть ли гарантия?", "Да. Одна бесплатная замена специалиста в оговорённый срок, бесплатный пробный день кандидата и возврат предоплаты, если в согласованный срок мы не представим минимум трёх подходящих кандидатов."),
        ("Ищете ли вы руководителей для иностранных компаний?", "Да. Мы работаем с местными и международными компаниями и ищем руководителей, которые будут работать в Узбекистане, в том числе со знанием иностранных языков."),
        ("Сколько стоит executive search?", "Стоимость рассчитывается индивидуально: она зависит от уровня позиции, сроков и сложности поиска. Оставьте заявку, и мы подготовим предложение в течение одного рабочего дня."),
    ]),
    read=("Полезно знать", "Статьи по теме", [
        (A + "kak-vybrat-kadrovoe-agentstvo-v-tashkente-fcdacdb7", "Как выбрать кадровое агентство в Ташкенте", "10 вопросов агентству до подписания договора"),
        (A + "intervyu-po-kompetentsiyam-119bd224", "Интервью по компетенциям", "Как оценивать кандидатов на собеседовании"),
        (A + "sovremennye-metody-otsenki-kandidatov-ca76824c", "Современные методы оценки кандидатов", "Ключевые подходы к оценке"),
        ("/recruitment.html", "Подбор персонала в Ташкенте", "Специалисты, IT и массовый подбор"),
    ]),
    options=["Executive search", "Подбор руководителя", "Подбор специалиста", "Массовый подбор", "Аутстаффинг", "HR-консалтинг"],
))

# ---------------------------------------------------------------- Executive search EN
PAGES.append(dict(
    file="executive-search-en.html", shell="consulting-en.html", lang="en", locale="en_US", alt=ES_ALT,
    home=("Home", SITE + "/index-en.html"), parent=("Recruitment", SITE + "/recruitment-en.html"),
    title="Executive Search in Uzbekistan – Headhunting in Tashkent | Human and Capital",
    short="Executive Search in Uzbekistan – Human and Capital",
    desc="Executive search and headhunting in Tashkent: direct search for C-level executives, senior managers and rare specialists across Uzbekistan. Confidential, with a replacement guarantee.",
    service="Executive search in Uzbekistan",
    eyebrow="Executive search · Uzbekistan",
    h1='Executive Search in <span class="accent">Uzbekistan</span>',
    lead="We find executives and rare specialists who are not actively looking for a job – through direct search, in-depth assessment and full confidentiality at every stage.",
    cta=("Discuss a role", "How we search", "#lp-process"),
    stats=[("5+", "years on the HR market of Uzbekistan"), ("500+", "positions filled for our clients"), ("20+", "HR specialists on the team")],
    marquee=["Executive search", "Headhunting", "C-level", "Heads of departments", "Rare specialists", "Confidential search"],
    intro=("What executive search is", "Direct search instead of waiting for applications", [
        "<strong>Executive search</strong> is the recruitment of executives and key specialists through direct search. Strong leaders rarely respond to job ads: they are already employed and valued by their companies. So we do not wait for CVs – we identify people with the right experience ourselves and approach them with your role personally.",
        "This is also called <strong>headhunting</strong>. It requires knowing the market: who works where, which teams are strong in your industry, what such people expect and what can motivate them beyond salary.",
        "Human and Capital runs executive search in Tashkent and across Uzbekistan for local and international companies. Building a team here from abroad? Start with our guide <a href=\"" + A + "hiring-in-uzbekistan-d0f28979\">Hiring in Uzbekistan</a>.",
    ]),
    svc=("Who we search for", "Roles for executive search", "We take on roles that drive business results and where a wrong hire is expensive.", [
        ("01 / C-LEVEL", "Top management", "Leaders responsible for the company's strategy and results.",
         ["CEO and managing director", "Chief financial officer (CFO)", "Chief operating officer (COO)", "Commercial director", "HR director"]),
        ("02 / HEADS", "Heads of departments", "People who build and lead teams inside the business.",
         ["Heads of sales and marketing", "IT directors and heads of engineering", "Heads of production and logistics", "Branch and regional managers", "Contact centre and BPO managers"]),
        ("03 / RARE EXPERTS", "Niche specialists", "Experts with a rare combination of experience that the market has only a few of.",
         ["Specialists with deep industry expertise", "Launch and project leaders", "Specialists with foreign languages", "Experts for entering the Uzbek market", "Roles that could not be filled any other way"]),
    ]),
    who=("When you need executive search", "Typical situations", "Typical requests", [
        "You need a leader, but the job ad attracts the wrong people",
        "The role must be filled confidentially while someone else still holds it",
        "The company is launching a new business line or entering Uzbekistan",
        "You need a candidate from a specific industry or specific companies",
        "A previous hire for this role did not work out, and the mistake must not be repeated",
    ], "Industries", ["IT", "Finance &amp; banking", "Retail", "Manufacturing", "Distribution", "Pharma &amp; Medicine", "Real Estate &amp; Construction", "Tourism &amp; Aviation", "HORECA", "BPO &amp; contact centres", "Government", "and many more"]),
    process=("How we search", "8 steps of executive search", "Every stage is agreed with you in advance – from the brief to the candidate's start date and probation.", [
        ("Brief", "We discuss the role's objectives, expected results, team and conditions."),
        ("Candidate profile", "We fix the must-have requirements, competencies and a list of target companies."),
        ("Market mapping", "We study where suitable people work and build a long list."),
        ("Direct approach", "We contact candidates personally and present the role confidentially."),
        ("Assessment", "Competency-based interviews, verification of experience and references."),
        ("Shortlist", "We present the best candidates with a detailed report on each."),
        ("Offer", "We help agree on the terms and bring the candidate to the start date."),
        ("Adaptation", "We stay in touch with the manager and the new hire during probation."),
    ]),
    why=("Why Human and Capital", "Guarantees and advantages", [
        ("Confidentiality", "We do not disclose your company name without your consent and are ready to sign an NDA."),
        ("Free replacement", "One free replacement of a hired specialist within the agreed terms."),
        ("Search guarantee", "If we do not present at least 3 suitable candidates within the agreed timeframe, the prepayment is refunded."),
        ("In-depth assessment", "Competency interviews, experience and reference checks before you meet a candidate."),
        ("Market insight", "We continuously track the labour market and executive pay expectations in Uzbekistan."),
        ("Experienced team", "Every member of our team has more than 2 years of experience in their field."),
    ]),
    reviews=("Client reviews", "What clients say", "index-en.html"),
    faq=("FAQ", "Executive search: frequently asked questions", [
        ("How is executive search different from regular recruitment?", "In regular recruitment a vacancy is posted and the recruiter works with applications. In executive search we identify candidates who are currently employed and not looking for a new job, and approach them with your role personally. This is how executives and rare specialists are hired."),
        ("How long does an executive search take?", "It depends on the role, the requirements, the market and the conditions you offer. We agree on the timeline before the search starts and keep you updated at every stage."),
        ("How do you ensure confidentiality?", "We do not reveal your company name to candidates without your consent, present the role anonymously and are ready to sign an NDA. This matters most when you are replacing a current executive."),
        ("How do you assess candidates?", "We run competency-based interviews, verify professional experience and references, and use case studies or tests when needed. You receive a shortlist with a detailed report on each candidate."),
        ("Is there a guarantee?", "Yes. One free replacement within the agreed terms, a free trial day for the candidate and a refund of the prepayment if we do not present at least three suitable candidates within the agreed timeframe."),
        ("Do you search for executives for international companies?", "Yes. We work with local and international companies and find leaders who will work in Uzbekistan, including candidates with English and other foreign languages."),
        ("How much does executive search cost?", "The cost is calculated individually and depends on the level of the role, the timeline and the complexity of the search. Send us a request and we will prepare a proposal within one business day."),
    ]),
    read=("Further reading", "Related pages", [
        ("/hr-services-uzbekistan.html", "HR services in Uzbekistan", "Recruitment, outstaffing and HR consulting in one place"),
        (A + "hiring-in-uzbekistan-d0f28979", "Hiring in Uzbekistan", "A practical guide for foreign companies"),
        ("/employer-of-record-uzbekistan.html", "Employer of Record in Uzbekistan", "Hire without opening a local entity"),
        ("/recruitment-en.html", "Recruitment agency in Uzbekistan", "Specialists, IT and mass recruitment"),
    ]),
    options=["Executive search", "Recruitment", "Mass recruitment", "Employer of Record", "Outstaffing", "HR consulting"],
))

# ---------------------------------------------------------------- Executive search UZ
PAGES.append(dict(
    file="executive-search-uz.html", shell="consulting-uz.html", lang="uz", locale="uz_UZ", alt=ES_ALT,
    home=("Bosh sahifa", SITE + "/index-uz.html"), parent=("Xodimlarni tanlash", SITE + "/recruitment-uz.html"),
    title="Executive search Toshkentda – top-menejerlar va rahbarlarni tanlash | Human and Capital",
    short="Executive search Toshkentda – Human and Capital",
    desc="Toshkentda executive search va hedhanting: butun O‘zbekiston bo‘ylab top-menejerlar, rahbarlar va noyob mutaxassislarni to‘g‘ridan-to‘g‘ri qidirish. Maxfiy, almashtirish kafolati bilan.",
    service="Executive search – O‘zbekistonda top-menejerlarni tanlash",
    eyebrow="Executive search · Toshkent",
    h1='Toshkentda executive search va <span class="accent">top-menejerlarni</span> tanlash',
    lead="Faol ish qidirmayotgan rahbarlar va noyob mutaxassislarni topamiz: to‘g‘ridan-to‘g‘ri qidiruv, chuqur baholash va har bir bosqichda to‘liq maxfiylik.",
    cta=("Lavozimni muhokama qilish", "Qanday qidiramiz", "#lp-process"),
    stats=[("5+", "yil O‘zbekiston HR bozorida"), ("500+", "mijozlar uchun yopilgan lavozim"), ("20+", "jamoadagi HR mutaxassis")],
    marquee=["Executive search", "Hedhanting", "Top-menejment", "Yo‘nalish rahbarlari", "Noyob mutaxassislar", "Maxfiy qidiruv"],
    intro=("Executive search nima", "Javob kutish o‘rniga to‘g‘ridan-to‘g‘ri qidiruv", [
        "<strong>Executive search</strong> – rahbarlar va asosiy mutaxassislarni to‘g‘ridan-to‘g‘ri qidirish usuli bilan tanlash. Kuchli top-menejerlar vakansiyalarga deyarli javob bermaydi: ular allaqachon ishlaydi va o‘z kompaniyalarida qadrlanadi. Shuning uchun biz rezyume kutmaymiz – kerakli tajribaga ega odamlarni o‘zimiz topamiz va ularga lavozimingizni shaxsan taklif qilamiz.",
        "Bunday qidiruv <strong>hedhanting</strong> deb ham ataladi. U bozorni bilishni talab qiladi: kim qayerda ishlayapti, sohangizda qaysi jamoalar kuchli, bunday mutaxassislar nimani kutadi va ularni puldan tashqari nima qiziqtirishi mumkin.",
        "Human and Capital Toshkentda va butun O‘zbekiston bo‘ylab mahalliy va xalqaro kompaniyalar uchun executive search olib boradi. Agar hali hamkor tanlayotgan bo‘lsangiz, <a href=\"" + A + "toshkentda-kadrlar-agentligini-qanday-tanlash-kerak-1f022de9\">Toshkentda kadrlar agentligini qanday tanlash kerak</a> maqolasini o‘qing.",
    ]),
    svc=("Kimni qidiramiz", "Executive search uchun lavozimlar", "Biznes natijasi bog‘liq bo‘lgan va xato ishga olish qimmatga tushadigan lavozimlarni olamiz.", [
        ("01 / TOP-MENEJMENT", "Birinchi shaxslar va C-level", "Kompaniya strategiyasi va natijasi uchun javob beradigan rahbarlar.",
         ["Bosh va ijrochi direktor", "Moliya direktori (CFO)", "Operatsion direktor (COO)", "Tijorat direktori", "Xodimlar bo‘yicha direktor (HRD)"]),
        ("02 / RAHBARLAR", "Yo‘nalish rahbarlari", "Biznes ichida jamoalarni quradigan va boshqaradiganlar.",
         ["Savdo va marketing rahbarlari", "IT-direktorlar va dasturlash rahbarlari", "Ishlab chiqarish va logistika rahbarlari", "Filial va mintaqaviy menejerlar", "Kontakt-markaz va BPO rahbarlari"]),
        ("03 / NOYOB EKSPERTLAR", "Tor mutaxassislar", "Bozorda kam uchraydigan, noyob tajribaga ega ekspertlar.",
         ["Soha bo‘yicha chuqur tajribali mutaxassislar", "Loyihalarni ishga tushirish rahbarlari", "Chet tillarini biladigan mutaxassislar", "O‘zbekiston bozoriga kirish uchun ekspertlar", "Boshqa yo‘l bilan yopib bo‘lmagan lavozimlar"]),
    ]),
    who=("Executive search qachon kerak", "Odatiy vazifalar", "Odatiy so‘rovlar", [
        "Rahbar kerak, lekin vakansiyaga mos bo‘lmagan odamlar javob beryapti",
        "Lavozimni maxfiy yopish kerak, hozir unda boshqa xodim ishlayapti",
        "Kompaniya yangi yo‘nalish ochmoqda yoki O‘zbekiston bozoriga kirmoqda",
        "Muayyan sohadan yoki muayyan kompaniyalardan nomzod kerak",
        "Bu lavozimga avvalgi ishga olish muvaffaqiyatsiz bo‘lgan va xatoni takrorlab bo‘lmaydi",
    ], "Sohalar", ["IT", "Moliya va banklar", "Chakana savdo", "Ishlab chiqarish", "Distributsiya", "Farmatsevtika va tibbiyot", "Ko‘chmas mulk va qurilish", "Turizm va aviatsiya", "HORECA", "BPO va kontakt-markazlar", "Davlat sektori", "va boshqalar"]),
    process=("Qanday qidiramiz", "Executive search 8 bosqichda", "Har bir bosqich siz bilan oldindan kelishiladi – brifdan nomzodning ishga chiqishi va sinov muddatigacha.", [
        ("Brif", "Lavozim vazifalari, kutilayotgan natijalar, jamoa va shartlarni muhokama qilamiz."),
        ("Nomzod profili", "Majburiy talablar, kompetensiyalar va maqsadli kompaniyalar ro‘yxatini belgilaymiz."),
        ("Bozor xaritasi", "Mos odamlar qayerda ishlashini o‘rganamiz va uzun ro‘yxat tuzamiz."),
        ("To‘g‘ridan-to‘g‘ri murojaat", "Nomzodlar bilan shaxsan bog‘lanamiz va lavozimni maxfiy taqdim etamiz."),
        ("Baholash", "Kompetensiyalar bo‘yicha suhbat, tajriba va tavsiyalarni tekshirish."),
        ("Qisqa ro‘yxat", "Eng yaxshi nomzodlarni har biri bo‘yicha batafsil hisobot bilan taqdim etamiz."),
        ("Taklif", "Shartlarni kelishishga va nomzodni ishga chiqishgacha olib borishga yordam beramiz."),
        ("Moslashuv", "Sinov muddatida rahbar va xodim bilan aloqada bo‘lamiz."),
    ]),
    why=("Nega Human and Capital", "Kafolatlar va afzalliklar", [
        ("Maxfiylik", "Roziligingizsiz kompaniya nomini oshkor qilmaymiz va NDA imzolashga tayyormiz."),
        ("Almashtirish kafolati", "Kelishilgan muddatda mutaxassisni bir marta bepul almashtirish."),
        ("Qidiruv kafolati", "Kelishilgan muddatda kamida 3 ta mos nomzod taqdim etmasak, oldindan to‘lovni qaytaramiz."),
        ("Chuqur baholash", "Nomzodni ko‘rishingizdan oldin kompetensiyalar bo‘yicha suhbat, tajriba va tavsiyalarni tekshirish."),
        ("Bozorni bilish", "O‘zbekistonda mehnat bozori va rahbarlarning daromad kutishlarini doimiy kuzatib boramiz."),
        ("Tajribali jamoa", "Jamoamizning har bir a’zosi o‘z sohasida 2 yildan ortiq ishlaydi."),
    ]),
    reviews=("Mijozlar fikri", "Biz haqimizda nima deyishadi", "index-uz.html"),
    faq=("Savol-javob", "Executive search: ko‘p beriladigan savollar", [
        ("Executive search oddiy tanlovdan nimasi bilan farq qiladi?", "Oddiy tanlovda vakansiya saytlarga joylanadi va javoblar bilan ishlanadi. Executive searchda biz hozir ishlayotgan va yangi joy qidirmayotgan nomzodlarni o‘zimiz topamiz va ularga lavozimingizni shaxsan taklif qilamiz. Rahbarlar va noyob mutaxassislar shunday tanlanadi."),
        ("Rahbarni qidirish qancha davom etadi?", "Muddat lavozimga, nomzodga qo‘yilgan talablarga, bozordagi vaziyatga va siz taklif qilayotgan shartlarga bog‘liq. Muddatni qidiruv boshlanishidan oldin kelishamiz va har bir bosqichda sizni xabardor qilib turamiz."),
        ("Maxfiylikni qanday ta’minlaysiz?", "Roziligingizsiz nomzodlarga kompaniya nomini aytmaymiz, lavozimni nomsiz taqdim etamiz va NDA imzolashga tayyormiz. Bu ayniqsa amaldagi rahbarga almashtiruv qidirayotganda muhim."),
        ("Nomzodlarni qanday baholaysiz?", "Kompetensiyalar bo‘yicha suhbat o‘tkazamiz, kasbiy tajriba va tavsiyalarni tekshiramiz, kerak bo‘lsa keyslar va testlardan foydalanamiz. Siz har bir nomzod bo‘yicha batafsil hisobotli qisqa ro‘yxat olasiz."),
        ("Kafolat bormi?", "Ha. Kelishilgan muddatda bir marta bepul almashtirish, nomzodning bepul sinov kuni va kelishilgan muddatda kamida uchta mos nomzod taqdim etilmasa, oldindan to‘lovni qaytarish."),
        ("Xalqaro kompaniyalar uchun rahbar qidirasizmi?", "Ha. Biz mahalliy va xalqaro kompaniyalar bilan ishlaymiz va O‘zbekistonda ishlaydigan rahbarlarni, jumladan chet tillarini biladigan nomzodlarni topamiz."),
        ("Executive search qancha turadi?", "Narx individual hisoblanadi: u lavozim darajasi, muddatlar va qidiruv murakkabligiga bog‘liq. So‘rov qoldiring – bir ish kuni ichida taklif tayyorlaymiz."),
    ]),
    read=("Foydali", "Mavzuga oid materiallar", [
        (A + "toshkentda-kadrlar-agentligini-qanday-tanlash-kerak-1f022de9", "Toshkentda kadrlar agentligini qanday tanlash kerak", "Shartnomadan oldin beriladigan 10 ta savol"),
        ("/recruitment-uz.html", "Toshkentda xodimlarni tanlash", "Mutaxassislar, IT va ommaviy tanlov"),
        ("/outstaffing-uz.html", "O‘zbekistonda xodimlar autstaffingi", "Rasmiylashtirish, ish haqi va hisobotlar"),
        ("/consulting-uz.html", "HR-konsalting", "HR-audit, baholash va moslashuv tizimlari"),
    ]),
    options=["Executive search", "Rahbarni tanlash", "Mutaxassisni tanlash", "Ommaviy tanlov", "Autstaffing", "HR-konsalting"],
))

# ---------------------------------------------------------------- Employer of Record EN
PAGES.append(dict(
    file="employer-of-record-uzbekistan.html", shell="consulting-en.html", lang="en", locale="en_US", alt=None,
    home=("Home", SITE + "/index-en.html"), parent=("HR services in Uzbekistan", SITE + "/hr-services-uzbekistan.html"),
    title="Employer of Record in Uzbekistan – EOR, Payroll & Recruitment | Human and Capital",
    short="Employer of Record in Uzbekistan – Human and Capital",
    desc="Employer of Record (EOR) in Uzbekistan for foreign companies: hire employees without a local entity. Recruitment, legal employment, payroll, taxes and labour law compliance with one Tashkent-based partner.",
    service="Employer of Record (EOR) in Uzbekistan",
    eyebrow="Employer of Record · Uzbekistan",
    h1='Employer of Record in <span class="accent">Uzbekistan</span>',
    lead="Hire employees in Uzbekistan without opening a local entity. We find the people, employ them under Uzbek labour law, run payroll and taxes – you manage their work.",
    cta=("Discuss your team", "How EOR works", "#lp-process"),
    stats=[("0", "local entities you need to open"), ("2–4", "weeks to a working employee for most roles"), ("1", "contract and one monthly invoice")],
    marquee=["Employer of Record", "EOR Uzbekistan", "Payroll", "Labour law compliance", "Recruitment included", "Remote teams"],
    intro=("What an Employer of Record is", "Your legal employer in Uzbekistan", [
        "An <strong>Employer of Record (EOR)</strong> is a company that legally employs people on behalf of another business. Human and Capital becomes the official employer of your team members in Uzbekistan: we sign employment contracts under Uzbek labour law, run payroll, pay taxes and keep HR records. The employees work full-time on your tasks, under your management.",
        "For a foreign company this is the fastest way to start hiring in Uzbekistan. Setting up a local legal entity takes months, an accountant, a lawyer and a payroll provider. With an EOR you get one partner, one contract and one invoice – and you can have an employee at work in a few weeks.",
        "Unlike most EOR platforms, we are a <strong>Tashkent-based recruitment agency</strong>: we also find the people. Recruitment, employment and day-to-day HR support come from one local team. Read more in our guide <a href=\"" + A + "hiring-in-uzbekistan-d0f28979\">Hiring in Uzbekistan</a>.",
    ]),
    svc=("What's included", "Recruitment, employment and compliance", "Every part of employing a team in Uzbekistan – handled by one partner.", [
        ("01 / RECRUITMENT", "We find your people", "Search and selection by our own recruiters, built into the service.",
         ["Role scoping and sourcing strategy", "CV screening and interviews", "Skills and language testing", "Reference checks", "Offer negotiation support"]),
        ("02 / EMPLOYMENT", "We employ them", "Official employment under the labour law of Uzbekistan.",
         ["Uzbek employment contracts", "Payroll processing and payslips", "Income tax and social tax filing", "Leave and absence tracking", "Probation and termination management"]),
        ("03 / COMPLIANCE &amp; HR", "We keep it compliant", "HR administration and reporting so you never deal with local bureaucracy.",
         ["Labour law compliance", "HR documentation and records", "Monthly reporting", "Attendance and performance monitoring", "NDA and data confidentiality"]),
    ]),
    compare=("EOR vs other options", "Ways to hire in Uzbekistan", ["", "Employer of Record", "Your own entity", "Contractors"], [
        ("Time to start", "A few weeks", "Several months", "Fast"),
        ("Local legal entity", "Not needed", "Required", "Not needed"),
        ("Employment under Uzbek labour law", "Yes", "Yes", "No"),
        ("Payroll and taxes", "Handled by us", "Your accountant", "Contractor's own"),
        ("Compliance risk for you", "Low", "On you", "Misclassification risk"),
        ("Recruitment", "Included", "Separate provider", "Separate provider"),
        ("Best for", "1–50 employees, fast start", "Large long-term operations", "Short one-off projects"),
    ]),
    who=("Who it's for", "Companies hiring in Uzbekistan from abroad", "Typical requests", [
        "A US or European company wants a remote team in Uzbekistan without a local entity",
        "A business needs multilingual support, sales or contact centre staff",
        "An IT company is adding developers, QA engineers or analysts in Tashkent",
        "A company is testing the Uzbek market before opening its own office",
        "An existing contractor setup needs to become compliant employment",
    ], "Roles we employ", ["Customer support", "Contact centre operators", "Interpreters", "Developers", "QA engineers", "Data and business analysts", "Sales and account managers", "Back-office and finance", "HR and recruitment", "Multilingual specialists", "Project managers", "and many more"]),
    process=("How EOR works", "From kick-off to a working employee", "A typical hire goes live in 2–4 weeks. Every step is agreed with you in advance.", [
        ("Scope and contract", "We define the role, agree on terms and timeline and sign one master agreement."),
        ("Candidate search", "Our recruiters source, screen and interview candidates from the local market."),
        ("Testing and selection", "Shortlisted candidates pass skills and language tests. You choose the hire."),
        ("Employment", "We sign an Uzbek employment contract with the employee and onboard them."),
        ("Payroll", "We run payroll, pay taxes and handle HR records every month."),
        ("Monthly invoice", "You receive one simple monthly invoice and regular reporting."),
        ("Support", "One account manager handles HR questions for you and the employee."),
        ("Scaling", "Add new team members at any time or reduce the team with notice."),
    ]),
    why=("Why Human and Capital", "A local EOR partner that also recruits", [
        ("Recruitment included", "You do not need a separate recruiter – we find and employ the people."),
        ("Local expertise", "Tashkent-based team that knows the labour market, salaries and labour law of Uzbekistan."),
        ("Replacement guarantee", "If a hired employee does not work out within the agreed period, we replace them."),
        ("One point of contact", "A dedicated account manager instead of several providers."),
        ("Confidentiality", "Every engagement is covered by an NDA; client and employee data are protected."),
        ("Multilingual talent", "Specialists with verified English, German, Arabic, Turkish, Korean, French and other languages."),
    ]),
    reviews=("Client reviews", "What clients say", "index-en.html"),
    faq=("FAQ", "Employer of Record in Uzbekistan: FAQ", [
        ("Do I need a legal entity in Uzbekistan to hire employees?", "No. With an Employer of Record we are the legal employer. Your employees get official contracts under Uzbek labour law, and you manage their work without registering a company in Uzbekistan."),
        ("Is using an EOR legal in Uzbekistan?", "Yes. The employees are officially employed by our company in Uzbekistan, with payroll, taxes and reporting handled in line with local law."),
        ("How fast can I hire through an EOR?", "For most roles a new employee can start within 2–4 weeks, including recruitment. Rare or senior roles may take longer; we agree on the timeline before the search starts."),
        ("Who manages the employee's daily work?", "You do. The employee works on your tasks, follows your processes and reports to your managers. We handle employment, payroll, taxes and HR administration."),
        ("What is the difference between EOR and outstaffing?", "They are very close. In both models we are the legal employer and you direct the work. Our EOR service also includes recruitment, so you get people, employment and payroll in one contract. See also our <a href=\"/outstaffing-en.html\">outstaffing page</a>."),
        ("Can you hire employees who already work for us as contractors?", "Yes. We can take your existing contractors in Uzbekistan into official employment, which removes the misclassification risk."),
        ("How is the cost of EOR calculated?", "The cost is calculated individually and depends on the number of employees, the roles and the scope of services. Send us a request and we will prepare a proposal within one business day."),
    ]),
    read=("Further reading", "Related pages", [
        ("/hr-services-uzbekistan.html", "HR services in Uzbekistan", "Recruitment, outstaffing and HR consulting in one place"),
        (A + "hiring-in-uzbekistan-d0f28979", "Hiring in Uzbekistan", "A practical guide for foreign companies"),
        ("/outstaffing-en.html", "Outstaffing in Uzbekistan", "Legal employment, payroll and reporting"),
        ("/executive-search-en.html", "Executive search in Uzbekistan", "Direct search for C-level and senior managers"),
    ]),
    options=["Employer of Record", "Outstaffing", "Recruitment", "Executive search", "Mass recruitment", "HR consulting"],
))

CSS = """
<style>
  /* ===== LANDING PAGES ===== */
  .hrs-stats{display:grid;grid-template-columns:1fr;gap:16px;width:100%;max-width:420px;}
  .hrs-stat{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);border-radius:18px;padding:24px 28px;
    display:flex;align-items:baseline;gap:18px;backdrop-filter:blur(6px);}
  .hrs-stat b{font-family:var(--ff-display);font-weight:700;font-size:clamp(34px,4vw,48px);color:var(--mustard);line-height:1;min-width:120px;}
  .hrs-stat span{font-size:15px;color:var(--grey-300);line-height:1.4;}
  #lp-intro,#lp-who,#lp-why,#lp-faq{background:var(--white);}
  #lp-services,#lp-reviews,#lp-read,#lp-compare{background:var(--grey-50);}
  .hrs-prose{max-width:760px;}
  .hrs-prose p{font-size:17px;color:var(--grey-700);line-height:1.8;margin-top:18px;}
  .hrs-prose p strong{color:var(--black);font-weight:600;}
  .hrs-prose p a{color:var(--mustard-dim);font-weight:600;}
  .hrs-svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;align-items:stretch;}
  .hrs-svc{display:flex;flex-direction:column;gap:18px;}
  .hrs-svc .hrs-num{font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--mustard-light);position:relative;}
  .hrs-svc h3{font-family:var(--ff-display);font-weight:600;font-size:21px;line-height:1.3;color:var(--white);position:relative;}
  .hrs-svc p{font-size:15px;color:var(--grey-300);line-height:1.7;position:relative;}
  .hrs-svc ul{list-style:none;display:flex;flex-direction:column;gap:10px;border-top:1px solid rgba(255,255,255,0.08);padding-top:18px;position:relative;}
  .hrs-svc li{display:flex;gap:11px;align-items:flex-start;font-size:14px;line-height:1.55;color:var(--grey-300);}
  .hrs-svc li::before{content:'';width:7px;height:7px;border-radius:50%;background:var(--mustard);flex-shrink:0;margin-top:7px;box-shadow:0 0 9px rgba(198,154,46,0.7);}
  .hrs-who-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;}
  .hrs-tags{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px;}
  .hrs-tags span{border:1px solid var(--grey-100);background:var(--grey-50);border-radius:999px;padding:9px 16px;font-size:14px;color:var(--grey-700);}
  .hrs-check{list-style:none;display:flex;flex-direction:column;gap:14px;margin-top:8px;}
  .hrs-check li{display:flex;gap:12px;font-size:16px;line-height:1.6;color:var(--grey-700);}
  .hrs-check li::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--mustard);flex-shrink:0;margin-top:9px;}
  .hrs-h3{font-family:var(--ff-display);font-weight:600;font-size:20px;margin-bottom:18px;color:var(--black);}
  #lp-process{background:var(--black);color:var(--white);}
  #lp-process .sec-title{color:var(--white);}
  #lp-process .sec-lead{color:var(--grey-300);}
  #lp-process .sec-eyebrow{color:var(--mustard-light);}
  .hrs-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;counter-reset:step;list-style:none;}
  .hrs-steps li{border:1px solid rgba(255,255,255,0.10);border-radius:16px;padding:24px 22px;background:rgba(255,255,255,0.03);}
  .hrs-steps li::before{counter-increment:step;content:counter(step,decimal-leading-zero);display:block;font-family:var(--ff-display);
    font-weight:700;font-size:22px;color:var(--mustard);margin-bottom:14px;}
  .hrs-steps h3{font-size:16px;font-weight:600;margin-bottom:8px;color:var(--white);}
  .hrs-steps p{font-size:14px;line-height:1.6;color:var(--grey-300);}
  .hrs-why-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
  .hrs-why{border:1px solid var(--grey-100);border-radius:18px;padding:28px 26px;background:var(--grey-50);}
  .hrs-why h3{font-family:var(--ff-display);font-weight:600;font-size:17px;line-height:1.35;margin-bottom:10px;}
  .hrs-why p{font-size:15px;line-height:1.65;color:var(--grey-700);}
  .hrs-rev-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
  .hrs-rev{background:var(--white);border:1px solid var(--grey-100);border-radius:18px;padding:28px 26px;display:flex;flex-direction:column;gap:18px;}
  .hrs-rev blockquote{font-size:15px;line-height:1.7;color:var(--grey-700);}
  .hrs-rev cite{font-style:normal;font-size:14px;color:var(--grey-500);margin-top:auto;}
  .hrs-rev cite b{display:block;color:var(--black);font-weight:600;font-size:15px;}
  .hrs-faq{max-width:860px;display:flex;flex-direction:column;gap:14px;}
  .hrs-faq .cons-acc-panel p{font-size:15px;line-height:1.7;color:var(--grey-300);border-top:1px solid rgba(255,255,255,0.08);padding-top:18px;}
  .hrs-faq .cons-acc-panel a{color:var(--mustard-light);}
  .hrs-faq .cons-acc-head h3{font-size:16px;}
  .lp-table-wrap{overflow-x:auto;border-radius:18px;border:1px solid var(--grey-100);background:var(--white);}
  .lp-table{width:100%;border-collapse:collapse;min-width:640px;font-size:15px;}
  .lp-table th,.lp-table td{padding:16px 20px;text-align:left;border-bottom:1px solid var(--grey-100);line-height:1.5;}
  .lp-table thead th{font-family:var(--ff-display);font-weight:600;font-size:15px;background:var(--grey-50);}
  .lp-table thead th:nth-child(2),.lp-table td:nth-child(2){background:rgba(198,154,46,0.08);}
  .lp-table tbody th{font-weight:600;color:var(--black);}
  .lp-table td{color:var(--grey-700);}
  .lp-table tr:last-child th,.lp-table tr:last-child td{border-bottom:none;}
  .rl-list{list-style:none;display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:980px;}
  .rl-list a{display:flex;flex-direction:column;gap:6px;padding:20px 22px;border-radius:16px;background:var(--white);border:1px solid var(--grey-100);text-decoration:none;color:var(--black);transition:border-color .2s, transform .2s;}
  .rl-list a:hover{border-color:var(--mustard);transform:translateY(-2px);}
  .rl-list b{font-family:var(--ff-display);font-weight:600;font-size:16px;line-height:1.35;}
  .rl-list span{font-size:14px;color:var(--grey-500);}
  @media (max-width:1080px){
    .hrs-svc-grid,.hrs-why-grid,.hrs-rev-grid{grid-template-columns:1fr 1fr;}
    .hrs-steps{grid-template-columns:1fr 1fr;}
    .hrs-who-grid{grid-template-columns:1fr;gap:40px;}
    .hrs-stats{margin:0 auto;}
    .hrs-hero .rec-hero-visual{order:1 !important;}
  }
  @media (max-width:720px){
    .hrs-svc-grid,.hrs-why-grid,.hrs-rev-grid,.hrs-steps,.rl-list{grid-template-columns:1fr;}
    .hrs-stats{grid-template-columns:repeat(3,1fr);gap:10px;max-width:none;}
    .hrs-stat{flex-direction:column;align-items:flex-start;gap:8px;padding:16px 14px;border-radius:14px;}
    .hrs-stat b{font-size:26px;min-width:0;}
    .hrs-stat span{font-size:12px;}
    .hrs-prose p{font-size:16px;}
  }
</style>
"""


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def reviews_from(index_file):
    """Отзывы с главной нужного языка: (текст, имя, должность)."""
    s = open(index_file, encoding="utf-8").read()
    out = re.findall(r'<p class="rev-text">(.*?)</p>.*?<div class="rev-name">(.*?)</div><div class="rev-role">(.*?)</div>', s, re.S)
    assert len(out) >= 3, index_file
    return out[:3]


def acc(q, a):
    return f"""      <div class="cons-card cons-acc reveal">
        <div class="cons-acc-head">
          <h3>{q}</h3>
          <span class="cons-acc-caret"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></span>
        </div>
        <div class="cons-acc-panel"><p>{a}</p></div>
      </div>"""


def sec_head(eyebrow, title, lead=None):
    lead_html = f'\n      <p class="sec-lead">{lead}</p>' if lead else ""
    return f"""    <div class="sec-head reveal">
      <p class="sec-eyebrow">{eyebrow}</p>
      <h2 class="sec-title">{title}</h2>{lead_html}
    </div>"""


def build(d):
    src = open(d["shell"], encoding="utf-8").read()
    url = f"{SITE}/{d['file']}"

    # ---------- head ----------
    style = src[src.index("<style>"):src.index("</style>") + len("</style>")]
    fonts = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com"/>.*?rel="stylesheet"/>', src, re.S).group(0)
    crumbs = [d["home"], d["parent"], (strip_tags(d["h1"]), url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "@id": url + "#service", "name": d["service"], "serviceType": d["service"],
         "description": d["desc"], "url": url, "areaServed": {"@type": "Country", "name": "Uzbekistan"},
         "provider": {"@id": SITE + "/#organization"}},
        {"@type": ["Organization", "EmploymentAgency"], "@id": SITE + "/#organization", "name": "Human and Capital",
         "url": SITE + "/", "logo": SITE + "/logo.png", "telephone": "+998903251336", "email": "akmal.s@human-capital.org",
         "address": {"@type": "PostalAddress", "streetAddress": "Farg‘ona yo‘li, 94", "addressLocality": "Tashkent", "addressCountry": "UZ"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in d["faq"][2]]},
    ]}
    alt = ""
    if d["alt"]:
        alt = "\n".join(f'<link rel="alternate" hreflang="{hl}" href="{SITE}/{f}"/>' for hl, f in d["alt"].items())
        alt += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/{d["alt"]["ru"]}"/>'
    head = f"""<!DOCTYPE html>
<html lang="{d['lang']}">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<script src="/hc-analytics.js" async></script>
<meta name="description" content="{d['desc']}"/>
<title>{d['title']}</title>
<!-- SEO -->
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="{url}"/>
{alt}
<!-- Open Graph -->
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Human and Capital"/>
<meta property="og:locale" content="{d['locale']}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{d['short']}"/>
<meta property="og:description" content="{d['desc']}"/>
<meta property="og:image" content="{SITE}/og-cover.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{d['short']}"/>
<meta name="twitter:description" content="{d['desc']}"/>
<meta name="twitter:image" content="{SITE}/og-cover.png"/>
<link rel="icon" href="/favicon.ico"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
{fonts}
{style}
{CSS}
</head>
"""

    # ---------- nav: языковое меню ведёт на версии этой страницы ----------
    nav = src[src.index('<nav id="nav">'):src.index("</nav>") + len("</nav>")]
    base = d["shell"].replace(".html", "").replace("-en", "").replace("-uz", "")
    targets = d["alt"] or {"ru": "index.html", "en": d["file"], "uz": "index-uz.html"}
    for hl, code in (("ru", "RU"), ("en", "ENG"), ("uz", "UZB")):
        shell_name = {"ru": base + ".html", "en": base + "-en.html", "uz": base + "-uz.html"}[hl]
        old = f'<a href="{shell_name}" data-lang="{code}">'
        assert old in nav, (d["file"], old)
        nav = nav.replace(old, f'<a href="{targets[hl]}" data-lang="{code}">')

    s_ = d
    svc_cards = "\n".join(f"""      <article class="cons-card hrs-svc reveal">
        <span class="hrs-num">{num}</span>
        <h3>{t}</h3>
        <p>{p}</p>
        <ul>
{chr(10).join(f'          <li>{x}</li>' for x in items)}
        </ul>
      </article>""" for num, t, p, items in s_["svc"][3])

    compare = ""
    if d.get("compare"):
        ce, ct, heads, rows = d["compare"]
        th = "".join(f"<th scope=\"col\">{h}</th>" for h in heads)
        trs = "\n".join("          <tr><th scope=\"row\">" + r[0] + "</th>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows)
        compare = f"""
<!-- COMPARE -->
<section id="lp-compare">
  <div class="container">
{sec_head(ce, ct)}
    <div class="lp-table-wrap reveal">
      <table class="lp-table">
        <thead><tr>{th}</tr></thead>
        <tbody>
{trs}
        </tbody>
      </table>
    </div>
  </div>
</section>
"""

    revs = reviews_from(d["reviews"][2])
    ie, it, ips = d["intro"]
    we, wt, wh1, wreq, wh2, wtags = d["who"]
    pe, pt, pl, steps = d["process"]
    ye, yt, whys = d["why"]
    fe, ft, faqs = d["faq"]
    re_, rt, reads = d["read"]
    main = f"""
<!-- HERO -->
<section class="rec-hero cons-hero hrs-hero" id="home">
  <div class="hero-aurora"><div class="aurora-blob"></div></div>
  <div class="hero-grain"></div>
  <div class="hero-glow g1"></div>
  <div class="hero-glow g2"></div>
  <div class="rec-hero-inner">
    <div class="rec-hero-text">
      <p class="hero-eyebrow"><span class="dot"></span>{d['eyebrow']}</p>
      <h1>{d['h1']}</h1>
      <p class="lead">{d['lead']}</p>
      <div class="hero-actions">
        <a href="#contact" class="btn btn-mustard">{d['cta'][0]}
          {ARROW.replace('<svg ', '<svg fill="none" stroke="currentColor" stroke-width="2" ')}
        </a>
        <a href="{d['cta'][2]}" class="btn btn-ghost">{d['cta'][1]}</a>
      </div>
    </div>
    <div class="rec-hero-visual">
      <div class="hrs-stats">
{chr(10).join(f'        <div class="hrs-stat"><b>{n}</b><span>{t}</span></div>' for n, t in d['stats'])}
      </div>
    </div>
  </div>
</section>

<!-- MARQUEE -->
<div class="marquee-wrap">
  <div class="marquee-track">
{chr(10).join(f'    <span class="marquee-item">{x} <span class="sep">·</span></span>' for x in d['marquee'] * 2)}
  </div>
</div>

<!-- INTRO -->
<section id="lp-intro">
  <div class="container">
    <div class="hrs-prose reveal">
      <p class="sec-eyebrow">{ie}</p>
      <h2 class="sec-title">{it}</h2>
{chr(10).join(f'      <p>{p}</p>' for p in ips)}
    </div>
  </div>
</section>

<!-- SERVICES -->
<section id="lp-services">
  <div class="container">
{sec_head(d['svc'][0], d['svc'][1], d['svc'][2])}
    <div class="hrs-svc-grid">
{svc_cards}
    </div>
  </div>
</section>
{compare}
<!-- WHO -->
<section id="lp-who">
  <div class="container">
{sec_head(we, wt)}
    <div class="hrs-who-grid">
      <div class="reveal">
        <h3 class="hrs-h3">{wh1}</h3>
        <ul class="hrs-check">
{chr(10).join(f'          <li>{x}</li>' for x in wreq)}
        </ul>
      </div>
      <div class="reveal">
        <h3 class="hrs-h3">{wh2}</h3>
        <div class="hrs-tags">
{chr(10).join(f'          <span>{x}</span>' for x in wtags)}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section id="lp-process">
  <div class="container">
{sec_head(pe, pt, pl)}
    <ol class="hrs-steps">
{chr(10).join(f'      <li class="reveal"><h3>{t}</h3><p>{p}</p></li>' for t, p in steps)}
    </ol>
  </div>
</section>

<!-- WHY -->
<section id="lp-why">
  <div class="container">
{sec_head(ye, yt)}
    <div class="hrs-why-grid">
{chr(10).join(f'      <div class="hrs-why reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in whys)}
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section id="lp-reviews">
  <div class="container">
{sec_head(d['reviews'][0], d['reviews'][1])}
    <div class="hrs-rev-grid">
{chr(10).join(f'      <figure class="hrs-rev reveal"><blockquote>“{q.strip()}”</blockquote><cite><b>{n}</b>{r}</cite></figure>' for q, n, r in revs)}
    </div>
  </div>
</section>

<!-- FAQ -->
<section id="lp-faq">
  <div class="container">
{sec_head(fe, ft)}
    <div class="hrs-faq">
{chr(10).join(acc(q, a) for q, a in faqs)}
    </div>
  </div>
</section>

<!-- READ -->
<section id="lp-read">
  <div class="container">
{sec_head(re_, rt)}
    <ul class="rl-list reveal">
{chr(10).join(f'      <li><a href="{u}"><b>{t}</b><span>{s}</span></a></li>' for u, t, s in reads)}
    </ul>
  </div>
</section>
"""

    # ---------- contact / footer / scripts из оболочки ----------
    tail = src[src.index('<section id="contact">'):src.index('<script src="https://cdn.jsdelivr.net/npm/lottie-web')]
    sel = re.search(r'<select id="service">.*?</select>', tail, re.S).group(0)
    first = re.search(r"<option value=\"\">.*?</option>", sel).group(0)
    tail = tail.replace(sel, '<select id="service">\n          ' + first + "\n" +
                        "\n".join(f"          <option>{o}</option>" for o in d["options"]) + "\n        </select>")
    scripts = src[src.index("<script>\n  try{"):]
    scripts = re.sub(r"<script>\n  try\{.*?\}catch\(e\)\{ console.error\('Lottie init error:', e\); \}\n", "<script>\n", scripts, count=1, flags=re.S)
    assert "Lottie init error" not in scripts and "—" not in main + head

    out = head + "<body>\n\n" + nav + "\n" + main + "\n" + tail + scripts
    open(d["file"], "w", encoding="utf-8").write(out)
    print("ok", d["file"], len(out))


def main():
    for d in PAGES:
        build(d)


if __name__ == "__main__":
    main()
