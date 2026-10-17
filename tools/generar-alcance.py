#!/usr/bin/env python3
"""Genera pages/arquitectura-alcance.html (borrador, noindex): el alcance de la arquitectura de Infinitum.
Se corre: python3 tools/generar-alcance.py && python3 build.py"""
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


ESCALAS = [
    (("INTERIORES", "INTERIORS"), ("Cada detalle, a la medida de su marca o su hogar", "Every detail, made to the measure of your brand or your home"),
     ("Oficinas, tiendas, restaurantes y casas por dentro: distribución, luz, materiales y carpintería fabricada por nosotros.",
      "Offices, stores, restaurants and homes from the inside: layout, light, materials and joinery made by us.")),
    (("CASAS", "HOMES"), ("Un hogar pensado para la manera en que vive su familia", "A home thought for the way your family lives"),
     ("Residencias y apartamentos, del lote a la primera cena en familia.",
      "Houses and apartments, from the plot to the first family dinner.")),
    (("EDIFICIOS", "BUILDINGS"), ("Sedes y edificios que hablan de quien los habita", "Headquarters and buildings that speak for those who inhabit them"),
     ("Desde la implantación en el terreno hasta la fachada, con la estructura resuelta desde el primer trazo.",
      "From the placement on the site to the façade, with the structure resolved from the first line.")),
    (("COMERCIO", "RETAIL"), ("Locales, paseos y centros comerciales", "Stores, promenades and shopping centers"),
     ("Recorridos que invitan a entrar, fachadas que se recuerdan y espacios donde el comercio se siente bien, como Paseo Junín.",
      "Routes that invite you in, façades that are remembered and spaces where retail feels right, like Paseo Junín.")),
]

parts = ['''<!--
title: El alcance de la arquitectura — Infinitum
desc: Del interior a la casa, del edificio al centro comercial: la arquitectura de Infinitum crece con la idea del cliente, con un solo equipo del primer trazo a la obra.
slug: arquitectura-alcance.html
robots: noindex
-->
''']

parts.append(f'''<section class="phero" style="min-height:clamp(520px,86vh,860px)">
  <img src="assets/img/paseo-junin/render-2.jpg" alt="" aria-hidden="true">
  <div class="phero__in">
    {eb("ARQUITECTURA · ALCANCE", "ARCHITECTURE · SCOPE")}
    {h(1, "El alcance lo define su proyecto.", "Your project defines the scope.")}
    {p("De un interior a un edificio, de una casa a un centro comercial. Pensamos cada escala con el mismo cuidado y la construimos con el mismo equipo.", "From an interior to a building, from a house to a shopping center. We think every scale with the same care and build it with the same team.")}
  </div>
</section>
''')

filas = ""
for n, (k, t, d) in enumerate(ESCALAS, 1):
    filas += f'''      <div class="esc__fila">
        <div class="esc__n">{n:02d}</div>
        <div><b {a(*k)}>{k[0]}</b><h3 {a(*t)}>{t[0]}</h3><p {a(*d)}>{d[0]}</p></div>
      </div>
'''
parts.append(f'''<section id="escalas" class="pv__proy">
  <div class="wrap">
    <div class="rise">
      {eb("UNA SOLA MANERA DE PENSAR", "ONE WAY OF THINKING")}
      {h(2, "Cuatro escalas, el mismo criterio.", "Four scales, the same judgment.")}
      {p("La arquitectura no cambia de calidad cuando cambia de tamaño. Lo que se aprende en el detalle de una puerta sirve para el edificio, y lo que se piensa para un edificio cuida el detalle de una puerta.", "Architecture does not change in quality when it changes in size. What is learned in the detail of a door serves the building, and what is thought for a building takes care of the detail of a door.")}
    </div>
    <div class="esc rise">
{filas}    </div>
    <div class="esc__cierre rise">
      {h(3, "Y cuando su idea crece, el equipo crece con ella.", "And when your idea grows, the team grows with it.")}
      {p("No ponemos el techo. Lo ponemos entre los dos, desde la primera conversación.", "We do not set the ceiling. We set it together, from the first conversation.")}
    </div>
  </div>
</section>
''')

parts.append(f'''<section id="paseo-junin" class="on-dark empresas">
  <div class="wrap">
    <div class="rise">
      {eb("PROYECTO DESTACADO · COMERCIO", "FEATURED PROJECT · RETAIL")}
      {h(2, "Paseo Junín", "Paseo Junín", "big")}
      {p("Un paseo comercial en El Santuario, Antioquia: una cubierta continua en madera, columnas vestidas de verde y una plaza escalonada que invita a entrar. Pensado para que el comercio y el paisaje se encuentren.", "A shopping promenade in El Santuario, Antioquia: a continuous timber canopy, green-wrapped columns and a stepped plaza that invites you in. Thought so that retail and landscape meet.", "lead")}
    </div>
    <div class="gal-ed gal-ed--3 rise">
      <a href="assets/img/paseo-junin/render-1.jpg" data-lb><img src="assets/img/paseo-junin/render-1.jpg" alt="Render del paseo comercial Paseo Junín, vista de esquina con cubierta en madera y vegetación" loading="lazy"></a>
      <a href="assets/img/paseo-junin/render-3.jpg" data-lb><img src="assets/img/paseo-junin/render-3.jpg" alt="Render del paseo comercial Paseo Junín, fachada continua y plaza escalonada" loading="lazy"></a>
      <a href="assets/img/paseo-junin/render-4.jpg" data-lb><img src="assets/img/paseo-junin/render-4.jpg" alt="Render del paseo comercial Paseo Junín, columnas vestidas de verde" loading="lazy"></a>
    </div>
    <dl class="ar-ficha-d rise">
      <div><dt {a("Tipología", "Typology")}>Tipología</dt><dd {a("Paseo comercial", "Shopping promenade")}>Paseo comercial</dd></div>
      <div><dt {a("Lugar", "Place")}>Lugar</dt><dd>El Santuario, Antioquia</dd></div>
      <div><dt {a("Alcance", "Scope")}>Alcance</dt><dd {a("Arquitectura y desarrollo del proyecto", "Architecture and project development")}>Arquitectura y desarrollo del proyecto</dd></div>
      <div><dt {a("Imágenes", "Images")}>Imágenes</dt><dd {a("Renders del proyecto", "Project renders")}>Renders del proyecto</dd></div>
    </dl>
  </div>
</section>
''')

parts.append(f'''<section class="on-dark">
  <div class="wrap center">
    {h(2, "Cuéntenos qué tan lejos llega su idea.", "Tell us how far your idea goes.", "big")}
    <p><a class="pill pill--gold" href="contacto.html" {a("Agendar una conversación", "Book a conversation")}>Agendar una conversación</a></p>
  </div>
</section>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
''')
(RAIZ / "pages" / "arquitectura-alcance.html").write_text("\n".join(parts), encoding="utf-8")
print("ok")
