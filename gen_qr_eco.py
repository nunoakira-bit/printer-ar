# -*- coding: utf-8 -*-
"""Gera um QR code por item do Ecossistema da Informacao, na pasta qrcodes/eco/.

Cada QR aponta para ecossistema.html?i=<id>. A pagina AR le o proprio conteudo
do QR para saber qual item mostrar, entao o mesmo QR serve para (a) abrir a
experiencia pelo app de camera e (b) ancorar a animacao sobre a bolinha impressa.
"""
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageFont

BASE = "https://nunoakira-bit.github.io/printer-ar/ecossistema.html"

# id do item -> (rotulo impresso, cor de acento)
ITEMS = {
    "doc":        ("Documento fisico", (122, 33, 64)),
    "scanner":    ("Scanners",         (176, 111, 214)),
    "multi":      ("Multifuncionais",  (176, 111, 214)),
    "computador": ("Computadores",     (91, 98, 112)),
    "airsafe":    ("AIR SAFE",         (18, 143, 168)),
    "air":        ("Air",              (232, 56, 47)),
    "flow":       ("Flow",             (242, 183, 5)),
    "cidadao":    ("Flow Cidadao",     (242, 113, 28)),
    "siga":       ("Siga",             (87, 195, 59)),
    "descarte":   ("Descarte",         (14, 122, 52)),
    "rdc":        ("RDC ARQ",          (14, 122, 52)),
    "nfc":        ("Leitores NFC",     (142, 95, 211)),
    "impressora": ("Impressoras",      (142, 95, 211)),
    "print3d":    ("Impressoras 3D",   (142, 95, 211)),
}

DARK = (11, 15, 20)
OUT = os.path.join(os.path.dirname(__file__), "qrcodes", "eco")
os.makedirs(OUT, exist_ok=True)


def load_font(size):
    for name in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def centered(draw, text, font, y, width, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (box[2] - box[0])) / 2, y), text, fill=fill, font=font)


for key, (label, accent) in ITEMS.items():
    url = f"{BASE}?i={key}"
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=12, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=DARK, back_color="white").convert("RGB")

    qw, qh = qr_img.size
    pad_top, pad_bottom = 40, 104
    canvas = Image.new("RGB", (qw, qh + pad_top + pad_bottom), "white")
    canvas.paste(qr_img, (0, pad_top))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([0, 0, qw, 10], fill=accent)
    centered(draw, label, load_font(42), qh + pad_top + 16, qw, DARK)
    centered(draw, "Aponte a camera", load_font(24), qh + pad_top + 70, qw, (90, 90, 90))

    path = os.path.join(OUT, f"qr-{key}.png")
    canvas.save(path)
    print(f"OK  {path}  ->  {url}")

print(f"\n{len(ITEMS)} QR codes gerados em: {OUT}")
print("Ajuste BASE no topo deste arquivo se a URL de publicacao mudar.")
