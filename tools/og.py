"""og.py — Dibuja la tarjeta social de 1200x630 con la paleta de la propia página.

Sin esta imagen (y sin las etiquetas OpenGraph que pone build.py) LinkedIn, Slack y
cualquier otro sitio donde se pegue el enlace no pueden construir una vista previa:
el <head> no tenía ni título. Se vio al intentar adjuntar el enlace en LinkedIn.
"""
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(AQUI), "og.png")
W, H = 1200, 630
FONDO, TINTA, TENUE, AMBAR, LINEA = "#070a11", "#eef2f8", "#6b7a94", "#f0a830", "#1c2433"

CAND = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]
MONO = ["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"]


def fuente(cands, size):
    for p in cands:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default(size)


im = Image.new("RGB", (W, H), FONDO)
d = ImageDraw.Draw(im)

# filete ámbar arriba: el mismo acento que la página usa donde algo se decide
d.rectangle([0, 0, W, 6], fill=AMBAR)

d.text((72, 92), "AUTONOMOUS QUANTITATIVE RESEARCH AGENT  ·  2026",
       font=fuente(MONO, 22), fill=TENUE)
d.text((72, 150), "Hypothesis Ledger", font=fuente(CAND, 96), fill=TINTA)
d.text((72, 272), "11,514 pre-registered hypotheses.", font=fuente(CAND, 40), fill=TINTA)
d.text((72, 324), "Zero survivors — and that is the result.", font=fuente(CAND, 40), fill=TENUE)

d.line([(72, 432), (W - 72, 432)], fill=LINEA, width=1)

cifras = [("50,794", "configurations measured"), ("t \u2265 4.24", "deflated bar"),
          ("0", "survivors"), ("547,569", "real H1 bars")]
x = 72
for val, et in cifras:
    col = AMBAR if val == "0" else TINTA
    d.text((x, 468), val, font=fuente(MONO, 38), fill=col)
    d.text((x, 520), et, font=fuente(MONO, 19), fill=TENUE)
    x += 272

d.text((72, 576), "maugarza2809-crypto.github.io/quant-research-agent",
       font=fuente(MONO, 20), fill=TENUE)

im.save(OUT, "PNG", optimize=True)
print(f"og.png — {W}x{H}, {os.path.getsize(OUT)/1024:.0f} kB")
