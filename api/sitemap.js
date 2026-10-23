/* /sitemap.xml (rewrite в vercel.json): страницы сайта на трёх языках + статьи из админки. */
"use strict";

const { SITE, articlePath, loadMaterials, vacancyPath, loadVacancies, PAGES, pageUrl, esc } = require("./_lib");

const LASTMOD_PAGES = "2026-10-23"; // обновлять при заметных правках страниц

module.exports = async function handler(req, res) {
  const out = ['<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'];
  for (const [p, prio] of PAGES) {
    const names = [p + ".html", p + "-en.html", p + "-uz.html"];
    for (const n of names) {
      out.push("  <url>", "    <loc>" + pageUrl(n) + "</loc>", "    <lastmod>" + LASTMOD_PAGES + "</lastmod>");
      ["ru", "en", "uz"].forEach((hl, i) =>
        out.push('    <xhtml:link rel="alternate" hreflang="' + hl + '" href="' + pageUrl(names[i]) + '"/>'));
      out.push('    <xhtml:link rel="alternate" hreflang="x-default" href="' + pageUrl(names[0]) + '"/>',
        "    <priority>" + prio + "</priority>", "  </url>");
    }
  }
  let ok = true;
  try {
    for (const m of await loadMaterials()) {
      out.push("  <url>", "    <loc>" + esc(SITE + articlePath(m)) + "</loc>",
        "    <lastmod>" + String(m.updated_at || m.created_at || "").slice(0, 10) + "</lastmod>",
        "    <priority>0.6</priority>", "  </url>");
    }
  } catch (e) {
    console.error(e);
    ok = false; // без статей, но карта сайта всё равно отдаётся
  }
  try {
    for (const v of await loadVacancies()) {
      out.push("  <url>", "    <loc>" + esc(SITE + vacancyPath(v)) + "</loc>",
        "    <lastmod>" + String(v.created_at || "").slice(0, 10) + "</lastmod>",
        "    <priority>0.7</priority>", "  </url>");
    }
  } catch (e) {
    console.error(e);
    ok = false; // без вакансий, но карта сайта всё равно отдаётся
  }
  // отдельные страницы без языковых версий
  out.push("  <url>", "    <loc>" + SITE + "/hr-services-uzbekistan.html</loc>", "    <lastmod>2026-10-22</lastmod>",
    "    <priority>0.9</priority>", "  </url>");
  out.push("  <url>", "    <loc>" + SITE + "/employer-of-record-uzbekistan.html</loc>", "    <lastmod>2026-10-23</lastmod>",
    "    <priority>0.9</priority>", "  </url>");
  out.push("  <url>", "    <loc>" + SITE + "/privacy.html</loc>", "    <priority>0.2</priority>", "  </url>", "</urlset>", "");
  res.statusCode = 200;
  res.setHeader("Content-Type", "application/xml; charset=utf-8");
  res.setHeader("Cache-Control", ok ? "public, max-age=0, s-maxage=600, stale-while-revalidate=86400" : "no-store");
  res.end(out.join("\n"));
};
