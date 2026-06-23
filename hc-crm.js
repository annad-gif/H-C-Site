/* ============================================================
   Human and Capital — интеграция сайта с Supabase
   ATS (RecruitPro)  : вакансии, отклики, кадровый резерв
   Staffly CRM       : заявки с сайта (воронка → «Новый лид»)

   Подключается одной строкой на каждой странице:
     <script src="hc-crm.js" defer></script>

   Серверная часть — в файлах ats_setup.sql и staffly_setup.sql
   (функции submit_lead / apply_to_vacancy и витрины public_*).
   ============================================================ */
(function () {
  "use strict";

  // --- проекты Supabase (anon-ключи публичные, это безопасно) ---
  var ATS = {
    url: "https://byerqfuuprmmykncjqms.supabase.co",
    key: "sb_publishable_JBo7zlA02IyeaJLuTdZX5A_YEatYU6_"
  };
  var STAFFLY = {
    url: "https://qgwfecctozkchcjabgsx.supabase.co",
    key: "sb_publishable_BZze9MRJ37YtILL6qWtfHA_N7NF7Ql6"
  };
  var PRIVACY_URL = "privacy.html";
  var POLICY_VERSION = "v1";

  // --- клиент supabase-js (грузим динамически с CDN) ---
  var _sb = null;
  async function sb() {
    if (_sb) return _sb;
    var m = await import("https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm");
    _sb = {
      ats: m.createClient(ATS.url, ATS.key, { auth: { persistSession: false } }),
      staffly: m.createClient(STAFFLY.url, STAFFLY.key, { auth: { persistSession: false } })
    };
    return _sb;
  }

  // --- helpers ---
  function txt(v) { return (v == null ? "" : String(v)).trim(); }
  function lines(s) {
    return txt(s).split(/\r?\n|•|·|;/).map(function (x) { return x.trim(); }).filter(Boolean);
  }
  function val(id) { var el = document.getElementById(id); return el ? txt(el.value) : ""; }
  function node(html) {
    var t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild;
  }
  function locale() { return (document.documentElement.lang || "ru").slice(0, 2); }

  // --- toast ---
  function toast(msg, ok) {
    var t = document.getElementById("hcToast");
    if (!t) {
      t = node('<div id="hcToast" style="position:fixed;left:50%;bottom:28px;transform:translateX(-50%);background:#0e0e0d;color:#fff;padding:14px 22px;border-radius:12px;font-size:14px;z-index:99999;opacity:0;transition:opacity .3s;max-width:90vw;box-shadow:0 12px 40px rgba(0,0,0,.35)"></div>');
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.borderLeft = (ok === false ? "3px solid #ef4444" : "3px solid #22c55e");
    t.style.opacity = "1";
    clearTimeout(t._h); t._h = setTimeout(function () { t.style.opacity = "0"; }, 4400);
  }

  // --- consent checkbox injection ---
  function consentMarkup(id) {
    return '<label class="hc-consent" style="display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.45;margin:4px 0 14px;color:#4a4844;cursor:pointer">' +
      '<input type="checkbox" id="' + id + '" style="margin-top:3px;width:16px;height:16px;flex:0 0 auto;accent-color:#c69a2e">' +
      '<span>Я даю согласие на обработку моих персональных данных в соответствии с ' +
      '<a href="' + PRIVACY_URL + '" target="_blank" rel="noopener" style="color:#8a701f;text-decoration:underline">Политикой обработки персональных данных</a>.</span>' +
      '</label>';
  }
  function injectConsent(form, id) {
    if (!form || document.getElementById(id)) return;
    var btn = form.querySelector('button[type="submit"], button:not([type]), input[type="submit"]');
    var n = node(consentMarkup(id));
    if (btn && btn.parentNode) btn.parentNode.insertBefore(n, btn);
    else form.appendChild(n);
  }
  function consentOk(id) { var c = document.getElementById(id); return !!(c && c.checked); }

  // --- honeypot (анти-спам) ---
  function honeypot(form) {
    if (form.querySelector(".hc-hp")) return;
    form.appendChild(node('<input class="hc-hp" type="text" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:0;height:0;opacity:0">'));
  }
  function isBot(form) { var h = form.querySelector(".hc-hp"); return !!(h && h.value); }

  // === ЗАЯВКИ → Staffly (deals, этап «Новый лид») ===
  async function submitLead(form) {
    if (isBot(form)) return { ok: true };
    if (!consentOk("hcLeadConsent")) { toast("Отметьте согласие на обработку данных", false); return { ok: false }; }
    var name = val("name"), email = val("email"), phone = val("phone"),
        company = val("company"), message = val("message");
    var service = (document.getElementById("service") || {}).value || "";
    if (!name) { toast("Укажите имя", false); return { ok: false }; }
    if (!email && !phone) { toast("Укажите телефон или email", false); return { ok: false }; }
    var head = (service ? "Услуга: " + service + "\n" : "") + (company ? "Компания: " + company + "\n" : "");
    var msg = head + message;
    try {
      var c = await sb();
      var r = await c.staffly.rpc("submit_lead", {
        p_name: name, p_email: email || null, p_phone: phone || null,
        p_message: msg || null, p_service: null,
        p_source: "Сайт: " + location.pathname, p_locale: locale(), p_consent: true
      });
      if (r.error) throw r.error;
      form.reset(); toast("Заявка отправлена! Мы свяжемся с вами."); return { ok: true };
    } catch (e) { console.error("submitLead", e); toast("Не удалось отправить. Попробуйте позже.", false); return { ok: false }; }
  }

  // === ВАКАНСИИ ← ATS (витрина public_vacancies) ===
  async function loadVacancies() {
    try {
      var c = await sb();
      var r = await c.ats.from("public_vacancies").select("*").order("created_at", { ascending: false });
      if (r.error) throw r.error;
      return (r.data || []).map(function (v) {
        var salary = "";
        if (v.budget) { try { salary = new Intl.NumberFormat("ru-RU").format(v.budget) + " UZS"; } catch (e) { salary = v.budget + " UZS"; } }
        return {
          id: v.id, field: "", title: txt(v.title), company: "", city: txt(v.location),
          salary: salary, type: txt(v.type),
          responsibilities: lines(v.description), requirements: lines(v.requirements), offer: lines(v.offer)
        };
      });
    } catch (e) { console.error("loadVacancies", e); return []; }
  }

  // === КАДРОВЫЙ РЕЗЕРВ ← ATS (витрина public_talent, без ПДн) ===
  async function loadTalent() {
    try {
      var c = await sb();
      var r = await c.ats.from("public_talent").select("*").order("created_at", { ascending: false });
      if (r.error) throw r.error;
      return (r.data || []).map(function (t) {
        var extra = [];
        if (t.field) extra.push("Сфера: " + t.field);
        if (t.format) extra.push("Формат: " + t.format);
        if (t.age) extra.push("Возраст: " + t.age);
        var head = txt(t.role) || txt(t.field);
        if (t.level) head = head ? head + " · " + txt(t.level) : txt(t.level);
        return {
          id: t.id, field: head, date: txt(t.created_at).slice(0, 10),
          city: txt(t.city), experience: txt(t.experience), results: txt(t.results),
          salary: "", languages: txt(t.languages), skills: Array.isArray(t.skills) ? t.skills : [],
          description: [txt(t.summary), extra.join(" · ")].filter(Boolean).join("\n")
        };
      });
    } catch (e) { console.error("loadTalent", e); return []; }
  }

  // === ОТКЛИК → ATS (резюме в Storage + apply_to_vacancy) ===
  async function submitApplication(vacancyId) {
    if (!consentOk("vcConsent")) { toast("Отметьте согласие на обработку данных", false); return { ok: false }; }
    var name = val("apName"), phone = val("apPhone"), email = val("apEmail");
    if (!name) { toast("Укажите имя", false); return { ok: false }; }
    if (!email && !phone) { toast("Укажите телефон или email", false); return { ok: false }; }
    var fileInput = document.getElementById("vcFile");
    var file = fileInput && fileInput.files && fileInput.files[0];
    try {
      var c = await sb();
      var resume_url = null, resume_name = null, resume_size = null;
      if (file) {
        if (file.size > 10 * 1024 * 1024) { toast("Файл резюме больше 10 МБ", false); return { ok: false }; }
        var safe = file.name.replace(/[^\w.\-]+/g, "_");
        var uid = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now());
        var path = "site/" + (vacancyId || "general") + "/" + uid + "-" + safe;
        var up = await c.ats.storage.from("resumes").upload(path, file, { upsert: false });
        if (up.error) throw up.error;
        resume_url = c.ats.storage.from("resumes").getPublicUrl(path).data.publicUrl;
        resume_name = file.name; resume_size = file.size;
      }
      var position = [
        val("apExp") ? "Опыт: " + val("apExp") : "",
        val("apSkills") ? "Навыки: " + val("apSkills") : "",
        val("apCity") ? "Город: " + val("apCity") : "",
        val("apMsg")
      ].filter(Boolean).join(" · ");
      var r = await c.ats.rpc("apply_to_vacancy", {
        p_vacancy_id: vacancyId || null, p_name: name, p_email: email || null, p_phone: phone || null,
        p_position: position || null, p_resume_name: resume_name, p_resume_url: resume_url,
        p_resume_size: resume_size, p_locale: locale(), p_consent: true
      });
      if (r.error) throw r.error;
      toast("Отклик отправлен! Спасибо."); return { ok: true };
    } catch (e) { console.error("submitApplication", e); toast("Не удалось отправить отклик. Попробуйте позже.", false); return { ok: false }; }
  }

  // --- авто-подключение ---
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var lead = document.getElementById("contactForm");
    if (lead) {
      injectConsent(lead, "hcLeadConsent");
      honeypot(lead);
      lead.addEventListener("submit", function (ev) {
        ev.preventDefault(); ev.stopPropagation(); submitLead(lead);
      }, true);
    }
    // форма отклика появляется в модалке позже — следим за DOM
    var obs = new MutationObserver(function () {
      var af = document.getElementById("vcApplyForm");
      if (af && !af.dataset.hcReady) { af.dataset.hcReady = "1"; injectConsent(af, "vcConsent"); honeypot(af); }
    });
    obs.observe(document.body, { childList: true, subtree: true });
  });

  window.HCCRM = {
    loadVacancies: loadVacancies, loadTalent: loadTalent,
    submitApplication: submitApplication, submitLead: submitLead,
    config: { POLICY_VERSION: POLICY_VERSION }
  };
})();
