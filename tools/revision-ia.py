#!/usr/bin/env python3
"""Arma las hojas de revision antes/despues del retoque IA y separa lo que pasa el control de fidelidad.
Uso: python3 tools/revision-ia.py   (lee ~/dev/retoque-ia-revision)"""
import json, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path.home() / "dev" / "retoque-ia-revision"
import math
from PIL import ImageFilter
est = {}
for f in sorted((R / "salida").glob("*.png")):
    est[f.stem] = "hecha"
trabajos = sorted(p.stem for p in (R / "entrada").glob("*.jpg"))
for n in trabajos:
    est.setdefault(n, "FALLO")


def huella(im, n=48):
    g = im.convert("L").resize((n, n), Image.LANCZOS).filter(ImageFilter.FIND_EDGES)
    v = list(g.getdata()); m = sum(v) / len(v); v = [x - m for x in v]
    sc = math.sqrt(sum(x * x for x in v)) or 1
    return [x / sc for x in v]


def fidelidad(n):
    a = Image.open(R / "entrada" / f"{n}.jpg").convert("RGB"); b = Image.open(R / "salida" / f"{n}.png").convert("RGB").resize(a.size)
    return sum(x * y for x, y in zip(huella(a), huella(b)))

UMBRAL = 0.93
ok, dudosas, fallos = [], [], []
for n, e in sorted(est.items()):
    if e == "hecha":
        sc = fidelidad(n)
        (ok if sc >= UMBRAL else dudosas).append((n, sc))
    else:
        fallos.append(n)
print("pasan:", len(ok), "dudosas:", len(dudosas), "fallos:", len(fallos))
json.dump({"ok": [n for n, _ in ok], "dudosas": [n for n, _ in dudosas], "fallos": fallos}, open(R / "clasificacion.json", "w"))
F = ImageFont.load_default(size=20)
(R / "hojas").mkdir(exist_ok=True)
for f in (R / "hojas").glob("*.jpg"): f.unlink()
todas = sorted(n for n in est if (R / "salida" / f"{n}.png").exists())
H = 330; per = 6
for k in range(0, len(todas), per):
    ch = todas[k:k + per]
    s = Image.new("RGB", (1900, (H + 8) * 3), "white"); d = ImageDraw.Draw(s)
    for j, n in enumerate(ch):
        sal = R / "salida" / f"{n}.png"; ent = R / "entrada" / f"{n}.jpg"
        if not sal.exists(): continue
        a = Image.open(ent).convert("RGB"); b = Image.open(sal).convert("RGB")
        ta = a.resize((round(a.width * H / a.height), H)); tb = b.resize((round(b.width * H / b.height), H))
        x0 = (j % 2) * 950; y0 = (j // 2) * (H + 8)
        s.paste(ta, (x0, y0)); s.paste(tb, (x0 + ta.width + 4, y0))
        marca = "OK" if n in [x for x, _ in ok] else "REVISAR"
        d.rectangle((x0, y0, x0 + 220, y0 + 26), fill=(0, 0, 0)); d.text((x0 + 4, y0 + 2), f"{n} antes  [{marca}]", fill=(255, 230, 80), font=F)
        d.rectangle((x0 + ta.width + 4, y0, x0 + ta.width + 104, y0 + 26), fill=(0, 0, 0)); d.text((x0 + ta.width + 8, y0 + 2), "despues", fill=(255, 230, 80), font=F)
    s.save(R / "hojas" / f"hoja-{k // per + 1:02d}.jpg", quality=80)
print("hojas:", len(list((R / 'hojas').glob('*.jpg'))))
