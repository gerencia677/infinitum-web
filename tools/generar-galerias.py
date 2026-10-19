#!/usr/bin/env python3
"""Genera las galerias completas de Arquitectura residencial y corporativa (mosaico por columnas, sin recortes).
Se corre: python3 tools/generar-galerias.py && python3 build.py"""
import glob, os
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def a(es, en):
    return f'data-es="{escape(es)}" data-en="{escape(en)}"'


def pagina(slug, pref, titulo, desc, hero, eb, h1, intro, alt, vuelta, cierre):
    fotos = sorted(glob.glob(str(RAIZ / "assets/img/galeria" / f"{pref}-*.jpg")))

    def ruta(f):
        b = os.path.basename(f)
        return f"assets/img/galeria2/{b}" if (RAIZ / "assets/img/galeria2" / b).exists() else f"assets/img/galeria/{b}"
    items = "".join(
        f'<a href="{ruta(f)}" data-lb><img src="{ruta(f)}" alt="{escape(alt[0])}, foto {i}" loading="lazy"></a>'
        for i, f in enumerate(fotos, 1))
    return f'''<!--
title: {titulo}
desc: {desc}
slug: {slug}
-->

<section class="phero">
  <img src="{hero}" alt="" aria-hidden="true">
  <div class="phero__in">
    <p class="eyebrow" {a(*eb)}>{eb[0]}</p>
    <h1 {a(*h1)}>{h1[0]}</h1>
    <p {a(*intro)}>{intro[0]}</p>
  </div>
</section>

<section class="pv__proy">
  <div class="wrap">
    <div class="gal-masonry rise">{items}</div>
    <p class="rise" style="text-align:center;margin-top:30px"><a class="pill pill--line" href="{vuelta[0]}" {a(vuelta[1], vuelta[2])}>{vuelta[1]}</a></p>
  </div>
</section>

<section class="on-dark">
  <div class="wrap center">
    <h2 class="big" {a(*cierre)}>{cierre[0]}</h2>
    <p><a class="pill pill--gold" href="contacto.html" {a("Agendar una conversación", "Book a conversation")}>Agendar una conversación</a></p>
  </div>
</section>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
'''


(RAIZ / "pages" / "arquitectura-residencial.html").write_text(pagina(
    "arquitectura-residencial.html", "res", "Arquitectura residencial — Infinitum",
    "Galería de arquitectura residencial de Infinitum: casas y apartamentos diseñados y construidos por un mismo equipo.",
    "assets/img/estudio/res-sala.jpg",
    ("GALERÍA · ARQUITECTURA RESIDENCIAL", "GALLERY · RESIDENTIAL ARCHITECTURE"),
    ("Hogares para vivirlos y heredarlos.", "Homes to live in and pass on."),
    ("Casas y apartamentos que la familia siente suyos desde el primer día. Los diseñamos y los construimos, cuidando la luz, los materiales y cada detalle.",
     "Houses and apartments the family feels are theirs from the first day. We design them and build them, caring for light, materials and every detail."),
    ("Arquitectura residencial de Infinitum", "Infinitum residential architecture"),
    ("estudio-de-arquitectura.html#residencial", "Volver al estudio de arquitectura", "Back to the architecture studio"),
    ("Conversemos sobre el hogar que usted imagina.", "Let us talk about the home you imagine.")), encoding="utf-8")

(RAIZ / "pages" / "arquitectura-corporativa.html").write_text(pagina(
    "arquitectura-corporativa.html", "cor", "Arquitectura corporativa — Infinitum",
    "Galería de arquitectura corporativa de Infinitum: oficinas y sedes trazadas y ejecutadas por un mismo equipo.",
    "assets/img/estudio/cor-sala.jpg",
    ("GALERÍA · ARQUITECTURA CORPORATIVA", "GALLERY · CORPORATE ARCHITECTURE"),
    ("Oficinas donde el equipo se siente bien.", "Offices where the team feels good."),
    ("Sedes y oficinas con luz, madera y orden. Las trazamos y las ejecutamos hasta la primera mañana de trabajo.",
     "Headquarters and offices with light, wood and order. We draw them and carry them out until the first working morning."),
    ("Arquitectura corporativa de Infinitum", "Infinitum corporate architecture"),
    ("estudio-de-arquitectura.html#corporativo", "Volver al estudio de arquitectura", "Back to the architecture studio"),
    ("Conversemos sobre la oficina que usted imagina.", "Let us talk about the office you imagine.")), encoding="utf-8")
print("ok")
