#!/usr/bin/env python3
"""Genera pages/paseo-junin.html: ficha del proyecto Paseo Junín (El Santuario, Antioquia) con su galería.
Se corre: python3 tools/generar-paseo-junin.py && python3 build.py"""
import glob, os
from html import escape
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent


def a(es, en): return f'data-es="{escape(es)}" data-en="{escape(en)}"'
def p(es, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c} {a(es, en)}>{es}</p>'
def h(n, es, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<h{n}{c} {a(es, en)}>{es}</h{n}>'
def eb(es, en): return f'<p class="eyebrow" {a(es, en)}>{es}</p>'


fotos = sorted(glob.glob(str(RAIZ / "assets/img/paseo-junin/pj-*.jpg")))
def ruta(f):
    b = os.path.basename(f)
    if (RAIZ / "assets/img/paseo-junin2" / b.replace(".jpg", "-b.jpg")).exists():
        return "assets/img/paseo-junin2/" + b.replace(".jpg", "-b.jpg")
    return f"assets/img/paseo-junin2/{b}" if (RAIZ / "assets/img/paseo-junin2" / b).exists() else f"assets/img/paseo-junin/{b}"


items = "".join(
    f'<a href="{ruta(f)}" data-lb><img src="{ruta(f)}" alt="Paseo Junín, paseo comercial en El Santuario, Antioquia, foto {i}" loading="lazy"></a>'
    for i, f in enumerate(fotos, 1))

html = f'''<!--
title: Paseo Junín — Infinitum
desc: Paseo Junín, paseo comercial en El Santuario, Antioquia, diseñado y construido por Infinitum: ladrillo, arcos, madera, vidrio y luz.
slug: paseo-junin.html
-->

<section class="phero" style="min-height:clamp(520px,86vh,860px)">
  <img src="assets/img/paseo-junin/hero-paseo-junin-v2.jpg" alt="" aria-hidden="true">
  <div class="phero__in">
    {eb("PROYECTO · ARQUITECTURA COMERCIAL", "PROJECT · COMMERCIAL ARCHITECTURE")}
    {h(1, "Paseo Junín", "Paseo Junín")}
    {p("Un paseo comercial en El Santuario, Antioquia, diseñado y construido por Infinitum. Un lugar que se reconoce desde la calle y se disfruta por dentro.", "A shopping promenade in El Santuario, Antioquia, designed and built by Infinitum. A place recognized from the street and enjoyed from within.")}
  </div>
</section>

<section class="pv__proy">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        {eb("EL PROYECTO", "THE PROJECT")}
        {h(2, "Arquitectura que invita a entrar.", "Architecture that invites you in.")}
      </div>
      <div>
        {p("Una volumetría oscura con rotulación luminosa abraza el paseo. Debajo, muros de ladrillo, arcos con jardineras, cielos de madera y vidrio dejan pasar la luz y la vegetación. De noche, la iluminación cálida dibuja cada arco y cada recorrido.", "A dark volume with luminous signage embraces the promenade. Beneath it, brick walls, arches with planters, timber ceilings and glass let light and greenery through. At night, warm lighting draws every arch and every route.")}
        <div class="pv__chips"><span {a("Arquitectura", "Architecture")}>Arquitectura</span><span {a("Ejecución de obra", "Construction")}>Ejecución de obra</span><span {a("Iluminación", "Lighting")}>Iluminación</span><span {a("Paisajismo", "Landscaping")}>Paisajismo</span></div>
      </div>
    </div>
    <dl class="ar-ficha-d ar-ficha-d--claro rise">
      <div><dt {a("Tipología", "Typology")}>Tipología</dt><dd {a("Paseo comercial", "Shopping promenade")}>Paseo comercial</dd></div>
      <div><dt {a("Lugar", "Place")}>Lugar</dt><dd>El Santuario, Antioquia</dd></div>
      <div><dt {a("Materiales", "Materials")}>Materiales</dt><dd {a("Ladrillo, aluminio compuesto, madera, vidrio y luz LED", "Brick, aluminum composite, timber, glass and LED light")}>Ladrillo, aluminio compuesto, madera, vidrio y luz LED</dd></div>
      <div><dt {a("Alcance", "Scope")}>Alcance</dt><dd {a("Arquitectura y ejecución de obra", "Architecture and construction")}>Arquitectura y ejecución de obra</dd></div>
    </dl>
    <div class="gal-masonry rise" style="margin-top:34px">{items}</div>
    <p class="rise" style="text-align:center;margin-top:30px"><a class="pill pill--line" href="arquitectura-alcance.html" {a("Ver el alcance de nuestra arquitectura", "See the scope of our architecture")}>Ver el alcance de nuestra arquitectura</a></p>
  </div>
</section>

<section class="on-dark">
  <div class="wrap center">
    {h(2, "Cuéntenos qué tan lejos llega su idea.", "Tell us how far your idea goes.", "big")}
    <p><a class="pill pill--gold" href="contacto.html" {a("Agendar una conversación", "Book a conversation")}>Agendar una conversación</a></p>
  </div>
</section>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
'''
(RAIZ / "pages" / "paseo-junin.html").write_text(html, encoding="utf-8")
print("ok", len(fotos))
