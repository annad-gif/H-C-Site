/* /api/materials – лёгкий список опубликованных материалов для resources*.html и analytics*.html.

   Раньше страницы сами запрашивали site_materials целиком (select=*): 42 статьи с полным HTML – ~440 КБ,
   из браузера в Узбекистане это шло 3–15 с. Здесь – только поля для карточек и фильтров, плюс `text`:
   начало текста без разметки для поиска по «Полезным материалам». Ответ кэшируется на CDN Vercel
   (s-maxage 300 + stale-while-revalidate), поэтому для посетителя это доли секунды; правка в админке
   появляется на страницах в течение ~5 минут (как и на страницах статей /articles/<slug>). */
"use strict";

const { loadMaterials } = require("./_lib");

const TEXT_LIMIT = 3000; // символов текста на материал – хватает для поиска по ключевым словам

function plain(html) {
  return String(html || "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/\s+/g, " ").trim().slice(0, TEXT_LIMIT);
}

module.exports = async function handler(req, res) {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  try {
    const rows = await loadMaterials();
    const list = rows.map(m => ({
      id: m.id, cat: m.cat, lang: m.lang, title: m.title, description: m.description,
      media_url: m.media_url, media_type: m.media_type, created_at: m.created_at, sort: m.sort,
      translation_of: m.translation_of, published: m.published,
      rubric: m.rubric || null, industries: m.industries || [], author_key: m.author_key || null,
      audience: m.audience || null, text: plain(m.body),
    }));
    res.setHeader("Cache-Control", "public, max-age=0, s-maxage=300, stale-while-revalidate=86400");
    res.statusCode = 200;
    return res.end(JSON.stringify(list));
  } catch (e) {
    console.error(e);
    res.statusCode = 503;
    res.setHeader("Cache-Control", "no-store");
    return res.end(JSON.stringify({ error: "materials unavailable" }));
  }
};
