/* Страница статьи: /articles/<slug> (rewrite в vercel.json → /api/article?slug=...).
   Отдаёт готовый HTML, чтобы поисковики видели текст статьи без выполнения JS. */
"use strict";

const fs = require("fs");
const path = require("path");
const { SITE, articleSlug, articlePath, loadMaterials, esc } = require("./_lib");
// Рубрики, отрасли и авторы раздела «Аналитика» (site_materials.rubric / industries / author_key)
const TAX = require("./_taxonomy.json");

// Оболочка и подписи на языке статьи (site_materials.lang); оболочки собирает tools/build_article_shell.py
const SHELLS = {
  ru: fs.readFileSync(path.join(__dirname, "_shell.html"), "utf8"),
  en: fs.readFileSync(path.join(__dirname, "_shell-en.html"), "utf8"),
  uz: fs.readFileSync(path.join(__dirname, "_shell-uz.html"), "utf8"),
};
const SHELL = SHELLS.ru;
const L10N = {
  ru: { locale: "ru-RU", og: "ru_RU", home: "Главная", homeUrl: "/", res: "Полезные материалы", resUrl: "/resources.html",
        cat: { article: "Статья", news: "Новость", video: "Видео", photo: "Фото" },
        ctaH: "Нужна помощь с подбором персонала?",
        ctaP: "Human and Capital – рекрутинговое агентство в Узбекистане. Найдём сотрудников под ваши задачи: от массового подбора до executive search.",
        ctaA: "Оставить заявку →", ctaUrl: "/recruitment.html#contact", related: "Читайте также", all: "Все материалы →",
        an: "Аналитика", anUrl: "/analytics.html", anAll: "Вся аналитика →",
        method: "Методология", period: "Период", sample: "Выборка",
        cta: {
          consult: ["Обсудим ваш найм?", "Подберём сотрудников под ваши задачи и поделимся данными рынка по вашей отрасли.", "Обсудить найм →"],
          download: ["Получите обзор по вашей отрасли", "Подготовим срез зарплат и сроков найма по вашей отрасли и позициям.", "Получить обзор →"],
          subscribe: ["Новые обзоры – раз в месяц", "Подпишитесь на канал аналитики Human and Capital в Telegram.", "Подписаться →"] },
        tg: ["Аналитика рынка труда Узбекистана – в нашем Telegram-канале", "Подписаться"],
        rf: { h: "Полная версия отчёта – в PDF", p: "Подробные таблицы по всем срезам и выводы для работодателя. Заполните форму – PDF откроется сразу.",
              name: "Имя", company: "Компания", role: "Должность", email: "Рабочий email", phone: "Телефон",
              opt: "необязательно", phoneHint: "для приглашения на презентацию отчёта", send: "Получить отчёт →",
              done: "Спасибо! Отчёт готов.", doneP: "Ссылка работает и при следующих визитах с этого устройства.", dl: "Скачать PDF" } },
  en: { locale: "en-GB", og: "en_US", home: "Home", homeUrl: "/index-en.html", res: "Resources", resUrl: "/resources-en.html",
        cat: { article: "Article", news: "News", video: "Video", photo: "Photo" },
        ctaH: "Need help hiring in Uzbekistan?",
        ctaP: "Human and Capital is an HR company in Tashkent: recruitment, executive search, outstaffing and HR consulting for local and international companies.",
        ctaA: "Send a request →", ctaUrl: "/hr-services-uzbekistan.html#contact", related: "Read also", all: "All resources →",
        an: "Insights", anUrl: "/analytics-en.html", anAll: "All insights →",
        method: "Methodology", period: "Period", sample: "Sample",
        cta: {
          consult: ["Let’s discuss your hiring", "We will find people for your roles and share market data for your industry.", "Discuss hiring →"],
          download: ["Get a review for your industry", "We will prepare salary and time-to-hire benchmarks for your industry and roles.", "Get the review →"],
          subscribe: ["New reviews every month", "Follow Human and Capital insights on Telegram.", "Subscribe →"] },
        tg: ["Uzbekistan labour market insights – on our Telegram channel", "Subscribe"],
        rf: { h: "Get the full report (PDF)", p: "Detailed tables for every breakdown and takeaways for employers. Fill in the form and the PDF opens right away.",
              name: "Name", company: "Company", role: "Job title", email: "Work email", phone: "Phone",
              opt: "optional", phoneHint: "to invite you to the report presentation", send: "Get the report →",
              done: "Thank you! Your report is ready.", doneP: "The link will also work on your next visits from this device.", dl: "Download PDF" } },
  uz: { locale: "uz-Latn-UZ", og: "uz_UZ", home: "Bosh sahifa", homeUrl: "/index-uz.html", res: "Foydali materiallar", resUrl: "/resources-uz.html",
        cat: { article: "Maqola", news: "Yangilik", video: "Video", photo: "Foto" },
        ctaH: "Xodim tanlashda yordam kerakmi?",
        ctaP: "Human and Capital – O‘zbekistondagi rekruting agentligi. Ommaviy tanlovdan executive searchgacha – vazifangizga mos xodimlarni topamiz.",
        ctaA: "Ariza qoldirish →", ctaUrl: "/recruitment-uz.html#contact", related: "Shuningdek o‘qing", all: "Barcha materiallar →",
        an: "Tahlil", anUrl: "/analytics-uz.html", anAll: "Barcha tahlillar →",
        method: "Metodologiya", period: "Davr", sample: "Tanlov hajmi",
        cta: {
          consult: ["Xodim tanlashni muhokama qilamizmi?", "Vazifalaringizga mos xodimlarni topamiz va sohangiz bo‘yicha bozor ma’lumotlarini ulashamiz.", "Muhokama qilish →"],
          download: ["Sohangiz bo‘yicha sharh oling", "Sohangiz va lavozimlaringiz bo‘yicha maoshlar va yollash muddatlari kesimini tayyorlaymiz.", "Sharhni olish →"],
          subscribe: ["Yangi sharhlar – har oy", "Human and Capital tahlil kanaliga Telegramda obuna bo‘ling.", "Obuna bo‘lish →"] },
        tg: ["O‘zbekiston mehnat bozori tahlili – Telegram kanalimizda", "Obuna bo‘lish"],
        rf: { h: "Hisobotning to‘liq versiyasi – PDF", p: "Barcha kesimlar bo‘yicha batafsil jadvallar va ish beruvchi uchun xulosalar. Formani to‘ldiring – PDF darhol ochiladi.",
              name: "Ism", company: "Kompaniya", role: "Lavozim", email: "Ish email", phone: "Telefon",
              opt: "ixtiyoriy", phoneHint: "hisobot taqdimotiga taklif qilish uchun", send: "Hisobotni olish →",
              done: "Rahmat! Hisobot tayyor.", doneP: "Havola shu qurilmadan keyingi tashriflarda ham ishlaydi.", dl: "PDF yuklab olish" } },
};
function langOf(m) { return L10N[m && m.lang] ? m.lang : "ru"; }
const CAT = L10N.ru.cat;

// --- раздел «Аналитика»: материал с рубрикой (site_materials.rubric) ---
function rubricOf(m) { return m && TAX.rubrics[m.rubric] ? m.rubric : null; }
const TG_URL = safeTg(TAX.telegram);
function safeTg(u) { u = String(u || "").trim(); return /^https:\/\/t\.me\/[A-Za-z0-9_+/-]+$/.test(u) ? u : ""; }

// 3–5 карточек «число + подпись» сразу после лида
function keyFiguresHTML(m) {
  const list = (Array.isArray(m.key_figures) ? m.key_figures : [])
    .filter(f => f && String(f.value || "").trim()).slice(0, 5);
  if (!list.length) return "";
  return '<div class="ar-kf">' + list.map(f => '<div class="ar-kf-item"><b>' + esc(String(f.value).trim()) + "</b>"
    + (f.label ? "<span>" + esc(String(f.label).trim()) + "</span>" : "") + "</div>").join("") + "</div>";
}
function authorOf(m) { return m && TAX.authors[m.author_key] ? TAX.authors[m.author_key] : null; }
function authorHTML(m, lang) {
  const a = authorOf(m);
  if (!a) return "";
  const name = a.name[lang] || a.name.ru, role = a.role[lang] || a.role.ru;
  const ext = /^https?:\/\//.test(a.url) && !a.url.startsWith(SITE);
  return '<a class="ar-author" href="' + esc(a.url) + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">"
    + '<img src="' + esc(a.photo) + '" alt="' + esc(name) + '" width="44" height="44" loading="lazy"/>'
    + "<span><b>" + esc(name) + "</b><i>" + esc(role) + "</i></span></a>";
}
function authorLD(m, lang) {
  const a = authorOf(m);
  if (!a) return { "@type": "Organization", name: "Human and Capital", url: SITE + "/" };
  if (a.type !== "Person") return { "@type": "Organization", name: a.name[lang] || a.name.ru, url: SITE + "/" };
  return { "@type": "Person", name: a.name[lang] || a.name.ru, jobTitle: a.role[lang] || a.role.ru, sameAs: [a.url],
    worksFor: { "@type": "Organization", "@id": SITE + "/#organization", name: "Human and Capital" } };
}
function methodHTML(m, L) {
  const rows = [[L.method, m.methodology], [L.period, m.period], [L.sample, m.sample_size]]
    .filter(r => String(r[1] || "").trim());
  if (!rows.length) return "";
  return '<aside class="ar-method">' + rows.map(r => "<p><b>" + esc(r[0]) + ".</b> " + esc(String(r[1]).trim()) + "</p>").join("") + "</aside>";
}
// Форма скачивания отчёта (ТЗ §4): cta = 'download' и задан gated_pdf_url.
// Отправку, согласие на ПДн, honeypot и показ кнопки «Скачать PDF» делает hc-crm.js (initReport).
function reportPdf(m) { return m && m.cta === "download" ? safeUrl(m.gated_pdf_url) : null; }
function reportHTML(m, L) {
  const R = L.rf, pdf = reportPdf(m);
  // opt – необязательное поле: [пометка, подсказка под полем]
  const field = (id, label, type, auto, opt) => '<label class="ar-rf-f" for="' + id + '"><span>' + esc(label)
    + (opt ? " <i>(" + esc(opt[0]) + ")</i>" : "") + '</span><input id="' + id + '" type="' + type + '" autocomplete="' + auto + '"'
    + (opt ? "" : " required") + ' maxlength="' + (type === "tel" ? 40 : 200) + '"/>' + (opt ? "<small>" + esc(opt[1]) + "</small>" : "") + "</label>";
  return '<aside class="ar-cta ar-report" id="report"><div class="ar-rf-head"><h2>' + esc(R.h) + "</h2><p>" + esc(R.p) + "</p></div>"
    + '<form class="ar-rf" id="hcReportForm" method="post" action="#report" novalidate data-id="' + esc(m.id) + '" data-report="' + esc(m.title)
    + '" data-rubric="' + esc(rubricOf(m) || "") + '" data-pdf="' + esc(pdf) + '"><div class="ar-rf-grid">'
    + field("rfName", R.name, "text", "name") + field("rfCompany", R.company, "text", "organization")
    + field("rfRole", R.role, "text", "organization-title") + field("rfEmail", R.email, "email", "email")
    + field("rfPhone", R.phone, "tel", "tel", [R.opt, R.phoneHint])
    + '</div><button type="submit">' + esc(R.send) + "</button></form>"
    + '<div class="ar-rf-done" hidden><div><b>' + esc(R.done) + "</b><p>" + esc(R.doneP) + "</p></div>"
    + '<a href="' + esc(pdf) + '" target="_blank" rel="noopener">' + esc(R.dl) + "</a></div></aside>"
    + '<script src="/hc-crm.js" defer></script>';
}
// CTA в конце статьи. Обычный материал — как раньше; аналитика — по полю cta.
// download без PDF ведёт на форму заявки.
function ctaHTML(m, L) {
  if (reportPdf(m)) return reportHTML(m, L);
  let h = L.ctaH, p = L.ctaP, a = L.ctaA, url = L.ctaUrl, ext = false;
  if (rubricOf(m)) {
    let kind = L.cta[m.cta] ? m.cta : "consult";
    if (kind === "subscribe" && !TG_URL) kind = "consult";
    [h, p, a] = L.cta[kind];
    if (kind === "subscribe") { url = TG_URL; ext = true; }
  }
  return '<aside class="ar-cta"><div><h2>' + esc(h) + "</h2><p>" + esc(p) + "</p></div>"
    + '<a href="' + esc(url) + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">" + esc(a) + "</a></aside>";
}
function tgHTML(m, L) {
  if (!rubricOf(m) || !TG_URL || m.cta === "subscribe") return "";
  return '<p class="ar-tg"><span>' + esc(L.tg[0]) + '</span><a href="' + esc(TG_URL) + '" target="_blank" rel="noopener">' + esc(L.tg[1]) + "</a></p>";
}

// --- очистка HTML тела статьи (его пишут в админке) ---
const ALLOWED = new Set(["p", "br", "h2", "h3", "h4", "ul", "ol", "li", "blockquote", "b", "strong", "i", "em", "u", "a", "img", "figure", "figcaption"]);
function attr(attrs, name) {
  const m = new RegExp("\\s" + name + "\\s*=\\s*(\"([^\"]*)\"|'([^']*)'|([^\\s>]+))", "i").exec(attrs);
  return m ? (m[2] ?? m[3] ?? m[4] ?? "") : null;
}
function safeUrl(u, allowMail) {
  u = String(u || "").trim().replace(/&amp;/g, "&");
  if (/^https?:\/\//i.test(u) || u.startsWith("/")) return u;
  if (allowMail && /^mailto:/i.test(u)) return u;
  return null;
}
function sanitize(body) {
  let s = String(body || "");
  if (!/[<>]/.test(s)) {
    return s.split(/\n{2,}/).map(p => p.trim()).filter(Boolean)
      .map(p => "<p>" + esc(p).replace(/\n/g, "<br>") + "</p>").join("");
  }
  s = s.replace(/<(script|style|iframe|object|embed|noscript|template)[\s\S]*?<\/\1\s*>/gi, "")
       .replace(/<!--[\s\S]*?-->/g, "");
  return s.replace(/<(\/?)([a-zA-Z0-9]+)([^>]*)>/g, (all, close, tag, attrs) => {
    tag = tag.toLowerCase();
    if (tag === "h1") tag = "h2";
    if (!ALLOWED.has(tag)) return "";
    if (close) return tag === "br" || tag === "img" ? "" : "</" + tag + ">";
    if (tag === "a") {
      const href = safeUrl(attr(attrs, "href"), true);
      if (!href) return "<a>";
      const ext = /^https?:\/\//i.test(href) && !href.startsWith(SITE);
      return '<a href="' + esc(href) + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">";
    }
    if (tag === "img") {
      const src = safeUrl(attr(attrs, "src"));
      if (!src) return "";
      return '<img src="' + esc(src) + '" alt="' + esc(attr(attrs, "alt") || "") + '" loading="lazy"/>';
    }
    return "<" + tag + ">";
  });
}
function plainText(html) {
  return String(html || "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/\s+/g, " ").trim();
}
function clip(s, n) {
  if (s.length <= n) return s;
  const cut = s.slice(0, n - 1);
  return cut.slice(0, cut.lastIndexOf(" ") > n * 0.6 ? cut.lastIndexOf(" ") : cut.length).replace(/[\s,.;:–-]+$/, "") + "…";
}
// «Прескрининг» + «Как мы экономим время…» → «Прескрининг: как мы экономим время…»
function headline(m) {
  const t = String(m.title || "").trim(), d = String(m.description || "").trim();
  if (!d) return t;
  const joined = t.replace(/[.:!?]+$/, "") + ": " + (/^[А-ЯЁA-Z][а-яёa-z]/.test(d) ? d[0].toLowerCase() + d.slice(1) : d);
  return joined.length <= 110 ? joined : t;
}
function ruDate(iso, locale) {
  try { return new Intl.DateTimeFormat(locale || "ru-RU", { day: "numeric", month: "long", year: "numeric", timeZone: "Asia/Tashkent" }).format(new Date(iso)).replace(/\s*г\.$/, ""); }
  catch (e) { return String(iso || "").slice(0, 10); }
}
function mediaHTML(m) {
  const u = String(m.media_url || "");
  if (!u) return "";
  if (m.media_type === "video") {
    const src = /<iframe/i.test(u) ? attr(u, "src") : null;
    if (src && /^https:\/\/(www\.)?(youtube\.com|youtube-nocookie\.com|player\.vimeo\.com)\//i.test(src))
      return '<div class="ar-cover"><iframe src="' + esc(src) + '" allowfullscreen loading="lazy" title="' + esc(m.title) + '"></iframe></div>';
    if (safeUrl(u)) return '<div class="ar-cover"><video src="' + esc(u) + '" controls preload="metadata"></video></div>';
    return "";
  }
  if (!safeUrl(u)) return "";
  return '<div class="ar-cover"><img src="' + esc(u) + '" alt="' + esc(m.title) + '" fetchpriority="high"/></div>';
}
function imageOf(m) { return m.media_type !== "video" && safeUrl(m.media_url) ? m.media_url : null; }

function relatedHTML(all, m) {
  const L = L10N[langOf(m)];
  const i = all.findIndex(x => x.id === m.id);
  const root = m.translation_of || m.id;
  const others = all.slice(i + 1).concat(all.slice(0, i)).filter(x => (x.translation_of || x.id) !== root);
  // сначала материалы на том же языке, внутри – того же типа
  const rub = rubricOf(m);
  const rank = x => (langOf(x) === langOf(m) ? 0 : 4) + (rub ? (rubricOf(x) === rub ? 0 : rubricOf(x) ? 1 : 2) : (x.cat === m.cat ? 0 : 1));
  const pick = others.map((x, k) => [x, k]).sort((a, b) => rank(a[0]) - rank(b[0]) || a[1] - b[1]).map(a => a[0]).slice(0, 3);
  if (!pick.length) return "";
  return '<section class="ar-related"><div class="container"><h2>' + esc(L.related) + '</h2><div class="ar-rel-grid">'
    + pick.map(r => {
      const img = imageOf(r);
      return '<a class="ar-rel" href="' + esc(articlePath(r)) + '"><div class="ar-rel-img">'
        + (img ? '<img src="' + esc(img) + '" alt="' + esc(r.title) + '" loading="lazy"/>' : "")
        + '</div><div class="ar-rel-body"><h3>' + esc(r.title) + "</h3><p>" + esc(r.description || "") + "</p></div></a>";
    }).join("")
    + '</div><a class="ar-all" href="' + (rub ? L.anUrl : L.resUrl) + '">' + esc(rub ? L.anAll : L.all) + '</a></div></section>';
}

// Языковые версии одной статьи: исходник + все материалы с translation_of = его id
function versionsOf(all, m) {
  const root = m.translation_of || m.id;
  const out = {};
  for (const x of all) if ((x.translation_of || x.id) === root && !out[langOf(x)]) out[langOf(x)] = x;
  return out;
}
const LANG_CODE = { ru: "RU", en: "ENG", uz: "UZB" };

function render(head, main, lang, versions, section) {
  let shell = SHELLS[lang] || SHELL;
  if (section === "analytics") {
    // оболочка подсвечивает «Полезные материалы»; у аналитики подсвечиваем «Аналитика»
    shell = shell.replace(/(href="\/resources(?:-en|-uz)?\.html") class="active"/, "$1")
      .replace(/href="(\/analytics(?:-en|-uz)?\.html)">/, 'href="$1" class="active">');
  }
  // переключатель языка ведёт на перевод этой статьи, если он есть
  for (const [hl, v] of Object.entries(versions || {})) {
    shell = shell.replace(new RegExp('<a href="[^"]*" data-lang="' + LANG_CODE[hl] + '">'),
      '<a href="' + esc(articlePath(v)) + '" data-lang="' + LANG_CODE[hl] + '">');
  }
  return shell.replace("{{HEAD}}", () => head).replace("{{MAIN}}", () => main);
}

function articlePage(all, m) {
  const url = SITE + articlePath(m);
  const h = headline(m);
  const bodyHtml = sanitize(m.body);
  const text = plainText(bodyHtml);
  const desc = clip(m.description && h === m.title ? String(m.description).trim().replace(/[.!?…]+$/, "") + ". " + text : text, 158);
  const img = imageOf(m);
  const lang = langOf(m), L = L10N[lang];
  const rub = rubricOf(m);
  const cat = rub ? TAX.rubrics[rub][lang] : (L.cat[m.cat] || L.cat.article);
  const sec = rub ? { name: L.an, url: L.anUrl } : { name: L.res, url: L.resUrl };
  const seoDesc = clip(String(m.seo_description || "").trim() || desc, 160);
  const ogImg = safeUrl(m.og_image) || img || SITE + "/og-cover.png";
  const industries = (Array.isArray(m.industries) ? m.industries : []).filter(k => TAX.industries[k]);
  const ld = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": m.cat === "news" ? "NewsArticle" : "BlogPosting",
        "@id": url + "#article",
        headline: h.slice(0, 110),
        description: seoDesc,
        mainEntityOfPage: url,
        url,
        inLanguage: lang,
        datePublished: m.created_at,
        dateModified: m.updated_at || m.created_at,
        image: ogImg,
        wordCount: text.split(" ").length,
        ...(rub ? { articleSection: cat } : {}),
        ...(industries.length ? { keywords: industries.map(k => TAX.industries[k][lang]).join(", ") } : {}),
        author: authorLD(m, lang),
        publisher: { "@type": "Organization", "@id": SITE + "/#organization", name: "Human and Capital",
          logo: { "@type": "ImageObject", url: SITE + "/logo.png" } },
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: L.home, item: SITE + L.homeUrl },
          { "@type": "ListItem", position: 2, name: sec.name, item: SITE + sec.url },
          { "@type": "ListItem", position: 3, name: m.title, item: url },
        ],
      },
    ],
  };
  const versions = versionsOf(all, m);
  const alt = Object.keys(versions).length > 1
    ? Object.entries(versions).map(([hl, v]) => '<link rel="alternate" hreflang="' + hl + '" href="' + esc(SITE + articlePath(v)) + '"/>')
      .concat('<link rel="alternate" hreflang="x-default" href="' + esc(SITE + articlePath(versions.ru || versions[langOf(m)])) + '"/>')
    : [];
  const title = (String(m.seo_title || "").trim() || h) + " – Human and Capital";
  const head = [
    "<title>" + esc(title) + "</title>",
    '<meta name="description" content="' + esc(seoDesc) + '"/>',
    '<meta name="robots" content="index, follow, max-image-preview:large"/>',
    '<link rel="canonical" href="' + esc(url) + '"/>',
    ...alt,
    '<meta property="og:type" content="article"/>',
    '<meta property="og:site_name" content="Human and Capital"/>',
    '<meta property="og:locale" content="' + L.og + '"/>',
    '<meta property="og:url" content="' + esc(url) + '"/>',
    '<meta property="og:title" content="' + esc(String(m.seo_title || "").trim() || h) + '"/>',
    '<meta property="og:description" content="' + esc(seoDesc) + '"/>',
    '<meta property="og:image" content="' + esc(ogImg) + '"/>',
    '<meta property="article:published_time" content="' + esc(m.created_at) + '"/>',
    '<meta property="article:modified_time" content="' + esc(m.updated_at || m.created_at) + '"/>',
    ...(rub ? ['<meta property="article:section" content="' + esc(cat) + '"/>'] : []),
    ...industries.map(k => '<meta property="article:tag" content="' + esc(TAX.industries[k][lang]) + '"/>'),
    '<meta name="twitter:card" content="summary_large_image"/>',
    '<meta name="twitter:title" content="' + esc(String(m.seo_title || "").trim() || h) + '"/>',
    '<meta name="twitter:description" content="' + esc(seoDesc) + '"/>',
    '<meta name="twitter:image" content="' + esc(ogImg) + '"/>',
    '<script type="application/ld+json">' + JSON.stringify(ld).replace(/</g, "\\u003c") + "</script>",
  ].join("\n");
  const main = '<header class="ar-hero"><div class="container">'
    + '<div class="ar-crumbs"><a href="' + L.homeUrl + '">' + esc(L.home) + '</a><span aria-hidden="true">/</span>'
    + '<a href="' + sec.url + '">' + esc(sec.name) + '</a></div>'
    + (rub ? '<a class="ar-badge" href="' + sec.url + "?rubric=" + rub + '">' + esc(cat) + "</a>" : '<span class="ar-badge">' + esc(cat) + "</span>")
    + "<h1>" + esc(m.title) + "</h1>"
    + (m.description ? '<p class="ar-lead">' + esc(m.description) + "</p>" : "")
    + '<div class="ar-byline">' + authorHTML(m, lang)
    + '<time class="ar-date" datetime="' + esc(String(m.created_at || "").slice(0, 10)) + '">' + esc(ruDate(m.created_at, L.locale)) + "</time></div>"
    + "</div></header>"
    + '<main class="ar-main"><div class="container"><article>'
    + keyFiguresHTML(m)
    + mediaHTML(m)
    + '<div class="ar-text">' + bodyHtml + "</div>"
    + methodHTML(m, L)
    + tgHTML(m, L)
    + "</article>"
    + ctaHTML(m, L)
    + "</div></main>"
    + relatedHTML(all, m);
  return render(head, main, lang, versions, rub ? "analytics" : "resources");
}

function notFoundPage() {
  return render(
    '<title>Материал не найден – Human and Capital</title>\n<meta name="robots" content="noindex"/>',
    '<main class="ar-404"><div class="container"><h1>Материал не найден</h1>'
    + "<p>Возможно, он был снят с публикации или ссылка устарела.</p>"
    + '<a href="/resources.html">Перейти ко всем материалам →</a></div></main>');
}

module.exports = async function handler(req, res) {
  const slug = String((req.query && req.query.slug) || "").toLowerCase().replace(/\/+$/, "");
  const idPart = (slug.match(/(?:^|-)([0-9a-f]{8})$/) || [])[1];
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  let all;
  try {
    all = await loadMaterials();
  } catch (e) {
    console.error(e);
    res.statusCode = 503;
    res.setHeader("Cache-Control", "no-store");
    res.setHeader("Retry-After", "60");
    return res.end(render('<title>Временная ошибка – Human and Capital</title>\n<meta name="robots" content="noindex"/>',
      '<main class="ar-404"><div class="container"><h1>Не удалось загрузить материал</h1><p>Попробуйте обновить страницу через минуту.</p>'
      + '<a href="/resources.html">Все материалы →</a></div></main>'));
  }
  const m = idPart && all.find(x => String(x.id).startsWith(idPart));
  if (!m) {
    res.statusCode = 404;
    res.setHeader("Cache-Control", "public, s-maxage=60");
    res.setHeader("Vercel-Cache-Tag", "materials");
    return res.end(notFoundPage());
  }
  if (slug !== articleSlug(m)) {
    // заголовок поменяли или ссылка набрана с ошибкой – ведём на актуальный адрес
    res.statusCode = 301;
    res.setHeader("Location", articlePath(m));
    res.setHeader("Cache-Control", "public, s-maxage=300");
    res.setHeader("Vercel-Cache-Tag", "materials");
    return res.end();
  }
  res.statusCode = 200;
  res.setHeader("Cache-Control", "public, max-age=0, s-maxage=300, stale-while-revalidate=86400");
  res.setHeader("Vercel-Cache-Tag", "materials"); // сброс при сохранении в админке – api/revalidate.js
  return res.end(articlePage(all, m));
};
