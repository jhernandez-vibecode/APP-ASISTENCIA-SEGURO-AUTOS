# -*- coding: utf-8 -*-
"""El launcher de Android recorta el maskable a un circulo. Todo lo que dibuja
(carro + INS) tiene que caber dentro del circulo seguro del 80 % = radio 204,8
sobre 512. Si algo se sale, el logo del INS aparece cortado en el telefono.
"""
import math
from PIL import Image

im = Image.open(r"C:\Users\segur\APP-ASISTENCIA-SEGURO-AUTOS\icon-maskable-512.png").convert("RGB")
w, h = im.size
cx = cy = 256.0
R = 512 * 0.80 / 2          # 204.8
px = im.load()

# El contenido es claro (carro blanco, INS gris claro); el fondo es navy/azul.
fuera, maxd, bbox = 0, 0.0, [w, h, 0, 0]
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        if r > 150 and g > 150 and b > 150:      # pixel de contenido
            d = math.hypot(x - cx, y - cy)
            maxd = max(maxd, d)
            if d > R:
                fuera += 1
            bbox[0] = min(bbox[0], x); bbox[1] = min(bbox[1], y)
            bbox[2] = max(bbox[2], x); bbox[3] = max(bbox[3], y)

print("circulo seguro (radio):      %.1f" % R)
print("punto de contenido mas lejos: %.1f" % maxd)
print("pixeles fuera del circulo:    %d" % fuera)
print("caja del contenido:           x %d-%d   y %d-%d" % tuple(bbox))
print("VEREDICTO:", "OK, nada se recorta" if fuera == 0 else "SE RECORTA — bajar el factor")
