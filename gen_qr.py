# -*- coding: utf-8 -*-
"""Gera QR codes provisorios (um por produto) com rotulo, na pasta qrcodes/."""
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "https://nunoakira-bit.github.io/printer-ar/"

# chave do produto -> rotulo exibido embaixo do QR
PRODUCTS = {
    "demo": "DEMO",
    "flow": "Flow",
}

ACCENT = (0, 160, 227)
DARK = (11, 15, 20)
OUT = os.path.join(os.path.dirname(__file__), "qrcodes")
os.makedirs(OUT, exist_ok=True)

def load_font(size):
    for name in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

for key, label in PRODUCTS.items():
    url = f"{BASE}?p={key}"
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=12, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=DARK, back_color="white").convert("RGB")

    qw, qh = qr_img.size
    pad_top, pad_bottom = 40, 110
    canvas = Image.new("RGB", (qw, qh + pad_top + pad_bottom), "white")
    canvas.paste(qr_img, (0, pad_top))
    draw = ImageDraw.Draw(canvas)

    # barra de marca no topo
    draw.rectangle([0, 0, qw, 10], fill=ACCENT)

    # rotulo do produto
    f_label = load_font(46)
    tb = draw.textbbox((0, 0), label, font=f_label)
    tw = tb[2] - tb[0]
    draw.text(((qw - tw) / 2, qh + pad_top + 18), label, fill=DARK, font=f_label)

    # instrucao
    f_small = load_font(24)
    sub = "Aponte a camera para escanear"
    sb = draw.textbbox((0, 0), sub, font=f_small)
    sw = sb[2] - sb[0]
    draw.text(((qw - sw) / 2, qh + pad_top + 74), sub, fill=(90, 90, 90), font=f_small)

    path = os.path.join(OUT, f"qr-{key}.png")
    canvas.save(path)
    print(f"OK  {path}  ->  {url}")

print("\nTodos os QR codes gerados em:", OUT)
