#!/usr/bin/env python3
"""Pasa a assets/img/galeria2 y assets/img/paseo-junin2 las fotos retocadas con IA que Juan David aprobo.
Uso: python3 tools/publicar-retoque-ia.py [--todas-ok | --lista res-001,cor-004] [--excluir res-050]"""
import argparse, json, shutil
from pathlib import Path
from PIL import Image, ImageFilter
RAIZ = Path(__file__).resolve().parent.parent
R = Path.home() / "dev" / "retoque-ia-revision"
ap = argparse.ArgumentParser(); ap.add_argument("--todas-ok", action="store_true"); ap.add_argument("--lista"); ap.add_argument("--excluir", default="")
a = ap.parse_args()
cl = json.loads((R / "clasificacion.json").read_text())
sel = cl["ok"] if a.todas_ok else (a.lista.split(",") if a.lista else [])
sel = [n for n in sel if n not in set(a.excluir.split(","))]
g2 = RAIZ / "assets/img/galeria2"; p2 = RAIZ / "assets/img/paseo-junin2"; g2.mkdir(exist_ok=True); p2.mkdir(exist_ok=True)
for n in sel:
    im = Image.open(R / "salida" / f"{n}.png").convert("RGB")
    long = max(im.size)
    if long < 1600:
        im = im.resize((round(im.width * 1600 / long), round(im.height * 1600 / long)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.3, percent=45, threshold=2))
    (p2 if n.startswith("pj-") else g2).mkdir(exist_ok=True)
    im.save((p2 if n.startswith("pj-") else g2) / f"{n}.jpg", quality=86, optimize=True, progressive=True)
print("publicadas en carpetas nuevas:", len(sel))
