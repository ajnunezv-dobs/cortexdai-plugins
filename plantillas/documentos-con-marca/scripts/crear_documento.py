"""Arma cualquier documento de Word con la marca de DObs: informe, resumen, acta, propuesta.

Uso:
    python scripts/crear_documento.py contenido.json informe.docx

La marca vive aquí y solo aquí: colores, tipografías, logotipo y dónde va cada cosa. Quien escribe el
contenido no elige nada de eso. Para otra empresa se cambia el bloque MARCA y el logotipo de `recursos/`.

Forma de `contenido.json` (hay un ejemplo completo en `ejemplos/documento.json`):

    {
      "tipo": "Informe de la semana",                             va en la franja, junto al logotipo
      "titulo": "El mes cerraría en 80.0 % de la meta",           la conclusión, no el tema
      "subtitulo": "Semana del día 20",
      "aviso": "Datos ficticios · demostración de CortexDAI",     obligatorio: va arriba y en el pie
      "secciones": [
        {"titulo": "Cómo va el mes", "parrafos": ["..."]},
        {"titulo": "Por sede", "tabla": {"columnas": ["Sede", "Cierre"], "filas": [["Sede A", "70.0 %"]]}},
        {"titulo": "Qué hacer", "vinetas": ["...", "..."]},
        {"titulo": "La cifra", "destacado": "Diez objetivos en riesgo y ninguno con una acción en curso"}
      ]
    }

Cada sección lleva `titulo` y al menos uno de: `parrafos`, `vinetas`, `tabla`, `destacado`.
"""

import json
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = os.path.dirname(os.path.abspath(__file__))
RECURSOS = os.path.join(AQUI, "..", "recursos")

# --------------------------------------------------------------------------- la marca de DObs
MARCA = {
    "tinta": "071832", "papel": "FFFFFF", "pistacho": "B3CC5C", "pistacho_texto": "55672A",
    "gris": "52627A", "linea": "DFE4EB", "fondo_suave": "F3F6EA",
    # Archivo y JetBrains Mono son las del manual; estas son sus sustitutas, que sí están en toda PC con Office.
    "titulos": "Segoe UI", "texto": "Segoe UI", "cifras": "Consolas",
    "logo_sobre_oscuro": "dobs-logotipo-papel.png",
    "firma": "CortexDAI",
}
TOPES = {"secciones": 20, "palabras": 4000, "vinetas": 12, "filas": 40, "columnas": 7}


def color(nombre):
    return RGBColor.from_string(MARCA[nombre])


def fondo(celda, nombre):
    sombra = OxmlElement("w:shd")
    sombra.set(qn("w:val"), "clear")
    sombra.set(qn("w:color"), "auto")
    sombra.set(qn("w:fill"), MARCA[nombre])
    celda._tc.get_or_add_tcPr().append(sombra)


def borde(parrafo, lado, nombre, grosor=12):
    """Una línea de color arriba o abajo del párrafo (grosor en octavos de punto)."""
    propiedades = parrafo._p.get_or_add_pPr()
    bordes = propiedades.find(qn("w:pBdr"))
    if bordes is None:
        bordes = OxmlElement("w:pBdr")
        propiedades.append(bordes)
    linea = OxmlElement(f"w:{lado}")
    for clave, valor in (("val", "single"), ("sz", str(grosor)), ("space", "4"), ("color", MARCA[nombre])):
        linea.set(qn(f"w:{clave}"), valor)
    bordes.append(linea)


def sin_bordes(tabla):
    propiedades = tabla._tbl.tblPr
    bordes = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        linea = OxmlElement(f"w:{lado}")
        linea.set(qn("w:val"), "nil")
        bordes.append(linea)
    propiedades.append(bordes)


def escribir(parrafo, contenido, tamano, tinta="tinta", fuente="texto", negrita=False, antes=0, despues=0):
    tramo = parrafo.add_run(contenido)
    tramo.font.size, tramo.font.bold, tramo.font.name = Pt(tamano), negrita, MARCA[fuente]
    tramo.font.color.rgb = color(tinta)
    tramo._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), MARCA[fuente])
    formato = parrafo.paragraph_format
    formato.space_before, formato.space_after, formato.line_spacing = Pt(antes), Pt(despues), 1.08
    return tramo


def es_numero(celda):
    limpio = str(celda).replace(",", "").replace("%", "").replace("US$", "").replace("−", "-").replace("+", "").strip()
    try:
        float(limpio)
        return True
    except ValueError:
        return False


def encabezado(doc, c):
    """Franja en tinta con el logotipo a la izquierda y el tipo de documento a la derecha."""
    franja = doc.add_table(rows=1, cols=2)
    franja.alignment = WD_TABLE_ALIGNMENT.CENTER
    sin_bordes(franja)
    izquierda, derecha = franja.rows[0].cells
    for celda in (izquierda, derecha):
        fondo(celda, "tinta")
    logo = izquierda.paragraphs[0]
    logo.paragraph_format.space_before, logo.paragraph_format.space_after = Pt(7), Pt(7)
    logo.add_run().add_picture(os.path.join(RECURSOS, MARCA["logo_sobre_oscuro"]), height=Cm(0.95))
    rotulo = derecha.paragraphs[0]
    rotulo.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    escribir(rotulo, c.get("tipo", "Documento").upper(), 8.5, "pistacho", "cifras", negrita=True, antes=12)
    escribir(doc.add_paragraph(), c["aviso"], 7.5, "gris", "cifras", antes=5)
    escribir(doc.add_paragraph(), c["titulo"], 19, "tinta", "titulos", negrita=True, antes=6)
    linea = doc.add_paragraph()
    escribir(linea, c.get("subtitulo", ""), 9.5, "gris", despues=4)
    borde(linea, "bottom", "pistacho", 18)


def tabla(doc, d):
    columnas, filas = d["columnas"], d["filas"]
    t = doc.add_table(rows=1 + len(filas), cols=len(columnas))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    sin_bordes(t)
    for i, nombre in enumerate(columnas):
        celda = t.rows[0].cells[i]
        fondo(celda, "tinta")
        escribir(celda.paragraphs[0], nombre, 8, "papel", negrita=True, antes=2, despues=2)
    # Una columna es de cifras si alguna de sus celdas lo es: toda ella, con su encabezado, se alinea a la derecha.
    de_cifras = [any(es_numero(fila[i]) for fila in filas) for i in range(len(columnas))]
    for i, celda in enumerate(t.rows[0].cells):
        if de_cifras[i]:
            celda.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for f, fila in enumerate(filas, start=1):
        for i, valor in enumerate(fila):
            celda = t.rows[f].cells[i]
            if f % 2 == 0:
                fondo(celda, "fondo_suave")
            parrafo = celda.paragraphs[0]
            numero = es_numero(valor)
            parrafo.alignment = WD_ALIGN_PARAGRAPH.RIGHT if de_cifras[i] else WD_ALIGN_PARAGRAPH.LEFT
            escribir(parrafo, str(valor), 8.5, "tinta", "cifras" if numero else "texto", antes=1.5, despues=1.5)


def seccion(doc, numero, d):
    cabeza = doc.add_paragraph()
    escribir(cabeza, f"{numero:02d}  ", 9, "pistacho_texto", "cifras", negrita=True, antes=9, despues=2)
    escribir(cabeza, d["titulo"].upper(), 9, "tinta", "titulos", negrita=True, antes=9, despues=2)
    for vineta in d.get("vinetas", []):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.45)
        p.paragraph_format.first_line_indent = Cm(-0.45)
        escribir(p, "■  ", 6, "pistacho")
        escribir(p, vineta, 9.5, despues=1)
    if d.get("tabla"):
        tabla(doc, d["tabla"])
    for parrafo in d.get("parrafos", []):
        escribir(doc.add_paragraph(), parrafo, 9.5, antes=3 if d.get("tabla") else 0, despues=2)
    if d.get("destacado"):
        caja = doc.add_table(rows=1, cols=1)
        sin_bordes(caja)
        fondo(caja.rows[0].cells[0], "fondo_suave")
        escribir(caja.rows[0].cells[0].paragraphs[0], d["destacado"], 10.5, "tinta", negrita=True, antes=4, despues=4)


def pie(doc, c):
    p = doc.sections[0].footer.paragraphs[0]
    borde(p, "top", "linea", 6)
    escribir(p, f"{MARCA['firma']}  ·  {c['aviso']}", 7, "gris", "cifras")


def revisar(c):
    """Se niega a armar un documento desmedido o que no dice que los datos son ficticios."""
    fallas = []
    if not c.get("aviso", "").strip():
        fallas.append("falta `aviso`: todo documento de la demo dice que los datos son ficticios")
    if not c.get("titulo", "").strip():
        fallas.append("falta `titulo`")
    secciones = c.get("secciones", [])
    if not 1 <= len(secciones) <= TOPES["secciones"]:
        fallas.append(f"van de 1 a {TOPES['secciones']} secciones; hay {len(secciones)}")
    palabras = 0
    for n, d in enumerate(secciones, start=1):
        if not any(d.get(k) for k in ("parrafos", "vinetas", "tabla", "destacado")):
            fallas.append(f"sección {n}: está vacía")
        if len(d.get("vinetas", [])) > TOPES["vinetas"]:
            fallas.append(f"sección {n}: máximo {TOPES['vinetas']} viñetas")
        t = d.get("tabla")
        if t:
            if len(t["columnas"]) > TOPES["columnas"] or len(t["filas"]) > TOPES["filas"]:
                fallas.append(f"sección {n}: la tabla admite {TOPES['columnas']} columnas y {TOPES['filas']} filas")
            if any(len(fila) != len(t["columnas"]) for fila in t["filas"]):
                fallas.append(f"sección {n}: alguna fila no tiene las mismas celdas que columnas")
            palabras += 6 * (1 + len(t["filas"]))  # una fila de tabla ocupa lo que una línea de texto corta
        palabras += sum(len(x.split()) for x in d.get("parrafos", []) + d.get("vinetas", []) + [d.get("destacado", "")])
    if palabras > TOPES["palabras"]:
        fallas.append(f"es demasiado largo: {palabras} palabras contando las tablas, el tope es {TOPES['palabras']}. Acorta")
    if fallas:
        raise SystemExit("No se armó el documento:\n- " + "\n- ".join(fallas))


def armar(c, salida):
    revisar(c)
    doc = Document()
    hoja = doc.sections[0]
    hoja.page_width, hoja.page_height = Cm(21), Cm(29.7)
    hoja.left_margin = hoja.right_margin = Cm(1.9)
    hoja.top_margin, hoja.bottom_margin = Cm(1.4), Cm(1.4)
    encabezado(doc, c)
    for n, d in enumerate(c["secciones"], start=1):
        seccion(doc, n, d)
    pie(doc, c)
    doc.save(salida)
    return len(c["secciones"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python crear_documento.py contenido.json salida.docx")
    with open(sys.argv[1], encoding="utf-8") as f:
        contenido = json.load(f)
    print(f"Listo: {armar(contenido, sys.argv[2])} secciones en {sys.argv[2]}")
