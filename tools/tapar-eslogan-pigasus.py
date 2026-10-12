"""Tapa el eslogan rojo de neón de la foto del punto de venta (hero-comercial-2.jpg).
Solo PIL. Marca los píxeles rojos, los engorda para llevarse el brillo y rellena cada columna
interpolando entre el muro de arriba y el de abajo, con un poco de grano para que no se vea liso.
Uso: python3 tools/tapar-eslogan-pigasus.py entrada.jpg salida.jpg"""
import random
import sys
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W, H = im.size
px = im.load()
# 1. máscara: rojo fuerte (R alto, G y B bajos) dentro de la franja donde vive el eslogan
mask = Image.new("L", (W, H), 0)
mp = mask.load()
for y in range(0, 420):
    for x in range(250, 1900):
        r, g, b = px[x, y]
        if r > 140 and r > g * 2.2 and r > b * 2.2:
            mp[x, y] = 255
# 2. engordar para incluir el brillo del neón y el borde suavizado
mask = mask.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.MaxFilter(9))
mp = mask.load()
random.seed(7)
out = im.copy()
op = out.load()


def media(x, ys):
    n = len(ys)
    return tuple(sum(px[x, y][c] for y in ys) / n for c in range(3))


for x in range(W):
    y = 0
    while y < H:
        if mp[x, y] and y < 440:
            y0 = y
            while y < 440 and mp[x, y]:
                y += 1
            y1 = y  # [y0, y1) tapado
            arriba = [yy for yy in range(max(0, y0 - 6), y0)] if y0 > 0 else []
            abajo = [yy for yy in range(y1 + 2, min(H, y1 + 8))]
            A = media(x, arriba) if arriba else None
            B = media(x, abajo) if abajo else None
            if A is None:
                A = B
            if B is None:
                B = A
            for yy in range(y0, y1):
                t = (yy - y0) / max(1, y1 - y0 - 1)
                g = random.gauss(0, 2.2)
                op[x, yy] = tuple(max(0, min(255, int(A[c] * (1 - t) + B[c] * t + g))) for c in range(3))
        else:
            y += 1
# 3. suaviza solo la zona tapada para que no queden columnas rayadas
suave = out.filter(ImageFilter.GaussianBlur(1.6))
fino = mask.filter(ImageFilter.GaussianBlur(3))
out = Image.composite(suave, out, fino.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.GaussianBlur(2)))
# 4. quita el tinte rojizo que dejó el brillo: dentro de la zona del eslogan el rojo se baja al nivel del gris
zona = mask.filter(ImageFilter.MaxFilter(61)).filter(ImageFilter.GaussianBlur(6))
zp = zona.load()
op = out.load()
for y in range(0, 440):
    for x in range(250, 1900):
        if zp[x, y] > 20:
            r, g, b = op[x, y]
            if r > g * 1.12:
                k = min(1.0, zp[x, y] / 160)
                nr = int(r * (1 - k) + ((g + b) / 2 * 1.04) * k)
                op[x, y] = (nr, g, b)
out.save(dst, quality=92)
print("listo", dst)
