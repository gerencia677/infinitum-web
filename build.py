#!/usr/bin/env python3
"""
Arma el sitio de Infinitum.

Junta cada archivo de `pages/` con la plantilla `templates/base.html`
y escribe el resultado en `docs/`. Copia `assets/` tal cual.

Se corre asi, y no necesita instalar nada:

    python3 build.py

La cabecera, el menu y el pie viven en UN solo archivo, `templates/base.html`.
Se cambian ahi una vez y quedan cambiados en las ocho paginas.
"""

import re
import shutil
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PLANTILLA = RAIZ / "templates" / "base.html"
PAGINAS = RAIZ / "pages"
ASSETS = RAIZ / "assets"
SALIDA = RAIZ / "docs"   # docs/ es la carpeta que GitHub Pages publica sola

# ---------- Años de trayectoria ----------
# Infinitum nació el 5 de abril de 2005 (orden de Juan David, 9-oct-2026). El año cumplido cambia
# cada 5 de abril. La página lo recalcula sola en el navegador; esto deja bien el HTML que se
# construye y las descripciones que leen Google y WhatsApp.
FUND_ANIO, FUND_MES, FUND_DIA = 2005, 4, 5
PALABRAS_ES = {21: "Veintiún", 22: "Veintidós", 23: "Veintitrés", 24: "Veinticuatro", 25: "Veinticinco",
               26: "Veintiséis", 27: "Veintisiete", 28: "Veintiocho", 29: "Veintinueve", 30: "Treinta"}
PALABRAS_EN = {21: "Twenty-one", 22: "Twenty-two", 23: "Twenty-three", 24: "Twenty-four", 25: "Twenty-five",
               26: "Twenty-six", 27: "Twenty-seven", 28: "Twenty-eight", 29: "Twenty-nine", 30: "Thirty"}


def anios_cumplidos(hoy=None):
    if hoy is None:
        hoy = datetime.now(timezone(timedelta(hours=-5)))  # hora de Colombia
    return hoy.year - FUND_ANIO - (0 if (hoy.month, hoy.day) >= (FUND_MES, FUND_DIA) else 1)


def valores_anios():
    n = anios_cumplidos()
    return {"[[ANIOS]]": str(n), "[[ANIOS_ES]]": PALABRAS_ES.get(n, str(n)),
            "[[ANIOS_EN]]": PALABRAS_EN.get(n, str(n)), "[[HASTA]]": str(FUND_ANIO + n)}


def poner_anios(texto):
    """Cambia los marcadores [[ANIOS]] solo en el texto visible, en aria-label y en meta content.
    Los atributos data-es y data-en conservan el marcador: el navegador lo resuelve al cambiar de idioma."""
    v = valores_anios()

    def cambiar(t):
        for k, x in v.items():
            t = t.replace(k, x)
        return t

    texto = re.sub(r">([^<>]*)<", lambda m: ">" + cambiar(m.group(1)) + "<", texto)
    texto = re.sub(r'(aria-label|content)="([^"]*)"', lambda m: '{}="{}"'.format(m.group(1), cambiar(m.group(2))), texto)
    return texto


CABECERA = re.compile(r"^<!--\s*(.*?)\s*-->", re.DOTALL)
SELLO = ""


def leer_frente(texto):
    """Saca el bloque de datos del principio de la pagina."""
    m = CABECERA.match(texto)
    if not m:
        return {}, texto
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea:
            k, v = linea.split(":", 1)
            datos[k.strip().lower()] = v.strip()
    return datos, texto[m.end():].lstrip("\n")


def main():
    if not PLANTILLA.exists():
        sys.exit("Falta templates/base.html")

    base = PLANTILLA.read_text(encoding="utf-8")
    global SELLO
    SELLO = time.strftime("%Y%m%d%H%M%S")

    # Se vacia por dentro, no se borra la carpeta. Si se borra, un servidor
    # que ya este corriendo ahi adentro se queda sirviendo archivos viejos
    # y uno cree que el cambio no sirvio. Costo un rato el 18-sep-2026.
    SALIDA.mkdir(parents=True, exist_ok=True)
    for hijo in SALIDA.iterdir():
        if hijo.is_dir():
            shutil.rmtree(hijo)
        else:
            hijo.unlink()

    shutil.copytree(ASSETS, SALIDA / "assets")

    archivos = sorted(PAGINAS.glob("*.html"))
    if not archivos:
        sys.exit("No hay paginas en pages/")

    for pag in archivos:
        crudo = pag.read_text(encoding="utf-8")
        datos, cuerpo = leer_frente(crudo)

        html = base
        html = html.replace("{{TITLE}}", datos.get("title", "Infinitum"))
        html = html.replace("{{DESC}}", datos.get("desc", ""))
        html = html.replace("{{SLUG}}", datos.get("slug", pag.name))
        html = html.replace("{{HDR_MOD}}", datos.get("hdr", ""))
        html = html.replace("{{CONTENT}}", cuerpo)
        html = poner_anios(html)
        # Sello de version en css y js. Sin esto el navegador se queda con
        # la copia vieja y uno jura que el cambio no sirvio.
        html = html.replace("assets/css/site.css", "assets/css/site.css?v=" + SELLO)
        html = html.replace("assets/js/site.js", "assets/js/site.js?v=" + SELLO)

        destino = SALIDA / pag.name
        destino.write_text(html, encoding="utf-8")
        print("  {:<22} {:>7,} bytes".format(pag.name, len(html)))

    # Para servidores que sirven carpetas sin index
    (SALIDA / "404.html").write_text(
        (SALIDA / "index.html").read_text(encoding="utf-8"), encoding="utf-8"
    )

    print("\nListo. {} paginas en docs/".format(len(archivos)))


if __name__ == "__main__":
    main()
