/* /api/hub?page=<имя> – разделы-списки для ботов без JavaScript (GPTBot, ClaudeBot, PerplexityBot и т. п.).

   resources*, analytics*, vacancies* и analytics-salaries* рисуют списки и калькулятор в браузере – в исходном HTML
   их нет, и AI-поисковики видят пустой раздел. middleware.js отправляет эти адреса сюда: функция берёт ту же
   статичную страницу и вставляет в контейнер списка простой список ссылок (статьи, вакансии) или таблицу зарплат.
   Скрипт страницы при загрузке всё равно заменяет содержимое контейнера своими карточками, а класс hc-js
   на <html> прячет вставку ещё до этого – посетитель с JavaScript видит страницу как раньше.

   Сами страницы не правятся (их собирают tools/*.py); при любой ошибке отдаётся статичная страница без вставки. */
"use strict";

const fs = require("fs");
const path = require("path");
const { SITE, articlePath, loadMaterials, vacancyPath, loadVacancies, esc } = require("./_lib");
const TAX = require("./_taxonomy.json");

// страница -> [язык, вид, id контейнера]
const PAGES = {};
for (const [base, kind, box] of [["resources", "materials", "rsGrid"], ["analytics", "analytics", "anGrid"],
  ["vacancies", "vacancies", "vcGrid"], ["analytics-salaries", "salaries", "slRes"]]) {
  PAGES[base] = ["ru", kind, box];
  PAGES[base + "-en"] = ["en", kind, box];
  PAGES[base + "-uz"] = ["uz", kind, box];
}

const L = {
  ru: { materials: "Все материалы", analytics: "Обзоры и исследования", vacancies: "Открытые вакансии",
    salaries: "Зарплатные ожидания кандидатов в Узбекистане", grp: "Направление", exp: "Опыт", med: "Медиана",
    iqr: "Типичная вилка (25–75%)", top: "Верхние 10% от", n: "Резюме", mln: "млн сум",
    note: "На руки в месяц, по данным {n} резюме, срез на {date}. Срезы меньше {min} резюме не показываются. Курс: 1 $ = {rate} сум." },
  en: { materials: "All resources", analytics: "Reviews and research", vacancies: "Open vacancies",
    salaries: "Candidates’ salary expectations in Uzbekistan", grp: "Role group", exp: "Experience", med: "Median",
    iqr: "Typical range (25–75%)", top: "Top 10% from", n: "CVs", mln: "m UZS",
    note: "Net per month, based on {n} CVs, snapshot of {date}. Slices with fewer than {min} CVs are not shown. Rate: $1 = {rate} UZS." },
  uz: { materials: "Barcha materiallar", analytics: "Sharhlar va tadqiqotlar", vacancies: "Ochiq vakansiyalar",
    salaries: "O‘zbekistonda nomzodlarning maosh kutilmalari", grp: "Yo‘nalish", exp: "Tajriba", med: "Mediana",
    iqr: "Odatiy oraliq (25–75%)", top: "Eng yuqori 10% dan", n: "Rezyume", mln: "mln so‘m",
    note: "Qo‘lga, oyiga, {n} ta rezyume asosida, {date} holatiga. {min} tadan kam rezyumeli kesimlar ko‘rsatilmaydi. Kurs: 1 $ = {rate} so‘m." },
};

const HEAD = '<script>document.documentElement.classList.add("hc-js")</script>'
  + '<style>.hc-js .hc-ssr{display:none!important}.hc-ssr{grid-column:1/-1;line-height:1.5}'
  + '.hc-ssr ul{padding-left:1.2em}.hc-ssr li{margin:.5em 0}.hc-ssr table{border-collapse:collapse;width:100%;font-size:14px}'
  + '.hc-ssr th,.hc-ssr td{border-bottom:1px solid #ddd;padding:4px 6px;text-align:left}</style>';

function readPage(name) {
  for (const dir of [path.join(__dirname, ".."), process.cwd()]) {
    try { return fs.readFileSync(path.join(dir, name + ".html"), "utf8"); } catch (e) { /* следующий путь */ }
  }
  throw new Error("нет файла " + name + ".html");
}

function date10(s) { return String(s || "").slice(0, 10); }

function materialsList(t, items) {
  if (!items.length) return "";
  return '<ul>' + items.map(m => '<li><a href="' + esc(SITE + articlePath(m)) + '">' + esc(m.title) + '</a>'
    + (m.description ? ' – ' + esc(m.description) : '') + ' <time datetime="' + esc(date10(m.created_at)) + '">'
    + esc(date10(m.created_at)) + '</time></li>').join("") + '</ul>';
}

async function materials(lang, t, onlyRubric) {
  const all = (await loadMaterials()).filter(m => (m.lang || "ru") === lang);
  const list = onlyRubric ? all.filter(m => m.rubric && TAX.rubrics && TAX.rubrics[m.rubric]) : all;
  if (!list.length) return "";
  return '<h2>' + esc(onlyRubric ? t.analytics : t.materials) + '</h2>' + materialsList(t, list);
}

async function vacancies(lang, t) {
  const list = await loadVacancies();
  if (!list.length) return "";
  return '<h2>' + esc(t.vacancies) + '</h2><ul>' + list.map(v => '<li><a href="' + esc(SITE + vacancyPath(v)) + '">'
    + esc(v.title) + '</a>' + [v.location, v.type].filter(Boolean).map(x => ' · ' + esc(x)).join("") + '</li>').join("") + '</ul>';
}

// подписи групп, сфер и стажа берём из самой страницы – они уже переведены на её язык (tools/build_salaries.py)
function pageConst(html, name) {
  const m = html.match(new RegExp("const " + name + " = (\\{[^\\n]*?\\})[,;]"));
  return m ? JSON.parse(m[1]) : null;
}

async function salaries(lang, t, html) {
  const GROUPS = pageConst(html, "GROUPS"), SPHERES = pageConst(html, "SPHERES"), EXP = pageConst(html, "EXP");
  const SPHERE_OF = (html.match(/SPHERE_OF = (\{[^\n]*?\})[,;]/) || [])[1];
  if (!GROUPS || !SPHERES || !EXP || !SPHERE_OF) throw new Error("на странице нет подписей калькулятора");
  const sphereOf = JSON.parse(SPHERE_OF);
  const r = await fetch(SITE + "/api/salaries");
  if (!r.ok) throw new Error("api/salaries " + r.status);
  const d = await r.json();
  const rate = Number(d.usd_rate) || 0;
  const loc = { ru: "ru-RU", en: "en-US", uz: "ru-RU" }[lang];
  const mln = v => (v / 1e6).toLocaleString(loc, { maximumFractionDigits: 1 }) + " " + t.mln
    + (rate ? " (~$" + Math.round(v / rate / 50) * 50 + ")" : ""); // как в калькуляторе: до 50 $
  const rng = (a, b) => (a / 1e6).toLocaleString(loc, { maximumFractionDigits: 1 }) + "–" + mln(b);
  const order = ["all", "0", "1-2", "3-5", "6+"];
  const rows = (d.resumes || []).filter(x => GROUPS[x.grp] && EXP[x.exp] && SPHERES[sphereOf[x.grp]]);
  let out = '<h2>' + esc(t.salaries) + '</h2>';
  for (const sp of Object.keys(SPHERES)) {
    const groups = Object.keys(GROUPS).filter(g => sphereOf[g] === sp);
    const body = [];
    for (const g of groups) for (const e of order) {
      const x = rows.find(y => y.grp === g && y.exp === e);
      if (x) body.push('<tr><td>' + esc(GROUPS[g]) + '</td><td>' + esc(EXP[e]) + '</td><td>' + esc(mln(x.p50)) + '</td><td>'
        + esc(rng(x.p25, x.p75)) + '</td><td>' + esc(mln(x.p90)) + '</td><td>' + x.n + '</td></tr>');
    }
    if (!body.length) continue;
    const meta = (d.spheres && d.spheres[sp]) || { resumes_total: d.resumes_total, snapshot_date: d.snapshot_date };
    out += '<h3>' + esc(SPHERES[sp]) + '</h3><table><caption>' + esc(t.note.replace("{n}", Number(meta.resumes_total || 0).toLocaleString(loc))
      .replace("{date}", date10(meta.snapshot_date)).replace("{min}", d.min_n || 30).replace("{rate}", Math.round(rate).toLocaleString(loc)))
      + '</caption><thead><tr><th>' + esc(t.grp) + '</th><th>' + esc(t.exp) + '</th><th>' + esc(t.med) + '</th><th>' + esc(t.iqr)
      + '</th><th>' + esc(t.top) + '</th><th>' + esc(t.n) + '</th></tr></thead><tbody>' + body.join("") + '</tbody></table>';
  }
  return out;
}

async function build(page) {
  const [lang, kind, box] = PAGES[page];
  const html = readPage(page);
  const t = L[lang];
  let block = "", tag = null, sMax = 300;
  try {
    if (kind === "materials") { block = await materials(lang, t, false); tag = "materials"; }
    else if (kind === "analytics") { block = await materials(lang, t, true); tag = "materials"; }
    else if (kind === "vacancies") block = await vacancies(lang, t);
    else { block = await salaries(lang, t, html); tag = "salaries"; sMax = 3600; }
  } catch (e) {
    console.error("hub " + page, e);
    return { html, ok: false };
  }
  if (!block) return { html, ok: true, tag, sMax };
  const open = new RegExp('(<div[^>]*id="' + box + '"[^>]*>)');
  if (!open.test(html) || html.indexOf("</head>") < 0) return { html, ok: false };
  // функции вместо строк замены: в суммах есть «$», а в строке замены «$1», «$2» означают группы
  const out = html.replace("</head>", () => HEAD + "</head>")
    .replace(open, tagOpen => tagOpen + '<div class="hc-ssr">' + block + '</div>');
  return { html: out, ok: true, tag, sMax };
}

module.exports = async function handler(req, res) {
  const page = String((req.query && req.query.page) || "");
  if (!PAGES[page]) { res.statusCode = 404; res.setHeader("Content-Type", "text/plain; charset=utf-8"); return res.end("Not found"); }
  let r;
  try { r = await build(page); } catch (e) {
    console.error("hub " + page, e);
    res.statusCode = 500; res.setHeader("Cache-Control", "no-store"); return res.end("Server error");
  }
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  // без вставки (ошибка источника) – короткий кэш, чтобы через минуту попробовать снова
  res.setHeader("Cache-Control", r.ok ? "public, max-age=0, s-maxage=" + r.sMax + ", stale-while-revalidate=86400" : "public, max-age=0, s-maxage=60");
  if (r.ok && r.tag) res.setHeader("Vercel-Cache-Tag", r.tag);
  res.end(r.html);
};

module.exports.build = build; // для локальной проверки
module.exports.PAGES = PAGES;
