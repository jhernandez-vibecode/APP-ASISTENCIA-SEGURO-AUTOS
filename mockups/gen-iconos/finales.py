# -*- coding: utf-8 -*-
"""Genera los 4 iconos de la PWA de Asistencia Autos — opcion C aprobada por JC
el 9 set 2026: el degradado que ya tenia la app, con la franja del INS abajo.

Calcado de `iconos_finales.py` del repo de Viajero (misma estructura y misma
convencion de archivos). Cambia el simbolo (car-side de FA 6.4.0, el que ya
usaba el icono de Autos) y el fondo (degradado navy->azul de la app).

Convencion, la que ya tenian los iconos de Autos — NO se cambia:
  - icon-192 / icon-512 / icon-180: RGB opaco, esquinas redondeadas rellenas
    de BLANCO. iOS y los launchers les aplican su propia mascara.
  - icon-maskable-512: RGB, a sangre y SIN esquinas redondeadas, porque la
    mascara del sistema recorta. El contenido cabe en el circulo seguro (80 %).

El logo del INS sale de `ins-blanco.png` del propio repo (MD5 a02c976...,
identico al de Viajero). NO se redibuja.
"""
import os
import subprocess
import shutil

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = r"C:\Users\segur\APP-ASISTENCIA-SEGURO-AUTOS"

CAR = ("M171.3 96H224v96H111.3l30.4-75.9C146.5 104 158.2 96 171.3 96zM272 192V96h81.2c9.7 0 18.9 4.4 25 12"
       "l67.2 84H272zm256.2 1L428.2 68c-18.2-22.8-45.8-36-75-36H171.3c-39.3 0-74.6 23.9-89.1 60.3L40.6 196.4"
       "C16.8 205.8 0 228.9 0 256V368c0 17.7 14.3 32 32 32H65.3c7.6 45.4 47.1 80 94.7 80s87.1-34.6 94.7-80"
       "H385.3c7.6 45.4 47.1 80 94.7 80s87.1-34.6 94.7-80H608c17.7 0 32-14.3 32-32V320c0-65.2-48.8-119-111.8-127z"
       "M434.7 368a48 48 0 1 1 90.5 32 48 48 0 1 1 -90.5-32zM160 336a48 48 0 1 1 0 96 48 48 0 1 1 0-96z")

FONDO = "linear-gradient(135deg,#0c2340,#0369a1)"

PAGINA = """<!doctype html><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;width:512px;height:512px;background:transparent}}
  .card{{position:relative;width:512px;height:512px;border-radius:{radio};
        background:{fondo};overflow:hidden}}
  .sym{{position:absolute;left:50%;transform:translateX(-50%)}}
  .ins{{position:absolute;left:50%;transform:translateX(-50%)}}
  .banda{{position:absolute;left:0;right:0;bottom:0;background:rgba(255,255,255,.085)}}
</style>
<div class="card">
  <div class="banda" style="height:{banda}px"></div>
  <svg class="sym" style="top:{top}px" width="{w}" height="{h}" viewBox="0 0 640 512" fill="#ffffff"><path d="{p}"/></svg>
  <img class="ins" src="ins.png" style="top:{ins_top}px;width:{ins_w}px;opacity:.80">
</div>
"""

# --- geometria de la version "any" ---
BANDA, W, TOP, INS_TOP, INS_W = 158, 268, 70, 404, 252
H = round(W * 512 / 640)          # el carro no es cuadrado: 640x512


def escribir(nombre, **kw):
    ruta = os.path.join(AQUI, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(PAGINA.format(p=CAR, fondo=FONDO, **kw))
    return ruta


def rasterizar(html, png):
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--default-background-color=00000000",
        "--virtual-time-budget=4000", "--window-size=512,512",
        "--screenshot=" + png, "file:///" + html.replace("\\", "/")
    ], capture_output=True)


shutil.copy(os.path.join(SALIDA, "ins-blanco.png"), os.path.join(AQUI, "ins.png"))

html_any = escribir("f-any.html", radio="112px", banda=BANDA, w=W, h=H,
                    top=TOP, ins_top=INS_TOP, ins_w=INS_W)

# --- maskable: el mismo dibujo al 80 %, centrado, a sangre y sin esquinas ---
K, c = 0.80, 256.0
html_msk = escribir("f-maskable.html", radio="0",
                    banda=round(512 - (c + ((512 - BANDA) - c) * K)),
                    w=round(W * K), h=round(H * K),
                    top=round(c + (TOP - c) * K),
                    ins_top=round(c + (INS_TOP - c) * K),
                    ins_w=round(INS_W * K))

png_any = os.path.join(AQUI, "_any.png")
png_msk = os.path.join(AQUI, "_maskable.png")
rasterizar(html_any, png_any)
rasterizar(html_msk, png_msk)

from PIL import Image

# Las esquinas transparentes se aplanan sobre BLANCO, como los iconos de hoy.
base = Image.open(png_any).convert("RGBA")
blanco = Image.new("RGBA", base.size, (255, 255, 255, 255))
blanco.alpha_composite(base)
plano = blanco.convert("RGB")

plano.save(os.path.join(SALIDA, "icon-512.png"))
plano.resize((192, 192), Image.LANCZOS).save(os.path.join(SALIDA, "icon-192.png"))
plano.resize((180, 180), Image.LANCZOS).save(os.path.join(SALIDA, "icon-180.png"))

Image.open(png_msk).convert("RGB").save(os.path.join(SALIDA, "icon-maskable-512.png"))

for n in ("icon-512.png", "icon-192.png", "icon-180.png", "icon-maskable-512.png"):
    im = Image.open(os.path.join(SALIDA, n))
    print("%-24s %s %s  esquina:%s" % (n, im.size, im.mode, im.getpixel((1, 1))))
