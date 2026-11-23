# Graph Report - H-C-Site  (2026-11-23)

## Corpus Check
- 15 files · ~133,884 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 580 nodes · 996 edges · 42 communities (28 shown, 14 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 105 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Генерация PDF-отчётов
- Общий шаблон лендингов (CSS, FAB, форма)
- Генераторы страниц (tools/*.py)
- Статьи и отзывы
- Рекрутинг-страница и аналитика
- API: страница статьи
- CRM-мост hc-crm.js
- API: хаб материалов
- API: хаб материалов (2)
- API: хаб материалов (3)
- Калькулятор зарплат
- Vercel и ревалидация
- HR-консалтинг и заявки
- Блоки аналитических статей
- Методология зарплат
- Редактор материалов
- Карточки аналитики
- Админка: данные и SEO
- Опросы и персданные
- Админка: разделы
- Вакансии и отклики
- Lottie-анимации
- Загрузка материалов
- Middleware и пакет
- Фильтры материалов/вакансий
- Раздел Аналитика и шаблон статьи
- Таксономия материалов
- Роли и права
- Блок Статьи по теме
- Маппинг вакансий CRM
- README
- IT-рекрутинг
- Языковые позиции
- Рекрутинг специалистов
- readHTML
- Демо-материалы
- Чипы полей
- Модалка вакансии
- Демо-вакансии

## God Nodes (most connected - your core abstractions)
1. `articlePage()` - 24 edges
2. `esc()` - 23 edges
3. `Employer of Record in Uzbekistan (EOR) & Payroll Services (EN page)` - 19 edges
4. `hr-services.html (HR-услуги в Узбекистане)` - 19 edges
5. `Executive search в Ташкенте – подбор топ-менеджеров (RU page)` - 18 edges
6. `Employer of Record и расчёт зарплаты в Узбекистане (RU page)` - 17 edges
7. `Spec: Analytics section on humancapital.uz (v1, 29.10.2026)` - 16 edges
8. `recruitment.html (Подбор персонала в Ташкенте)` - 16 edges
9. `outstaffing.html (Аутстаффинг)` - 15 edges
10. `hr-services-uzbekistan.html (HR services in Uzbekistan)` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Calculator methodology: resumes from last 90 days, quantiles not means, slices n<30 hidden, gross->net -12%` --semantically_similar_to--> `Processing: medians only, slice shown if >= 10 answers, drop <90s responses`  [INFERRED] [semantically similar]
  analytics-salaries.html → docs/analytics/survey-candidates.md
- `articleSlug` --references--> `articleSlug()`  [EXTRACTED]
  resources.html → api/_lib.js
- `Calculator methodology: resumes from last 90 days, quantiles not means, slices n<30 hidden, gross->net -12%` --semantically_similar_to--> `USD converted at 11 925 UZS/$ (CBU avg Jul-Oct 2026)`  [INFERRED] [semantically similar]
  analytics-salaries.html → docs/analytics/it-salaries-trial-2026-10-29.md
- `Home contactForm (toast only, TODO backend; hc-crm.js loaded)` --conceptually_related_to--> `submit_lead RPC -> Staffly CRM 'Новый лид'`  [AMBIGUOUS]
  index.html → docs/analytics/spec-analytics-section.md
- `GROUPS / SPHERE_OF / EXP taxonomies (23 groups in it/sales/fin)` --semantically_similar_to--> `hh role directory: 25 IT roles mapped into 13 groups`  [INFERRED] [semantically similar]
  analytics-salaries.html → docs/analytics/it-salaries-trial-2026-10-29.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Admin Google sign-in and role-gated access** — admin_google_oauth_login, admin_checksession, admin_site_admins_table, admin_perms, admin_can, admin_applyrolevisibility [EXTRACTED 1.00]
- **EOR page language versions (RU / EN / UZ)** — employer_of_record_page, employer_of_record_uzbekistan_page, employer_of_record_hreflang_cluster [EXTRACTED 1.00]
- **EOR one-partner offer: recruitment + employment + payroll under one contract** — employer_of_record_eor_service, employer_of_record_payroll_service, employer_of_record_recruitment_included, employer_of_record_eor_process [EXTRACTED 1.00]
- **Кнопка звонка в FAB «Связаться» на всех страницах** — analytics_salaries_fab_phone_call_button, analytics_fab_phone_call_button, api_shell_fab_phone_call_button, consulting_fab_phone_call_button, employer_of_record_uzbekistan_fab_phone_call_button, employer_of_record_fab_phone_call_button, executive_search_fab_phone_call_button, hr_services_uzbekistan_fab_phone_call_button, hr_services_fab_phone_call_button, index_fab_phone_call_button, outstaffing_fab_phone_call_button, recruitment_fab_phone_call_button, resources_fab_phone_call_button, vacancies_fab_phone_call_button [EXTRACTED 1.00]
- **Three HR service lines of the hub page (recruitment, outstaffing, HR consulting)** — hr_services_recruitment_executive_search, hr_services_outstaffing_service, hr_services_hr_consulting_audit, hr_services_page [EXTRACTED 1.00]
- **Recruitment Guarantee Package** — recruitment_free_replacement, recruitment_free_trial_day, recruitment_prepayment_refund, recruitment_confidentiality, recruitment_probation_support [EXTRACTED 1.00]
- **Recruitment Formats Offered** — recruitment_specialist_recruitment, recruitment_executive_search, recruitment_it_recruiting, recruitment_mass_recruitment, recruitment_language_positions [EXTRACTED 1.00]
- **Personal data consent and privacy obligations** — privacy_policy, privacy_law_zru_547, docs_analytics_spec_analytics_section_pd_localization_issue, docs_analytics_survey_candidates_separate_raffle_form, docs_analytics_survey_hr_directors_hr_directors_survey [INFERRED 0.75]
- **Analytics section implementation (spec -> generated pages -> taxonomy)** — docs_analytics_spec_analytics_section_spec_doc, docs_analytics_spec_analytics_section_analytics_page_spec, docs_analytics_spec_analytics_section_build_analytics_tool, analytics_page, analytics_tax, analytics_salaries_page [INFERRED 0.85]
- **Material publishing flow: admin editor to Supabase to public Useful Materials page** — admin_matmodal, admin_wiremateditor, admin_matuploadimage, admin_pushcrm, admin_site_materials_table, admin_refreshsitecache, resources_materials_api, resources_loadmaterials [INFERRED 0.85]
- **Minimum-sample publication rules across salary data sources** — docs_analytics_it_salaries_trial_2026_10_29_n30_threshold, docs_analytics_survey_candidates_salary_processing_rules, docs_analytics_survey_hr_directors_slice_min_5_companies, analytics_salaries_methodology [INFERRED 0.85]
- **Outstaffing value proposition (BPO focus, multilingual pool, IT Park, turnkey scope)** — outstaffing_bpo_specialization, outstaffing_language_talent_pool, outstaffing_it_park_residency, outstaffing_service_scope, outstaffing_advantages [INFERRED 0.85]
- **Lead Capture Flow** — recruitment_contactform, recruitment_contact_form_submit_handler, recruitment_lead_backend_todo, recruitment_fab_contact_widget [INFERRED 0.85]
- **Vacancy browse and apply flow via HCCRM** — vacancies_loadvacancies, vacancies_cardhtml, vacancies_detailhtml, vacancies_applyhtml, vacancies_bindapply, vacancies_hccrm_bridge [INFERRED 0.85]
- **Duplicated client-side lead capture forms with pending CRM backend** — hr_services_contact_form, hr_services_uzbekistan_contact_form, outstaffing_contact_form [INFERRED 0.95]
- **Service landing pages built on the shared lp-/hrs- template** — employer_of_record_page, employer_of_record_uzbekistan_page, executive_search_page, employer_of_record_landing_page_template [INFERRED 0.95]

## Communities (42 total, 14 thin omitted)

### Community 0 - "Генерация PDF-отчётов"
Cohesion: 0.07
Nodes (24): bars(), build(), bars(), grp_table(), head(), page(), e(), e() (+16 more)

### Community 1 - "Общий шаблон лендингов (CSS, FAB, форма)"
Cohesion: 0.07
Nodes (52): Client reviews (Satori Capital, TEZBULUT, KAN Dental Clinic), Contact form #contactForm (toast on submit, CRM backend TODO, hc-crm.js), Shared site CSS design system (mustard/black tokens, self-hosted Inter and Unbounded fonts, hero aurora, nav, FAB), Employer of Record (EOR) for foreign companies without a local entity, FAB «Связаться»: кнопка звонка tel:+998903251336 (hr-services.html), FAQ accordion: HR-услуги в Узбекистане (8 questions), Guarantees: free replacement, search guarantee (3 candidates or refund), free trial day, confidentiality, 8-step HR process (Заявка, Анализ, Договор, Поиск, Оценка, Интервью, Выход, Адаптация) (+44 more)

### Community 2 - "Генераторы страниц (tools/*.py)"
Cohesion: 0.08
Nodes (21): build(), shell(), absolutize(), build(), acc(), build(), main(), reviews_from() (+13 more)

### Community 3 - "Статьи и отзывы"
Cohesion: 0.06
Nodes (41): Article: Hiring in Uzbekistan (guide for foreign companies), Article: What a support agent costs in 2026, Article: Интервью по компетенциям, Article: IT salaries in Uzbekistan, autumn 2026, Article: Как выбрать кадровое агентство в Ташкенте, Article: Современные методы оценки кандидатов, Client reviews: Satori Capital, TEZBULUT, KAN Dental Clinic, Contact form (#contactForm) with service select and TODO backend to /api/leads (+33 more)

### Community 4 - "Рекрутинг-страница и аналитика"
Cohesion: 0.06
Nodes (34): CLAUDE.md: правила graphify (query перед grep/чтением, update после правок), load(), 8-Step Recruitment Process (request to adaptation), Recruitment Automation Orbit (AI tools + recruiter expertise), AI Resume Analysis Tools, Confidentiality Guarantee, Contact Form Submit Handler (toast + reset), Contact Section (phone, email, WhatsApp, socials) (+26 more)

### Community 5 - "API: страница статьи"
Cohesion: 0.12
Nodes (37): ALLOWED, articlePage(), attr(), authorHTML(), authorLD(), authorsOf(), clip(), ctaHTML() (+29 more)

### Community 6 - "CRM-мост hc-crm.js"
Cohesion: 0.16
Nodes (31): amsg(), applyAttempt(), applyError(), consentMarkup(), consentOk(), goal(), honeypot(), initReport() (+23 more)

### Community 7 - "API: хаб материалов"
Cohesion: 0.13
Nodes (21): articlePath(), articleSlug(), cache, loadMaterials(), PAGES, pageUrl(), TR, vacancyPath() (+13 more)

### Community 8 - "API: хаб материалов (2)"
Cohesion: 0.18
Nodes (13): build(), date10(), fs, L, materials(), materialsList(), pageConst(), PAGES (+5 more)

### Community 9 - "API: хаб материалов (3)"
Cohesion: 0.25
Nodes (15): block(), clip(), employmentType(), fs, isOnsite(), isRemote(), lines(), notFoundPage() (+7 more)

### Community 10 - "Калькулятор зарплат"
Cohesion: 0.16
Nodes (10): Executive search box: IT leads / C-level 6+ yrs $4 000–10 000, FAB «Связаться»: кнопка звонка tel:+998903251336 (analytics-salaries.html), init() – fetch /api/salaries, Calculator lead form ('Получить расчёт') sent by hc-crm.js, Salary calculator page: IT, sales, finance (RU, generated by build_salaries.py), render() – median, IQR, p90, USD share, experience ladder, vacancy forks, spheres(), syncLead() – calculator context into hidden lead message (+2 more)

### Community 11 - "Vercel и ревалидация"
Cohesion: 0.14
Nodes (11): includeFiles, includeFiles, includeFiles, functions, api/article.js, api/hub.js, api/vacancy.js, headers (+3 more)

### Community 12 - "HR-консалтинг и заявки"
Cohesion: 0.18
Nodes (13): renderRequests, reqViewModal, Supabase RPC site_applications, Staffly sales CRM (site_leads_count), Accordion service cards (.cons-acc), Consulting contact form, FAB «Связаться»: кнопка звонка tel:+998903251336 (consulting.html), HR Consulting page (HR-консалтинг) (+5 more)

### Community 13 - "Блоки аналитических статей"
Cohesion: 0.23
Nodes (13): load() – fetch /api/materials filtered by rubric and lang, TAX taxonomy constant (rubrics, industries, authors, telegram), admin.html analytics fields and publish validation, CTA variants: consult / download / subscribe, Gated report form -> PDF on request only, Industry taxonomy v1 (general, it, finance, retail, ... public), Key figures block (.ar-kf-), Methodology block (methodology / period / sample_size) (+5 more)

### Community 14 - "Методология зарплат"
Cohesion: 0.18
Nodes (9): GROUPS / SPHERE_OF / EXP taxonomies (23 groups in it/sales/fin), note() – methodology footnote, hh role directory: 25 IT roles mapped into 13 groups, it_salaries.sql / build_hh_roles.py / hh_roles.csv (ATS repo db/analytics), Middle costs ~2x junior (8.0 -> 14.3 mln UZS), RecruitPro ATS (candidate data source), IT salary expectations trial export (29.10.2026), USD converted at 11 925 UZS/$ (CBU avg Jul-Oct 2026) (+1 more)

### Community 15 - "Редактор материалов"
Cohesion: 0.17
Nodes (12): AN_STRICT strict analytics rubrics, hcSanitizePaste, MAT_AUD audience tabs, matAnalyticsData, matAnalyticsHTML, matModal (material editor), renderMaterials, TAXONOMY (rubrics, industries, authors) (+4 more)

### Community 16 - "Карточки аналитики"
Cohesion: 0.21
Nodes (11): articleUrl() – mirrors api/_lib.js articleSlug, card(), featured() – flagship annual/salary material, filters() – rubric chips and industry select, fmtDate() (analytics), imgOf(), init(), render() – filter list, sync URL ?rubric&industry (+3 more)

### Community 17 - "Админка: данные и SEO"
Cohesion: 0.27
Nodes (11): checkSession, loadAllData, matRow, matUploadImage, pushCRM (Supabase persistence), sendInvite, Supabase table seo_pages, Supabase table site_admins (admin whitelist) (+3 more)

### Community 18 - "Опросы и персданные"
Cohesion: 0.24
Nodes (7): Candidate survey 'Работа и зарплаты 2026', Q7: expected income increase on job change, HR directors survey 'Найм и зарплаты: итоги 2026, планы 2027', Q13: planned salary indexation 2027, Public talent pool shows only anonymised data with separate consent, Law of Uzbekistan 'On Personal Data' ZRU-547, Personal data processing policy (RU, draft v1)

### Community 19 - "Админка: разделы"
Cohesion: 0.20
Nodes (10): custModal, empModal, go (section router), renderAnalytics, renderCustomers, renderEmployees, renderOverview, renderSeo (+2 more)

### Community 20 - "Вакансии и отклики"
Cohesion: 0.20
Nodes (10): renderVacancies, Supabase table vacancies (ATS), vacModal, applyHTML (application form), bindApply, FAB «Связаться»: кнопка звонка tel:+998903251336 (vacancies.html), window.HCCRM bridge (hc-crm.js), JobPosting markup on /vacancies/<slug> (api/vacancy.js) (+2 more)

### Community 21 - "Lottie-анимации"
Cohesion: 0.36
Nodes (9): later(), load(), request(), start(), halt(), run(), sync(), tick() (+1 more)

### Community 22 - "Загрузка материалов"
Cohesion: 0.22
Nodes (9): Admin Panel (Панель управления), Google OAuth Login via Supabase, refreshSiteCache, FAB «Связаться»: кнопка звонка tel:+998903251336 (resources.html), loadMaterials, mapDbMaterial, /api/materials endpoint, PAGE_LANG (+1 more)

### Community 23 - "Middleware и пакет"
Cohesion: 0.25
Nodes (6): config, dependencies, @vercel/functions@3.10.1, description, private, @vercel/functions

### Community 24 - "Фильтры материалов/вакансий"
Cohesion: 0.22
Nodes (9): applyFilters (materials), articleSlug, articleUrl, cardHTML (material card), render (materials), thumbSrc, applyFilters (vacancies), cardHTML (vacancy card) (+1 more)

### Community 25 - "Раздел Аналитика и шаблон статьи"
Cohesion: 0.32
Nodes (8): FAB «Связаться»: кнопка звонка tel:+998903251336 (analytics.html), Analytics section page (RU, generated by build_analytics.py), Article page shell template ({{HEAD}} / {{MAIN}}), Shell navigation menu incl. 'Аналитика' link, FAB «Связаться»: кнопка звонка tel:+998903251336 (api/_shell.html), /analytics section page spec (hero, featured report, rubric/industry filters in URL), tools/build_analytics.py (generates analytics*.html), robots.txt: allow all + sitemap humancapital.uz/sitemap.xml

### Community 26 - "Таксономия материалов"
Cohesion: 0.33
Nodes (6): AUTHORS constant (akmal, anna, team) with schema.org Person, Home contactForm (toast only, TODO backend; hc-crm.js loaded), FAB «Связаться»: кнопка звонка tel:+998903251336 (index.html), Founders section: Anna Dju (CEO), Akmal Saipov (CCO), Home page (RU) – recruiting agency in Uzbekistan, Organization/EmploymentAgency + WebSite JSON-LD

### Community 27 - "Роли и права"
Cohesion: 0.50
Nodes (4): applyRoleVisibility, can, enterApp, PERMS role permission matrix

## Ambiguous Edges - Review These
- `Supabase RPC site_applications` → `Prescreening (IT/BPO resumes and vendor proposals)`  [AMBIGUOUS]
  consulting.html · relation: conceptually_related_to
- `submit_lead RPC -> Staffly CRM 'Новый лид'` → `Home contactForm (toast only, TODO backend; hc-crm.js loaded)`  [AMBIGUOUS]
  index.html · relation: conceptually_related_to
- `recruitment.html (Подбор персонала в Ташкенте)` → `startRoadmap()`  [AMBIGUOUS]
  recruitment.html · relation: references

## Knowledge Gaps
- **83 isolated node(s):** `reqViewModal`, `matRow`, `Public talent pool shows only anonymised data with separate consent`, `renderOverview`, `Google Search Console / Looker Studio embed` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 175 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Employer of Record и расчёт зарплаты в Узбекистане (RU page)` connect `Статьи и отзывы` to `Общий шаблон лендингов (CSS, FAB, форма)`, `Рекрутинг-страница и аналитика`, `CRM-мост hc-crm.js`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `reqViewModal`, `matRow`, `Public talent pool shows only anonymised data with separate consent` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Генерация PDF-отчётов` be split into smaller, more focused modules?**
  _Cohesion score 0.0734006734006734 - nodes in this community are weakly interconnected._
- **Why does `recruitment.html (Подбор персонала в Ташкенте)` connect `Рекрутинг-страница и аналитика` to `Статьи и отзывы`, `CRM-мост hc-crm.js`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `Общий шаблон лендингов (CSS, FAB, форма)` be split into smaller, more focused modules?**
  _Cohesion score 0.06787330316742081 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Supabase RPC site_applications` and `Prescreening (IT/BPO resumes and vendor proposals)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `submit_lead RPC -> Staffly CRM 'Новый лид'` and `Home contactForm (toast only, TODO backend; hc-crm.js loaded)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._