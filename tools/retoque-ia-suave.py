#!/usr/bin/env python3
"""Segunda pasada, mas suave, para las fotos que el control de fidelidad marco dudosas."""
import json, subprocess, time, math, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageFilter
R = Path.home() / "dev" / "retoque-ia-revision"
PY = Path.home() / ".claude/skills/nano-banana/.venv/bin/python"; EDIT = Path.home() / ".claude/skills/nano-banana/scripts/edit_image.py"
P = ("Very light, conservative photographic retouch of a real photograph. Change NOTHING about the content: every object, piece of furniture, book, plant, decoration, "
     "their count, position, size and color, the architecture and the camera framing stay exactly identical to the source, with no object added, removed or moved. "
     "Only gently: straighten slightly tilted vertical lines, balance exposure and white balance with warm natural light, and make flat surfaces a little cleaner and smoother. "
     "Photorealistic, same image.")
def huella(im, n=48):
    g = im.convert("L").resize((n, n), Image.LANCZOS).filter(ImageFilter.FIND_EDGES); v = list(g.getdata()); m = sum(v) / len(v); v = [x - m for x in v]
    s = math.sqrt(sum(x * x for x in v)) or 1; return [x / s for x in v]
def ratio(w, h):
    r = w / h; o = {"1:1": 1, "3:2": 1.5, "2:3": 2/3, "4:3": 4/3, "3:4": .75, "16:9": 16/9, "9:16": 9/16, "4:5": .8, "5:4": 1.25}
    return min(o, key=lambda k: abs(o[k] - r))
def hacer(n):
    ent = R / "entrada" / f"{n}.jpg"; sal = R / "salida_suave" / f"{n}.png"; sal.parent.mkdir(exist_ok=True)
    if sal.exists(): return n, "ya"
    w, h = Image.open(ent).size
    for _ in range(8):
        r = subprocess.run([str(PY), str(EDIT), str(ent), P, str(sal), "--aspect", ratio(w, h)], capture_output=True, text=True, timeout=300)
        if sal.exists(): break
        if "RESOURCE_EXHAUSTED" in (r.stderr + r.stdout): time.sleep(70)
    if not sal.exists(): return n, "FALLO"
    a = Image.open(ent).convert("RGB"); b = Image.open(sal).convert("RGB").resize(a.size)
    return n, f"{sum(x*y for x, y in zip(huella(a), huella(b))):.2f}"
if __name__ == "__main__":
    dud = json.load(open(R / "clasificacion.json"))["dudosas"]
    with ThreadPoolExecutor(3) as ex:
        res = dict(ex.map(hacer, dud))
    json.dump(res, open(R / "suave.json", "w"), indent=1); print(res)
