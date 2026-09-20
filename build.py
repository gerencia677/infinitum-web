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
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PLANTILLA = RAIZ / "templates" / "base.html"
PAGINAS = RAIZ / "pages"
ASSETS = RAIZ / "assets"
SALIDA = RAIZ / "docs"   # docs/ es la carpeta que GitHub Pages publica sola

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
