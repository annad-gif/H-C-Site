/* /api/revalidate – сброс кэша CDN для материалов после сохранения в админке (admin.html → refreshSiteCache).

   Списки (/api/materials), страницы статей (/articles/<slug>) и sitemap помечены тегом кэша «materials»
   (заголовок Vercel-Cache-Tag). Здесь тег сбрасывается, и следующий запрос собирает страницу заново –
   правка видна сразу, а не через 5 минут.

   Кто может вызвать: только вошедший администратор сайта. Токен сессии Supabase из админки проверяется
   так же, как это делает RLS таблицы site_materials: rpc site_admin_role() от имени пользователя. */
"use strict";

const SB_URL = "https://byerqfuuprmmykncjqms.supabase.co";
const SB_KEY = "sb_publishable_JBo7zlA02IyeaJLuTdZX5A_YEatYU6_"; // публичный ключ, как в api/_lib.js

async function isSiteAdmin(token) {
  if (!token) return false;
  const r = await fetch(SB_URL + "/rest/v1/rpc/site_admin_role", {
    method: "POST",
    headers: { apikey: SB_KEY, Authorization: "Bearer " + token, "Content-Type": "application/json" },
    body: "{}",
  });
  if (!r.ok) return false;
  const role = await r.json();
  return role != null && role !== "";
}

module.exports = async function handler(req, res) {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.statusCode = 405; return res.end(JSON.stringify({ ok: false, error: "POST only" })); }
  const token = String(req.headers.authorization || "").replace(/^Bearer\s+/i, "").trim();
  try {
    if (!(await isSiteAdmin(token))) { res.statusCode = 403; return res.end(JSON.stringify({ ok: false, error: "forbidden" })); }
    // удалить, а не пометить устаревшим: иначе первый посетитель после правки ещё увидит старую версию
    const { dangerouslyDeleteByTag } = await import("@vercel/functions");
    await dangerouslyDeleteByTag("materials");
    res.statusCode = 200;
    return res.end(JSON.stringify({ ok: true }));
  } catch (e) {
    console.error("revalidate", e);
    res.statusCode = 500;
    return res.end(JSON.stringify({ ok: false, error: String(e && e.message || e).slice(0, 200) }));
  }
};
