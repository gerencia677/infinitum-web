#!/usr/bin/env python3
"""Panel de retoque de Infinitum: arquitectura + producto, solo con Pillow.

Cuatro voces, una receta (ver pages de la bóveda: Panel de Retoque):
  1. Retocador de arquitectura: balance de blancos, sombras abiertas sin aplastar, claridad local.
  2. Retocador de producto: blancos limpios, color vivo en lo que se vende, brillo controlado en vidrio y metal.
  3. Director de arte: viñeta suave, tono cálido en las luces y frío en las sombras, sin saturar de más.
  4. Revisor de verdad: no cambia nada construido, no agrega ni quita objetos. Solo luz, color y nitidez.

Uso: python3 tools/retoque-comercial.py entrada.jpg salida.jpg [interior|fachada]
"""
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageChops, ImageStat

def balance_blancos(im, fuerza=0.55):
    st = ImageStat.Stat(im.resize((64, 64)))
    r, g, b = st.mean
    m = (r + g + b) / 3
    k = [1 + (m / c - 1) * fuerza for c in (r, g, b)]
    ch = [c.point(lambda v, f=f: min(255, int(v * f))) for c, f in zip(im.split(), k)]
    return Image.merge("RGB", ch)

def curva(im, sombras=0.10, luces=0.06, s=0.16):
    """Abre sombras, recupera luces y da una S suave."""
    lut = []
    for v in range(256):
        x = v / 255
        x = x + sombras * (1 - x) ** 2.4 * (1 - x)          # levanta las sombras
        x = x - luces * x ** 3                              # contiene las luces
        y = x + s * (x - 0.5) * (1 - abs(2 * x - 1)) * 2    # curva en S
        lut.append(max(0, min(255, int(round(y * 255)))))
    return im.point(lut * 3)

def claridad(im, radio=36, cantidad=38):
    return im.filter(ImageFilter.UnsharpMask(radius=radio, percent=cantidad, threshold=0))

def vibrance(im, cantidad=0.28):
    return ImageEnhance.Color(im).enhance(1 + cantidad * 0.5)

def brillo_neon(im, umbral=238, radio=9, fuerza=0.30):
    lum = im.convert("L").point(lambda v: 255 if v >= umbral else 0).filter(ImageFilter.GaussianBlur(radio))
    glow = Image.composite(im, Image.new("RGB", im.size, (0, 0, 0)), lum).filter(ImageFilter.GaussianBlur(radio / 2))
    return Image.blend(im, ImageChops.screen(im, glow), fuerza)

def tono(im, calido=(255, 232, 205), frio=(214, 228, 255), fuerza=0.07):
    lum = im.convert("L")
    luces = lum.point(lambda v: int(255 * (v / 255) ** 2.2))
    sombras = lum.point(lambda v: int(255 * (1 - v / 255) ** 2.2))
    a = ImageChops.multiply(im, Image.new("RGB", im.size, calido))
    b = ImageChops.multiply(im, Image.new("RGB", im.size, frio))
    im = Image.composite(Image.blend(im, a, fuerza * 2.2), im, luces)
    return Image.composite(Image.blend(im, b, fuerza * 2.2), im, sombras)

def vineta(im, fuerza=0.14):
    w, h = im.size
    m = Image.radial_gradient("L").resize((w, h)).point(lambda v: int(255 * min(1, max(0, (v / 255 - 0.55) / 0.45) ** 1.6)))
    oscuro = ImageChops.multiply(im, Image.new("RGB", im.size, (205, 205, 215)))
    return Image.composite(Image.blend(im, oscuro, fuerza * 3), im, m)

def retocar(im, modo="interior", ancho=2560):
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = im.filter(ImageFilter.GaussianBlur(0.8))                    # limpia la compresión de WhatsApp
    im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    im = balance_blancos(im, 0.5 if modo == "interior" else 0.35)
    im = ImageOps.autocontrast(im, cutoff=0.25)
    im = curva(im, sombras=0.07, luces=0.04, s=0.10)
    im = claridad(im, 40, 22)
    im = vibrance(im, 0.26 if modo == "interior" else 0.18)
    if modo == "interior":
        pass
    im = vineta(im, 0.07)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.3, percent=85, threshold=2))   # nitidez final
    return im

if __name__ == "__main__":
    ent, sal = sys.argv[1], sys.argv[2]
    modo = sys.argv[3] if len(sys.argv) > 3 else "interior"
    retocar(Image.open(ent), modo).save(sal, quality=88, optimize=True, progressive=True)
