/* ============================================================
   Human and Capital — веб-аналитика (Google Analytics 4 + Яндекс Метрика)

   Подключается в <head> каждой публичной страницы:
     <script src="/hc-analytics.js" async></script>

   Цели (одинаковые идентификаторы в GA4 и Метрике):
     generate_lead  — отправлена заявка с сайта (hc-crm.js → submitLead)
     vacancy_apply  — отправлен отклик на вакансию (hc-crm.js → submitApplication)
     click_phone / click_email / click_telegram / click_whatsapp — клики по контактам
   ============================================================ */
(function () {
  "use strict";

  var GA4_ID = "G-2RE32L3X9T";
  var YM_ID = 113714067; // Яндекс Метрика

  // --- Google Analytics 4 ---
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  if (GA4_ID) {
    gtag("js", new Date());
    gtag("config", GA4_ID);
    load("https://www.googletagmanager.com/gtag/js?id=" + GA4_ID);
  }

  // --- Яндекс Метрика ---
  if (YM_ID) {
    window.ym = window.ym || function () { (window.ym.a = window.ym.a || []).push(arguments); };
    window.ym.l = 1 * new Date();
    load("https://mc.yandex.ru/metrika/tag.js");
    ym(YM_ID, "init", { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });
  }

  function load(src) {
    var s = document.createElement("script");
    s.async = true; s.src = src;
    document.head.appendChild(s);
  }

  // --- цели: hcGoal("generate_lead", { form: "contact" }) ---
  function goal(name, params) {
    try { if (GA4_ID) gtag("event", name, params || {}); } catch (e) {}
    try { if (YM_ID && window.ym) ym(YM_ID, "reachGoal", name, params || {}); } catch (e) {}
  }
  window.hcGoal = goal;

  // --- клики по контактам ---
  var CONTACTS = [
    [/^tel:/i, "click_phone"],
    [/^mailto:/i, "click_email"],
    [/^https?:\/\/(t\.me|telegram\.me)\//i, "click_telegram"],
    [/^https?:\/\/(wa\.me|api\.whatsapp\.com)\//i, "click_whatsapp"]
  ];
  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest && ev.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    for (var i = 0; i < CONTACTS.length; i++) {
      if (CONTACTS[i][0].test(href)) { goal(CONTACTS[i][1], { link_url: href }); return; }
    }
  }, true);
})();
