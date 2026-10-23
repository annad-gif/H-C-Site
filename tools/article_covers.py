"""Обложки статей 1600x900 в стиле сайта (светлый фон, тёмно-синий заголовок, горчичный акцент).

Добавьте обложку в COVERS (имя → HTML левой и правой колонок) и запустите:
    python3 tools/article_covers.py <папка для html>
затем отрисуйте PNG и сожмите в JPEG:
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
      --allow-file-access-from-files --window-size=1600,900 --virtual-time-budget=6000 \
      --screenshot=<имя>.png file://<папка>/<имя>.html
    sips -s format jpeg -s formatOptions 86 <имя>.png --out img/articles/<slug статьи>.jpg
В статье (site_materials) – media_type='image', media_url='https://humancapital.uz/img/articles/<slug>.jpg'.
"""
import os, sys
D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
LOGO = "file://" + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo.png")

ICON = {
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0113 0"/><circle cx="17" cy="9" r="2.8"/><path d="M15.5 14.2A5.5 5.5 0 0122 20"/>',
 "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
}
def ic(name): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>'

BASE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Unbounded:wght@600;700;800&display=block" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:900px;overflow:hidden}
body{background:#eef1f5;font-family:Inter,sans-serif;color:#13294a;display:flex;align-items:center;justify-content:center}
.card{width:1520px;height:820px;background:#f8fafc;border-radius:36px;box-shadow:0 18px 50px rgba(19,41,74,.10);padding:70px 80px;display:grid;grid-template-columns:1.05fr .95fr;gap:60px;position:relative;overflow:hidden}
.card:before{content:"";position:absolute;width:620px;height:620px;border-radius:50%;right:-180px;top:-200px;background:radial-gradient(circle,rgba(198,154,46,.18),rgba(198,154,46,0) 70%)}
.logo{height:62px;margin-bottom:64px}
h1{font-family:Unbounded,sans-serif;font-weight:800;font-size:66px;line-height:1.08;text-transform:uppercase;letter-spacing:-.5px}
h1 .acc{color:#c69a2e}
.sub{margin-top:30px;font-size:31px;font-weight:600;color:#1d8a83;line-height:1.35}
.foot{position:absolute;left:80px;bottom:56px;font-size:21px;color:#6b7686;font-weight:500}
.right{display:flex;flex-direction:column;justify-content:center;gap:22px;position:relative;z-index:1}
.item{display:flex;align-items:center;gap:24px;background:#fff;border:1px solid #e3e8ef;border-radius:24px;padding:26px 30px;box-shadow:0 8px 24px rgba(19,41,74,.06)}
.ico{width:66px;height:66px;flex:0 0 66px;border-radius:18px;background:rgba(198,154,46,.14);color:#b0861f;display:flex;align-items:center;justify-content:center}
.ico svg{width:34px;height:34px}
.item b{display:block;font-size:27px;font-weight:700;line-height:1.25}
.item span{display:block;font-size:20px;color:#5c6878;margin-top:4px;line-height:1.35}
.num{font-family:Unbounded,sans-serif;font-weight:700;color:#c69a2e;font-size:30px;width:50px;flex:0 0 50px}
.funnel{display:flex;flex-direction:column;align-items:center;gap:16px}
.fb{height:96px;border-radius:20px;display:flex;align-items:center;justify-content:center;gap:16px;color:#fff;font-weight:700;font-size:27px}
.fb svg{width:32px;height:32px}
</style></head><body><div class="card">%s</div></body></html>"""

COVERS = {
"agency": f"""
<div><img class="logo" src="{LOGO}">
<h1>Как выбрать <span class="acc">кадровое агентство</span> в Ташкенте</h1>
<p class="sub">10 вопросов, которые стоит задать до подписания договора</p></div>
<div class="right">
 <div class="item"><div class="num">01</div><div><b>Кто ведёт вакансию?</b><span>опыт и загрузка рекрутера</span></div></div>
 <div class="item"><div class="num">04</div><div><b>Как оценивают кандидатов?</b><span>прескрининг, интервью, язык</span></div></div>
 <div class="item"><div class="num">06</div><div><b>Какая гарантия замены?</b><span>срок и условия</span></div></div>
 <div class="item"><div class="num">10</div><div><b>Какая отчётность?</b><span>воронка и обратная связь о рынке</span></div></div>
</div>
<div class="foot">humancapital.uz · Полезные материалы</div>""",

"mass": f"""
<div><img class="logo" src="{LOGO}">
<h1>Массовый подбор персонала <span class="acc">в Узбекистане</span></h1>
<p class="sub">Как закрыть десятки однотипных вакансий в сжатые сроки</p></div>
<div class="right"><div class="funnel">
 <div class="fb" style="width:100%;background:#13294a">{ic('people')}Отклики</div>
 <div class="fb" style="width:86%;background:#1d5f7a">{ic('search')}Прескрининг</div>
 <div class="fb" style="width:72%;background:#1d8a83">{ic('user')}Собеседования</div>
 <div class="fb" style="width:58%;background:#c69a2e">{ic('shield')}Выход на работу</div>
</div></div>
<div class="foot">humancapital.uz · Полезные материалы</div>""",

"hiring_en": f"""
<div><img class="logo" src="{LOGO}">
<h1>Hiring in <span class="acc">Uzbekistan</span></h1>
<p class="sub">A practical guide for foreign companies building a team in Tashkent</p></div>
<div class="right">
 <div class="item"><div class="ico">{ic('building')}</div><div><b>Local entity</b><span>hire directly on your own payroll</span></div></div>
 <div class="item"><div class="ico">{ic('people')}</div><div><b>Outstaffing</b><span>a local provider is the legal employer</span></div></div>
 <div class="item"><div class="ico">{ic('doc')}</div><div><b>Contractors</b><span>for short, defined projects</span></div></div>
</div>
<div class="foot">humancapital.uz · Resources</div>""",
}

for name, body in COVERS.items():
    open(os.path.join(D, name + ".html"), "w", encoding="utf-8").write(BASE.replace("%s", body, 1))
print("ok", list(COVERS))
