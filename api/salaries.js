/* /api/salaries – данные для калькулятора зарплат (analytics-salaries*.html, tools/build_salaries.py).

   Источник – функция public_salary_stats() в базе ATS (миграция Recruitpro db/migrations/
   2026-10-29_public_salary_stats.sql): только агрегаты последнего успешного прогона hh-resumes и сводка вилок
   открытых вакансий, срезы меньше 30 наблюдений функция не отдаёт. Расчёт обновляется 1-го и 15-го числа,
   поэтому ответ живёт на CDN Vercel час (+ stale-while-revalidate): для посетителя это доли секунды. */
"use strict";

const SB_URL = "https://byerqfuuprmmykncjqms.supabase.co";
const SB_KEY = "sb_publishable_JBo7zlA02IyeaJLuTdZX5A_YEatYU6_"; // публичный ключ, как в api/_lib.js

module.exports = async function handler(req, res) {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  try {
    const r = await fetch(SB_URL + "/rest/v1/rpc/public_salary_stats", {
      method: "POST",
      headers: { apikey: SB_KEY, Authorization: "Bearer " + SB_KEY, "Content-Type": "application/json" },
      body: "{}",
    });
    if (!r.ok) throw new Error("public_salary_stats " + r.status + ": " + (await r.text()).slice(0, 200));
    const data = await r.json();
    if (!data || !Array.isArray(data.resumes) || !data.resumes.length) throw new Error("public_salary_stats: пустой ответ");
    res.setHeader("Cache-Control", "public, max-age=0, s-maxage=3600, stale-while-revalidate=86400");
    res.setHeader("Vercel-Cache-Tag", "salaries");
    res.statusCode = 200;
    return res.end(JSON.stringify(data));
  } catch (e) {
    console.error(e);
    res.statusCode = 503;
    res.setHeader("Cache-Control", "no-store");
    return res.end(JSON.stringify({ error: "salaries unavailable" }));
  }
};
