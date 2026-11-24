"""Arma una presentación de PowerPoint (16:9) con la marca de DObs a partir de un archivo JSON.

    python scripts/crear_presentacion.py contenido.json salida.pptx

La marca vive aquí y solo aquí: colores, tipografías, logotipo y dónde va cada cosa. Quien escribe el
contenido no elige nada de eso. Para otra empresa se cambia el bloque MARCA y los dos logotipos de
`recursos/`; el resto no se toca.

El JSON:

    {"antetitulo": "Comité comercial", "titulo": "...", "subtitulo": "...",
     "aviso": "Datos ficticios · demostración de CortexDAI",
     "diapositivas": [
       {"tipo": "cifras",  "titulo": "...", "cifras": [{"valor": "10,000", "rotulo": "...", "destacada": true}], "nota": "..."},
       {"tipo": "vinetas", "titulo": "...", "vinetas": ["...", "..."], "nota": "..."},
       {"tipo": "tabla",   "titulo": "...", "columnas": ["Sede", "Meta"], "filas": [["Sede A", "10,000", {"estado": "rojo", "texto": "Atrasada"}]], "nota": "..."},
       {"tipo": "frase",   "texto": "...", "fuente": "..."},
       {"tipo": "cierre",  "titulo": "...", "vinetas": ["..."]}]}

Topes (lo que pasa de aquí no cabe y el programa se niega, en vez de entregar una lámina que se desborda):
4 cifras, 5 viñetas, 8 filas y 6 columnas por lámina.
"""
import json
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

AQUI = os.path.dirname(os.path.abspath(__file__))
RECURSOS = os.path.join(AQUI, "..", "recursos")

# --------------------------------------------------------------------------- la marca de DObs
MARCA = {
    "tinta": "071832", "papel": "FFFFFF", "pistacho": "B3CC5C", "pistacho_texto": "55672A",
    "gris": "52627A", "gris_claro": "A3AFC2", "linea": "DFE4EB", "linea_oscura": "1C3355",
    "ambar": "D99A1F", "rojo": "A32B2B", "sin_dato": "8B9397",
    # Archivo y JetBrains Mono son las del manual; estas son sus sustitutas, que sí están en toda PC con Office.
    "titulos": "Segoe UI", "texto": "Segoe UI", "cifras": "Consolas",
    "logo_sobre_oscuro": "dobs-logotipo-papel.png", "logo_sobre_claro": "dobs-logotipo-tinta.png",
    # Sobre pistacho el logotipo va entero en tinta (manual de marca): a color, la «D» se pierde.
    "logo_sobre_acento": "dobs-logotipo-mono.png",
    "firma": "CortexDAI",
}
ESTADOS = {"verde": "pistacho", "ambar": "ambar", "rojo": "rojo", "sin_dato": "sin_dato"}
ANCHO, ALTO, MARGEN = 13.333, 7.5, 0.9
TOPES = {"cifras": 4, "vinetas": 5, "filas": 8, "columnas": 6}


def color(nombre):
    return RGBColor.from_string(MARCA[nombre])


def texto(lamina, x, y, ancho, alto, contenido, tamano, tinta="tinta", fuente="texto", negrita=False,
          alinear=PP_ALIGN.LEFT, ancla=MSO_ANCHOR.TOP, interlineado=1.1, una_linea=False):
    caja = lamina.shapes.add_textbox(Inches(x), Inches(y), Inches(ancho), Inches(alto))
    marco = caja.text_frame
    marco.word_wrap = not una_linea
    marco.vertical_anchor = ancla
    for lado in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(marco, lado, 0)
    for i, linea in enumerate(contenido if isinstance(contenido, list) else [contenido]):
        parrafo = marco.paragraphs[0] if i == 0 else marco.add_paragraph()
        parrafo.alignment = alinear
        parrafo.line_spacing = interlineado
        tramo = parrafo.add_run()
        tramo.text = str(linea)
        tramo.font.size, tramo.font.bold, tramo.font.name = Pt(tamano), negrita, MARCA[fuente]
        tramo.font.color.rgb = color(tinta)
    return caja


def forma(lamina, tipo, x, y, ancho, alto, relleno):
    f = lamina.shapes.add_shape(tipo, Inches(x), Inches(y), Inches(ancho), Inches(alto))
    f.fill.solid()
    f.fill.fore_color.rgb = color(relleno)
    f.line.fill.background()
    f.shadow.inherit = False
    return f


def nueva(pres, fondo="papel"):
    lamina = pres.slides.add_slide(pres.slide_layouts[6])
    relleno = lamina.background.fill
    relleno.solid()
    relleno.fore_color.rgb = color(fondo)
    return lamina


def pie(lamina, numero, aviso, fondo="papel"):
    """Logotipo y firma a la izquierda, el aviso al centro y el número a la derecha: en TODAS las láminas."""
    oscuro = fondo == "tinta"
    logo = MARCA["logo_sobre_oscuro" if oscuro else "logo_sobre_acento" if fondo == "pistacho" else "logo_sobre_claro"]
    alto_logo = 0.3
    lamina.shapes.add_picture(os.path.join(RECURSOS, logo), Inches(MARGEN), Inches(ALTO - 0.72), height=Inches(alto_logo))
    tenue = "gris_claro" if oscuro else ("tinta" if fondo == "pistacho" else "gris")
    texto(lamina, MARGEN + 1.1, ALTO - 0.68, 1.6, 0.3, MARCA["firma"], 11, tenue, "titulos", negrita=True, ancla=MSO_ANCHOR.MIDDLE)
    texto(lamina, 3.6, ALTO - 0.68, ANCHO - 7.2, 0.3, aviso, 10, tenue, "cifras", alinear=PP_ALIGN.CENTER, ancla=MSO_ANCHOR.MIDDLE)
    texto(lamina, ANCHO - MARGEN - 1, ALTO - 0.68, 1, 0.3, f"{numero:02d}", 10, tenue, "cifras", alinear=PP_ALIGN.RIGHT, ancla=MSO_ANCHOR.MIDDLE)


def titulo_de_lamina(lamina, d, tinta="tinta"):
    texto(lamina, MARGEN, 0.75, ANCHO - 2 * MARGEN, 1.3, d["titulo"], 30, tinta, "titulos", negrita=True, interlineado=1.0)


def nota(lamina, d, y=6.05):
    if d.get("nota"):
        texto(lamina, MARGEN, y, ANCHO - 2 * MARGEN, 0.6, d["nota"], 12, "gris")


# --------------------------------------------------------------------------- tipos de lámina
def portada(pres, c):
    lamina = nueva(pres, "tinta")
    lamina.shapes.add_picture(os.path.join(RECURSOS, MARCA["logo_sobre_oscuro"]), Inches(MARGEN), Inches(0.8), height=Inches(0.62))
    if c.get("antetitulo"):
        texto(lamina, MARGEN, 2.5, ANCHO - 2 * MARGEN, 0.4, c["antetitulo"].upper(), 12, "pistacho", "cifras")
    texto(lamina, MARGEN, 2.95, ANCHO - 2 * MARGEN, 2.2, c["titulo"], 44, "papel", "titulos", negrita=True, interlineado=1.0)
    if c.get("subtitulo"):
        texto(lamina, MARGEN, 5.2, 9.5, 1.0, c["subtitulo"], 18, "gris_claro")
    texto(lamina, MARGEN, ALTO - 0.68, ANCHO - 2 * MARGEN, 0.3, c["aviso"], 10, "gris_claro", "cifras", ancla=MSO_ANCHOR.MIDDLE)


def cifras(pres, d, numero, aviso):
    lamina = nueva(pres)
    titulo_de_lamina(lamina, d)
    lista = d["cifras"]
    ancho = (ANCHO - 2 * MARGEN) / len(lista)
    # La cifra nunca se parte en dos renglones: se achica hasta caber en su columna (0.56 = ancho de un carácter
    # de Consolas). Todas las cifras de la lámina van del mismo tamaño: el de la más larga.
    mas_larga = max(len(str(c["valor"])) for c in lista)
    tamano = int(min(54, (ancho - 0.45) * 72 / (0.56 * mas_larga)))
    for i, cifra in enumerate(lista):
        x = MARGEN + i * ancho
        valor = str(cifra["valor"])
        if cifra.get("destacada"):
            # El pistacho no se lee como texto sobre blanco: el destacado es una barra, y la cifra sigue en tinta.
            forma(lamina, MSO_SHAPE.RECTANGLE, x, 2.55, 0.9, 0.09, "pistacho")
        texto(lamina, x, 2.8, ancho - 0.3, 1.2, valor, tamano, "tinta", "cifras", negrita=True, ancla=MSO_ANCHOR.BOTTOM, una_linea=True)
        texto(lamina, x, 4.15, ancho - 0.4, 1.6, cifra["rotulo"], 14, "gris", interlineado=1.2)
    nota(lamina, d)
    pie(lamina, numero, aviso)


def vinetas(pres, d, numero, aviso, fondo="papel"):
    lamina = nueva(pres, fondo)
    oscuro = fondo == "tinta"
    titulo_de_lamina(lamina, d, "papel" if oscuro else "tinta")
    y = 2.35
    for linea in d["vinetas"]:
        forma(lamina, MSO_SHAPE.OVAL, MARGEN, y + 0.13, 0.13, 0.13, "pistacho" if oscuro else "tinta")
        texto(lamina, MARGEN + 0.4, y, ANCHO - 2 * MARGEN - 0.4, 0.7, linea, 18, "papel" if oscuro else "tinta", interlineado=1.15)
        y += 0.72 if len(str(linea)) <= 95 else 0.98
    if not oscuro:
        nota(lamina, d)
    pie(lamina, numero, aviso, fondo)


def es_numero(celda):
    return bool(re.fullmatch(r"[−\-+]?[\d.,\s]+\s?(%|pp|USD|d|días|cajas)?", str(celda).strip()))


def tabla(pres, d, numero, aviso):
    lamina = nueva(pres)
    titulo_de_lamina(lamina, d)
    columnas, filas = d["columnas"], d["filas"]
    ancho_total = ANCHO - 2 * MARGEN
    primera = ancho_total * (0.3 if len(columnas) > 3 else 0.4)
    resto = (ancho_total - primera) / max(len(columnas) - 1, 1)
    equis = [MARGEN] + [MARGEN + primera + i * resto for i in range(len(columnas) - 1)]
    anchos = [primera] + [resto] * (len(columnas) - 1)
    a_la_derecha = [all(es_numero(f[i]) for f in filas if not isinstance(f[i], dict)) and
                    not any(isinstance(f[i], dict) for f in filas) for i in range(len(columnas))]
    y, alto_fila = 2.2, min(0.46, 3.6 / max(len(filas), 1))
    for i, rotulo in enumerate(columnas):
        texto(lamina, equis[i], y, anchos[i] - 0.35, 0.3, str(rotulo).upper(), 10, "gris", "cifras",
              alinear=PP_ALIGN.RIGHT if a_la_derecha[i] else PP_ALIGN.LEFT, ancla=MSO_ANCHOR.MIDDLE)
    y += 0.36
    forma(lamina, MSO_SHAPE.RECTANGLE, MARGEN, y, ancho_total, 0.02, "tinta")
    for fila in filas:
        for i, celda in enumerate(fila):
            x = equis[i]
            if isinstance(celda, dict):
                forma(lamina, MSO_SHAPE.OVAL, x, y + alto_fila / 2 - 0.07, 0.14, 0.14, ESTADOS.get(celda.get("estado"), "sin_dato"))
                texto(lamina, x + 0.25, y, anchos[i] - 0.4, alto_fila, celda.get("texto", ""), 14, "tinta", ancla=MSO_ANCHOR.MIDDLE)
            else:
                texto(lamina, x, y, anchos[i] - 0.35, alto_fila, celda, 14, "tinta", "cifras" if a_la_derecha[i] else "texto",
                      negrita=(i == 0), alinear=PP_ALIGN.RIGHT if a_la_derecha[i] else PP_ALIGN.LEFT, ancla=MSO_ANCHOR.MIDDLE)
        y += alto_fila
        forma(lamina, MSO_SHAPE.RECTANGLE, MARGEN, y, ancho_total, 0.01, "linea")
    nota(lamina, d, y=max(y + 0.2, 6.05) if y < 6.0 else 6.25)
    pie(lamina, numero, aviso)


def frase(pres, d, numero, aviso):
    lamina = nueva(pres, "pistacho")
    texto(lamina, MARGEN, 1.6, 10.2, 3.4, d["texto"], 36, "tinta", "titulos", negrita=True, ancla=MSO_ANCHOR.MIDDLE, interlineado=1.1)
    if d.get("fuente"):
        texto(lamina, MARGEN, 5.3, 10, 0.4, d["fuente"], 12, "tinta", "cifras")
    pie(lamina, numero, aviso, "pistacho")


def cierre(pres, d, numero, aviso):
    vinetas(pres, d, numero, aviso, fondo="tinta")


TIPOS = {"cifras": cifras, "vinetas": vinetas, "tabla": tabla, "frase": frase, "cierre": cierre}


# --------------------------------------------------------------------------- revisión y armado
def revisar(c):
    """Devuelve la lista de problemas del contenido. Vacía = se puede armar."""
    p = []
    for campo in ("titulo", "aviso", "diapositivas"):
        if not c.get(campo):
            p.append(f"falta «{campo}»")
    for n, d in enumerate(c.get("diapositivas") or [], start=2):
        tipo = d.get("tipo")
        if tipo not in TIPOS:
            p.append(f"lámina {n}: tipo «{tipo}» no existe (hay: {', '.join(TIPOS)})")
            continue
        if tipo != "frase" and not d.get("titulo"):
            p.append(f"lámina {n}: falta el título")
        if tipo == "frase" and not d.get("texto"):
            p.append(f"lámina {n}: falta el texto de la frase")
        if tipo == "cifras" and not 1 <= len(d.get("cifras") or []) <= TOPES["cifras"]:
            p.append(f"lámina {n}: van de 1 a {TOPES['cifras']} cifras")
        if tipo in ("vinetas", "cierre") and not 1 <= len(d.get("vinetas") or []) <= TOPES["vinetas"]:
            p.append(f"lámina {n}: van de 1 a {TOPES['vinetas']} viñetas")
        if tipo == "tabla":
            columnas, filas = d.get("columnas") or [], d.get("filas") or []
            if not 2 <= len(columnas) <= TOPES["columnas"]:
                p.append(f"lámina {n}: van de 2 a {TOPES['columnas']} columnas")
            if not 1 <= len(filas) <= TOPES["filas"]:
                p.append(f"lámina {n}: van de 1 a {TOPES['filas']} filas; parte la tabla en dos láminas")
            if any(len(f) != len(columnas) for f in filas):
                p.append(f"lámina {n}: hay filas con distinto número de celdas que columnas")
        if len(str(d.get("titulo") or "")) > 90:
            p.append(f"lámina {n}: el título pasa de 90 caracteres")
    return p


def armar(c, salida):
    problemas = revisar(c)
    if problemas:
        raise SystemExit("No se armó la presentación:\n  · " + "\n  · ".join(problemas))
    pres = Presentation()
    pres.slide_width, pres.slide_height = Inches(ANCHO), Inches(ALTO)
    portada(pres, c)
    for numero, d in enumerate(c["diapositivas"], start=2):
        TIPOS[d["tipo"]](pres, d, numero, c["aviso"])
    pres.save(salida)
    return len(pres.slides)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python scripts/crear_presentacion.py contenido.json salida.pptx")
    with open(sys.argv[1], encoding="utf-8") as f:
        contenido = json.load(f)
    print(f"Listo: {armar(contenido, sys.argv[2])} láminas en {sys.argv[2]}")
