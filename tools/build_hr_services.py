"""Собирает hr-services-uzbekistan.html из оболочки consulting-en.html (стили, меню, форма, подвал)."""
import json, re, sys

ROOT = sys.argv[1]
src = open(f"{ROOT}/consulting-en.html", encoding="utf-8").read()

URL = "https://humancapital.uz/hr-services-uzbekistan.html"
TITLE = "HR Services in Uzbekistan – Recruitment, Outstaffing, HR Consulting | Human and Capital"
SHORT_TITLE = "HR Services in Uzbekistan – Human and Capital"
DESC = ("HR services in Uzbekistan for local and international companies: recruitment and executive search, "
        "outstaffing with legal employment and payroll, HR consulting and HR audit. Tashkent-based team, 500+ positions filled.")

# ---------- head ----------
style_start, style_end = src.index("<style>"), src.index("</style>") + len("</style>")
fonts = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com"/>.*?rel="stylesheet"/>', src, re.S).group(0)

faq = [
    ("What HR services do you provide in Uzbekistan?",
     "Human and Capital provides three groups of HR services: recruitment (search and selection, executive search, IT and mass recruitment), "
     "outstaffing (legal employment, payroll and support of staff working for your company) and HR consulting (HR audit, staffing schedules "
     "and standard documents, assessment and training systems, onboarding, motivation and labour market analysis)."),
    ("Do you work with international companies?",
     "Yes. We work with local and international companies. International clients most often come to us for outstaffing and for building "
     "teams in Uzbekistan, including multilingual staff with verified English, German, Arabic, Turkish, Korean, French and other languages."),
    ("Can you legally employ staff in Uzbekistan for a foreign company?",
     "Yes, this is what outstaffing is for. We take on the legal employment of specialists, payroll, compliance with Uzbek labour law and "
     "timely reporting, while the employees work on your tasks. We operate within the IT Park preferential legal and tax regime."),
    ("How long does it take to fill a position?",
     "Timelines depend on the brief, the situation on the labour market and the conditions offered to the candidate. We agree on the "
     "timeline before the search starts and keep you updated at every stage."),
    ("What if a hired candidate does not work out?",
     "Every recruitment project includes one free replacement within the agreed terms, a free trial day for the candidate and support for "
     "both the employer and the employee during the probation period."),
    ("How is the cost of HR services calculated?",
     "The cost is calculated individually. It depends on the service, the level of the role, the timeline and the complexity of the search "
     "or the project. Send us your request and we will prepare a proposal within one business day."),
    ("Which industries do you hire for?",
     "IT, finance, government, tourism and aviation, real estate and construction, HORECA, manufacturing, distribution, pharma and medicine, "
     "retail, BPO and contact centres, and many more."),
    ("Where are you located?",
     "Our office is in Tashkent, Farg‘ona yo‘li 94. We hire specialists across Uzbekistan and work with clients remotely as well."),
]

ld = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Service",
            "@id": URL + "#service",
            "name": "HR Services in Uzbekistan",
            "serviceType": "HR services",
            "description": DESC,
            "url": URL,
            "areaServed": {"@type": "Country", "name": "Uzbekistan"},
            "provider": {"@id": "https://humancapital.uz/#organization"},
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "HR services",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Recruitment and executive search", "url": "https://humancapital.uz/recruitment-en.html"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Outstaffing", "url": "https://humancapital.uz/outstaffing-en.html"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "HR consulting", "url": "https://humancapital.uz/consulting-en.html"}},
                ],
            },
        },
        {
            "@type": ["Organization", "EmploymentAgency"],
            "@id": "https://humancapital.uz/#organization",
            "name": "Human and Capital",
            "url": "https://humancapital.uz/",
            "logo": "https://humancapital.uz/logo.png",
            "telephone": "+998903251336",
            "email": "akmal.s@human-capital.org",
            "address": {"@type": "PostalAddress", "streetAddress": "Farg‘ona yo‘li, 94", "addressLocality": "Tashkent", "addressCountry": "UZ"},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://humancapital.uz/index-en.html"},
                {"@type": "ListItem", "position": 2, "name": "HR Services in Uzbekistan", "item": URL},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
        },
    ],
}

extra_css = """
<style>
  /* ===== HR SERVICES PAGE ===== */
  .hrs-stats{display:grid;grid-template-columns:1fr;gap:16px;width:100%;max-width:420px;}
  .hrs-stat{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);border-radius:18px;padding:24px 28px;
    display:flex;align-items:baseline;gap:18px;backdrop-filter:blur(6px);}
  .hrs-stat b{font-family:var(--ff-display);font-weight:700;font-size:clamp(34px,4vw,48px);color:var(--mustard);line-height:1;min-width:120px;}
  .hrs-stat span{font-size:15px;color:var(--grey-300);line-height:1.4;}
  #hrs-intro{background:var(--white);}
  .hrs-prose{max-width:760px;}
  .hrs-prose p{font-size:17px;color:var(--grey-700);line-height:1.8;margin-top:18px;}
  .hrs-prose p strong{color:var(--black);font-weight:600;}
  .hrs-prose p a{color:var(--mustard-dim);font-weight:600;}
  #hrs-services{background:var(--grey-50);}
  .hrs-svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;align-items:stretch;}
  .hrs-svc{display:flex;flex-direction:column;gap:18px;}
  .hrs-svc .hrs-num{font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--mustard-light);position:relative;}
  .hrs-svc h3{font-family:var(--ff-display);font-weight:600;font-size:21px;line-height:1.3;color:var(--white);position:relative;}
  .hrs-svc p{font-size:15px;color:var(--grey-300);line-height:1.7;position:relative;}
  .hrs-svc ul{list-style:none;display:flex;flex-direction:column;gap:10px;border-top:1px solid rgba(255,255,255,0.08);padding-top:18px;position:relative;}
  .hrs-svc li{display:flex;gap:11px;align-items:flex-start;font-size:14px;line-height:1.55;color:var(--grey-300);}
  .hrs-svc li::before{content:'';width:7px;height:7px;border-radius:50%;background:var(--mustard);flex-shrink:0;margin-top:7px;box-shadow:0 0 9px rgba(198,154,46,0.7);}
  .hrs-svc .hrs-more{margin-top:auto;display:inline-flex;align-items:center;gap:8px;color:var(--mustard-light);font-weight:600;font-size:14px;text-decoration:none;position:relative;}
  .hrs-svc .hrs-more svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:2;transition:transform .2s;}
  .hrs-svc .hrs-more:hover svg{transform:translateX(4px);}
  #hrs-who{background:var(--white);}
  .hrs-who-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;}
  .hrs-tags{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px;}
  .hrs-tags span{border:1px solid var(--grey-100);background:var(--grey-50);border-radius:999px;padding:9px 16px;font-size:14px;color:var(--grey-700);}
  .hrs-check{list-style:none;display:flex;flex-direction:column;gap:14px;margin-top:8px;}
  .hrs-check li{display:flex;gap:12px;font-size:16px;line-height:1.6;color:var(--grey-700);}
  .hrs-check li::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--mustard);flex-shrink:0;margin-top:9px;}
  .hrs-h3{font-family:var(--ff-display);font-weight:600;font-size:20px;margin-bottom:18px;color:var(--black);}
  #hrs-process{background:var(--black);color:var(--white);}
  #hrs-process .sec-title{color:var(--white);}
  #hrs-process .sec-lead{color:var(--grey-300);}
  #hrs-process .sec-eyebrow{color:var(--mustard-light);}
  .hrs-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;counter-reset:step;list-style:none;}
  .hrs-steps li{border:1px solid rgba(255,255,255,0.10);border-radius:16px;padding:24px 22px;background:rgba(255,255,255,0.03);}
  .hrs-steps li::before{counter-increment:step;content:counter(step,decimal-leading-zero);display:block;font-family:var(--ff-display);
    font-weight:700;font-size:22px;color:var(--mustard);margin-bottom:14px;}
  .hrs-steps h3{font-size:16px;font-weight:600;margin-bottom:8px;color:var(--white);}
  .hrs-steps p{font-size:14px;line-height:1.6;color:var(--grey-300);}
  #hrs-why{background:var(--white);}
  .hrs-why-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
  .hrs-why{border:1px solid var(--grey-100);border-radius:18px;padding:28px 26px;background:var(--grey-50);}
  .hrs-why h3{font-family:var(--ff-display);font-weight:600;font-size:17px;line-height:1.35;margin-bottom:10px;}
  .hrs-why p{font-size:15px;line-height:1.65;color:var(--grey-700);}
  #hrs-reviews{background:var(--grey-50);}
  .hrs-rev-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
  .hrs-rev{background:var(--white);border:1px solid var(--grey-100);border-radius:18px;padding:28px 26px;display:flex;flex-direction:column;gap:18px;}
  .hrs-rev blockquote{font-size:15px;line-height:1.7;color:var(--grey-700);}
  .hrs-rev cite{font-style:normal;font-size:14px;color:var(--grey-500);margin-top:auto;}
  .hrs-rev cite b{display:block;color:var(--black);font-weight:600;font-size:15px;}
  #hrs-faq{background:var(--white);}
  .hrs-faq{max-width:860px;display:flex;flex-direction:column;gap:14px;}
  .hrs-faq .cons-acc-panel p{font-size:15px;line-height:1.7;color:var(--grey-300);border-top:1px solid rgba(255,255,255,0.08);padding-top:18px;}
  .hrs-faq .cons-acc-head h3{font-size:16px;}
  @media (max-width:1080px){
    .hrs-svc-grid,.hrs-why-grid,.hrs-rev-grid{grid-template-columns:1fr 1fr;}
    .hrs-steps{grid-template-columns:1fr 1fr;}
    .hrs-who-grid{grid-template-columns:1fr;gap:40px;}
    .hrs-stats{margin:0 auto;}
    .hrs-hero .rec-hero-visual{order:1 !important;}
  }
  @media (max-width:720px){
    .hrs-svc-grid,.hrs-why-grid,.hrs-rev-grid,.hrs-steps{grid-template-columns:1fr;}
    .hrs-stats{grid-template-columns:repeat(3,1fr);gap:10px;max-width:none;}
    .hrs-stat{flex-direction:column;align-items:flex-start;gap:8px;padding:16px 14px;border-radius:14px;}
    .hrs-stat b{font-size:26px;min-width:0;}
    .hrs-stat span{font-size:12px;}
    .hrs-prose p{font-size:16px;}
  }
</style>
"""

head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<script src="/hc-analytics.js" async></script>
<meta name="description" content="{DESC}"/>
<title>{TITLE}</title>
<!-- SEO -->
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="{URL}"/>
<!-- Open Graph -->
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Human and Capital"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:url" content="{URL}"/>
<meta property="og:title" content="{SHORT_TITLE}"/>
<meta property="og:description" content="{DESC}"/>
<meta property="og:image" content="https://humancapital.uz/og-cover.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{SHORT_TITLE}"/>
<meta name="twitter:description" content="{DESC}"/>
<meta name="twitter:image" content="https://humancapital.uz/og-cover.png"/>
<link rel="icon" href="/favicon.ico"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
{fonts}
{src[style_start:style_end]}
{extra_css}
</head>
"""

# ---------- nav ----------
nav = src[src.index('<nav id="nav">'):src.index("</nav>") + len("</nav>")]
nav = nav.replace('<li><a href="https://humancapital.uz/staffly/ru">Outstaffing</a></li>',
                  '<li><a href="outstaffing-en.html">Outstaffing</a></li>\n        <li><a href="hr-services-uzbekistan.html">All HR services</a></li>')
nav = nav.replace('<a href="consulting.html" data-lang="RU">', '<a href="index.html" data-lang="RU">')
nav = nav.replace('<a href="consulting-en.html" data-lang="ENG">', '<a href="hr-services-uzbekistan.html" data-lang="ENG">')
nav = nav.replace('<a href="consulting-uz.html" data-lang="UZB">', '<a href="index-uz.html" data-lang="UZB">')
assert "hr-services-uzbekistan.html" in nav and "staffly/ru" not in nav

ARROW = '<svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'

def acc(q, a):
    return f"""      <div class="cons-card cons-acc reveal">
        <div class="cons-acc-head">
          <h3>{q}</h3>
          <span class="cons-acc-caret"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></span>
        </div>
        <div class="cons-acc-panel"><p>{a}</p></div>
      </div>"""

steps = [
    ("Initial request", "You describe the task: the role, the team or the HR process you need help with."),
    ("Needs analysis", "We analyse your requirements and agree on a search or project strategy."),
    ("Contract", "We sign a contract with clear scope, timelines and guarantees."),
    ("Sourcing", "We search for candidates, run interviews and shortlist the best options."),
    ("Assessment", "We assess candidates objectively using international methodologies."),
    ("Client interviews", "You meet the shortlisted candidates with full information on each of them."),
    ("Onboarding", "We support the candidate up to their first working day."),
    ("Adaptation", "We stay in touch with the employee and the employer during the probation period."),
]

reviews = [
    ("Working with Human and Capital was very productive. They quickly shortlisted 5 candidates, and we held joint interviews remotely. "
     "We chose the first candidate and hired them. I recommend this company for recruitment.", "Alexander Golenkov", "Director, TEZBULUT"),
    ("The team quickly and clearly understood my needs, helped define the key requirements for the candidate and organized the recruitment "
     "process as efficiently as possible. They provided only relevant and carefully vetted candidates, which saved a lot of time.",
     "Dilshod Kabulniyazov", "Operations Director, Satori Capital"),
    ("The team demonstrated a deep understanding of our needs, the market specifics and the strategic importance of each position. At every "
     "stage of recruitment, the company specialists showed high professionalism, responsiveness and engagement.", "Andrey Ten", "CEO, Variant Retail"),
]

main = f"""
<!-- HERO -->
<section class="rec-hero cons-hero hrs-hero" id="home">
  <div class="hero-aurora"><div class="aurora-blob"></div></div>
  <div class="hero-grain"></div>
  <div class="hero-glow g1"></div>
  <div class="hero-glow g2"></div>
  <div class="rec-hero-inner">
    <div class="rec-hero-text">
      <p class="hero-eyebrow"><span class="dot"></span>HR services · Uzbekistan</p>
      <h1>HR Services in <span class="accent">Uzbekistan</span></h1>
      <p class="lead">Recruitment, outstaffing and HR consulting for local and international companies – one Tashkent-based partner for hiring, legal employment and HR processes.</p>
      <div class="hero-actions">
        <a href="#contact" class="btn btn-mustard">Discuss your task
          {ARROW.replace('<svg ', '<svg fill="none" stroke="currentColor" stroke-width="2" ')}
        </a>
        <a href="#hrs-services" class="btn btn-ghost">Our services</a>
      </div>
    </div>
    <div class="rec-hero-visual">
      <div class="hrs-stats">
        <div class="hrs-stat"><b>5+</b><span>years on the HR market of Uzbekistan</span></div>
        <div class="hrs-stat"><b>500+</b><span>positions filled for our clients</span></div>
        <div class="hrs-stat"><b>20+</b><span>HR specialists on the team</span></div>
      </div>
    </div>
  </div>
</section>

<!-- MARQUEE -->
<div class="marquee-wrap">
  <div class="marquee-track">
{chr(10).join(f'    <span class="marquee-item">{x} <span class="sep">·</span></span>' for x in ["Recruitment", "Executive search", "IT recruitment", "Mass recruitment", "Outstaffing", "Payroll & legal employment", "HR consulting", "HR audit"] * 2)}
  </div>
</div>

<!-- INTRO -->
<section id="hrs-intro">
  <div class="container">
    <div class="hrs-prose reveal">
      <p class="sec-eyebrow">HR company in Tashkent</p>
      <h2 class="sec-title">One partner for hiring, staffing and HR</h2>
      <p><strong>Human and Capital</strong> is an HR company based in Tashkent that provides <strong>HR services in Uzbekistan</strong> to local businesses and international companies entering the Uzbek market. We find the right people, employ and support them on your behalf when needed, and help you build HR processes that keep them in the company.</p>
      <p>Instead of working with separate recruitment, outstaffing and consulting providers, you get one team that knows the local labour market, labour law and hiring practices – and that covers the whole cycle from the first request to the employee's adaptation.</p>
      <p>Our motto is simple: <strong>people and time are the most valuable resources</strong>. We help you find the first while saving the second.</p>
      <p>Planning to build a team here from abroad? Start with our guide <a href="/articles/hiring-in-uzbekistan-d0f28979">Hiring in Uzbekistan</a>: the three employment models, the local talent market and the hiring process step by step.</p>
    </div>
  </div>
</section>

<!-- SERVICES -->
<section id="hrs-services">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">What we do</p>
      <h2 class="sec-title">Our HR services</h2>
      <p class="sec-lead">Three service lines that can be ordered separately or combined into a single HR solution for your company.</p>
    </div>
    <div class="hrs-svc-grid">
      <article class="cons-card hrs-svc reveal">
        <span class="hrs-num">01 / RECRUITMENT</span>
        <h3>Recruitment &amp; executive search</h3>
        <p>End-to-end search and selection of specialists at every level – from entry roles to C-level executives and rare niche experts.</p>
        <ul>
          <li>Search &amp; selection of middle and senior specialists</li>
          <li>Executive search through direct approach</li>
          <li>IT recruitment</li>
          <li>Mass recruitment for retail, BPO and manufacturing</li>
          <li>Hiring from our candidate database</li>
        </ul>
        <a href="recruitment-en.html" class="hrs-more">Recruitment details {ARROW}</a>
      </article>
      <article class="cons-card hrs-svc reveal">
        <span class="hrs-num">02 / OUTSTAFFING</span>
        <h3>Outstaffing &amp; legal employment</h3>
        <p>We take on the employment, payroll and support of your staff in Uzbekistan, so you can scale a team without opening a local HR department.</p>
        <ul>
          <li>Legal employment and payroll</li>
          <li>Compliance with Uzbek labour law and reporting</li>
          <li>Sourcing, assessment and monitoring of staff</li>
          <li>Multilingual teams for BPO, contact centres and support</li>
          <li>IT Park residency benefits</li>
        </ul>
        <a href="outstaffing-en.html" class="hrs-more">Outstaffing details {ARROW}</a>
      </article>
      <article class="cons-card hrs-svc reveal">
        <span class="hrs-num">03 / HR CONSULTING</span>
        <h3>HR consulting &amp; HR audit</h3>
        <p>Turnkey solutions that put your HR processes in order – from documents and structure to assessment, onboarding and motivation.</p>
        <ul>
          <li>HR audit, staffing schedule and standard documents</li>
          <li>Training, evaluation and assessment systems</li>
          <li>Onboarding system design</li>
          <li>Motivation and corporate culture</li>
          <li>Labour market analysis and pre-screening</li>
        </ul>
        <a href="consulting-en.html" class="hrs-more">HR consulting details {ARROW}</a>
      </article>
    </div>
  </div>
</section>

<!-- WHO WE WORK WITH -->
<section id="hrs-who">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">Who we work with</p>
      <h2 class="sec-title">For local and international companies</h2>
    </div>
    <div class="hrs-who-grid">
      <div class="reveal">
        <h3 class="hrs-h3">Typical requests</h3>
        <ul class="hrs-check">
          <li>A foreign company needs a team in Uzbekistan without setting up its own HR and payroll</li>
          <li>A growing business needs to fill key roles quickly and without mistakes</li>
          <li>A company is looking for a top manager or a rare specialist</li>
          <li>Dozens of similar roles must be filled in a short time</li>
          <li>HR processes need an audit, documents or an onboarding and assessment system</li>
        </ul>
      </div>
      <div class="reveal">
        <h3 class="hrs-h3">Industries</h3>
        <div class="hrs-tags">
{chr(10).join(f'          <span>{x}</span>' for x in ["IT", "Finance", "Government", "Tourism &amp; Aviation", "Real Estate &amp; Construction", "HORECA", "Manufacturing", "Distribution", "Pharma &amp; Medicine", "Retail", "BPO &amp; contact centres", "and many more"])}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section id="hrs-process">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">How we work</p>
      <h2 class="sec-title">A simple, transparent process</h2>
      <p class="sec-lead">Every step is agreed with you in advance – from the first request to the employee's adaptation.</p>
    </div>
    <ol class="hrs-steps">
{chr(10).join(f'      <li class="reveal"><h3>{t}</h3><p>{d}</p></li>' for t, d in steps)}
    </ol>
  </div>
</section>

<!-- WHY US -->
<section id="hrs-why">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">Why Human and Capital</p>
      <h2 class="sec-title">Guarantees and advantages</h2>
    </div>
    <div class="hrs-why-grid">
      <div class="hrs-why reveal"><h3>Free replacement</h3><p>One free replacement of a hired specialist within the agreed terms.</p></div>
      <div class="hrs-why reveal"><h3>Search guarantee</h3><p>If we do not present at least 3 suitable candidates within the agreed timeframe, the prepayment is refunded.</p></div>
      <div class="hrs-why reveal"><h3>Free trial day</h3><p>The candidate's first trial day is free of charge for the employer.</p></div>
      <div class="hrs-why reveal"><h3>Experienced team</h3><p>Every member of our team has more than 2 years of experience in their field.</p></div>
      <div class="hrs-why reveal"><h3>Deep market insight</h3><p>We continuously track labour market trends and salary expectations in Uzbekistan.</p></div>
      <div class="hrs-why reveal"><h3>Confidentiality</h3><p>We guarantee full confidentiality of all data provided by clients and candidates.</p></div>
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section id="hrs-reviews">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">Client reviews</p>
      <h2 class="sec-title">What clients say</h2>
    </div>
    <div class="hrs-rev-grid">
{chr(10).join(f'      <figure class="hrs-rev reveal"><blockquote>“{q}”</blockquote><cite><b>{n}</b>{r}</cite></figure>' for q, n, r in reviews)}
    </div>
  </div>
</section>

<!-- FAQ -->
<section id="hrs-faq">
  <div class="container">
    <div class="sec-head reveal">
      <p class="sec-eyebrow">FAQ</p>
      <h2 class="sec-title">HR services in Uzbekistan: frequently asked questions</h2>
    </div>
    <div class="hrs-faq">
{chr(10).join(acc(q, a) for q, a in faq)}
    </div>
  </div>
</section>
"""

# ---------- contact / footer / fab / toast ----------
tail_start = src.index('<section id="contact">')
tail_end = src.index('<script src="https://cdn.jsdelivr.net/npm/lottie-web')
tail = src[tail_start:tail_end]
old_select = re.search(r'<select id="service">.*?</select>', tail, re.S).group(0)
tail = tail.replace(old_select, """<select id="service">
          <option value="">Select a service</option>
          <option>Recruitment</option>
          <option>Executive search</option>
          <option>Mass recruitment</option>
          <option>Outstaffing</option>
          <option>HR consulting</option>
          <option>HR audit</option>
        </select>""")
tail = tail.replace('<a href="#contact">Contacts</a>', '<a href="index-en.html">Home</a>\n    <a href="recruitment-en.html">Recruitment</a>\n    <a href="outstaffing-en.html">Outstaffing</a>\n    <a href="consulting-en.html">HR consulting</a>\n    <a href="#contact">Contacts</a>', 1)

# основной скрипт страницы – без инициализации Lottie (анимации на этой странице нет)
scripts = src[src.index("<script>\n  try{"):]
scripts = re.sub(r"<script>\n  try\{.*?\}catch\(e\)\{ console.error\('Lottie init error:', e\); \}\n", "<script>\n", scripts, count=1, flags=re.S)
assert "recLottie" not in scripts

out = head + "<body>\n\n" + nav + "\n" + main + "\n" + tail + scripts
open(f"{ROOT}/hr-services-uzbekistan.html", "w", encoding="utf-8").write(out)
print("ok", len(out))
