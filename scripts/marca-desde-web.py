"""Saca la marca de un cliente de su web pública y deja lista su ficha para el generador (generar-cliente.py).

    python scripts/marca-desde-web.py <web del cliente> <carpeta privada del cliente> "<Nombre>" [id]

Qué hace, sin que nadie dibuje nada:
  1. Lee la página de inicio y busca el logotipo: las imágenes que dicen «logo» en su dirección, su texto o su clase.
     Si la web las sirve en varios tamaños, baja la más grande.
  2. Elige el mejor candidato (más ancho que alto, con fondo transparente) y lo recorta a su borde.
  3. Arma las dos versiones que piden los programas de marca: para fondo oscuro (lo claro del logo queda blanco) y
     para fondo claro (lo blanco del logo pasa al color oscuro de la marca).
  4. Saca los colores: el de acento es el color saturado que más aparece en el logo; el oscuro, el negro o azul
     oscuro de la marca si lo tiene (si no, el acento oscurecido); y el acento para texto, oscurecido hasta que se
     lea sobre blanco.
  5. Escribe `cliente.json` (si ya existía, conserva sus grupos y plantillas) y `vista-de-la-marca.png` para revisarla.

Revisa SIEMPRE la vista antes de entregar: una web puede tener más de un logo (el de una marca que representan, por
ejemplo). Lo que se baje queda en `<carpeta>/web/`. Solo se lee la web pública del cliente; nada se publica.
"""
import colorsys
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter

from PIL import Image, ImageDraw

AGENTE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
TOPE_BYTES = 15 * 1024 * 1024
ALTO_FINAL = 400


def bajar(url: str) -> tuple[bytes, str]:
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        datos = r.read(TOPE_BYTES + 1)
        if len(datos) > TOPE_BYTES:
            raise ValueError("demasiado grande")
        return datos, r.headers.get("Content-Type", "")


def candidatos(html: str, base: str) -> list[str]:
    """Direcciones de imágenes que parecen el logotipo, la de más tamaño primero cuando hay varias del mismo archivo."""
    vistas = {}
    for etiqueta in re.findall(r"<(?:img|source)\b[^>]*>", html, re.I):
        if not re.search(r"logo", etiqueta, re.I):
            continue
        for url in re.findall(r"""(?:src|srcset|data-src)=["']([^"']+)""", etiqueta, re.I):
            for parte in url.split(","):
                u = urllib.parse.urljoin(base, parte.strip().split(" ")[0].replace("&amp;", "&"))
                if not re.search(r"\.(png|webp|jpe?g|gif)(\?|$)", u, re.I):
                    continue
                archivo = urllib.parse.urlparse(u).path
                ancho = int((re.search(r"width=(\d+)", u) or [0, 0])[1] or 0)
                if archivo not in vistas or ancho > vistas[archivo][0]:
                    vistas[archivo] = (ancho, u)
    # Si la web sirve versiones achicadas (como HubSpot: /hs-fs/hubfs/x.png?width=…), se prueba también el original.
    urls = []
    for _, u in sorted(vistas.values(), reverse=True):
        original = re.sub(r"/hs-fs/hubfs/", "/hubfs/", u.split("?")[0])
        urls += [original, u] if original != u.split("?")[0] or "?" in u else [u]
    return list(dict.fromkeys(urls))


def puntaje(im: Image.Image, url: str) -> float:
    ancho, alto = im.size
    p = 0.0
    p += 3 if "logo" in url.lower() else 0
    p += 2 if im.mode in ("RGBA", "LA", "P") and im.convert("RGBA").getextrema()[3][0] < 255 else 0
    p += 2 if 1.5 <= ancho / max(alto, 1) <= 12 else 0
    p += min(ancho, 2000) / 2000
    return p


def pixeles_de(im):
    return im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()


def luz(rgb) -> float:
    r, g, b = (c / 255 for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b) -> float:
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    la = 0.2126 * lin(a[0]) + 0.7152 * lin(a[1]) + 0.0722 * lin(a[2])
    lb = 0.2126 * lin(b[0]) + 0.7152 * lin(b[1]) + 0.0722 * lin(b[2])
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def hexa(rgb) -> str:
    return "".join(f"{c:02X}" for c in rgb[:3])


def oscurecer(rgb, factor):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb[:3]))
    return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, max(0.0, l * factor), s))


def colores(im: Image.Image, extra: Image.Image | None = None) -> dict:
    """Acento: el color saturado que más aparece. Oscuro: un negro o azul oscuro de la marca, si lo hay."""
    cuenta = Counter()
    for fuente in [im] + ([extra] if extra else []):
        chica = fuente.convert("RGBA").copy()
        chica.thumbnail((300, 300))
        for r, g, b, a in pixeles_de(chica):
            if a > 200:
                cuenta[(r // 8 * 8, g // 8 * 8, b // 8 * 8)] += 1
    saturados = [(n, c) for c, n in cuenta.items() if colorsys.rgb_to_hls(*(x / 255 for x in c))[2] > 0.45 and 0.15 < luz(c) < 0.85]
    oscuros = [(n, c) for c, n in cuenta.items() if luz(c) < 0.18]
    acento = max(saturados)[1] if saturados else (31, 78, 121)
    oscuro = max(oscuros)[1] if oscuros else oscurecer(acento, 0.35)
    acento_texto = acento
    while contraste(acento_texto, (255, 255, 255)) < 4.5:
        acento_texto = oscurecer(acento_texto, 0.9)
    return {"oscuro": hexa(oscuro), "acento": hexa(acento), "acento_texto": hexa(acento_texto)}


def versiones(im: Image.Image, oscuro_hex: str) -> tuple[Image.Image, Image.Image]:
    """(para fondo oscuro, para fondo claro). Lo claro y sin color del logo es lo que cambia; el color se queda."""
    im = im.convert("RGBA")
    oscuro = tuple(int(oscuro_hex[i:i + 2], 16) for i in (0, 2, 4))
    pixeles = [p for p in pixeles_de(im) if p[3] > 200]
    claro_dominante = sum(luz(p) for p in pixeles) / max(len(pixeles), 1) > 0.55

    def cambiar(fuente, de_claro, a):
        nueva = []
        for r, g, b, al in pixeles_de(fuente):
            s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[2]
            neutro = s < 0.25
            es = (luz((r, g, b)) > 0.75) if de_claro else (luz((r, g, b)) < 0.25)
            nueva.append((*a, al) if al and neutro and es else (r, g, b, al))
        copia = Image.new("RGBA", fuente.size)
        copia.putdata(nueva)
        return copia

    if claro_dominante:
        return im, cambiar(im, True, oscuro)
    return cambiar(im, False, (255, 255, 255)), im


def vista(sobre_oscuro, sobre_claro, marca: dict, ruta: str) -> None:
    ancho = 900
    lienzo = Image.new("RGB", (ancho, 420), "#FFFFFF")
    d = ImageDraw.Draw(lienzo)
    d.rectangle((0, 0, ancho, 150), fill="#" + marca["oscuro"])
    for i, (fondo, logo, y) in enumerate(((marca["oscuro"], sobre_oscuro, 25), ("FFFFFF", sobre_claro, 175))):
        chico = logo.copy()
        chico.thumbnail((ancho - 60, 100))
        lienzo.paste(chico, (30, y), chico)
    for i, clave in enumerate(("oscuro", "acento", "acento_texto")):
        d.rectangle((30 + i * 290, 310, 290 + i * 290, 380), fill="#" + marca[clave])
        d.text((30 + i * 290, 388), f"{clave}: #{marca[clave]}", fill="#333333")
    lienzo.save(ruta)


def principal(web: str, carpeta: str, nombre: str, id_: str) -> dict:
    os.makedirs(os.path.join(carpeta, "web"), exist_ok=True)
    html, _ = bajar(web)
    html = html.decode("utf-8", "ignore")
    mejores = []
    for u in candidatos(html, web)[:12]:
        try:
            datos, tipo = bajar(u)
            im = Image.open(io.BytesIO(datos))
            if im.width * im.height > 60_000_000:
                continue   # una imagen así no es un logotipo, y abrirla agota la memoria del trabajo de alta
            im.draft("RGBA", (2400, 2400))
            im.load()
            # Achicada apenas se abre: un logotipo de 17.000 px de ancho (el de Grupo Pana) agotaba la memoria del alta.
            im.thumbnail((2400, 2400))
        except Exception:
            continue
        mejores.append((puntaje(im, u), u, im))
    if not mejores:
        raise SystemExit("No encontré el logotipo en la página de inicio. Déjalo a mano en la carpeta y completa cliente.json.")
    mejores.sort(key=lambda x: x[0], reverse=True)
    _, url, logo = mejores[0]
    logo = logo.convert("RGBA")
    logo = logo.crop(logo.getbbox() or (0, 0, *logo.size))
    if logo.height > ALTO_FINAL:
        logo = logo.resize((round(logo.width * ALTO_FINAL / logo.height), ALTO_FINAL), Image.LANCZOS)
    logo.save(os.path.join(carpeta, "web", "logo-original.png"))
    icono = None
    m = re.search(r"""<link[^>]+rel=["'][^"']*icon[^"']*["'][^>]*href=["']([^"']+)""", html, re.I)
    if m:
        try:
            datos, _ = bajar(urllib.parse.urljoin(web, m.group(1).replace("&amp;", "&")))
            icono = Image.open(io.BytesIO(datos)).convert("RGBA")
        except Exception:
            icono = None
    marca = colores(logo, icono)
    sobre_oscuro, sobre_claro = versiones(logo, marca["oscuro"])
    sobre_oscuro.save(os.path.join(carpeta, "logo-sobre-oscuro.png"))
    sobre_claro.save(os.path.join(carpeta, "logo-sobre-claro.png"))
    ruta = os.path.join(carpeta, "cliente.json")
    ficha = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {"version": "1.0.0"}
    ficha.update({"id": id_, "nombre": nombre})
    ficha["marca"] = {**ficha.get("marca", {}), **marca, "tipografia": ficha.get("marca", {}).get("tipografia", "Segoe UI"),
                      "logo_sobre_oscuro": "logo-sobre-oscuro.png", "logo_sobre_claro": "logo-sobre-claro.png"}
    ficha["origen_de_la_marca"] = {"web": web, "logo": url}
    json.dump(ficha, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    vista(sobre_oscuro, sobre_claro, marca, os.path.join(carpeta, "vista-de-la-marca.png"))
    return {"logo": url, **marca}


if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit(__doc__)
    web, carpeta, nombre = sys.argv[1:4]
    id_ = sys.argv[4] if len(sys.argv) == 5 else re.sub(r"[^a-z0-9]+", "-", nombre.lower()).strip("-")
    r = principal(web, carpeta, nombre, id_)
    print(f"Logo: {r['logo']}\nColores: oscuro #{r['oscuro']} · acento #{r['acento']} · acento para texto #{r['acento_texto']}")
    print(f"Revisa {os.path.join(carpeta, 'vista-de-la-marca.png')} antes de generar los plugins.")
