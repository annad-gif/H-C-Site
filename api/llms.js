/* /llms.txt, /llms-en.txt, /llms-uz.txt (rewrite в vercel.json): описание сайта для языковых моделей
   по стандарту llmstxt.org. Страницы услуг – отсюда, статьи и аналитика – из админки (site_materials),
   поэтому новая статья попадает в файл сама. Сброс кэша при сохранении – тег «materials», как у sitemap. */
"use strict";

const { SITE, articlePath, loadMaterials, pageUrl } = require("./_lib");

const FILES = { ru: "/llms.txt", en: "/llms-en.txt", uz: "/llms-uz.txt" };

// [RU, EN, UZ] – английские адреса исторические, как в sitemap.js
const P = {
  home: ["index.html", "index-en.html", "index-uz.html"],
  hr: ["hr-services.html", "hr-services-uzbekistan.html", "hr-services-uz.html"],
  rec: ["recruitment.html", "recruitment-en.html", "recruitment-uz.html"],
  exec: ["executive-search.html", "executive-search-en.html", "executive-search-uz.html"],
  out: ["outstaffing.html", "outstaffing-en.html", "outstaffing-uz.html"],
  eor: ["employer-of-record.html", "employer-of-record-uzbekistan.html", "employer-of-record-uz.html"],
  cons: ["consulting.html", "consulting-en.html", "consulting-uz.html"],
  an: ["analytics.html", "analytics-en.html", "analytics-uz.html"],
  sal: ["analytics-salaries.html", "analytics-salaries-en.html", "analytics-salaries-uz.html"],
  vac: ["vacancies.html", "vacancies-en.html", "vacancies-uz.html"],
  res: ["resources.html", "resources-en.html", "resources-uz.html"],
  priv: ["privacy.html", "privacy-en.html", "privacy-uz.html"],
};
const IDX = { ru: 0, en: 1, uz: 2 };

const T = {
  ru: {
    summary: "Human and Capital – рекрутинговое агентство и HR-компания в Ташкенте, Узбекистан. Подбор персонала, IT-рекрутинг, executive search, аутстаффинг, Employer of Record (EOR) и расчёт зарплаты, HR-консалтинг для местных и международных компаний.",
    about: [
      "Ключевые факты:",
      "- Офис: Ташкент, Мирабадский район, улица Фаргона йули, 94. Работаем по всему Узбекистану.",
      "- Больше 5 лет на рынке, 500+ закрытых вакансий, в команде 20+ специалистов.",
      "- Языки работы: русский, английский, узбекский.",
      "- Клиенты: местные компании, BPO и контакт-центры, иностранные компании, которые нанимают в Узбекистане без своего юрлица.",
      "- Стоимость услуг рассчитывается индивидуально под задачу.",
      "- Контакты: +998 90 325 13 36, WhatsApp +998 95 863 11 99, akmal.s@human-capital.org, Telegram https://t.me/Djuanna555, LinkedIn https://www.linkedin.com/company/human-and-capital/",
    ],
    services: "Услуги",
    svc: {
      hr: "обзор всех HR-услуг для местных и международных компаний",
      rec: "подбор специалистов и руководителей, IT-рекрутинг и массовый подбор; гарантия замены, бесплатный пробный день кандидата",
      exec: "прямой поиск топ-менеджеров, руководителей и редких специалистов, конфиденциально",
      out: "оформление сотрудников в штат агентства, расчёт зарплаты и отчётность; команды для BPO и международных компаний",
      eor: "найм в Узбекистане без открытия юрлица: оформление по трудовому законодательству, ежемесячный payroll, налоги и отчётность; payroll отдельно для компаний со своим юрлицом",
      cons: "HR-аудит, обучение и аттестация, адаптация, анализ рынка труда, прескрининг",
    },
    names: { hr: "HR-услуги в Узбекистане", rec: "Подбор персонала", exec: "Executive search", out: "Аутстаффинг", eor: "Employer of Record и payroll", cons: "HR-консалтинг" },
    data: "Аналитика рынка труда и зарплаты",
    an: ["Аналитика рынка труда", "зарплатные обзоры и кейсы на данных наших проектов в Узбекистане"],
    sal: ["Калькулятор зарплат", "медиана, вилка и верхние 10% зарплатных ожиданий в IT, продажах и финансах по опыту"],
    articles: "Статьи",
    jobs: "Для соискателей",
    vac: ["Вакансии", "открытые позиции в Ташкенте и Узбекистане, отклик онлайн"],
    other: "Другие языки",
    opt: "Optional",
    res: ["Все материалы", "статьи, новости, видео и фото"],
    priv: ["Политика конфиденциальности", "обработка персональных данных"],
  },
  en: {
    summary: "Human and Capital is a recruitment agency and HR company in Tashkent, Uzbekistan. Recruitment, IT hiring, executive search, outstaffing, Employer of Record (EOR) and payroll, and HR consulting for local and international companies.",
    about: [
      "Key facts:",
      "- Office: 94 Fargona yuli, Mirabad district, Tashkent. We work across Uzbekistan.",
      "- 5+ years on the market, 500+ positions filled, 20+ specialists on the team.",
      "- Working languages: English, Russian, Uzbek.",
      "- Clients: local companies, BPO and contact centres, foreign companies hiring in Uzbekistan without a local entity.",
      "- Pricing is quoted individually for each project.",
      "- Contacts: +998 90 325 13 36, WhatsApp +998 95 863 11 99, akmal.s@human-capital.org, Telegram https://t.me/Djuanna555, LinkedIn https://www.linkedin.com/company/human-and-capital/",
    ],
    services: "Services",
    svc: {
      hr: "overview of HR services for local and international companies",
      rec: "specialists and managers, IT and mass recruitment; free replacement guarantee and a free trial day for the candidate",
      exec: "confidential direct search for C-level executives, senior managers and rare specialists",
      out: "legal employment of staff on the agency's payroll, salary calculation and reporting; teams for BPO and international companies",
      eor: "hire in Uzbekistan without opening a local entity: employment under Uzbek labour law, monthly payroll, taxes and reporting; standalone payroll for companies with their own entity",
      cons: "HR audit, training and assessment, onboarding, labour market analysis, pre-screening",
    },
    names: { hr: "HR services in Uzbekistan", rec: "Recruitment", exec: "Executive search", out: "Outstaffing", eor: "Employer of Record and payroll", cons: "HR consulting" },
    data: "Labour market data and salaries",
    an: ["Labour market insights", "salary reviews and case studies based on our recruitment data in Uzbekistan"],
    sal: ["Salary calculator", "median, range and top 10% of salary expectations in IT, sales and finance by experience"],
    articles: "Articles",
    jobs: "For candidates",
    vac: ["Jobs", "open positions in Tashkent and Uzbekistan, apply online"],
    other: "Other languages",
    opt: "Optional",
    res: ["All resources", "articles, news, videos and photos"],
    priv: ["Privacy policy", "processing of personal data"],
  },
  uz: {
    summary: "Human and Capital – Toshkentdagi rekruting agentligi va HR kompaniyasi, O‘zbekiston. Xodimlarni tanlash, IT-rekrutment, executive search, autstaffing, Employer of Record (EOR) va ish haqi hisobi, mahalliy va xalqaro kompaniyalar uchun HR-konsalting.",
    about: [
      "Asosiy faktlar:",
      "- Ofis: Toshkent, Mirobod tumani, Farg‘ona yo‘li, 94. Butun O‘zbekiston bo‘ylab ishlaymiz.",
      "- Bozorda 5 yildan ortiq, 500+ yopilgan vakansiya, jamoada 20+ mutaxassis.",
      "- Ish tillari: o‘zbek, rus, ingliz.",
      "- Mijozlar: mahalliy kompaniyalar, BPO va kontakt-markazlar, O‘zbekistonda yuridik shaxssiz xodim yollayotgan xorijiy kompaniyalar.",
      "- Xizmatlar narxi har bir loyiha uchun alohida hisoblanadi.",
      "- Kontaktlar: +998 90 325 13 36, WhatsApp +998 95 863 11 99, akmal.s@human-capital.org, Telegram https://t.me/Djuanna555, LinkedIn https://www.linkedin.com/company/human-and-capital/",
    ],
    services: "Xizmatlar",
    svc: {
      hr: "mahalliy va xalqaro kompaniyalar uchun barcha HR xizmatlari",
      rec: "mutaxassis va rahbarlarni tanlash, IT-rekrutment va ommaviy tanlov; almashtirish kafolati, nomzodning bepul sinov kuni",
      exec: "top-menejerlar, rahbarlar va noyob mutaxassislarni maxfiy to‘g‘ridan-to‘g‘ri qidirish",
      out: "xodimlarni agentlik shtatiga qonuniy rasmiylashtirish, ish haqi hisobi va hisobotlar; BPO va xalqaro kompaniyalar uchun jamoalar",
      eor: "yuridik shaxs ochmasdan O‘zbekistonda xodim yollash: mehnat qonunchiligi bo‘yicha rasmiylashtirish, oylik payroll, soliqlar va hisobotlar; o‘z yuridik shaxsi bor kompaniyalar uchun alohida payroll",
      cons: "HR-audit, o‘qitish va attestatsiya, moslashtirish, mehnat bozori tahlili, preskrining",
    },
    names: { hr: "O‘zbekistonda HR xizmatlari", rec: "Xodimlarni tanlash", exec: "Executive search", out: "Autstaffing", eor: "Employer of Record va payroll", cons: "HR-konsalting" },
    data: "Mehnat bozori tahlili va maoshlar",
    an: ["Mehnat bozori tahlili", "loyihalarimiz ma’lumotlari asosidagi maosh sharhlari va keyslar"],
    sal: ["Maosh kalkulyatori", "IT, savdo va moliyada tajriba bo‘yicha maosh kutilmalarining medianasi, oralig‘i va eng yuqori 10%"],
    articles: "Maqolalar",
    jobs: "Nomzodlar uchun",
    vac: ["Vakansiyalar", "Toshkent va O‘zbekistondagi ochiq lavozimlar, onlayn ariza"],
    other: "Boshqa tillar",
    opt: "Optional",
    res: ["Barcha materiallar", "maqolalar, yangiliklar, video va fotolar"],
    priv: ["Maxfiylik siyosati", "shaxsiy ma’lumotlarni qayta ishlash"],
  },
};
const LANG_NAMES = { ru: "Русский", en: "English", uz: "O‘zbekcha" };

// одна строка без markdown-ломающих символов
function clean(s) { return String(s || "").replace(/\s+/g, " ").replace(/[\[\]]/g, "").trim(); }
function link(name, url, note) { return "- [" + clean(name) + "](" + url + ")" + (note ? ": " + clean(note) : ""); }

function build(lang, materials) {
  const t = T[lang], i = IDX[lang];
  const page = k => pageUrl(P[k][i]);
  const out = ["# Human and Capital", "", "> " + t.summary, "", ...t.about, ""];

  out.push("## " + t.services, "");
  for (const k of ["hr", "rec", "exec", "out", "eor", "cons"]) out.push(link(t.names[k], page(k), t.svc[k]));
  out.push("");

  const mine = (materials || []).filter(m => m.lang === lang && m.cat !== "news");
  const salary = mine.filter(m => m.rubric);
  const other = mine.filter(m => !m.rubric);
  const note = m => m.seo_description || m.description;

  out.push("## " + t.data, "", link(t.an[0], page("an"), t.an[1]), link(t.sal[0], page("sal"), t.sal[1]));
  for (const m of salary) out.push(link(m.title, SITE + articlePath(m), note(m)));
  out.push("");

  if (other.length) {
    out.push("## " + t.articles, "");
    for (const m of other) out.push(link(m.title, SITE + articlePath(m), note(m)));
    out.push("");
  }

  out.push("## " + t.jobs, "", link(t.vac[0], page("vac"), t.vac[1]), "");

  out.push("## " + t.other, "");
  for (const l of ["ru", "en", "uz"]) if (l !== lang) out.push(link(LANG_NAMES[l], SITE + FILES[l]));
  out.push("");

  out.push("## " + t.opt, "", link(t.res[0], page("res"), t.res[1]), link(t.priv[0], page("priv"), t.priv[1]),
    link("Sitemap", SITE + "/sitemap.xml"), "");
  return out.join("\n");
}

module.exports = async function handler(req, res) {
  const lang = T[req.query && req.query.lang] ? req.query.lang : "ru";
  let materials = [], ok = true;
  try {
    materials = await loadMaterials();
  } catch (e) {
    console.error(e);
    ok = false; // без статей, но файл всё равно отдаётся
  }
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", ok ? "public, max-age=0, s-maxage=600, stale-while-revalidate=86400" : "no-store");
  if (ok) res.setHeader("Vercel-Cache-Tag", "materials");
  res.end(build(lang, materials));
};

module.exports.build = build; // для локальной проверки
