/* ============================================================
   INFINITUM — Comportamiento del sitio
   Version 2026-09-18 1800 v1
   Sin dependencias. Todo en un archivo, a proposito.
   ============================================================ */

(function () {
  'use strict';

  /* ---------- 1. Cabecera solida al bajar ---------- */

  var hdr = document.querySelector('.hdr');
  if (hdr) {
    var onScroll = function () {
      if (window.scrollY > 40) { hdr.classList.add('solid'); }
      else { hdr.classList.remove('solid'); }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 2. Menu de pantalla completa ---------- */

  var menu = document.querySelector('.menu');
  var openBtn = document.querySelector('.burger');
  var closeBtn = document.querySelector('.menu__close');

  function setMenu(open) {
    if (!menu) { return; }
    menu.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    if (openBtn) { openBtn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    menu.setAttribute('aria-hidden', open ? 'false' : 'true');
  }

  if (openBtn) { openBtn.addEventListener('click', function () { setMenu(true); }); }
  if (closeBtn) { closeBtn.addEventListener('click', function () { setMenu(false); }); }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { setMenu(false); }
  });

  /* Marca en que pagina estamos */
  var here = location.pathname.split('/').pop() || 'index.html';
  Array.prototype.forEach.call(document.querySelectorAll('.menu__nav a'), function (a) {
    if (a.getAttribute('href') === here) { a.classList.add('is-here'); }
  });

  /* ---------- 3. Carrusel del heroe ---------- */

  var hero = document.querySelector('.hero');
  if (hero) {
    var slides = hero.querySelectorAll('.hero__media img');
    var word = hero.querySelector('.hero__word');
    var dots = hero.querySelectorAll('.hero__dots button');
    var i = 0;
    var timer = null;

    function show(n) {
      if (!slides.length) { return; }
      i = (n + slides.length) % slides.length;
      Array.prototype.forEach.call(slides, function (s, k) { s.classList.toggle('on', k === i); });
      Array.prototype.forEach.call(dots, function (d, k) { d.classList.toggle('on', k === i); });
      if (word) {
        var label = slides[i].getAttribute('data-label') || '';
        word.style.opacity = '0';
        setTimeout(function () {
          word.textContent = label;
          word.style.opacity = '1';
        }, 320);
      }
    }

    function start() { stop(); timer = setInterval(function () { show(i + 1); }, 6000); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    Array.prototype.forEach.call(dots, function (d, k) {
      d.addEventListener('click', function () { show(k); start(); });
    });

    if (word) { word.style.transition = 'opacity 0.32s ease'; }
    show(0);
    start();

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stop(); } else { start(); }
    });
  }

  /* ---------- 4. Filtros de proyectos ---------- */

  var filters = document.querySelector('.filters');
  if (filters) {
    filters.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) { return; }
      var cat = btn.getAttribute('data-cat');
      Array.prototype.forEach.call(filters.querySelectorAll('button'), function (b) {
        b.classList.toggle('on', b === btn);
      });
      Array.prototype.forEach.call(document.querySelectorAll('.grid .card'), function (c) {
        var show = cat === 'all' || c.getAttribute('data-cat') === cat;
        c.classList.toggle('hide', !show);
      });
    });
  }

  /* ---------- 5. Aparicion al hacer scroll ---------- */

  var risers = document.querySelectorAll('.rise');
  if (risers.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px 14% 0px', threshold: 0 });
      Array.prototype.forEach.call(risers, function (r) { io.observe(r); });
    } else {
      Array.prototype.forEach.call(risers, function (r) { r.classList.add('in'); });
    }
  }

  /* ---------- 6. Espanol / Ingles ---------- */

  var LANG_KEY = 'infinitum-lang';

  function readLang() {
    try { return localStorage.getItem(LANG_KEY) || 'es'; } catch (err) { return 'es'; }
  }
  function saveLang(v) {
    try { localStorage.setItem(LANG_KEY, v); } catch (err) { /* modo privado, se ignora */ }
  }

  function applyLang(lang) {
    document.documentElement.setAttribute('lang', lang);
    Array.prototype.forEach.call(document.querySelectorAll('[data-es]'), function (el) {
      var txt = el.getAttribute('data-' + lang);
      if (txt !== null && txt !== undefined) { el.textContent = txt; }
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-ph-es]'), function (el) {
      var ph = el.getAttribute('data-ph-' + lang);
      if (ph) { el.setAttribute('placeholder', ph); }
    });
    Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) {
      b.classList.toggle('on', b.getAttribute('data-lang') === lang);
    });
    saveLang(lang);
  }

  Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) {
    b.addEventListener('click', function () { applyLang(b.getAttribute('data-lang')); });
  });

  applyLang(readLang());

  /* ---------- 7. Formulario de contacto ---------- */

  var form = document.querySelector('form[data-contact]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var lines = [
        'Nombre: ' + (d.get('nombre') || ''),
        'Ciudad: ' + (d.get('ciudad') || ''),
        'Correo: ' + (d.get('correo') || ''),
        'Telefono: ' + (d.get('telefono') || ''),
        '',
        (d.get('mensaje') || '')
      ];
      var body = encodeURIComponent(lines.join('\n'));
      var asunto = encodeURIComponent('Solicitud de cotizacion desde la web');
      window.location.href = 'mailto:gerencia@mg.com.co?subject=' + asunto + '&body=' + body;
    });
  }

  /* ---------- 8. Ano del pie ---------- */

  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
