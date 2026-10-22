/* Страница статьи: /articles/<slug> (rewrite в vercel.json → /api/article?slug=...).
   Отдаёт готовый HTML, чтобы поисковики видели текст статьи без выполнения JS. */
"use strict";

const fs = require("fs");
const path = require("path");
const { SITE, articleSlug, articlePath, loadMaterials, esc } = require("./_lib");

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
        ctaP: "Human and Capital — рекрутинговое агентство в Узбекистане. Найдём сотрудников под ваши задачи: от массового подбора до executive search.",
        ctaA: "Оставить заявку →", ctaUrl: "/index.html#contact", related: "Читайте также", all: "Все материалы →" },
  en: { locale: "en-GB", og: "en_US", home: "Home", homeUrl: "/index-en.html", res: "Resources", resUrl: "/resources-en.html",
        cat: { article: "Article", news: "News", video: "Video", photo: "Photo" },
        ctaH: "Need help hiring in Uzbekistan?",
        ctaP: "Human and Capital is an HR company in Tashkent: recruitment, executive search, outstaffing and HR consulting for local and international companies.",
        ctaA: "Send a request →", ctaUrl: "/hr-services-uzbekistan.html#contact", related: "Read also", all: "All resources →" },
  uz: { locale: "uz-Latn-UZ", og: "uz_UZ", home: "Bosh sahifa", homeUrl: "/index-uz.html", res: "Foydali materiallar", resUrl: "/resources-uz.html",
        cat: { article: "Maqola", news: "Yangilik", video: "Video", photo: "Foto" },
        ctaH: "Xodim tanlashda yordam kerakmi?",
        ctaP: "Human and Capital — O‘zbekistondagi rekruting agentligi. Ommaviy tanlovdan executive searchgacha — vazifangizga mos xodimlarni topamiz.",
        ctaA: "Ariza qoldirish →", ctaUrl: "/index-uz.html#contact", related: "Shuningdek o‘qing", all: "Barcha materiallar →" },
};
function langOf(m) { return L10N[m && m.lang] ? m.lang : "ru"; }
const CAT = L10N.ru.cat;

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
  return cut.slice(0, cut.lastIndexOf(" ") > n * 0.6 ? cut.lastIndexOf(" ") : cut.length).replace(/[\s,.;:—-]+$/, "") + "…";
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
  const others = all.slice(i + 1).concat(all.slice(0, i)).filter(x => x.id !== m.id);
  // сначала материалы на том же языке, внутри — того же типа
  const rank = x => (langOf(x) === langOf(m) ? 0 : 2) + (x.cat === m.cat ? 0 : 1);
  const pick = others.map((x, k) => [x, k]).sort((a, b) => rank(a[0]) - rank(b[0]) || a[1] - b[1]).map(a => a[0]).slice(0, 3);
  if (!pick.length) return "";
  return '<section class="ar-related"><div class="container"><h2>' + esc(L.related) + '</h2><div class="ar-rel-grid">'
    + pick.map(r => {
      const img = imageOf(r);
      return '<a class="ar-rel" href="' + esc(articlePath(r)) + '"><div class="ar-rel-img">'
        + (img ? '<img src="' + esc(img) + '" alt="' + esc(r.title) + '" loading="lazy"/>' : "")
        + '</div><div class="ar-rel-body"><h3>' + esc(r.title) + "</h3><p>" + esc(r.description || "") + "</p></div></a>";
    }).join("")
    + '</div><a class="ar-all" href="' + L.resUrl + '">' + esc(L.all) + '</a></div></section>';
}

function render(head, main, lang) {
  return (SHELLS[lang] || SHELL).replace("{{HEAD}}", () => head).replace("{{MAIN}}", () => main);
}

function articlePage(all, m) {
  const url = SITE + articlePath(m);
  const h = headline(m);
  const bodyHtml = sanitize(m.body);
  const text = plainText(bodyHtml);
  const desc = clip(m.description && h === m.title ? m.description + ". " + text : text, 158);
  const img = imageOf(m);
  const lang = langOf(m), L = L10N[lang];
  const cat = L.cat[m.cat] || L.cat.article;
  const ld = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": m.cat === "news" ? "NewsArticle" : "BlogPosting",
        "@id": url + "#article",
        headline: h.slice(0, 110),
        description: desc,
        mainEntityOfPage: url,
        url,
        inLanguage: lang,
        datePublished: m.created_at,
        dateModified: m.updated_at || m.created_at,
        image: img || SITE + "/og-cover.png",
        wordCount: text.split(" ").length,
        author: { "@type": "Organization", name: "Human and Capital", url: SITE + "/" },
        publisher: { "@type": "Organization", "@id": SITE + "/#organization", name: "Human and Capital",
          logo: { "@type": "ImageObject", url: SITE + "/logo.png" } },
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: L.home, item: SITE + L.homeUrl },
          { "@type": "ListItem", position: 2, name: L.res, item: SITE + L.resUrl },
          { "@type": "ListItem", position: 3, name: m.title, item: url },
        ],
      },
    ],
  };
  const title = h + " — Human and Capital";
  const head = [
    "<title>" + esc(title) + "</title>",
    '<meta name="description" content="' + esc(desc) + '"/>',
    '<meta name="robots" content="index, follow, max-image-preview:large"/>',
    '<link rel="canonical" href="' + esc(url) + '"/>',
    '<meta property="og:type" content="article"/>',
    '<meta property="og:site_name" content="Human and Capital"/>',
    '<meta property="og:locale" content="' + L.og + '"/>',
    '<meta property="og:url" content="' + esc(url) + '"/>',
    '<meta property="og:title" content="' + esc(h) + '"/>',
    '<meta property="og:description" content="' + esc(desc) + '"/>',
    '<meta property="og:image" content="' + esc(img || SITE + "/og-cover.png") + '"/>',
    '<meta property="article:published_time" content="' + esc(m.created_at) + '"/>',
    '<meta property="article:modified_time" content="' + esc(m.updated_at || m.created_at) + '"/>',
    '<meta name="twitter:card" content="summary_large_image"/>',
    '<meta name="twitter:title" content="' + esc(h) + '"/>',
    '<meta name="twitter:description" content="' + esc(desc) + '"/>',
    '<meta name="twitter:image" content="' + esc(img || SITE + "/og-cover.png") + '"/>',
    '<script type="application/ld+json">' + JSON.stringify(ld).replace(/</g, "\\u003c") + "</script>",
  ].join("\n");
  const main = '<header class="ar-hero"><div class="container">'
    + '<div class="ar-crumbs"><a href="' + L.homeUrl + '">' + esc(L.home) + '</a><span aria-hidden="true">/</span>'
    + '<a href="' + L.resUrl + '">' + esc(L.res) + '</a></div>'
    + '<span class="ar-badge">' + esc(cat) + "</span>"
    + "<h1>" + esc(m.title) + "</h1>"
    + (m.description ? '<p class="ar-lead">' + esc(m.description) + "</p>" : "")
    + '<time class="ar-date" datetime="' + esc(String(m.created_at || "").slice(0, 10)) + '">' + esc(ruDate(m.created_at, L.locale)) + "</time>"
    + "</div></header>"
    + '<main class="ar-main"><div class="container"><article>'
    + mediaHTML(m)
    + '<div class="ar-text">' + bodyHtml + "</div></article>"
    + '<aside class="ar-cta"><div><h2>' + esc(L.ctaH) + "</h2>"
    + "<p>" + esc(L.ctaP) + "</p></div>"
    + '<a href="' + L.ctaUrl + '">' + esc(L.ctaA) + "</a></aside>"
    + "</div></main>"
    + relatedHTML(all, m);
  return render(head, main, lang);
}

function notFoundPage() {
  return render(
    '<title>Материал не найден — Human and Capital</title>\n<meta name="robots" content="noindex"/>',
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
    return res.end(render('<title>Временная ошибка — Human and Capital</title>\n<meta name="robots" content="noindex"/>',
      '<main class="ar-404"><div class="container"><h1>Не удалось загрузить материал</h1><p>Попробуйте обновить страницу через минуту.</p>'
      + '<a href="/resources.html">Все материалы →</a></div></main>'));
  }
  const m = idPart && all.find(x => String(x.id).startsWith(idPart));
  if (!m) {
    res.statusCode = 404;
    res.setHeader("Cache-Control", "public, s-maxage=60");
    return res.end(notFoundPage());
  }
  if (slug !== articleSlug(m)) {
    // заголовок поменяли или ссылка набрана с ошибкой — ведём на актуальный адрес
    res.statusCode = 301;
    res.setHeader("Location", articlePath(m));
    res.setHeader("Cache-Control", "public, s-maxage=300");
    return res.end();
  }
  res.statusCode = 200;
  res.setHeader("Cache-Control", "public, max-age=0, s-maxage=300, stale-while-revalidate=86400");
  return res.end(articlePage(all, m));
};
