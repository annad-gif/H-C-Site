"""Страницы раздела «Аналитика»: analytics.html, analytics-en.html, analytics-uz.html.

Оболочка (head со стилями, меню, подвал, кнопка «Связаться», скрипт меню) берётся из resources*.html
того же языка; содержимое и скрипт – ниже. Материалы раздела – site_materials с заполненным rubric
(ТЗ: docs/analytics/spec-analytics-section.md, §2). Рубрики, отрасли, авторы, ссылка на Telegram –
api/_taxonomy.json.

Запускать после правок меню/подвала в resources*.html или текстов ниже:
    python3 tools/build_analytics.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://humancapital.uz"
TAX = json.load(open(os.path.join(ROOT, "api", "_taxonomy.json"), encoding="utf-8"))
FILES = {"ru": "analytics.html", "en": "analytics-en.html", "uz": "analytics-uz.html"}
SRC = {"ru": "resources.html", "en": "resources-en.html", "uz": "resources-uz.html"}

T = {
    "ru": dict(
        title="Аналитика рынка труда Узбекистана – Human and Capital",
        desc="Аналитика Human and Capital: зарплатные обзоры, пульс рынка труда, практика найма и кейсы на данных наших проектов в Узбекистане.",
        eyebrow="Аналитика · данные наших проектов",
        h1="Аналитика рынка труда Узбекистана",
        lead="Зарплаты, спрос на специалистов и сроки найма – на данных подбора Human and Capital и открытой статистики. В каждом материале – методология и размер выборки.",
        feat="Главный обзор", feat_a="Читать обзор →", all="Все", all_ind="Все отрасли", ind_label="Отрасль",
        shown="Показано <b>{n}</b> из {m}", count="Материалов: {n}", loading="Загрузка…",
        empty_none="Скоро здесь появятся первые обзоры.", empty_filter="По выбранным фильтрам материалов пока нет.",
        tg="Подписаться в Telegram", read="Читать",
        cta_h="Нужны данные по вашей отрасли или позиции?",
        cta_p="Подготовим срез зарплат и сроков найма под вашу задачу и поможем закрыть вакансию.",
        cta_a="Обсудить найм →", cta_url="recruitment.html#contact", locale="ru-RU", og="ru_RU"),
    "en": dict(
        title="Uzbekistan Labour Market Insights – Human and Capital",
        desc="Human and Capital insights: salary reviews, labour market pulse, hiring practice and case studies based on our recruitment data in Uzbekistan.",
        eyebrow="Insights · our recruitment data",
        h1="Uzbekistan Labour Market Insights",
        lead="Salaries, talent demand and time to hire – based on Human and Capital recruitment data and open statistics. Every piece states its methodology and sample size.",
        feat="Featured review", feat_a="Read the review →", all="All", all_ind="All industries", ind_label="Industry",
        shown="Showing <b>{n}</b> of {m}", count="Materials: {n}", loading="Loading…",
        empty_none="The first reviews will appear here soon.", empty_filter="No materials for the selected filters yet.",
        tg="Follow on Telegram", read="Read",
        cta_h="Need data for your industry or role?",
        cta_p="We will prepare salary and time-to-hire benchmarks for your task and help you fill the role.",
        cta_a="Discuss hiring →", cta_url="hr-services-uzbekistan.html#contact", locale="en-GB", og="en_US"),
    "uz": dict(
        title="O‘zbekiston mehnat bozori tahlili – Human and Capital",
        desc="Human and Capital tahlili: maosh sharhlari, mehnat bozori pulsi, yollash amaliyoti va O‘zbekistondagi loyihalarimiz ma’lumotlari asosidagi keyslar.",
        eyebrow="Tahlil · loyihalarimiz ma’lumotlari",
        h1="O‘zbekiston mehnat bozori tahlili",
        lead="Maoshlar, mutaxassislarga talab va yollash muddatlari – Human and Capital loyihalari va ochiq statistika asosida. Har bir materialda metodologiya va tanlov hajmi ko‘rsatiladi.",
        feat="Asosiy sharh", feat_a="Sharhni o‘qish →", all="Barchasi", all_ind="Barcha sohalar", ind_label="Soha",
        shown="<b>{n}</b> / {m} ko‘rsatilmoqda", count="Materiallar: {n}", loading="Yuklanmoqda…",
        empty_none="Birinchi sharhlar tez orada shu yerda paydo bo‘ladi.", empty_filter="Tanlangan filtrlar bo‘yicha hozircha materiallar yo‘q.",
        tg="Telegramda obuna bo‘lish", read="O‘qish",
        cta_h="Sohangiz yoki lavozimingiz bo‘yicha ma’lumot kerakmi?",
        cta_p="Vazifangiz uchun maoshlar va yollash muddatlari kesimini tayyorlaymiz va vakansiyani yopishga yordam beramiz.",
        cta_a="Muhokama qilish →", cta_url="recruitment-uz.html#contact", locale="uz-Latn-UZ", og="uz_UZ"),
}

CSS = """
/* ---------- раздел «Аналитика» (tools/build_analytics.py) ---------- */
.an-hero{padding:132px 0 56px;background:var(--black);position:relative;overflow:hidden;}
.an-hero .rs-count{margin-bottom:14px;}
.an-hero h1{font-family:var(--ff-display);font-weight:700;color:var(--white);font-size:clamp(32px,4.8vw,56px);line-height:1.06;margin:0 0 16px;max-width:820px;}
.an-hero .lead{color:var(--grey-300);font-size:17px;line-height:1.6;max-width:680px;}
.an-tg{display:inline-flex;align-items:center;gap:8px;margin-top:26px;padding:13px 20px;border-radius:12px;background:var(--mustard);color:var(--black);font-weight:600;text-decoration:none;}
.an-tg:hover{background:var(--mustard-light);}
.an-tg[hidden]{display:none;}
.an-feat{display:grid;grid-template-columns:1.1fr 1fr;gap:0;margin-top:40px;border-radius:20px;overflow:hidden;background:var(--black-soft);border:1px solid rgba(255,255,255,.08);text-decoration:none;color:var(--white);}
.an-feat[hidden]{display:none;}
.an-feat-img{min-height:240px;background:linear-gradient(135deg,#8a701f,#0e0e0d);}
.an-feat-img img{width:100%;height:100%;object-fit:cover;display:block;}
.an-feat-body{padding:30px 32px;display:flex;flex-direction:column;gap:12px;justify-content:center;}
.an-feat-k{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mustard-light);}
.an-feat-body h2{font-family:var(--ff-display);font-weight:600;font-size:clamp(20px,2.4vw,28px);line-height:1.25;}
.an-feat-body p{color:var(--grey-300);font-size:15px;line-height:1.55;}
.an-feat-body b{color:var(--mustard-light);font-weight:600;margin-top:4px;}
.an-feat:hover .an-feat-body b{color:var(--white);}
#an-list{background:var(--grey-50);padding:40px 0 90px;}
.an-filters{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;justify-content:space-between;margin-bottom:26px;}
.an-chips{display:flex;flex-wrap:wrap;gap:8px;}
.an-chips[hidden]{display:none;}
.an-chip{padding:9px 16px;border-radius:999px;border:1px solid var(--grey-100);background:var(--white);color:var(--grey-700);font-size:13.5px;cursor:pointer;transition:all .2s;white-space:nowrap;font-family:inherit;}
.an-chip:hover{border-color:var(--mustard);color:var(--black);}
.an-chip.active{background:var(--black);border-color:var(--black);color:var(--white);font-weight:600;}
.an-ind{display:flex;align-items:center;gap:10px;font-size:13.5px;color:var(--grey-700);}
.an-ind select{padding:9px 34px 9px 14px;border-radius:10px;border:1px solid var(--grey-100);background:var(--white);font:inherit;color:var(--black);cursor:pointer;max-width:100%;}
.an-ind[hidden]{display:none;}
.an-shown{font-size:13.5px;color:var(--grey-700);margin-bottom:18px;}
.an-shown b{color:var(--black);}
.an-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}
.an-card{display:flex;flex-direction:column;background:var(--white);border:1px solid var(--grey-100);border-radius:18px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .25s,border-color .25s,box-shadow .25s;}
.an-card:hover{transform:translateY(-4px);border-color:var(--mustard);box-shadow:0 18px 40px rgba(14,14,13,.10);}
.an-thumb{position:relative;aspect-ratio:16/10;background:linear-gradient(135deg,#2a2a28,#0e0e0d);overflow:hidden;}
.an-thumb img{width:100%;height:100%;object-fit:cover;display:block;}
.an-badge{position:absolute;top:12px;left:12px;font-size:11px;letter-spacing:.05em;text-transform:uppercase;font-weight:600;padding:5px 10px;border-radius:999px;background:rgba(14,14,13,.78);color:var(--mustard-light);}
.an-body{padding:16px 18px 20px;display:flex;flex-direction:column;gap:8px;flex:1;}
.an-meta{font-size:12px;color:var(--grey-500);}
.an-body h3{font-family:var(--ff-display);font-weight:600;font-size:17px;line-height:1.32;color:var(--black);}
.an-body p{font-size:13.5px;line-height:1.55;color:var(--grey-700);}
.an-empty{padding:48px 20px;text-align:center;color:var(--grey-500);font-size:15px;background:var(--white);border:1px dashed var(--grey-100);border-radius:18px;}
.an-skel{height:300px;border-radius:18px;background:linear-gradient(90deg,#efefed,#f7f7f5,#efefed);background-size:200% 100%;animation:anSk 1.4s infinite;}
@keyframes anSk{to{background-position:-200% 0;}}
.an-cta{margin-top:48px;padding:32px 34px;border-radius:20px;background:var(--black);color:var(--white);display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap;}
.an-cta h2{font-family:var(--ff-display);font-weight:600;font-size:22px;line-height:1.3;margin-bottom:6px;}
.an-cta p{color:var(--grey-300);font-size:15px;line-height:1.5;max-width:520px;}
.an-cta a{display:inline-flex;padding:14px 22px;border-radius:12px;background:var(--mustard);color:var(--black);font-weight:600;text-decoration:none;white-space:nowrap;}
.an-cta a:hover{background:var(--mustard-light);}
@media (max-width:980px){ .an-grid{grid-template-columns:repeat(2,1fr);} .an-feat{grid-template-columns:1fr;} .an-feat-img{min-height:180px;aspect-ratio:16/8;} }
@media (max-width:640px){
  .an-hero{padding:110px 0 40px;} .an-grid{grid-template-columns:1fr;}
  .an-feat-body{padding:22px 20px;} .an-cta{padding:26px 22px;}
  .an-chips{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;margin:0 -18px;padding-left:18px;padding-right:18px;scrollbar-width:none;}
  .an-chips::-webkit-scrollbar{display:none;}
  .an-ind,.an-ind select{width:100%;}
}
"""

MAIN = """
<section class="an-hero" id="home">
  <div class="container">
    <p class="rs-count"><span class="dot"></span><span>{eyebrow}</span></p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <a class="an-tg" id="anTg" href="#" target="_blank" rel="noopener" hidden>{tg}</a>
    <a class="an-feat" id="anFeat" href="#" hidden></a>
  </div>
</section>

<section id="an-list">
  <div class="container">
    <div class="an-filters">
      <div class="an-chips" id="anChips" role="tablist"></div>
      <label class="an-ind" id="anIndWrap" hidden>{ind_label}<select id="anInd"></select></label>
    </div>
    <p class="an-shown" id="anShown"></p>
    <div class="an-grid" id="anGrid"></div>
    <div class="an-cta">
      <div><h2>{cta_h}</h2><p>{cta_p}</p></div>
      <a href="{cta_url}">{cta_a}</a>
    </div>
  </div>
</section>
"""

JS = r"""
const PAGE_LANG = %(lang)s;
const T = %(t)s;
const TAX = %(tax)s;
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function lbl(o){ return o ? (o[PAGE_LANG] || o.ru) : ''; }
// адрес статьи /articles/<slug> – та же функция в api/_lib.js (articleSlug), менять синхронно
const SLUG_TR={"а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"yo","ж":"zh","з":"z","и":"i","й":"y","к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"kh","ц":"ts","ч":"ch","ш":"sh","щ":"sch","ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya","ў":"o","қ":"q","ғ":"g","ҳ":"h","‘":"","’":"","ʻ":"","ʼ":"","'":""};
function articleUrl(m){
  const base=String(m.title||'').toLowerCase().split('').map(c=>(c in SLUG_TR?SLUG_TR[c]:c)).join('')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,70).replace(/-+$/,'');
  const id=String(m.id).slice(0,8); return '/articles/'+(base?base+'-'+id:id);
}
// узбекских месяцев в браузерах часто нет («2026 M10 29») – формат как у api/article.js на сервере: «23-oktabr, 2026»
const UZ_MONTHS=['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentabr','oktabr','noyabr','dekabr'];
function fmtDate(iso){ if(PAGE_LANG==='uz'){ const d=new Date(new Date(iso).getTime()+5*3600000); if(!isNaN(d)) return d.getUTCDate()+'-'+UZ_MONTHS[d.getUTCMonth()]+', '+d.getUTCFullYear(); }
  try{ return new Intl.DateTimeFormat(T.locale,{day:'numeric',month:'long',year:'numeric',timeZone:'Asia/Tashkent'}).format(new Date(iso)).replace(/\s*г\.$/,''); }catch(e){ return String(iso||'').slice(0,10); } }
function imgOf(m){ return (m.media_type==='image'||m.media_type==='photo') && /^(https?:\/\/|\/)/.test(m.media_url||'') ? m.media_url : ''; }
function authorName(m){ return String(m.author_key||'').split(',').map(k=>TAX.authors[k.trim()]).filter(Boolean).map(a=>lbl(a.name)).join(', '); }

const grid=document.getElementById('anGrid'), chipsEl=document.getElementById('anChips'),
  indWrap=document.getElementById('anIndWrap'), indSel=document.getElementById('anInd'),
  shownEl=document.getElementById('anShown'), feat=document.getElementById('anFeat');
let ALL=[], rubric='', industry='';

async function load(){
  // лёгкий список с CDN сайта (api/materials.js) – без полного HTML статей
  const r=await fetch('/api/materials');
  if(!r.ok) throw new Error('materials '+r.status);
  const rows=(await r.json()).filter(m=>TAX.rubrics[m.rubric]);
  // из языковых версий одного материала – на языке страницы, иначе оригинал (как в resources.html)
  const pick={}, score=x=>x.lang===PAGE_LANG?0:(x.translation_of?2:1);
  for(const m of rows){ const g=m.translation_of||m.id; if(!pick[g]||score(m)<score(pick[g])) pick[g]=m; }
  return rows.filter(m=>pick[m.translation_of||m.id]===m)
    .sort((a,b)=>(a.lang===PAGE_LANG?0:1)-(b.lang===PAGE_LANG?0:1));
}

function card(m){
  const img=imgOf(m), au=authorName(m);
  return '<a class="an-card" href="'+esc(articleUrl(m))+'">'
    +'<div class="an-thumb">'+(img?'<img src="'+esc(img)+'" alt="'+esc(m.title)+'" loading="lazy"/>':'')
    +'<span class="an-badge">'+esc(lbl(TAX.rubrics[m.rubric]))+'</span></div>'
    +'<div class="an-body"><span class="an-meta">'+esc(fmtDate(m.created_at))+(au?' · '+esc(au):'')
    +(m.lang&&m.lang!==PAGE_LANG?' · '+esc(m.lang.toUpperCase()):'')+'</span>'
    +'<h3>'+esc(m.title)+'</h3>'+(m.description?'<p>'+esc(m.description)+'</p>':'')+'</div></a>';
}

function featured(){
  const m=ALL.find(x=>x.rubric==='annual'||x.rubric==='salary');
  if(!m){ feat.hidden=true; return; }
  const img=imgOf(m);
  feat.href=articleUrl(m);
  feat.innerHTML='<div class="an-feat-img">'+(img?'<img src="'+esc(img)+'" alt="'+esc(m.title)+'"/>':'')+'</div>'
    +'<div class="an-feat-body"><span class="an-feat-k">'+esc(T.feat)+' · '+esc(lbl(TAX.rubrics[m.rubric]))+'</span>'
    +'<h2>'+esc(m.title)+'</h2>'+(m.description?'<p>'+esc(m.description)+'</p>':'')+'<b>'+esc(T.feat_a)+'</b></div>';
  feat.hidden=false;
}

function filters(){
  const rubs=Object.keys(TAX.rubrics).filter(k=>ALL.some(m=>m.rubric===k));
  if(rubric && !rubs.includes(rubric)) rubric='';
  chipsEl.innerHTML=[['',T.all]].concat(rubs.map(k=>[k,lbl(TAX.rubrics[k])]))
    .map(([k,n])=>'<button type="button" class="an-chip'+(k===rubric?' active':'')+'" data-r="'+k+'">'+esc(n)+'</button>').join('');
  chipsEl.hidden=rubs.length<2;
  const inds=Object.keys(TAX.industries).filter(k=>k!=='general'&&ALL.some(m=>(m.industries||[]).includes(k)));
  if(industry && !inds.includes(industry)) industry='';
  indSel.innerHTML='<option value="">'+esc(T.all_ind)+'</option>'
    +inds.map(k=>'<option value="'+k+'"'+(k===industry?' selected':'')+'>'+esc(lbl(TAX.industries[k]))+'</option>').join('');
  indWrap.hidden=!inds.length;
}

function render(){
  // отраслевой фильтр: материал «для всех отраслей» (general или без отрасли) виден при любом выборе
  const list=ALL.filter(m=>(!rubric||m.rubric===rubric)
    &&(!industry||!(m.industries||[]).length||(m.industries||[]).includes(industry)||(m.industries||[]).includes('general')));
  if(!ALL.length){ grid.innerHTML='<div class="an-empty" style="grid-column:1/-1">'+esc(T.empty_none)+'</div>'; shownEl.textContent=''; return; }
  grid.innerHTML=list.length?list.map(card).join(''):'<div class="an-empty" style="grid-column:1/-1">'+esc(T.empty_filter)+'</div>';
  shownEl.innerHTML=T.shown.replace('{n}',list.length).replace('{m}',ALL.length);
  const q=new URLSearchParams(); if(rubric)q.set('rubric',rubric); if(industry)q.set('industry',industry);
  history.replaceState(null,'',location.pathname+(q.toString()?'?'+q:'')+location.hash);
}

chipsEl.addEventListener('click',e=>{ const b=e.target.closest('[data-r]'); if(!b)return; rubric=b.dataset.r;
  chipsEl.querySelectorAll('.an-chip').forEach(x=>x.classList.toggle('active',x===b)); render(); });
indSel.addEventListener('change',()=>{ industry=indSel.value; render(); });

(async function init(){
  const p=new URLSearchParams(location.search); rubric=p.get('rubric')||''; industry=p.get('industry')||'';
  if(/^https:\/\/t\.me\/[A-Za-z0-9_+\/-]+$/.test(TAX.telegram||'')){ const tg=document.getElementById('anTg'); tg.href=TAX.telegram; tg.hidden=false; }
  grid.innerHTML=Array(3).fill('<div class="an-skel"></div>').join('');
  try{ ALL=await load(); }catch(e){ console.error('analytics', e); ALL=[]; }
  featured(); filters(); render();
})();
"""


def build(lang):
    src = open(os.path.join(ROOT, SRC[lang]), encoding="utf-8").read()
    t = T[lang]

    def grab(pattern):
        m = re.search(pattern, src, re.S)
        if not m:
            raise SystemExit("не найдено в " + SRC[lang] + ": " + pattern)
        return m.group(0)

    head = grab(r"<!DOCTYPE html>.*?</head>")
    for l, f in SRC.items():
        head = head.replace(SITE + "/" + f, SITE + "/" + FILES[l])
    def attr(h, rx, val):
        new, n = re.subn(rx, lambda m: m.group(1) + val.replace("&", "&amp;").replace('"', "&quot;") + m.group(2), h)
        if not n:
            raise SystemExit("не найдено в head " + SRC[lang] + ": " + rx)
        return new
    head = re.sub(r"<title>.*?</title>", "<title>" + t["title"] + "</title>", head, count=1, flags=re.S)
    head = attr(head, r'(<meta name="description" content=")[^"]*(")', t["desc"])
    head = attr(head, r'(<meta property="og:title" content=")[^"]*(")', t["title"])
    head = attr(head, r'(<meta property="og:description" content=")[^"]*(")', t["desc"])
    head = attr(head, r'(<meta name="twitter:title" content=")[^"]*(")', t["title"])
    head = attr(head, r'(<meta name="twitter:description" content=")[^"]*(")', t["desc"])
    head = head.replace("</head>", "<style>" + CSS + "</style>\n</head>")

    nav = grab(r'<nav id="nav">.*?</nav>')
    nav = nav.replace(' class="active"', "")
    for l, f in SRC.items():
        nav = nav.replace('<a href="' + f + '" data-lang=', '<a href="' + FILES[l] + '" data-lang=')
    nav, n = re.subn(r'<a href="(analytics(?:-en|-uz)?\.html)">', r'<a href="\1" class="active">', nav, count=1)
    if not n:
        raise SystemExit("в меню " + SRC[lang] + " нет пункта «Аналитика» – сначала добавьте его")

    tail = grab(r'<footer>.*?</footer>\s*<div class="fab-wrap" id="fabWrap">.*?</script>')
    menu_js = grab(r"const nav=document.getElementById\('nav'\);.*?langMenu\.classList\.remove\('open'\);langCurrent\.textContent=langOriginal;\} \}\);")
    menu_js = menu_js.replace(
        "window.addEventListener('scroll',()=>{ nav.classList.toggle('scrolled', window.scrollY>Math.max(window.innerHeight*0.7,80)); });",
        "const onScroll=()=>nav.classList.toggle('scrolled', window.scrollY>40); onScroll(); window.addEventListener('scroll',onScroll);")

    t_js = {k: t[k] for k in ("feat", "feat_a", "all", "all_ind", "shown", "empty_none", "empty_filter", "locale")}
    tax_js = {"rubrics": TAX["rubrics"], "industries": TAX["industries"], "telegram": TAX.get("telegram", ""),
              "authors": {k: {"name": v["name"]} for k, v in TAX["authors"].items()}}
    js = JS % {"lang": json.dumps(lang), "t": json.dumps(t_js, ensure_ascii=False),
               "tax": json.dumps(tax_js, ensure_ascii=False)}

    out = (head.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n<!-- Сгенерировано tools/build_analytics.py – не править вручную -->", 1)
           + "\n<body>\n\n" + nav + "\n" + MAIN.format(**t) + "\n" + tail
           + "\n\n<script>\n" + js.strip() + "\n\n" + menu_js + "\n</script>\n<script src=\"hc-crm.js\" defer></script>\n</body>\n</html>\n")
    open(os.path.join(ROOT, FILES[lang]), "w", encoding="utf-8").write(out)
    return FILES[lang]


print("ok: " + ", ".join(build(l) for l in FILES))
