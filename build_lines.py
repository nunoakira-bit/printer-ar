# -*- coding: utf-8 -*-
"""Gera assets/eco/lines.json: as polilinhas dos conectores REALMENTE impressos.

O pulso corre por cima destas coordenadas, entao elas tem que sair do PDF.
Cada polilinha guarda de qual(is) bolinha(s) ela encosta e em qual ponta, para o
app saber por qual extremidade o pulso deve comecar.
"""
import fitz, json, math, os

PDF = r"C:\Users\User\Desktop\Printer\backdrop 2026\catalogo flow\backdrop.pdf"
OUT = r"D:\Aplicativos locais Printer\printer-ar\assets\eco\lines.json"

POS = {
    "doc": (198, 1007), "scanner": (468, 1012), "multi": (452, 1282),
    "computador": (510, 625), "airsafe": (900, 633), "print3d": (1086, 456),
    "air": (961, 1052), "flow": (1347, 1046), "siga": (1783, 1044),
    "cidadao": (1347, 1421), "descarte": (1567, 1420), "rdc": (1936, 1403),
    "nfc": (1780, 630), "impressora": (2077, 645),
}
NEAR = 200          # raio para considerar que a ponta encosta na bolinha

page = fitz.open(PDF)[0]

def flatten(d):
    pts = []
    for item in d["items"]:
        op = item[0]
        if op == "l":
            a, b = item[1], item[2]
            if not pts: pts.append((a.x, a.y))
            pts.append((b.x, b.y))
        elif op == "c":
            a, b, c, e = item[1], item[2], item[3], item[4]
            if not pts: pts.append((a.x, a.y))
            for k in range(1, 9):
                t = k/8; m = 1-t
                pts.append((m**3*a.x + 3*m*m*t*b.x + 3*m*t*t*c.x + t**3*e.x,
                            m**3*a.y + 3*m*m*t*b.y + 3*m*t*t*c.y + t**3*e.y))
    return pts

def dedupe(pts, eps=1.0):
    out = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, out[-1]) > eps:
            out.append(p)
    return out

lines = []
for d in page.get_drawings():
    if d.get("type") not in ("s", "sf"):
        continue
    col = d.get("color") or (0, 0, 0)
    w = d.get("width") or 0
    # os aneis tracejados em volta dos icones sao brancos e grossos: nao sao conectores
    if w > 5 or (col[0] > .95 and col[1] > .95 and col[2] > .95):
        continue
    pts = flatten(d)
    if len(pts) < 2:
        continue
    pts = dedupe(pts)
    if len(pts) < 2:
        continue
    length = sum(math.dist(pts[i], pts[i+1]) for i in range(len(pts)-1))
    if length < 45:
        continue
    # fechado (contorno) -> nao e conector
    if math.dist(pts[0], pts[-1]) < 6 and length > 200:
        continue

    ends = {}
    for label, p in (("a", pts[0]), ("b", pts[-1])):
        best, bd = None, 1e9
        for k, c in POS.items():
            dd = math.dist(p, c)
            if dd < bd: best, bd = k, dd
        ends[label] = best if bd <= NEAR else None

    if ends["a"] is None and ends["b"] is None:
        continue

    r, g, b = col
    kind = "loop" if (r > .5 and g < .3) else ("print" if (r > .7 and b > .8 and g < .8) else "flow")
    lines.append({
        "a": ends["a"], "b": ends["b"], "kind": kind,
        "len": round(length, 1),
        "pts": [[round(x, 1), round(y, 1)] for x, y in pts],
    })

lines.sort(key=lambda l: -l["len"])

touch = {k: 0 for k in POS}
for l in lines:
    for e in (l["a"], l["b"]):
        if e: touch[e] += 1

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"pageWidthPt": 2250, "lines": lines}, open(OUT, "w"))

print(f"{len(lines)} conectores impressos -> {OUT}")
print(f"{os.path.getsize(OUT)/1024:.1f} KB\n")
print("linhas que encostam em cada bolinha:")
for k, n in sorted(touch.items(), key=lambda x: -x[1]):
    flag = "  <-- NENHUMA" if n == 0 else ""
    print(f"  {k:11s} {n}{flag}")
