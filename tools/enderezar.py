#!/usr/bin/env python3
"""Detecta la inclinacion de las verticales y endereza la foto (solo Pillow).
Uso: python3 tools/enderezar.py entrada.jpg [salida.jpg]   o   importar angulo() y enderezar()"""
import math, sys
from PIL import Image, ImageFilter, ImageOps

KX = ImageFilter.Kernel((3, 3), [-1, 0, 1, -2, 0, 2, -1, 0, 1], scale=1, offset=128)
KY = ImageFilter.Kernel((3, 3), [-1, -2, -1, 0, 0, 0, 1, 2, 1], scale=1, offset=128)


def angulo(im, rango=6.0, paso=0.5):
    """Grados que hay que girar la foto (positivo = antihorario) para dejar las verticales rectas.
    Voto tipo Hough: se prueba cada giro y gana el que alinea mas bordes verticales en lineas largas."""
    g = ImageOps.exif_transpose(im).convert("L")
    g.thumbnail((480, 480), Image.LANCZOS)
    g = g.filter(ImageFilter.GaussianBlur(1.0))
    W, H = g.size
    gx = list(g.filter(KX).getdata()); gy = list(g.filter(KY).getdata())
    pts = []
    for idx, (a, b) in enumerate(zip(gx, gy)):
        dx = a - 128; dy = b - 128
        m = math.hypot(dx, dy)
        if m < 60: continue
        d = (math.degrees(math.atan2(dy, dx)) + 90) % 180 - 90
        if abs(d) <= rango + 6:
            pts.append((idx % W - W / 2, idx // W - H / 2, m))
    if len(pts) < 200: return 0.0, 0.0
    ang = [i * paso - rango for i in range(int(2 * rango / paso) + 1)]
    scores = []
    for t in ang:
        c, sn = math.cos(math.radians(t)), math.sin(math.radians(t))
        acc = {}
        for x, y, m in pts:
            r = round(x * c + y * sn)          # distancia de la recta casi vertical de angulo t
            acc[r] = acc.get(r, 0) + m
        scores.append(sum(v * v for v in acc.values()))
    i = max(range(len(ang)), key=lambda k: scores[k])
    media = sum(scores) / len(scores)
    return ang[i], scores[i] / media


def angulo_hist(im, rango=7.0, paso=0.25):
    """Segundo estimador: histograma de direccion de los bordes casi verticales, ponderado por fuerza."""
    g = ImageOps.exif_transpose(im).convert("L")
    g.thumbnail((520, 520), Image.LANCZOS)
    g = g.filter(ImageFilter.GaussianBlur(1.2))
    gx = list(g.filter(KX).getdata()); gy = list(g.filter(KY).getdata())
    n = int(2 * rango / paso) + 1
    hist = [0.0] * n
    for a, b in zip(gx, gy):
        dx = a - 128; dy = b - 128
        m = math.hypot(dx, dy)
        if m < 40: continue
        d = (math.degrees(math.atan2(dy, dx)) + 90) % 180 - 90
        if -rango <= d <= rango: hist[int((d + rango) / paso)] += m
    sm = [sum(hist[max(0, i - 4):i + 5]) / 9 for i in range(n)]
    i = max(range(n), key=lambda k: sm[k])
    return -(i * paso - rango)


def enderezar(im, ang):
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    r = im.rotate(ang, resample=Image.BICUBIC, expand=False)
    t = math.radians(abs(ang))
    k = 1 / (math.cos(t) + math.sin(t) * max(w / h, h / w))
    nw, nh = w * k, h * k
    x0, y0 = (w - nw) / 2, (h - nh) / 2
    return r.crop((round(x0), round(y0), round(x0 + nw), round(y0 + nh)))


if __name__ == "__main__":
    im = Image.open(sys.argv[1]); a, c = angulo(im)
    print(f"angulo {a:+.2f} confianza {c:.2f}")
    if len(sys.argv) > 2: enderezar(im, a).save(sys.argv[2], quality=90)
