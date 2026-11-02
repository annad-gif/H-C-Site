"""Собирает оболочки страниц статей из resources*.html.

Страницы /articles/<slug> рендерит функция api/article.js, страницы вакансий – api/vacancy.js.
Чтобы шапка, подвал и стили совпадали с остальным сайтом, они берутся из раздела
«Полезные материалы» на языке статьи (site_materials.lang):

  - article.css          – стили resources.html + стили статьи (tools/article-extra.css)
  - api/_shell.html      – RU: <nav>, <footer>, кнопка «Связаться» и скрипт меню (из resources.html)
  - api/_shell-en.html   – EN (из resources-en.html)
  - api/_shell-uz.html   – UZ (из resources-uz.html)

Запускать после правок меню/подвала/стилей в resources*.html:
    python3 tools/build_article_shell.py

Пишет article.css, api/_shell.html, api/_shell-en.html, api/_shell-uz.html – только если все три языка разобрались
без ошибок. Стили статьи правьте в tools/article-extra.css, общие стили и меню – в resources*.html, а не в article.css
и не в api/_shell*.html. Проверка: после запуска git diff пустой.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = [("ru", "resources.html", "_shell.html"),
         ("en", "resources-en.html", "_shell-en.html"),
         ("uz", "resources-uz.html", "_shell-uz.html")]


def absolutize(html):
    # страница статьи живёт в /articles/, поэтому относительные ссылки делаем от корня
    return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|data:)([^"]+)"', r'\1="/\2"', html)


def build(lang, src_name, out_name):
    src = open(os.path.join(ROOT, src_name), encoding="utf-8").read()

    def grab(pattern):
        m = re.search(pattern, src, re.S)
        if not m:
            raise SystemExit("не найдено в " + src_name + ": " + pattern)
        return m.group(0)

    # в resources*.html два <style>: первый – @font-face (шрифты с /fonts) и мелочи для телефона, второй – стили страницы
    fonts = grab(r"<style>\n/\* Inter и Unbounded[^\n]*\*/\n(?:@font-face\{[^\n]*\}\n)+") + "</style>"
    style = grab(r"<style>\s*:root\{.*?</style>")[len("<style>"):-len("</style>")]
    nav = absolutize(grab(r'<nav id="nav">.*?</nav>'))
    nav = nav.replace(' class="active"', "")
    # подсвечиваем «Полезные материалы» в меню (пункты переключателя языка имеют data-lang и не попадают)
    nav, n = re.subn(r'href="(/resources(?:-en|-uz)?\.html)">', r'href="\1" class="active">', nav, count=1)
    if not n:
        raise SystemExit("не найден пункт меню «Полезные материалы» в " + src_name)
    footer = absolutize(grab(r"<footer>.*?</footer>"))
    fab = absolutize(grab(r'<div class="fab-wrap" id="fabWrap">.*?</script>'))
    menu_js = grab(r"const nav=document.getElementById\('nav'\);.*?langCurrent.textContent=a.dataset.lang\); \}\);")
    menu_js = menu_js.replace(
        "window.addEventListener('scroll',()=>{ nav.classList.toggle('scrolled', window.scrollY>Math.max(window.innerHeight*0.7,80)); });",
        "const onScroll=()=>nav.classList.toggle('scrolled', window.scrollY>40); onScroll(); window.addEventListener('scroll',onScroll);")

    shell = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<script src="/hc-analytics.js" async></script>
{{{{HEAD}}}}
<link rel="icon" href="/favicon.ico"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
{fonts}
<link rel="stylesheet" href="/article.css"/>
</head>
<body class="ar-page">

{nav}

{{{{MAIN}}}}

{footer}

{fab}
<script>
{menu_js}
</script>
</body>
</html>
"""
    return style, shell


# сначала собираем всё в памяти и пишем, только если все три языка разобрались без ошибок
out = {}
for lang, src_name, out_name in LANGS:
    style, out["api/" + out_name] = build(lang, src_name, out_name)
    if lang == "ru":
        extra = open(os.path.join(ROOT, "tools", "article-extra.css"), encoding="utf-8").read()
        out["article.css"] = ("/* Сгенерировано tools/build_article_shell.py из resources.html – не править вручную */\n"
                              + style.strip() + "\n\n" + extra)
for name, text in out.items():
    open(os.path.join(ROOT, name), "w", encoding="utf-8").write(text)
print("ok: " + ", ".join(out))
