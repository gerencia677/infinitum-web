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
  if (menu) { menu.addEventListener('click', function (e) { if (e.target === menu) { setMenu(false); } }); }
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
        if (word.textContent.trim() === label) { return; }   // ya dice eso, no parpadea
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
      // Red de seguridad. Si algo falla, a los 2,5 segundos se ve todo.
      setTimeout(function () {
        Array.prototype.forEach.call(risers, function (r) { r.classList.add('in'); });
      }, 2500);
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

  /* Anos cumplidos: Infinitum nacio el 5 de abril de 2005. El numero cambia cada 5 de abril, en hora de Colombia. */
  var PAL_ES = { 21: 'Veintiún', 22: 'Veintidós', 23: 'Veintitrés', 24: 'Veinticuatro', 25: 'Veinticinco', 26: 'Veintiséis', 27: 'Veintisiete', 28: 'Veintiocho', 29: 'Veintinueve', 30: 'Treinta' };
  var PAL_EN = { 21: 'Twenty-one', 22: 'Twenty-two', 23: 'Twenty-three', 24: 'Twenty-four', 25: 'Twenty-five', 26: 'Twenty-six', 27: 'Twenty-seven', 28: 'Twenty-eight', 29: 'Twenty-nine', 30: 'Thirty' };
  function aniosCumplidos() {
    var n = ahoraBogota(), y, m, d;
    if (n) { y = parseInt(n.fecha.slice(0, 4), 10); m = parseInt(n.fecha.slice(5, 7), 10); d = parseInt(n.fecha.slice(8, 10), 10); }
    else { var h = new Date(); y = h.getFullYear(); m = h.getMonth() + 1; d = h.getDate(); }
    return y - 2005 - ((m > 4 || (m === 4 && d >= 5)) ? 0 : 1);
  }
  function ponerTokens(txt) {
    var n = aniosCumplidos();
    return txt.replace(/\[\[ANIOS\]\]/g, String(n)).replace(/\[\[ANIOS_ES\]\]/g, PAL_ES[n] || String(n))
      .replace(/\[\[ANIOS_EN\]\]/g, PAL_EN[n] || String(n)).replace(/\[\[HASTA\]\]/g, String(2005 + n));
  }

  function applyLang(lang) {
    document.documentElement.setAttribute('lang', lang);
    Array.prototype.forEach.call(document.querySelectorAll('[data-es]'), function (el) {
      var txt = el.getAttribute('data-' + lang);
      if (txt !== null && txt !== undefined) { el.textContent = ponerTokens(txt); }
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
    var ok = document.createElement('div');
    ok.className = 'form-ok';
    ok.hidden = true;
    ok.setAttribute('role', 'status');
    form.parentNode.insertBefore(ok, form.nextSibling);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var en = (readLang() === 'en');
      var d = new FormData(form);
      var nombre = (d.get('nombre') || '').toString().trim();
      var texto = [
        'Nombre: ' + nombre,
        'Ciudad: ' + (d.get('ciudad') || ''),
        'Correo: ' + (d.get('correo') || ''),
        'Telefono: ' + (d.get('telefono') || ''),
        '',
        (d.get('mensaje') || '')
      ].join('\n');
      var asunto = 'Solicitud de cotizacion desde la web';
      // Va a ventas. Gerencia queda en copia para que nada se pierda.
      var mail = 'mailto:ventas@mg.com.co?cc=gerencia@mg.com.co'
        + '&subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(texto);
      var wa = 'https://wa.me/573188367218?text='
        + encodeURIComponent('Hola, soy ' + nombre + '. Escribo desde la pagina de Infinitum.\n\n' + (d.get('mensaje') || ''));
      ok.innerHTML =
        '<h3>' + (en ? 'Almost done' : 'Casi listo') + '</h3>' +
        '<p>' + (en
          ? 'Your message is ready. Choose how to send it. We reply within 12 business hours.'
          : 'Su mensaje está listo. Elija cómo enviarlo. Le respondemos en menos de 12 horas hábiles.') + '</p>' +
        '<div class="form-ok__btns">' +
        '<a class="pill pill--gold" href="' + mail + '">' + (en ? 'Open my email' : 'Abrir mi correo') + '</a>' +
        '<a class="pill" style="background:var(--navy);color:#fff" href="' + wa + '" target="_blank" rel="noopener">' + (en ? 'Send on WhatsApp' : 'Enviar por WhatsApp') + '</a>' +
        '</div>';
      ok.hidden = false;
      try { ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (x) {}
      window.location.href = mail;   // intenta abrir el correo; si no abre, quedan los dos botones
    });
  }

  /* ---------- 8. De que pagina salio el lead ---------- */

  var waBtn = document.querySelector('[data-wa]');
  if (waBtn) {
    var deDonde = (document.title.split('—')[0] || '').trim();
    var saludo = (!deDonde || deDonde === 'Infinitum')
      ? 'Hola, escribo desde la pagina de Infinitum. Quiero cotizar un proyecto.'
      : 'Hola, escribo desde la pagina de Infinitum, seccion ' + deDonde
        + '. Quiero cotizar un proyecto.';
    waBtn.setAttribute('href', waBtn.getAttribute('href') + '?text=' + encodeURIComponent(saludo));
  }

  /* ---------- 9. Ano del pie ---------- */

  /* ---------- 7. Horario de atencion: abierto o fuera de horario, en hora de Colombia ---------- */
  /* Lunes 8:00 a 16:00, martes a viernes 8:00 a 16:30, sabado 8:00 a 12:00. Festivos (Ley Emiliani) de oct-2026 a 2027;
     despues de 2027 hay que agregar los del ano nuevo o el estado dira "abierto" un festivo. */
  var FESTIVOS = ['2026-10-12', '2026-11-02', '2026-11-16', '2026-12-08', '2026-12-25',
    '2027-01-01', '2027-01-11', '2027-03-22', '2027-03-25', '2027-03-26', '2027-05-10', '2027-05-31', '2027-06-07',
    '2027-07-05', '2027-07-20', '2027-08-07', '2027-08-16', '2027-10-18', '2027-11-01', '2027-11-15', '2027-12-08', '2027-12-25'];
  var HORARIO = { 1: [480, 960], 2: [480, 990], 3: [480, 990], 4: [480, 990], 5: [480, 990], 6: [480, 720] };
  var DIAS_ES = ['el domingo', 'el lunes', 'el martes', 'el miércoles', 'el jueves', 'el viernes', 'el sábado'];
  var DIAS_EN = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function ahoraBogota() {
    try {
      var f = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Bogota', year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', hour12: false, weekday: 'short' }).formatToParts(new Date());
      var o = {}; f.forEach(function (p) { o[p.type] = p.value; });
      var dias = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      return { fecha: o.year + '-' + o.month + '-' + o.day, dia: dias[o.weekday], min: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
    } catch (err) { return null; }
  }
  function sumarDia(fecha, n) {
    var d = new Date(fecha + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n);
    return { fecha: d.toISOString().slice(0, 10), dia: d.getUTCDay() };
  }
  function laboral(fecha, dia) { return HORARIO[dia] && FESTIVOS.indexOf(fecha) === -1; }

  function pintarEstado() {
    var els = document.querySelectorAll('[data-estado]');
    if (!els.length) { return; }
    var n = ahoraBogota();
    if (!n) { return; }
    var h = laboral(n.fecha, n.dia) ? HORARIO[n.dia] : null;
    var es, en, abierto = !!(h && n.min >= h[0] && n.min < h[1]);
    if (abierto) {
      es = 'Atendemos ahora'; en = 'We are available now';
    } else {
      var cuando_es, cuando_en;
      if (h && n.min < h[0]) { cuando_es = 'hoy'; cuando_en = 'today'; }
      else {
        var k = 1, s = sumarDia(n.fecha, 1);
        while (!laboral(s.fecha, s.dia) && k < 8) { k += 1; s = sumarDia(n.fecha, k); }
        cuando_es = (k === 1) ? 'mañana' : DIAS_ES[s.dia]; cuando_en = (k === 1) ? 'tomorrow' : DIAS_EN[s.dia];
      }
      es = 'Fuera de horario. Le respondemos ' + cuando_es + ' desde las 8:00 a. m.';
      en = 'Outside office hours. We reply ' + cuando_en + ' from 8:00 am.';
    }
    var lang = document.documentElement.getAttribute('lang') === 'en' ? 'en' : 'es';
    Array.prototype.forEach.call(els, function (el) {
      el.setAttribute('data-es', es); el.setAttribute('data-en', en);
      el.textContent = lang === 'en' ? en : es;
      el.classList.toggle('off', !abierto);
    });
  }
  pintarEstado();
  setInterval(pintarEstado, 60000);

  /* ---------- 8. Los anos de trayectoria: el numero cambia solo cada 5 de abril ---------- */
  function pintarAnios() {
    var n = aniosCumplidos();
    Array.prototype.forEach.call(document.querySelectorAll('[data-anios]'), function (el) { el.textContent = String(n); });
    Array.prototype.forEach.call(document.querySelectorAll('.sello__v em'), function (el) { el.innerHTML = '2005<br>' + (2005 + n); });
    var sello = document.querySelector('.sello');
    if (sello) { sello.setAttribute('aria-label', n + ' años de trayectoria, desde 2005'); }
    applyLang(readLang());
  }
  pintarAnios();
  setInterval(function () { if (aniosCumplidos() !== window.__aniosPintados) { window.__aniosPintados = aniosCumplidos(); pintarAnios(); } }, 600000);
  window.__aniosPintados = aniosCumplidos();

  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
