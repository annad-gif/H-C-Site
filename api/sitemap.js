/* /sitemap.xml (rewrite в vercel.json): страницы сайта на трёх языках + статьи из админки. */
"use strict";

const { SITE, articlePath, loadMaterials, vacancyPath, loadVacancies, PAGES, pageUrl, esc } = require("./_lib");

const LASTMOD_PAGES = "2026-10-23"; // обновлять при заметных правках страниц

// [RU, EN, UZ] – английские адреса исторические, их не меняем
const TRIOS = [
  [["hr-services.html", "hr-services-uzbekistan.html", "hr-services-uz.html"], "0.9"],
  [["employer-of-record.html", "employer-of-record-uzbekistan.html", "employer-of-record-uz.html"], "0.9"],
  [["privacy.html", "privacy-en.html", "privacy-uz.html"], "0.2"],
];

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
  // страницы, у которых адреса языковых версий не по схеме p / p-en / p-uz
  for (const [names, prio] of TRIOS) {
    for (const n of names) {
      out.push("  <url>", "    <loc>" + pageUrl(n) + "</loc>", "    <lastmod>" + LASTMOD_PAGES + "</lastmod>");
      ["ru", "en", "uz"].forEach((hl, i) =>
        out.push('    <xhtml:link rel="alternate" hreflang="' + hl + '" href="' + pageUrl(names[i]) + '"/>'));
      out.push('    <xhtml:link rel="alternate" hreflang="x-default" href="' + pageUrl(names[0]) + '"/>',
        "    <priority>" + prio + "</priority>", "  </url>");
    }
  }
  out.push("</urlset>", "");
  res.statusCode = 200;
  res.setHeader("Content-Type", "application/xml; charset=utf-8");
  res.setHeader("Cache-Control", ok ? "public, max-age=0, s-maxage=600, stale-while-revalidate=86400" : "no-store");
  if (ok) res.setHeader("Vercel-Cache-Tag", "materials");
  res.end(out.join("\n"));
};
