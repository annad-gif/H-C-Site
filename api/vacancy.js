/* Страница вакансии: /vacancies/<slug> (rewrite в vercel.json → /api/vacancy?slug=...).
   Отдаёт готовый HTML с разметкой JobPosting, чтобы поисковики видели вакансию без выполнения JS.
   Отклик — через модальное окно на vacancies.html (?apply=<id>), там же форма и загрузка резюме. */
"use strict";

const fs = require("fs");
const path = require("path");
const { SITE, vacancySlug, vacancyPath, loadVacancies, esc } = require("./_lib");

const SHELL = fs.readFileSync(path.join(__dirname, "_shell.html"), "utf8")
  // в меню подсвечиваем «Наши вакансии», а не «Полезные материалы»
  .replace(' class="active">Полезные материалы', ">Полезные материалы")
  .replace('href="/vacancies.html">', 'href="/vacancies.html" class="active">');

// те же разделители, что в hc-crm.js (lines): каждая строка/пункт — отдельный элемент списка
function lines(s) {
  return String(s == null ? "" : s).split(/\r?\n|•|·|;/).map(x => x.trim().replace(/^[-–—*]\s*/, "")).filter(Boolean);
}
function block(title, s) {
  const items = lines(s);
  if (!items.length) return "";
  const body = items.length === 1 ? "<p>" + esc(items[0]) + "</p>" : "<ul>" + items.map(i => "<li>" + esc(i) + "</li>").join("") + "</ul>";
  return "<h2>" + esc(title) + "</h2>" + body;
}
function clip(s, n) {
  if (s.length <= n) return s;
  const cut = s.slice(0, n - 1);
  return cut.slice(0, cut.lastIndexOf(" ") > n * 0.6 ? cut.lastIndexOf(" ") : cut.length).replace(/[\s,.;:—-]+$/, "") + "…";
}
function ruDate(iso) {
  try { return new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "long", year: "numeric", timeZone: "Asia/Tashkent" }).format(new Date(iso)).replace(/\s*г\.$/, ""); }
  catch (e) { return String(iso || "").slice(0, 10); }
}
function salary(v) {
  const n = Number(v.budget);
  if (!n || n <= 0) return "";
  return new Intl.NumberFormat("ru-RU").format(n).replace(/ /g, " ") + " сум";
}
function isRemote(v) { return /remote|удал/i.test(String(v.location || "")); }
function isOnsite(v) { return /tashkent|ташкент/i.test(String(v.location || "")) || !isRemote(v); }
function place(v) {
  const parts = [];
  if (isOnsite(v)) parts.push("Ташкент");
  if (isRemote(v)) parts.push(parts.length ? "удалённо" : "Удалённо");
  return parts.join(" / ");
}
function employmentType(t) {
  t = String(t || "").toLowerCase();
  if (/част|part/.test(t)) return "PART_TIME";
  if (/стаж|intern/.test(t)) return "INTERN";
  if (/контракт|подряд|contract/.test(t)) return "CONTRACTOR";
  if (/времен|temp/.test(t)) return "TEMPORARY";
  return "FULL_TIME";
}

function render(head, main) {
  return SHELL.replace("{{HEAD}}", () => head).replace("{{MAIN}}", () => main);
}

function vacancyPage(all, v) {
  const url = SITE + vacancyPath(v);
  const where = place(v);
  const pay = salary(v);
  const facts = [where, v.type, pay].filter(Boolean);
  const textHtml = block("Описание и обязанности", v.description) + block("Требования", v.requirements) + block("Условия", v.offer);
  const plain = [v.description, v.requirements, v.offer].map(x => lines(x).join(". ")).filter(Boolean).join(". ");
  const desc = clip("Вакансия «" + v.title + "» — " + facts.join(", ") + ". " + (plain ? plain + ". " : "")
    + "Откликнитесь онлайн через Human and Capital.", 158);

  const jp = {
    "@context": "https://schema.org",
    "@type": "JobPosting",
    title: v.title,
    description: "<p>Вакансия «" + esc(v.title) + "» от рекрутингового агентства Human and Capital.</p>"
      + (textHtml || "<p>" + esc(v.title) + " — " + esc(facts.join(", ")) + ".</p>"),
    datePosted: String(v.created_at || "").slice(0, 10),
    employmentType: employmentType(v.type),
    hiringOrganization: { "@type": "Organization", name: "Human and Capital", sameAs: SITE + "/", logo: SITE + "/logo.png" },
    identifier: { "@type": "PropertyValue", name: "Human and Capital", value: String(v.id) },
    directApply: true,
    url,
  };
  if (isOnsite(v)) jp.jobLocation = { "@type": "Place", address: { "@type": "PostalAddress", addressLocality: "Tashkent", addressRegion: "Tashkent", addressCountry: "UZ" } };
  if (isRemote(v)) {
    jp.jobLocationType = "TELECOMMUTE";
    jp.applicantLocationRequirements = { "@type": "Country", name: "Uzbekistan" };
  }
  if (Number(v.budget) > 0) {
    jp.baseSalary = { "@type": "MonetaryAmount", currency: "UZS", value: { "@type": "QuantitativeValue", value: Number(v.budget), unitText: "MONTH" } };
  }
  const ld = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Главная", item: SITE + "/" },
      { "@type": "ListItem", position: 2, name: "Вакансии", item: SITE + "/vacancies.html" },
      { "@type": "ListItem", position: 3, name: v.title, item: url },
    ],
  };

  const title = "Вакансия «" + v.title + "» — " + (where || "Ташкент") + " | Human and Capital";
  const head = [
    "<title>" + esc(title) + "</title>",
    '<meta name="description" content="' + esc(desc) + '"/>',
    '<meta name="robots" content="index, follow"/>',
    '<link rel="canonical" href="' + esc(url) + '"/>',
    '<meta property="og:type" content="website"/>',
    '<meta property="og:site_name" content="Human and Capital"/>',
    '<meta property="og:locale" content="ru_RU"/>',
    '<meta property="og:url" content="' + esc(url) + '"/>',
    '<meta property="og:title" content="' + esc("Вакансия «" + v.title + "»") + '"/>',
    '<meta property="og:description" content="' + esc(desc) + '"/>',
    '<meta property="og:image" content="' + SITE + '/og-cover.png"/>',
    '<meta name="twitter:card" content="summary_large_image"/>',
    '<meta name="twitter:title" content="' + esc("Вакансия «" + v.title + "»") + '"/>',
    '<meta name="twitter:description" content="' + esc(desc) + '"/>',
    '<script type="application/ld+json">' + JSON.stringify(jp).replace(/</g, "\\u003c") + "</script>",
    '<script type="application/ld+json">' + JSON.stringify(ld).replace(/</g, "\\u003c") + "</script>",
  ].join("\n");

  const applyHref = "/vacancies.html?apply=" + encodeURIComponent(v.id);
  const others = all.filter(x => x.id !== v.id).slice(0, 6);
  const main = '<header class="ar-hero"><div class="container">'
    + '<div class="ar-crumbs"><a href="/">Главная</a><span aria-hidden="true">/</span>'
    + '<a href="/vacancies.html">Вакансии</a></div>'
    + '<span class="ar-badge">Вакансия</span>'
    + "<h1>" + esc(v.title) + "</h1>"
    + '<ul class="vac-facts">' + facts.map(f => "<li>" + esc(f) + "</li>").join("") + "</ul>"
    + '<div class="vac-actions"><a class="vac-apply" href="' + esc(applyHref) + '">Откликнуться на вакансию →</a>'
    + '<time class="ar-date" datetime="' + esc(String(v.created_at || "").slice(0, 10)) + '">Опубликовано ' + esc(ruDate(v.created_at)) + "</time></div>"
    + "</div></header>"
    + '<main class="ar-main"><div class="container"><article>'
    + '<div class="ar-text">'
    + (textHtml || "<p>Подробности о вакансии расскажем при первом контакте. Оставьте отклик — рекрутер свяжется с вами.</p>")
    + "<h2>Как откликнуться</h2>"
    + "<p>Нажмите «Откликнуться на вакансию», заполните короткую форму или загрузите резюме (PDF, DOC, DOCX). "
    + "Заявка попадёт напрямую к рекрутеру Human and Capital, и мы свяжемся с вами, если ваш опыт подходит под требования.</p>"
    + "</div>"
    + '<p class="vac-bottom"><a class="vac-apply" href="' + esc(applyHref) + '">Откликнуться на вакансию →</a></p>'
    + "</article>"
    + '<aside class="ar-cta"><div><h2>Ищете сотрудников в свою компанию?</h2>'
    + "<p>Human and Capital — рекрутинговое агентство в Узбекистане. Подберём специалистов и руководителей, закроем массовые позиции.</p></div>"
    + '<a href="/recruitment.html">Подбор персонала →</a></aside>'
    + "</div></main>"
    + (others.length
      ? '<section class="ar-related"><div class="container"><h2>Другие вакансии</h2><ul class="vac-list">'
        + others.map(o => '<li><a href="' + esc(vacancyPath(o)) + '"><b>' + esc(o.title) + "</b><span>"
          + esc([place(o), o.type, salary(o)].filter(Boolean).join(" · ")) + "</span></a></li>").join("")
        + '</ul><a class="ar-all" href="/vacancies.html">Все вакансии →</a></div></section>'
      : "");
  return render(head, main);
}

function notFoundPage() {
  return render(
    '<title>Вакансия закрыта — Human and Capital</title>\n<meta name="robots" content="noindex"/>',
    '<main class="ar-404"><div class="container"><h1>Вакансия закрыта или не найдена</h1>'
    + "<p>Возможно, позиция уже закрыта. Посмотрите другие открытые вакансии или оставьте резюме в кадровом резерве.</p>"
    + '<a href="/vacancies.html">Все вакансии →</a></div></main>');
}

module.exports = async function handler(req, res) {
  const slug = String((req.query && req.query.slug) || "").toLowerCase().replace(/\/+$/, "");
  const idPart = (slug.match(/(?:^|-)([0-9a-f]{8})$/) || [])[1];
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  let all;
  try {
    all = await loadVacancies();
  } catch (e) {
    console.error(e);
    res.statusCode = 503;
    res.setHeader("Cache-Control", "no-store");
    res.setHeader("Retry-After", "60");
    return res.end(render('<title>Временная ошибка — Human and Capital</title>\n<meta name="robots" content="noindex"/>',
      '<main class="ar-404"><div class="container"><h1>Не удалось загрузить вакансию</h1><p>Попробуйте обновить страницу через минуту.</p>'
      + '<a href="/vacancies.html">Все вакансии →</a></div></main>'));
  }
  const v = idPart && all.find(x => String(x.id).startsWith(idPart));
  if (!v) {
    res.statusCode = 404;
    res.setHeader("Cache-Control", "public, s-maxage=60");
    return res.end(notFoundPage());
  }
  if (slug !== vacancySlug(v)) {
    res.statusCode = 301;
    res.setHeader("Location", vacancyPath(v));
    res.setHeader("Cache-Control", "public, s-maxage=300");
    return res.end();
  }
  res.statusCode = 200;
  res.setHeader("Cache-Control", "public, max-age=0, s-maxage=300, stale-while-revalidate=86400");
  return res.end(vacancyPage(all, v));
};
