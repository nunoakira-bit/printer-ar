# -*- coding: utf-8 -*-
"""Recorta, do backdrop.pdf, um alvo de rastreio por bolinha.

Cada alvo cobre a bolinha + titulo + legenda, o que da textura suficiente para o
matcher. Grava tambem targets.json com o retangulo de cada alvo em pontos do PDF
-- é esse retangulo que permite mapear qualquer ponto do backdrop para a tela
depois, a partir da pose do alvo rastreado.
"""
import fitz, os, json

PDF = r"C:\Users\User\Desktop\Printer\backdrop 2026\catalogo flow\backdrop.pdf"
OUT = r"D:\Aplicativos locais Printer\printer-ar\assets\eco\targets"
os.makedirs(OUT, exist_ok=True)

# centro de cada bolinha, em pontos do PDF
POS = {
    "doc": (198, 1007), "scanner": (468, 1012), "multi": (452, 1282),
    "computador": (510, 625), "airsafe": (900, 633), "print3d": (1086, 456),
    "air": (961, 1052), "flow": (1347, 1046), "siga": (1783, 1044),
    "cidadao": (1347, 1421), "descarte": (1567, 1420), "rdc": (1936, 1403),
    "nfc": (1780, 630), "impressora": (2077, 645),
}

# ordem estavel: é o targetIndex que o app usa
ORDER = ["doc", "scanner", "multi", "computador", "airsafe", "air", "flow",
         "cidadao", "siga", "descarte", "rdc", "nfc", "impressora", "print3d"]

HALF = 120        # meia-largura do alvo, em pt (240pt ~ 32cm num backdrop de 300cm)
DY = 34           # desloca para baixo, para pegar titulo e legenda
DPI = 200
PAGE_W_PT = 2250

doc = fitz.open(PDF)
page = doc[0]
pw, ph = page.rect.width, page.rect.height

targets = []
for i, key in enumerate(ORDER):
    cx, cy = POS[key]
    cy_t = cy + DY
    x0, y0 = cx - HALF, cy_t - HALF
    x1, y1 = cx + HALF, cy_t + HALF
    # nao deixa sair da pagina
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(pw, x1), min(ph, y1)

    pix = page.get_pixmap(clip=fitz.Rect(x0, y0, x1, y1), dpi=DPI)
    pix.save(os.path.join(OUT, f"{i:02d}-{key}.png"))

    targets.append({
        "index": i, "id": key,
        "rect": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
        "px": [pix.width, pix.height],
    })
    print(f"{i:02d} {key:11s} rect={[round(x0),round(y0),round(x1),round(y1)]} px={pix.width}x{pix.height}")

json.dump({"pageWidthPt": PAGE_W_PT, "targets": targets},
          open(os.path.join(OUT, "targets.json"), "w"), indent=1)
print(f"\n{len(targets)} alvos em {OUT}")
