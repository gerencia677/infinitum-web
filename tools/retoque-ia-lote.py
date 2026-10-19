#!/usr/bin/env python3
"""Retoque fiel con IA, en lote, sobre las fotos publicadas (galerias de Arquitectura y Paseo Junin).
Corrige verticales, luz y limpieza SIN rediseñar: el edificio, los muebles y los materiales quedan como en la foto.
Deja todo en una carpeta de revision con antes/despues; NO publica. Uso: python3 tools/retoque-ia-lote.py [--solo res-005,cor-003] [--workers 6]"""
import os, sys, json, math, subprocess, collections, argparse, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
LISTAS = Path("/Users/juangomezramirez/Desktop/01 COLOMBIA/INFINITUM LATAM/FOTOS PROYECTOS INFINITUM/FOTOS ORGANIZADAS/_LISTAS PARA PUBLICAR")
PJ = Path("/Users/juangomezramirez/Desktop/01 COLOMBIA/ARQUITECTURA/HECTOR HELI GOMEZ/2026 HECTOR HELI GOMEZ/OCTUBRE 2026 HECTOR HELI GOMEZ/FOTOS PASEO JUNIN SANTUARIO OBRA TERMINADA")
SALIDA = Path.home() / "dev" / "retoque-ia-revision"
EDIT = Path.home() / ".claude/skills/nano-banana/scripts/edit_image.py"
PY = Path.home() / ".claude/skills/nano-banana/.venv/bin/python"
CONLOGO = {"Diabono", "Virtual Zone Technology", "Insumos Oro Rosa oficina", "Oficinas Bot 21 Bitania", "Oficinas Bot 21 (2020)"}
PJ_IDS = [24, 46, 111, 109, 121, 79, 82, 85, 20, 43, 94, 72, 61, 75, 92, 58, 150, 28, 27, 44, 84, 77, 80, 34, 23, 140]

PROMPT = ("STRICT FIDELITY photographic retouch of a real architectural photograph, as a top architectural photographer would do in post-production. "
          "The architecture, the layout, every piece of furniture, every object, the materials and their real colors, the signs and the camera viewpoint must stay EXACTLY as in the source: "
          "do not redesign, do not invent, do not add or move any architectural element, furniture or decor. Only do this: "
          "(1) straighten the image so vertical lines are truly vertical and horizontal lines level, correcting lens distortion and converging verticals; "
          "(2) balance exposure and white balance with warm, natural, elegant light, recover shadows and highlights, and make the light lines and fixtures look even and aligned; "
          "(3) make surfaces crisp and clean: flat panels with straight clean joints, no waviness, no bubbles, no stains, crisp wood and stone; "
          "(4) remove only what does not belong: stray cables, plastic covers, boxes, bags, trash, temporary signs, price tags, cones, clutter and passers-by, and for exteriors the messy surroundings, replacing them with a natural clean continuation; "
          "(5) keep warm brown wood and brick clearly distinct from black and grey materials. Photorealistic, natural, no text added.")


def trabajos():
    t = []
    for cat, pre in (("Residencial", "res"), ("Corporativo", "cor")):
        por = collections.OrderedDict()
        for p in sorted(os.listdir(LISTAS / cat)):
            d = LISTAS / cat / p
            if d.is_dir() and p not in CONLOGO:
                por[p] = sorted(os.listdir(d))
        k = 0
        orden = []
        while any(por.values()):
            for p in list(por):
                if por[p]:
                    orden.append(LISTAS / cat / p / por[p].pop(0))
        for k, f in enumerate(orden, 1):
            t.append((f"{pre}-{k:03d}", f))
    for k, i in enumerate(PJ_IDS, 1):
        t.append((f"pj-{k:02d}", PJ / f"paseo-junin-{i:03d}.jpg"))
    return t


def preparar(src, dst):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(dst, quality=92)
    return im.size


def ratio(w, h):
    r = w / h
    opts = {"1:1": 1, "3:2": 1.5, "2:3": 2 / 3, "4:3": 4 / 3, "3:4": 0.75, "16:9": 16 / 9, "9:16": 9 / 16, "4:5": 0.8, "5:4": 1.25}
    return min(opts, key=lambda k: abs(opts[k] - r))


def huella(im, n=48):
    g = im.convert("L").resize((n, n), Image.LANCZOS).filter(ImageFilter.FIND_EDGES)
    v = list(g.getdata()); m = sum(v) / len(v); v = [x - m for x in v]
    s = math.sqrt(sum(x * x for x in v)) or 1
    return [x / s for x in v]


def procesar(job):
    nombre, src = job
    ent = SALIDA / "entrada" / f"{nombre}.jpg"; sal = SALIDA / "salida" / f"{nombre}.png"
    if sal.exists():
        return nombre, "ya"
    ent.parent.mkdir(parents=True, exist_ok=True); sal.parent.mkdir(parents=True, exist_ok=True)
    w, h = preparar(src, ent)
    for intento in range(10):
        r = subprocess.run([str(PY), str(EDIT), str(ent), PROMPT, str(sal), "--aspect", ratio(w, h)], capture_output=True, text=True, timeout=300)
        if not sal.exists() and "RESOURCE_EXHAUSTED" in (r.stderr + r.stdout):
            time.sleep(75); continue          # limite de gasto por minuto: se espera y se reintenta
        if sal.exists():
            a = Image.open(ent).convert("RGB"); b = Image.open(sal).convert("RGB")
            sc = sum(x * y for x, y in zip(huella(a), huella(b.resize(a.size))))
            return nombre, f"ok {sc:.2f}"
        time.sleep(4)
    return nombre, "FALLO " + (r.stderr or r.stdout)[-120:]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--solo"); ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    jobs = trabajos()
    if a.solo:
        s = set(a.solo.split(",")); jobs = [j for j in jobs if j[0] in s]
    print(len(jobs), "fotos", flush=True)
    SALIDA.mkdir(parents=True, exist_ok=True)
    res = {}
    with ThreadPoolExecutor(a.workers) as ex:
        for nombre, est in ex.map(procesar, jobs):
            res[nombre] = est; print(nombre, est, flush=True)
            (SALIDA / "estado.json").write_text(json.dumps(res, indent=1))
