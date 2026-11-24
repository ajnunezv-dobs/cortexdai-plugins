"""Arma cualquier libro de Excel con la marca de DObs: una o varias hojas de tabla.

Uso:
    python scripts/crear_hoja.py contenido.json ventas-por-sede.xlsx

La marca vive aquí y solo aquí: colores, tipografías, logotipo y dónde va cada cosa. Quien escribe el
contenido no elige nada de eso. Para otra empresa se cambia el bloque MARCA y el logotipo de `recursos/`.

Forma de `contenido.json` (hay un ejemplo completo en `ejemplos/hoja.json`):

    {
      "aviso": "Datos ficticios · demostración de CortexDAI",      obligatorio: va en todas las hojas
      "hojas": [
        {"nombre": "Por sede",                                       el nombre de la pestaña (31 letras como máximo)
         "titulo": "Avance del mes por sede",
         "subtitulo": "Datos al día 20",
         "columnas": ["Sede", "Vendido", "Meta", "Cierre proyectado %"],
         "filas": [["Sede A", 5000, 10000, 60.0]],
         "total": ["Total", 50000, 62500, 80.0],                     opcional: el que entrega el conector, no se suma aquí
         "nota": "El mes en curso va a medias."}                     opcional
      ]
    }

Las cifras van como número, no como texto: así se pueden ordenar y sumar. Los enteros salen con separador de
miles; los decimales, con un decimal.
"""

import json
import os
import sys

from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

AQUI = os.path.dirname(os.path.abspath(__file__))
RECURSOS = os.path.join(AQUI, "..", "recursos")

# --------------------------------------------------------------------------- la marca de DObs
MARCA = {
    "tinta": "071832", "papel": "FFFFFF", "pistacho": "B3CC5C", "pistacho_texto": "55672A",
    "gris": "52627A", "linea": "DFE4EB", "fondo_suave": "F3F6EA", "ambar": "D99A1F",
    "texto": "Segoe UI", "cifras": "Consolas",
    "logo_sobre_oscuro": "dobs-logotipo-papel.png",
    "firma": "CortexDAI",
}
TOPES = {"hojas": 8, "columnas": 12, "filas": 500}
ANCHO_FRANJA = 96  # en caracteres de ancho de columna


def relleno(nombre):
    return PatternFill("solid", start_color=MARCA[nombre], end_color=MARCA[nombre])


def letra(tamano, tinta="tinta", negrita=False, fuente="texto"):
    return Font(name=MARCA[fuente], size=tamano, bold=negrita, color=MARCA[tinta])


def cabecera(hoja, c, columnas, cifras=()):
    """Franja en tinta con el logotipo, el título de la hoja y el aviso de datos ficticios."""
    # La franja mide al menos ANCHO_FRANJA: una tabla angosta se completa con columnas vacías a la derecha,
    # para que el título y el logotipo quepan sin montarse.
    anchos = [ancho for _, _, ancho in columnas]
    while sum(anchos) < ANCHO_FRANJA:
        anchos.append(min(14, max(4, ANCHO_FRANJA - sum(anchos))))
    ultima = len(anchos)
    for col, ancho in enumerate(anchos, start=1):
        hoja.column_dimensions[hoja.cell(1, col).column_letter].width = ancho
    for fila, alto in ((1, 12), (2, 26), (3, 18), (4, 12), (5, 20)):
        hoja.row_dimensions[fila].height = alto
    for fila in range(1, 5):
        for col in range(1, ultima + 1):
            hoja.cell(fila, col).fill = relleno("tinta")
    logo = Image(os.path.join(RECURSOS, MARCA["logo_sobre_oscuro"]))
    logo.height, logo.width = 40, round(40 * 1600 / 521)
    desde, ancho = ultima, anchos[-1]
    while ancho < 20 and desde > 1:  # el logotipo empieza donde le queda sitio dentro de la franja
        desde -= 1
        ancho += anchos[desde - 1]
    hoja.add_image(logo, f"{hoja.cell(2, desde).column_letter}2")
    hoja.cell(2, 1, c["titulo"]).font = letra(16, "papel", negrita=True)
    hoja.cell(3, 1, c.get("subtitulo", "")).font = letra(9.5, "pistacho")
    hoja.cell(5, 1, c["aviso"]).font = letra(8, "gris", fuente="cifras")
    for i, (nombre, _, ancho) in enumerate(columnas, start=1):
        celda = hoja.cell(6, i, nombre)
        celda.fill, celda.font = relleno("tinta"), letra(9.5, "papel", negrita=True)
        celda.alignment = Alignment(vertical="center", wrap_text=True, horizontal="right" if nombre in cifras else "left")
        celda.border = Border(bottom=Side(style="medium", color=MARCA["pistacho"]))
    hoja.row_dimensions[6].height = 24
    hoja.freeze_panes = "A7"
    hoja.sheet_view.showGridLines = False
    hoja.page_setup.orientation, hoja.page_setup.fitToWidth, hoja.page_setup.fitToHeight = "landscape", 1, 0
    hoja.sheet_properties.pageSetUpPr.fitToPage = True
    hoja.oddFooter.center.text = f"{MARCA['firma']} · {c['aviso']}"


def celda_de_dato(hoja, fila, col, valor, par, negrita=False):
    celda = hoja.cell(fila, col, valor)
    numero = isinstance(valor, (int, float)) and not isinstance(valor, bool)
    celda.font = letra(9.5, negrita=negrita, fuente="cifras" if numero else "texto")
    celda.alignment = Alignment(vertical="top", wrap_text=not numero, horizontal="right" if numero else "left")
    celda.border = Border(bottom=Side(style="thin", color=MARCA["linea"]))
    if numero:
        celda.number_format = "#,##0" if float(valor).is_integer() else "#,##0.0"
    if par:
        celda.fill = relleno("fondo_suave")
    return celda


def numero(valor):
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def ancho_de(nombre, valores):
    largo = max([len(str(nombre))] + [len(f"{v:,}") if numero(v) else len(str(v)) for v in valores])
    return max(10, min(48, largo + 4))


def hoja_de_tabla(hoja, h, aviso):
    hoja.title = h["nombre"]
    hoja.sheet_properties.tabColor = MARCA["pistacho"]
    filas = h["filas"]
    columnas = [(nombre, None, ancho_de(nombre, [f[i] for f in filas] + ([h["total"][i]] if h.get("total") else [])))
                for i, nombre in enumerate(h["columnas"])]
    # Una columna es de cifras si alguna de sus celdas lo es: su encabezado se alinea como ellas.
    cifras = {nombre for i, nombre in enumerate(h["columnas"]) if any(numero(f[i]) for f in filas)}
    cabecera(hoja, {"titulo": h.get("titulo", h["nombre"]), "subtitulo": h.get("subtitulo", ""), "aviso": aviso}, columnas, cifras)
    for n, fila in enumerate(filas, start=1):
        for col, valor in enumerate(fila, start=1):
            celda_de_dato(hoja, 6 + n, col, valor, n % 2 == 0)
    siguiente = 7 + len(filas)
    if h.get("total"):
        for col, valor in enumerate(h["total"], start=1):
            celda = celda_de_dato(hoja, siguiente, col, valor, False, negrita=True)
            celda.border = Border(top=Side(style="medium", color=MARCA["tinta"]))
        siguiente += 1
    if h.get("nota"):
        hoja.cell(siguiente + 1, 1, h["nota"]).font = letra(9, "gris")
    hoja.auto_filter.ref = f"A6:{hoja.cell(6, len(columnas)).column_letter}{6 + len(filas)}"


def revisar(c):
    fallas = []
    if not c.get("aviso", "").strip():
        fallas.append("falta `aviso`: todo archivo de la demo dice que los datos son ficticios")
    hojas = c.get("hojas", [])
    if not 1 <= len(hojas) <= TOPES["hojas"]:
        fallas.append(f"van de 1 a {TOPES['hojas']} hojas; hay {len(hojas)}")
    nombres = [str(h.get("nombre", "")) for h in hojas]
    if len(set(nombres)) != len(nombres):
        fallas.append("dos hojas tienen el mismo nombre")
    for n, h in enumerate(hojas, start=1):
        nombre, columnas, filas = str(h.get("nombre", "")), h.get("columnas", []), h.get("filas", [])
        if not nombre.strip() or len(nombre) > 31 or any(x in nombre for x in "[]:*?/"):
            fallas.append(f"hoja {n}: el nombre va de 1 a 31 letras, sin corchetes, dos puntos, asterisco, interrogación ni barra")
        if not 1 <= len(columnas) <= TOPES["columnas"]:
            fallas.append(f"hoja {n}: van de 1 a {TOPES['columnas']} columnas")
        if not 1 <= len(filas) <= TOPES["filas"]:
            fallas.append(f"hoja {n}: van de 1 a {TOPES['filas']} filas")
        if any(len(f) != len(columnas) for f in filas + ([h["total"]] if h.get("total") else [])):
            fallas.append(f"hoja {n}: alguna fila no tiene las mismas celdas que columnas")
    if fallas:
        raise SystemExit("No se armó el libro:" + "".join(chr(10) + "- " + f for f in fallas))


def armar(c, salida):
    revisar(c)
    libro = Workbook()
    for n, h in enumerate(c["hojas"]):
        hoja_de_tabla(libro.active if n == 0 else libro.create_sheet(), h, c["aviso"])
    libro.save(salida)
    return len(c["hojas"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python crear_hoja.py contenido.json salida.xlsx")
    with open(sys.argv[1], encoding="utf-8") as f:
        contenido = json.load(f)
    print(f"Listo: {armar(contenido, sys.argv[2])} hojas en {sys.argv[2]}")
