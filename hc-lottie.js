/* ============================================================
   Human and Capital – ленивый запуск Lottie-анимаций

   Подключается вместо CDN-скрипта lottie-web:
     <script src="/hc-lottie.js"></script>

   Страницы вызывают lottie.loadAnimation(...) как раньше, но:
   – сама библиотека (/vendor/, сборка только с SVG-рендером) грузится
     после события load и не мешает первой отрисовке страницы;
   – анимация играет, только пока она видна на экране и вкладка активна,
     и не перерисовывается чаще собственной частоты кадров. На телефонах
     постоянная анимация занимала до 20–40% процессора.
   ============================================================ */
(function () {
  "use strict";
  if (window.lottie) return;

  var SRC = "/vendor/lottie_svg-5.12.2.min.js";
  var queue = [];
  var requested = false;

  window.lottie = {
    loadAnimation: function (opts) {
      queue.push(opts);
      request();
    }
  };

  function request() {
    if (requested) return;
    requested = true;
    if (document.readyState === "complete") later(load);
    else window.addEventListener("load", function () { later(load); });
  }

  function later(fn) {
    if (window.requestIdleCallback) requestIdleCallback(fn, { timeout: 1500 });
    else setTimeout(fn, 200);
  }

  function load() {
    var s = document.createElement("script");
    s.src = SRC;
    s.onload = function () {
      var real = window.lottie;
      if (!real || !real.loadAnimation) return;
      queue.forEach(function (opts) { start(real, opts); });
      queue = [];
    };
    document.head.appendChild(s);
  }

  function start(real, opts) {
    var el = opts && opts.container;
    if (!el) return;
    var cfg = {};
    for (var k in opts) cfg[k] = opts[k];
    cfg.autoplay = false;

    var anim;
    try { anim = real.loadAnimation(cfg); } catch (e) { console.warn("Lottie init failed", e); return; }
    anim.setSubframe(false);

    // На телефонах 60-кадровые анимации рисуем с частотой 30 кадров/с:
    // для фоновой иллюстрации разница не заметна, а нагрузка вдвое меньше.
    var capped = window.matchMedia && matchMedia("(max-width:1080px)").matches;
    var STEP = 1000 / 30;
    var raf = 0, last = 0, t0 = 0, pos = 0;
    function tick(t) {
      raf = requestAnimationFrame(tick);
      if (t - last < STEP - 2) return;
      last = t;
      var total = anim.totalFrames;
      if (!total) return;
      var f = pos + (t - t0) / 1000 * anim.frameRate;
      if (opts.loop === false && f >= total - 1) { anim.goToAndStop(total - 1, true); halt(); return; }
      anim.goToAndStop(f % total, true);
    }
    function run() {
      if (!capped || anim.frameRate <= 30) { anim.play(); return; }
      if (raf) return;
      t0 = last = performance.now();
      raf = requestAnimationFrame(tick);
    }
    function halt() {
      if (raf) { cancelAnimationFrame(raf); raf = 0; pos = anim.currentFrame; }
      anim.pause();
    }

    var wanted = opts.autoplay !== false;
    var visible = !("IntersectionObserver" in window);
    function sync() {
      if (wanted && visible && !document.hidden && anim.isLoaded) run();
      else halt();
    }

    if (!visible) {
      new IntersectionObserver(function (entries) {
        visible = entries[entries.length - 1].isIntersecting;
        sync();
      }, { rootMargin: "100px" }).observe(el);
    }
    document.addEventListener("visibilitychange", sync);
    anim.addEventListener("DOMLoaded", sync);
  }
})();
