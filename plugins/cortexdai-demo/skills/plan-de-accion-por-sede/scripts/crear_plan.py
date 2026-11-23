"""Arma el plan de acción de una sede en Excel, con la marca de DObs.

Uso:
    python scripts/crear_plan.py contenido.json plan.xlsx

La marca vive aquí y solo aquí: colores, tipografías, logotipo y dónde va cada cosa. Quien escribe el
contenido no elige nada de eso. Para otra empresa se cambia el bloque MARCA y el logotipo de `recursos/`.

Forma de `contenido.json` (hay un ejemplo completo en `ejemplo.json`):

    {
      "titulo": "Plan de acción · Sede A",
      "subtitulo": "Lo que queda del mes · datos al día 20",
      "aviso": "Datos ficticios · demostración de CortexDAI",       obligatorio: va en las dos hojas
      "acciones": [
        {"accion": "Liquidar Producto 1", "linea": "Línea 1", "cajas": 1000,
         "por_que": "120 días de cobertura", "responsable": "Sin responsable", "fecha_limite": "2026-01-31"}
      ],
      "meta": [
        {"linea": "Línea 1", "vendido": 500, "meta": 1000, "esperado": 800, "cierre": 600, "faltan": 400}
      ],
      "total": {"linea": "Total", "vendido": 5000, "meta": 10000, "esperado": 8000, "cierre": 6000, "faltan": 4000},
      "nota": "Faltan 4,000 cajas para la meta del mes."
    }

Las cajas van como número, no como texto. El `total` es el que entrega el conector: el programa no suma.
"""

import datetime
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
TOPE_ACCIONES = 12
PLAN = [("Nº", None, 5), ("Acción", "accion", 44), ("Línea", "linea", 18), ("Cajas", "cajas", 11), ("Por qué", "por_que", 54),
        ("Responsable", "responsable", 22), ("Fecha límite", "fecha_limite", 14), ("Estado", None, 13)]
META = [("Línea", "linea", 26), ("Vendido", "vendido", 14), ("Meta", "meta", 14), ("Esperado a la fecha", "esperado", 20),
        ("Cierre proyectado", "cierre", 19), ("Faltan para la meta", "faltan", 20)]


CIFRAS = {"Cajas"} | {nombre for nombre, clave, _ in META if clave != "linea"}


def relleno(nombre):
    return PatternFill("solid", start_color=MARCA[nombre], end_color=MARCA[nombre])


def letra(tamano, tinta="tinta", negrita=False, fuente="texto"):
    return Font(name=MARCA[fuente], size=tamano, bold=negrita, color=MARCA[tinta])


def cabecera(hoja, c, columnas):
    """Franja en tinta con el logotipo, el título de la hoja y el aviso de datos ficticios."""
    ultima = len(columnas)
    for fila, alto in ((1, 12), (2, 26), (3, 18), (4, 12), (5, 20)):
        hoja.row_dimensions[fila].height = alto
    for fila in range(1, 5):
        for col in range(1, ultima + 1):
            hoja.cell(fila, col).fill = relleno("tinta")
    logo = Image(os.path.join(RECURSOS, MARCA["logo_sobre_oscuro"]))
    logo.height, logo.width = 40, round(40 * 1600 / 521)
    desde, ancho = ultima, columnas[-1][2]
    while ancho < 20 and desde > 1:  # el logotipo empieza donde le queda sitio dentro de la franja
        desde -= 1
        ancho += columnas[desde - 1][2]
    hoja.add_image(logo, f"{hoja.cell(2, desde).column_letter}2")
    hoja.cell(2, 1, c["titulo"]).font = letra(16, "papel", negrita=True)
    hoja.cell(3, 1, c.get("subtitulo", "")).font = letra(9.5, "pistacho")
    hoja.cell(5, 1, c["aviso"]).font = letra(8, "gris", fuente="cifras")
    for i, (nombre, _, ancho) in enumerate(columnas, start=1):
        celda = hoja.cell(6, i, nombre)
        celda.fill, celda.font = relleno("tinta"), letra(9.5, "papel", negrita=True)
        celda.alignment = Alignment(vertical="center", wrap_text=True, horizontal="right" if nombre in CIFRAS else "left")
        celda.border = Border(bottom=Side(style="medium", color=MARCA["pistacho"]))
        hoja.column_dimensions[celda.column_letter].width = ancho
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
        celda.number_format = "#,##0"
    if par:
        celda.fill = relleno("fondo_suave")
    return celda


def fecha(valor):
    try:
        return datetime.date.fromisoformat(str(valor))
    except ValueError:
        return valor


def hoja_plan(hoja, c):
    hoja.title = "Plan"
    hoja.sheet_properties.tabColor = MARCA["pistacho"]
    cabecera(hoja, c, PLAN)
    for n, a in enumerate(c["acciones"], start=1):
        fila = 6 + n
        valores = [n, a["accion"], a.get("linea", ""), a["cajas"], a.get("por_que", ""),
                   a.get("responsable") or "Sin responsable", fecha(a.get("fecha_limite", "")), a.get("estado", "Pendiente")]
        for col, valor in enumerate(valores, start=1):
            celda = celda_de_dato(hoja, fila, col, valor, n % 2 == 0)
            if isinstance(valor, datetime.date):
                celda.number_format, celda.alignment = "DD/MM/YYYY", Alignment(vertical="top", horizontal="left")
        hoja.cell(fila, 1).font = letra(9.5, "pistacho_texto", negrita=True, fuente="cifras")
        hoja.cell(fila, 2).font = letra(9.5, negrita=True)
        hoja.cell(fila, 8).font = letra(9, "ambar", negrita=True)
    if c.get("nota"):
        hoja.cell(8 + len(c["acciones"]), 2, c["nota"]).font = letra(9, "gris")
    hoja.auto_filter.ref = f"A6:H{6 + len(c['acciones'])}"


def hoja_meta(hoja, c):
    hoja.sheet_properties.tabColor = MARCA["tinta"]
    cabecera(hoja, dict(c, titulo="Meta del mes", subtitulo=c.get("subtitulo", "")), META)
    filas = list(c.get("meta", []))
    for n, m in enumerate(filas, start=1):
        for col, (_, clave, _) in enumerate(META, start=1):
            celda_de_dato(hoja, 6 + n, col, m.get(clave, ""), n % 2 == 0)
    if c.get("total"):
        fila = 7 + len(filas)
        for col, (_, clave, _) in enumerate(META, start=1):
            celda = celda_de_dato(hoja, fila, col, c["total"].get(clave, ""), False, negrita=True)
            celda.border = Border(top=Side(style="medium", color=MARCA["tinta"]))
    if c.get("nota"):
        hoja.cell(9 + len(filas), 1, c["nota"]).font = letra(9, "gris")


def revisar(c):
    fallas = []
    if not c.get("aviso", "").strip():
        fallas.append("falta `aviso`: todo archivo de la demo dice que los datos son ficticios")
    if not c.get("titulo", "").strip():
        fallas.append("falta `titulo`")
    acciones = c.get("acciones", [])
    if not 1 <= len(acciones) <= TOPE_ACCIONES:
        fallas.append(f"van de 1 a {TOPE_ACCIONES} acciones; hay {len(acciones)}")
    for n, a in enumerate(acciones, start=1):
        if not str(a.get("accion", "")).strip():
            fallas.append(f"acción {n}: falta `accion`")
        if not isinstance(a.get("cajas"), (int, float)) or isinstance(a.get("cajas"), bool):
            fallas.append(f"acción {n}: `cajas` va como número, sin comas ni texto")
    for n, m in enumerate(list(c.get("meta", [])) + ([c["total"]] if c.get("total") else []), start=1):
        for clave in ("vendido", "meta", "esperado", "cierre", "faltan"):
            if clave in m and (not isinstance(m[clave], (int, float)) or isinstance(m[clave], bool)):
                fallas.append(f"meta, fila {n}: `{clave}` va como número")
    if fallas:
        raise SystemExit("No se armó el plan:\n- " + "\n- ".join(fallas))


def armar(c, salida):
    revisar(c)
    c = dict(c, acciones=sorted(c["acciones"], key=lambda a: -a["cajas"]))  # de más cajas a menos
    libro = Workbook()
    hoja_plan(libro.active, c)
    hoja_meta(libro.create_sheet("Meta del mes"), c)
    libro.save(salida)
    return len(c["acciones"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python crear_plan.py contenido.json salida.xlsx")
    with open(sys.argv[1], encoding="utf-8") as f:
        contenido = json.load(f)
    print(f"Listo: {armar(contenido, sys.argv[2])} acciones en {sys.argv[2]}")
