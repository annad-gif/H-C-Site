/* Общий код для api/article.js и api/sitemap.js.
   Материалы берутся из таблицы site_materials проекта ATS (тот же публичный
   ключ, что использует resources.html в браузере). */
"use strict";

const SITE = "https://humancapital.uz";
const SB_URL = "https://byerqfuuprmmykncjqms.supabase.co";
const SB_KEY = "sb_publishable_JBo7zlA02IyeaJLuTdZX5A_YEatYU6_";

// --- адрес статьи: /articles/<транслит заголовка>-<первые 8 символов id> ---
// Та же функция продублирована в resources*.html (articleSlug) — менять синхронно.
const TR = { "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"yo","ж":"zh","з":"z","и":"i","й":"y","к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"kh","ц":"ts","ч":"ch","ш":"sh","щ":"sch","ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya","ў":"o","қ":"q","ғ":"g","ҳ":"h" };
function articleSlug(m) {
  const base = String(m.title || "").toLowerCase().split("").map(c => (c in TR ? TR[c] : c)).join("")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 70).replace(/-+$/, "");
  const id = String(m.id).slice(0, 8);
  return base ? base + "-" + id : id;
}
function articlePath(m) { return "/articles/" + articleSlug(m); }

// --- загрузка материалов (кэш на время жизни инстанса функции) ---
let cache = { at: 0, data: null };
async function loadMaterials() {
  if (cache.data && Date.now() - cache.at < 60 * 1000) return cache.data;
  const url = SB_URL + "/rest/v1/site_materials?select=*&published=eq.true&order=sort.asc,created_at.desc";
  const r = await fetch(url, { headers: { apikey: SB_KEY, Authorization: "Bearer " + SB_KEY } });
  if (!r.ok) throw new Error("site_materials " + r.status + ": " + (await r.text()).slice(0, 200));
  const data = await r.json();
  cache = { at: Date.now(), data };
  return data;
}

// --- статические страницы сайта для sitemap ---
const PAGES = [
  ["index", "1.0"], ["recruitment", "0.9"], ["outstaffing", "0.9"], ["consulting", "0.9"],
  ["vacancies", "0.8"], ["resources", "0.7"], ["talent-pool", "0.6"],
];
function pageUrl(name) { return name === "index.html" ? SITE + "/" : SITE + "/" + name; }

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

module.exports = { SITE, articleSlug, articlePath, loadMaterials, PAGES, pageUrl, esc };
