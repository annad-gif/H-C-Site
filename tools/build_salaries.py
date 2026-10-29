"""Калькулятор зарплат в IT: analytics-salaries.html, analytics-salaries-en.html, analytics-salaries-uz.html.

Оболочка (head, меню, подвал, кнопка «Связаться») – из resources*.html через tools/build_analytics.py (shell).
Данные – /api/salaries (api/salaries.js → функция public_salary_stats() в базе ATS): агрегаты последнего успешного
прогона, срезы меньше 30 наблюдений не приходят. Форма «Получить расчёт» – #contactForm, её подхватывает hc-crm.js
(согласие, honeypot, submit_lead в Staffly с источником «Сайт: /analytics-salaries…»).

Запускать после правок меню/подвала в resources*.html или текстов ниже:
    python3 tools/build_salaries.py
"""
import json
import os

from build_analytics import ROOT, shell

FILES = {"ru": "analytics-salaries.html", "en": "analytics-salaries-en.html", "uz": "analytics-salaries-uz.html"}
HUB = {"ru": "analytics.html", "en": "analytics-en.html", "uz": "analytics-uz.html"}
ARTICLE = "/articles/zarplaty-v-it-v-uzbekistane-osen-2026-ed99d01e"  # обзор осени 2026, есть только на русском

GROUPS = {  # порядок в списке; ключи – grp в hh_resume_stats
    "it_core": ("Все IT-направления", "All IT roles", "Barcha IT yo‘nalishlari"),
    "dev": ("Разработка", "Software development", "Dasturlash"),
    "it_lead": ("Руководители IT: тимлиды, CTO, CIO", "IT leadership: team leads, CTO, CIO", "IT rahbarlari: timlidlar, CTO, CIO"),
    "product": ("Продакт-менеджмент", "Product management", "Mahsulot menejmenti"),
    "ba_sa": ("Бизнес- и системный анализ", "Business and systems analysis", "Biznes va tizim tahlili"),
    "data": ("Данные и аналитика: BI, Data Science", "Data and analytics: BI, data science", "Ma’lumotlar va tahlil: BI, Data Science"),
    "devops": ("DevOps", "DevOps", "DevOps"),
    "qa": ("Тестирование (QA)", "QA and testing", "Testlash (QA)"),
    "security": ("Информационная безопасность", "Information security", "Axborot xavfsizligi"),
    "infra": ("Системное администрирование и сети", "System administration and networks", "Tizim ma’muriyati va tarmoqlar"),
    "support": ("Техническая поддержка", "Technical support", "Texnik yordam"),
}
EXP = {  # корзины стажа в hh_resume_stats: «1-2» – от 1 года до 3 лет, «3-5» – от 3 до 6 лет
    "all": ("Любой", "Any", "Har qanday"),
    "0": ("Без опыта", "No experience", "Tajribasiz"),
    "1-2": ("1–3 года", "1–3 years", "1–3 yil"),
    "3-5": ("3–6 лет", "3–6 years", "3–6 yil"),
    "6+": ("6+ лет", "6+ years", "6+ yil"),
}
LI = {"ru": 0, "en": 1, "uz": 2}

T = {
    "ru": dict(
        title="Зарплаты в IT в Узбекистане: калькулятор – Human and Capital",
        desc="Сколько просят IT-специалисты в Узбекистане: медиана, вилка и верхние 10% зарплатных ожиданий по направлению и опыту. Обновляется 1-го и 15-го числа.",
        back="Аналитика", eyebrow="Инструмент · обновляется 1-го и 15-го числа",
        h1="Сколько просят IT-специалисты в Узбекистане",
        lead="Выберите направление и опыт – покажем медиану, рабочую вилку и верхние 10% зарплатных ожиданий кандидатов, а где хватает данных – вилки в открытых вакансиях.",
        l_grp="Направление", l_exp="Опыт", l_cur="Показывать в", c_uzs="Сумах", c_usd="Долларах",
        few="Мало данных: меньше 30 резюме",
        r_title="{grp} · опыт: {exp} · медиана ожиданий, на руки в месяц",
        k_iqr="рабочая вилка (25–75% резюме)", k_top="просят верхние 10%", k_usd="указывают сумму в долларах",
        k_n="резюме в срезе, {t}% – Ташкент", from_="от {v}",
        leg_iqr="25–75%", leg_top="75–90%", leg_med="медиана",
        ladder="По опыту: вилка 25–75% и медиана", ladder_na="мало данных",
        vac_h="Что предлагают работодатели",
        vac_p="Типичная вилка в открытых вакансиях – {f} – {t} на руки: медианы нижней и верхней границ, {n} вакансий с указанной зарплатой.",
        vac_none="В этом срезе меньше 30 открытых вакансий с указанной зарплатой – вилки не показываем. Есть данные для:",
        exec_h="Executive search",
        exec_p="По проектам Human and Capital: руководители IT-направлений и C-level с опытом 6+ лет – $4 000–10 000 на руки.",
        loading="Загружаем расчёт…", error="Не удалось загрузить данные. Обновите страницу чуть позже.",
        lead_h="Нужна вилка под конкретную позицию?",
        lead_p="Учтём отрасль, стек, формат работы и уровень позиции и подскажем, какую вилку закладывать в оффер.",
        f_name="Имя", f_company="Компания", f_pos="Позиция, которую нужно рассчитать", f_pos_ph="Например: Senior Java-разработчик, финтех, офис в Ташкенте",
        f_phone="Телефон или Telegram", f_email="Email", f_send="Получить расчёт",
        art="Подробный обзор: «Зарплаты в IT в Узбекистане: осень 2026» →",
        note=("<b>Методология.</b> Ожидания кандидатов – из резюме, доступных агентству как работодателю на job-сайтах "
              "Узбекистана: IT-резюме с указанной зарплатой, обновлённые за последние 90 дней ({total} резюме). "
              "Суммы – «на руки» в месяц; зарплаты в долларах и других валютах пересчитаны по курсу на дату расчёта "
              "({rate} сум за $1). Показаны медиана и квантили, а не средние; срезы, где меньше 30 резюме, скрыты. "
              "Вилки в вакансиях – медианы нижней и верхней границ в открытых вакансиях с указанной зарплатой на {vdate}; "
              "суммы «до вычета налога» пересчитаны в «на руки» (−12%). Расчёт от {date}, обновляется 1-го и 15-го числа. "
              "Для сравнения: средняя начисленная зарплата в программировании по данным Нацкомстата за январь–сентябрь "
              "2026 года – 22,3 млн сум до вычета налога."),
        uzs="{v} млн сум", locale="ru-RU"),
    "en": dict(
        title="IT Salaries in Uzbekistan: Salary Calculator – Human and Capital",
        desc="How much IT specialists in Uzbekistan ask for: median, range and top 10% of salary expectations by role and experience. Updated on the 1st and 15th of each month.",
        back="Insights", eyebrow="Tool · updated on the 1st and 15th",
        h1="What IT specialists in Uzbekistan ask for",
        lead="Pick a role group and experience to see the median, the typical range and the top 10% of candidates’ salary expectations – and, where there is enough data, the ranges in open vacancies.",
        l_grp="Role group", l_exp="Experience", l_cur="Show in", c_uzs="UZS", c_usd="USD",
        few="Not enough data: fewer than 30 CVs",
        r_title="{grp} · experience: {exp} · median expectation, net per month",
        k_iqr="typical range (25–75% of CVs)", k_top="top 10% ask for", k_usd="state their salary in USD",
        k_n="CVs in this slice, {t}% in Tashkent", from_="{v}+",
        leg_iqr="25–75%", leg_top="75–90%", leg_med="median",
        ladder="By experience: 25–75% range and median", ladder_na="not enough data",
        vac_h="What employers offer",
        vac_p="Typical range in open vacancies: {f} – {t} net (medians of the lower and upper bounds, {n} vacancies with a stated salary).",
        vac_none="Fewer than 30 open vacancies with a stated salary in this slice, so we do not show ranges. Data is available for:",
        exec_h="Executive search",
        exec_p="Human and Capital projects: heads of IT and C-level executives with 6+ years of experience – $4,000–10,000 net.",
        loading="Loading…", error="Could not load the data. Please refresh the page a bit later.",
        lead_h="Need a range for a specific role?",
        lead_p="We will factor in the industry, tech stack, work format and seniority and suggest the range to put in your offer.",
        f_name="Name", f_company="Company", f_pos="Role to benchmark", f_pos_ph="E.g. Senior Java developer, fintech, office in Tashkent",
        f_phone="Phone or Telegram", f_email="Email", f_send="Get a benchmark",
        art="Full review (in Russian): “IT salaries in Uzbekistan: autumn 2026” →",
        note=("<b>Methodology.</b> Candidates’ expectations come from CVs available to the agency as an employer on job "
              "sites in Uzbekistan: IT CVs with a stated salary updated within the last 90 days ({total} CVs). Amounts are "
              "net per month; salaries in USD and other currencies are converted at the rate on the calculation date "
              "(UZS {rate} per $1). We show the median and quantiles, not averages; slices with fewer than 30 CVs are hidden. "
              "Vacancy ranges are medians of the lower and upper bounds in open vacancies with a stated salary as of {vdate}; "
              "gross amounts are converted to net (−12%). Calculated on {date}, updated on the 1st and 15th of each month. "
              "For reference: the average accrued salary in programming according to the Statistics Agency for "
              "January–September 2026 is UZS 22.3m before tax."),
        uzs="UZS {v}m", locale="en-GB"),
    "uz": dict(
        title="O‘zbekistonda IT maoshlari: kalkulyator – Human and Capital",
        desc="O‘zbekistonda IT mutaxassislari qancha maosh so‘raydi: yo‘nalish va tajriba bo‘yicha mediana, oraliq va eng yuqori 10%. Har oyning 1 va 15-sanasida yangilanadi.",
        back="Tahlil", eyebrow="Vosita · har oyning 1 va 15-sanasida yangilanadi",
        h1="O‘zbekistonda IT mutaxassislari qancha so‘raydi",
        lead="Yo‘nalish va tajribani tanlang – nomzodlar maosh kutilmalarining medianasi, ishchi oralig‘i va eng yuqori 10% ko‘rsatiladi, ma’lumot yetarli bo‘lsa – ochiq vakansiyalardagi oraliqlar ham.",
        l_grp="Yo‘nalish", l_exp="Tajriba", l_cur="Valyuta", c_uzs="So‘m", c_usd="Dollar",
        few="Ma’lumot kam: 30 tadan kam rezyume",
        r_title="{grp} · tajriba: {exp} · kutilma medianasi, qo‘lga oylik",
        k_iqr="ishchi oraliq (rezyumelarning 25–75%)", k_top="eng yuqori 10% so‘raydi", k_usd="maoshni dollarda ko‘rsatgan",
        k_n="kesimdagi rezyumelar, {t}% – Toshkent", from_="{v} dan",
        leg_iqr="25–75%", leg_top="75–90%", leg_med="mediana",
        ladder="Tajriba bo‘yicha: 25–75% oraliq va mediana", ladder_na="ma’lumot kam",
        vac_h="Ish beruvchilar nima taklif qiladi",
        vac_p="Ochiq vakansiyalardagi odatiy oraliq: qo‘lga {f} – {t} (quyi va yuqori chegaralar medianasi, maosh ko‘rsatilgan {n} ta vakansiya).",
        vac_none="Bu kesimda maosh ko‘rsatilgan ochiq vakansiyalar 30 tadan kam, oraliqlarni ko‘rsatmaymiz. Ma’lumot bor:",
        exec_h="Executive search",
        exec_p="Human and Capital loyihalari bo‘yicha: 6+ yil tajribali IT yo‘nalishi rahbarlari va C-level – qo‘lga $4 000–10 000.",
        loading="Yuklanmoqda…", error="Ma’lumotlarni yuklab bo‘lmadi. Sahifani birozdan keyin yangilang.",
        lead_h="Aniq lavozim uchun oraliq kerakmi?",
        lead_p="Soha, texnologiyalar, ish formati va lavozim darajasini hisobga olib, offerga qanday oraliq qo‘yishni maslahat beramiz.",
        f_name="Ism", f_company="Kompaniya", f_pos="Hisoblash kerak bo‘lgan lavozim", f_pos_ph="Masalan: Senior Java dasturchi, fintex, Toshkentdagi ofis",
        f_phone="Telefon yoki Telegram", f_email="Email", f_send="Hisob-kitob olish",
        art="Batafsil sharh (rus tilida): «O‘zbekistonda IT maoshlari: kuz 2026» →",
        note=("<b>Metodologiya.</b> Nomzodlar kutilmalari – agentlikka ish beruvchi sifatida O‘zbekiston job-saytlarida "
              "mavjud rezyumelardan: so‘nggi 90 kunda yangilangan, maosh ko‘rsatilgan IT rezyumelar ({total} ta). "
              "Summalar – oyiga qo‘lga; dollar va boshqa valyutadagi maoshlar hisob-kitob sanasidagi kurs bo‘yicha "
              "qayta hisoblangan ($1 uchun {rate} so‘m). O‘rtacha emas, mediana va kvantillar ko‘rsatilgan; 30 tadan kam "
              "rezyumeli kesimlar yashirilgan. Vakansiyalardagi oraliqlar – {vdate} holatiga maosh ko‘rsatilgan ochiq "
              "vakansiyalardagi quyi va yuqori chegaralar medianasi; soliq chegirilgunga qadar summalar qo‘lga hisoblangan "
              "(−12%). Hisob-kitob sanasi – {date}, har oyning 1 va 15-sanasida yangilanadi. Taqqoslash uchun: Statistika "
              "agentligi ma’lumotlariga ko‘ra, 2026-yil yanvar–sentabrda dasturlashda o‘rtacha hisoblangan maosh – "
              "soliqqa qadar 22,3 mln so‘m."),
        uzs="{v} mln so‘m", locale="ru-RU"),
}

CSS = """
/* ---------- калькулятор зарплат (tools/build_salaries.py) ---------- */
.sl-hero{padding:132px 0 52px;background:var(--black);}
.sl-back{display:inline-flex;gap:6px;color:var(--grey-300);font-size:14px;text-decoration:none;margin-bottom:18px;}
.sl-back:hover{color:var(--mustard-light);}
.sl-hero h1{font-family:var(--ff-display);font-weight:700;color:var(--white);font-size:clamp(28px,4.4vw,52px);line-height:1.08;margin:0 0 16px;max-width:860px;}
.sl-hero .lead{color:var(--grey-300);font-size:17px;line-height:1.6;max-width:720px;}
#sl-tool{background:var(--grey-50);padding:40px 0 90px;}
.sl-panel{display:grid;grid-template-columns:300px minmax(0,1fr);gap:24px;align-items:start;}
.sl-ctl{background:var(--white);border:1px solid var(--grey-100);border-radius:18px;padding:20px;position:sticky;top:96px;}
.sl-lbl{display:block;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--grey-500);margin:0 0 8px;}
.sl-field{margin-bottom:20px;}.sl-field:last-child{margin-bottom:0;}
.sl-ctl select{width:100%;padding:11px 12px;border-radius:10px;border:1px solid var(--grey-100);background:var(--white);font:inherit;font-size:14.5px;color:var(--black);cursor:pointer;}
.sl-seg{display:flex;flex-wrap:wrap;gap:6px;}
.sl-seg button{padding:8px 13px;border-radius:999px;border:1px solid var(--grey-100);background:var(--white);color:var(--grey-700);font:inherit;font-size:13.5px;cursor:pointer;transition:all .2s;}
.sl-seg button:hover:not(:disabled){border-color:var(--mustard);color:var(--black);}
.sl-seg button[aria-pressed="true"]{background:var(--black);border-color:var(--black);color:var(--white);font-weight:600;}
.sl-seg button:disabled{opacity:.45;cursor:not-allowed;text-decoration:line-through;}
.sl-card{background:var(--white);border:1px solid var(--grey-100);border-radius:18px;padding:26px 28px;min-height:420px;}
.sl-ttl{font-size:14px;color:var(--grey-700);margin-bottom:6px;}
.sl-big{font-family:var(--ff-display);font-weight:700;font-size:clamp(30px,4.6vw,48px);line-height:1.08;}
.sl-alt{color:var(--mustard-dim);font-weight:600;margin-top:6px;}
.sl-bar{position:relative;height:14px;background:var(--grey-100);border-radius:7px;margin:26px 0 8px;}
.sl-bar .iqr{position:absolute;top:0;bottom:0;background:var(--mustard);border-radius:7px;}
.sl-bar .top{position:absolute;top:0;bottom:0;background:var(--mustard-light);opacity:.45;border-radius:0 7px 7px 0;}
.sl-bar .med{position:absolute;top:-6px;bottom:-6px;width:3px;margin-left:-1px;background:var(--black);border-radius:2px;}
.sl-scale{display:flex;justify-content:space-between;gap:12px;font-size:12.5px;color:var(--grey-500);flex-wrap:wrap;}
.sl-leg{display:flex;gap:14px;flex-wrap:wrap;}
.sl-leg i{display:inline-block;width:12px;height:8px;border-radius:3px;margin-right:5px;vertical-align:middle;}
.sl-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:22px;}
.sl-kpi{border-top:2px solid var(--black);padding-top:9px;}
.sl-kpi b{display:block;font-family:var(--ff-display);font-weight:600;font-size:17px;line-height:1.3;}
.sl-kpi span{font-size:13px;color:var(--grey-700);line-height:1.4;display:block;margin-top:3px;}
.sl-ladder{margin-top:26px;}
.sl-row{display:grid;grid-template-columns:110px minmax(0,1fr) 110px;gap:12px;align-items:center;padding:8px 6px;border-top:1px solid var(--grey-100);font-size:14px;width:100%;background:none;border-left:0;border-right:0;border-bottom:0;font-family:inherit;color:inherit;text-align:left;cursor:pointer;border-radius:6px;}
.sl-row:hover{background:var(--grey-50);}
.sl-row.on{font-weight:600;}
.sl-row.na{color:var(--grey-500);cursor:default;}
.sl-row.na:hover{background:none;}
.sl-mini{position:relative;height:8px;background:var(--grey-100);border-radius:4px;}
.sl-mini i{position:absolute;top:0;bottom:0;background:var(--mustard);border-radius:4px;}
.sl-mini em{position:absolute;top:-3px;bottom:-3px;width:2px;margin-left:-1px;background:var(--black);}
.sl-row .v{text-align:right;white-space:nowrap;}
.sl-box{margin-top:16px;background:var(--white);border:1px dashed var(--mustard);border-radius:16px;padding:18px 20px;font-size:14.5px;line-height:1.55;color:var(--grey-700);}
.sl-box h3{font-family:var(--ff-display);font-weight:600;font-size:15px;color:var(--black);margin-bottom:6px;}
.sl-box[hidden]{display:none;}
.sl-box.exec{border-style:solid;border-color:var(--black);}
.sl-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
.sl-links button{padding:7px 12px;border-radius:999px;border:1px solid var(--grey-100);background:var(--grey-50);font:inherit;font-size:13px;cursor:pointer;}
.sl-links button:hover{border-color:var(--mustard);}
.sl-skel{height:360px;border-radius:12px;background:linear-gradient(90deg,#efefed,#f7f7f5,#efefed);background-size:200% 100%;animation:slSk 1.4s infinite;}
@keyframes slSk{to{background-position:-200% 0;}}
.sl-err{padding:40px 10px;text-align:center;color:var(--grey-700);}
.sl-lead{margin-top:44px;padding:34px;border-radius:20px;background:var(--black);color:var(--white);display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:28px;align-items:start;}
.sl-lead h2{font-family:var(--ff-display);font-weight:600;font-size:24px;line-height:1.3;margin-bottom:10px;}
.sl-lead p{color:var(--grey-300);font-size:15px;line-height:1.55;}
.sl-form{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.sl-form label{display:flex;flex-direction:column;gap:6px;font-size:13px;color:var(--grey-300);}
.sl-form .wide{grid-column:1/-1;}
.sl-form input{padding:12px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.18);background:var(--black-soft);color:var(--white);font:inherit;font-size:14.5px;}
.sl-form input:focus{outline:none;border-color:var(--mustard);}
.sl-form .hc-consent{grid-column:1/-1;flex-direction:row!important;color:var(--grey-300)!important;margin:2px 0!important;}
.sl-form .hc-consent a{color:var(--mustard-light)!important;}
.sl-form button[type=submit]{grid-column:1/-1;justify-self:start;padding:14px 24px;border-radius:12px;border:0;background:var(--mustard);color:var(--black);font:inherit;font-weight:600;cursor:pointer;}
.sl-form button[type=submit]:hover{background:var(--mustard-light);}
.sl-art{display:inline-block;margin-top:26px;color:var(--black);font-weight:600;text-decoration:none;border-bottom:2px solid var(--mustard);}
.sl-art:hover{color:var(--mustard-dim);}
.sl-note{margin-top:22px;font-size:13px;line-height:1.6;color:var(--grey-700);max-width:900px;}
@media (max-width:900px){ .sl-panel{grid-template-columns:1fr;} .sl-ctl{position:static;} .sl-lead{grid-template-columns:1fr;} }
@media (max-width:640px){
  .sl-hero{padding:110px 0 40px;} .sl-card{padding:20px 18px;min-height:0;} .sl-kpis{grid-template-columns:1fr 1fr;}
  .sl-row{grid-template-columns:84px minmax(0,1fr) 92px;gap:8px;font-size:13px;padding:8px 2px;}
  .sl-lead{padding:24px 20px;} .sl-form{grid-template-columns:1fr;}
}
"""

MAIN = """
<section class="sl-hero" id="home">
  <div class="container">
    <a class="sl-back" href="{hub}">← {back}</a>
    <p class="rs-count"><span class="dot"></span><span>{eyebrow}</span></p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>

<section id="sl-tool">
  <div class="container">
    <div class="sl-panel">
      <aside class="sl-ctl">
        <div class="sl-field"><label class="sl-lbl" for="slGrp">{l_grp}</label><select id="slGrp"></select></div>
        <div class="sl-field"><span class="sl-lbl">{l_exp}</span><div class="sl-seg" id="slExp"></div></div>
        <div class="sl-field"><span class="sl-lbl">{l_cur}</span><div class="sl-seg" id="slCur"></div></div>
      </aside>
      <div>
        <div class="sl-card" id="slRes" aria-live="polite"><div class="sl-skel"></div></div>
        <div class="sl-box" id="slVac" hidden></div>
        <div class="sl-box exec" id="slExec" hidden><h3>{exec_h}</h3>{exec_p}</div>
      </div>
    </div>

    <div class="sl-lead" id="lead">
      <div><h2>{lead_h}</h2><p>{lead_p}</p></div>
      <form class="sl-form" id="contactForm" novalidate>
        <label>{f_name}<input id="name" name="name" autocomplete="name" required></label>
        <label>{f_company}<input id="company" name="company" autocomplete="organization"></label>
        <label class="wide">{f_pos}<input id="slPos" placeholder="{f_pos_ph}"></label>
        <label>{f_phone}<input id="phone" name="phone" type="tel" autocomplete="tel"></label>
        <label>{f_email}<input id="email" name="email" type="email" autocomplete="email"></label>
        <textarea id="message" hidden></textarea>
        <button type="submit">{f_send}</button>
      </form>
    </div>

    <a class="sl-art" href="{article}">{art}</a>
    <p class="sl-note" id="slNote"></p>
  </div>
</section>
"""

JS = r"""
const PAGE_LANG = %(lang)s;
const T = %(t)s;
const GROUPS = %(groups)s;
const EXP = %(exp)s;
const EXP_ORDER = ['all','0','1-2','3-5','6+']; // ключ «0» в объекте JS всегда идёт первым – порядок задаём явно
// для заявки в CRM – по-русски, независимо от языка страницы
const GROUPS_RU = %(groups_ru)s, EXP_RU = %(exp_ru)s;
const UZ_MONTHS=['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentabr','oktabr','noyabr','dekabr'];
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function fmtDate(iso){ const [y,m,d]=String(iso||'').slice(0,10).split('-').map(Number); if(!y) return '';
  if(PAGE_LANG==='uz') return d+'-'+UZ_MONTHS[m-1]+', '+y;
  try{ return new Intl.DateTimeFormat(T.locale,{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(Date.UTC(y,m-1,d))).replace(/\s*г\.$/,''); }catch(e){ return iso; } }

const grpSel=document.getElementById('slGrp'), expEl=document.getElementById('slExp'), curEl=document.getElementById('slCur'),
  resEl=document.getElementById('slRes'), vacEl=document.getElementById('slVac'), execEl=document.getElementById('slExec'),
  noteEl=document.getElementById('slNote');
let DATA=null, R={}, V={}, s={g:'it_core', e:'all', c:'uzs'};

const num=(v,d)=>new Intl.NumberFormat(PAGE_LANG==='en'?'en-GB':'ru-RU',{maximumFractionDigits:d}).format(v);
const uzs=v=>T.uzs.replace('{v}', num(v/1e6, v>=1e8?0:1));
const usd=v=>'$'+num(Math.round(v/DATA.usd_rate/50)*50, 0);
const f=v=>s.c==='usd'?usd(v):uzs(v), alt=v=>'≈ '+(s.c==='usd'?uzs(v):usd(v));
const row=(g,e)=>R[g+'|'+e];

function seg(el, items, key){
  el.innerHTML=items.map(([k,t])=>{ const off=key==='e'&&!row(s.g,k);
    return '<button type="button" data-k="'+k+'" aria-pressed="'+(s[key]===k)+'"'+(off?' disabled title="'+esc(T.few)+'"':'')+'>'+esc(t)+'</button>'; }).join('');
}

function render(){
  grpSel.value=s.g;
  seg(expEl, EXP_ORDER.map(k=>[k,EXP[k]]), 'e');
  seg(curEl, [['uzs',T.c_uzs],['usd',T.c_usd]], 'c');
  const x=row(s.g,s.e); if(!x) return;
  const vis=EXP_ORDER.map(e=>row(s.g,e)).filter(Boolean);
  const max=Math.max(...vis.map(r=>r.p90))*1.05, pc=v=>(Math.min(v/max,1)*100).toFixed(2)+'%%';
  const span=(a,b)=>'left:'+pc(a)+';width:calc('+pc(b)+' - '+pc(a)+')';
  resEl.innerHTML='<p class="sl-ttl">'+esc(T.r_title.replace('{grp}',GROUPS[s.g]).replace('{exp}',EXP[s.e].toLowerCase()))+'</p>'
    +'<div class="sl-big">'+f(x.p50)+'</div><div class="sl-alt">'+alt(x.p50)+'</div>'
    +'<div class="sl-bar" role="img" aria-label="'+esc(f(x.p25)+' – '+f(x.p75)+', '+T.leg_med+' '+f(x.p50))+'"><div class="iqr" style="'+span(x.p25,x.p75)+'"></div>'
    +'<div class="top" style="'+span(x.p75,x.p90)+'"></div><div class="med" style="left:'+pc(x.p50)+'"></div></div>'
    +'<div class="sl-scale"><span class="sl-leg"><span><i style="background:var(--mustard)"></i>'+esc(T.leg_iqr)+'</span>'
    +'<span><i style="background:var(--mustard-light);opacity:.6"></i>'+esc(T.leg_top)+'</span>'
    +'<span><i style="background:var(--black);width:3px"></i>'+esc(T.leg_med)+'</span></span><span>0 – '+f(max)+'</span></div>'
    +'<div class="sl-kpis">'
    +'<div class="sl-kpi"><b>'+f(x.p25)+' – '+f(x.p75)+'</b><span>'+esc(T.k_iqr)+'</span></div>'
    +'<div class="sl-kpi"><b>'+esc(T.from_.replace('{v}',f(x.p90)))+'</b><span>'+esc(T.k_top)+'</span></div>'
    +'<div class="sl-kpi"><b>'+Math.round(x.n_usd/x.n*100)+'%%</b><span>'+esc(T.k_usd)+'</span></div>'
    +'<div class="sl-kpi"><b>'+num(x.n,0)+'</b><span>'+esc(T.k_n.replace('{t}',Math.round(x.n_tashkent/x.n*100)))+'</span></div></div>'
    +'<div class="sl-ladder"><span class="sl-lbl">'+esc(T.ladder)+'</span>'
    +EXP_ORDER.filter(e=>e!=='all').map(e=>{ const r=row(s.g,e);
      if(!r) return '<div class="sl-row na"><span>'+esc(EXP[e])+'</span><span>'+esc(T.ladder_na)+'</span><span class="v">n &lt; 30</span></div>';
      return '<button type="button" class="sl-row'+(e===s.e?' on':'')+'" data-e="'+e+'"><span>'+esc(EXP[e])+'</span>'
        +'<span class="sl-mini"><i style="'+span(r.p25,r.p75)+'"></i><em style="left:'+pc(r.p50)+'"></em></span><span class="v">'+f(r.p50)+'</span></button>'; }).join('')
    +'</div>';

  const v=V[s.g+'|'+s.e];
  if(v){ vacEl.innerHTML='<h3>'+esc(T.vac_h)+'</h3>'+esc(T.vac_p.replace('{f}',f(v.from_p50)).replace('{t}',f(v.to_p50)).replace('{n}',num(v.n,0))); }
  else { vacEl.innerHTML='<h3>'+esc(T.vac_h)+'</h3>'+esc(T.vac_none)+'<div class="sl-links">'
    +vacAlt().map(r=>'<button type="button" data-g="'+r.grp+'" data-e="'+r.exp+'">'+esc(GROUPS[r.grp]+' · '+EXP[r.exp].toLowerCase())+'</button>').join('')+'</div>'; }
  vacEl.hidden=!DATA.vacancies.length;
  execEl.hidden=!(s.g==='it_lead'&&(s.e==='6+'||s.e==='all'));

  const q=new URLSearchParams(); if(s.g!=='it_core')q.set('g',s.g); if(s.e!=='all')q.set('e',s.e); if(s.c!=='uzs')q.set('c',s.c);
  history.replaceState(null,'',location.pathname+(q.toString()?'?'+q:'')+location.hash);
  syncLead();
}

// куда перейти, если в срезе нет вилок: другой опыт той же группы, иначе группы с вилками при любом опыте
function vacAlt(){ const same=DATA.vacancies.filter(r=>r.grp===s.g&&r.exp!==s.e);
  return same.length?same:DATA.vacancies.filter(r=>r.exp==='all'); }
function set(g,e){ s.g=g; s.e=row(g,e)?e:'all'; render(); }
grpSel.addEventListener('change',()=>set(grpSel.value,s.e));
expEl.addEventListener('click',e=>{ const b=e.target.closest('button[data-k]'); if(b&&!b.disabled){ s.e=b.dataset.k; render(); } });
curEl.addEventListener('click',e=>{ const b=e.target.closest('button[data-k]'); if(b){ s.c=b.dataset.k; render(); } });
resEl.addEventListener('click',e=>{ const b=e.target.closest('button[data-e]'); if(b){ s.e=b.dataset.e; render(); } });
vacEl.addEventListener('click',e=>{ const b=e.target.closest('button[data-g]'); if(b) set(b.dataset.g,b.dataset.e); });

// контекст расчёта – в скрытое поле «message» формы заявки (её отправляет hc-crm.js)
const posEl=document.getElementById('slPos'), msgEl=document.getElementById('message');
function syncLead(){
  const x=DATA&&row(s.g,s.e);
  msgEl.value='Калькулятор зарплат IT: '+GROUPS_RU[s.g]+', опыт: '+EXP_RU[s.e].toLowerCase()+(x?', медиана ожиданий '+(x.p50/1e6).toFixed(1).replace('.',',')+' млн сум':'')
    +'\nПозиция: '+(posEl.value.trim()||'—')+'\nЯзык страницы: '+PAGE_LANG;
}
posEl.addEventListener('input',syncLead);
document.getElementById('contactForm').addEventListener('reset',()=>setTimeout(syncLead,0));

(async function init(){
  const p=new URLSearchParams(location.search);
  try{
    const r=await fetch('/api/salaries'); if(!r.ok) throw new Error('salaries '+r.status);
    DATA=await r.json();
    for(const x of DATA.resumes) R[x.grp+'|'+x.exp]=x;
    for(const x of DATA.vacancies) V[x.grp+'|'+x.exp]=x;
  }catch(e){ console.error('salaries',e); resEl.innerHTML='<p class="sl-err">'+esc(T.error)+'</p>'; syncLead(); return; }
  for(const g of Object.keys(GROUPS)) if(row(g,'all')) grpSel.add(new Option(GROUPS[g],g));
  const g=p.get('g'); if(g&&row(g,'all')) s.g=g;
  const e=p.get('e'); if(e&&row(s.g,e)) s.e=e;
  if(p.get('c')==='usd') s.c='usd';
  noteEl.innerHTML=T.note.replace('{total}',num(DATA.resumes_total,0)).replace('{rate}',num(Math.round(DATA.usd_rate),0))
    .replace('{date}',esc(fmtDate(DATA.snapshot_date))).replace('{vdate}',esc(fmtDate(DATA.vacancies_date)));
  render();
})();
"""


def build(lang):
    t = T[lang]
    i = LI[lang]
    head, nav, tail, menu_js = shell(lang, FILES, t["title"], t["desc"])
    head = head.replace("</head>", "<style>" + CSS + "</style>\n</head>")
    main = MAIN.format(hub=HUB[lang], article=ARTICLE, **t)
    t_js = {k: t[k] for k in ("few", "r_title", "k_iqr", "k_top", "k_usd", "k_n", "from_", "leg_iqr", "leg_top", "leg_med",
                              "ladder", "ladder_na", "vac_h", "vac_p", "vac_none", "error", "note", "uzs", "locale",
                              "c_uzs", "c_usd")}
    js = JS % {"lang": json.dumps(lang), "t": json.dumps(t_js, ensure_ascii=False),
               "groups": json.dumps({k: v[i] for k, v in GROUPS.items()}, ensure_ascii=False),
               "exp": json.dumps({k: v[i] for k, v in EXP.items()}, ensure_ascii=False),
               "groups_ru": json.dumps({k: v[0] for k, v in GROUPS.items()}, ensure_ascii=False),
               "exp_ru": json.dumps({k: v[0] for k, v in EXP.items()}, ensure_ascii=False)}
    out = (head.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n<!-- Сгенерировано tools/build_salaries.py – не править вручную -->", 1)
           + "\n<body>\n\n" + nav + "\n" + main + "\n" + tail
           + "\n\n<script>\n" + js.strip() + "\n\n" + menu_js + "\n</script>\n<script src=\"hc-crm.js\" defer></script>\n</body>\n</html>\n")
    open(os.path.join(ROOT, FILES[lang]), "w", encoding="utf-8").write(out)
    return FILES[lang]


if __name__ == "__main__":
    print("ok: " + ", ".join(build(l) for l in FILES))
