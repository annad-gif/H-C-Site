/* Routing Middleware: разделы-списки отдаются через api/hub.js – та же статичная страница плюс список ссылок
   или таблица зарплат в HTML для ботов без JavaScript. Обычный rewrite в vercel.json тут не сработает:
   у Vercel статичный файл всегда важнее rewrite. Остальные адреса сайта middleware не трогает (matcher). */
import { rewrite } from "@vercel/functions";

export const config = {
  matcher: [
    "/resources.html", "/resources-en.html", "/resources-uz.html",
    "/analytics.html", "/analytics-en.html", "/analytics-uz.html",
    "/vacancies.html", "/vacancies-en.html", "/vacancies-uz.html",
    "/analytics-salaries.html", "/analytics-salaries-en.html", "/analytics-salaries-uz.html",
  ],
};

export default function middleware(request) {
  const page = new URL(request.url).pathname.replace(/^\//, "").replace(/\.html$/, "");
  return rewrite(new URL("/api/hub?page=" + encodeURIComponent(page), request.url));
}
