"""Revisa el repositorio de plugins antes de cada publicación: python scripts/validar.py

- cada plugin del marketplace existe, y su nombre coincide con su plugin.json;
- cada skill está en skills/<nombre>/SKILL.md con `name` igual a su carpeta y con descripción;
- ninguna skill nombra una herramienta que el conector no tiene (las siete fijas de CortexDAI);
- ninguna trae cifras ni nombres de una empresa (las cifras salen siempre del conector);
- nada de `bin/` arriba (claude.ai no lo instala) ni de enlaces con clave.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERRAMIENTAS = {"estado_de_los_datos", "describir_datos", "como_vamos", "avance_contra_meta", "evolucion",
                "stock_por_antiguedad", "consultar_sql"}
#: La demo (Distribuidora Andina) tiene su propio conector, con otras herramientas. Su dirección lleva clave y por eso el
#: plugin de la demo no trae `.mcp.json`: el conector de la demo se agrega a mano y nunca se escribe en este repositorio.
HERRAMIENTAS_DEMO = {"describir_datos", "estado_de_los_datos", "como_vamos_este_mes", "avance_contra_meta", "ventas",
                     "stock_por_antiguedad", "que_pedir", "objetivos", "fuentes", "competencia", "consultar_sql"}
#: Lo que se parece a una herramienta en un SKILL.md: `palabra_con_guion_bajo` entre comillas invertidas.
PARECE_HERRAMIENTA = re.compile(r"`([a-z]+(?:_[a-z]+)+)`")
#: Campos de las respuestas del conector que sí se nombran (no son herramientas).
CAMPOS = {"hay_datos", "cumplimiento_a_la_fecha_pct", "cumplimiento_pct", "en_palabras", "variacion_anual_pct", "separar_por",
          "meta_a_la_fecha"}
CAMPOS_DEMO = {"sin_venta", "se_acaba", "fecha_foto", "coincide_con_la_pantalla", "en_riesgo", "datos_al", "cierre_proyectado_pct",
               "esperado_a_la_fecha", "faltan_cajas", "cajas_vendidas", "sin_dato"}
CIFRA = re.compile(r"\b\d{1,3}(,\d{3})+\b|\b\d+\.\d\s?%")
fallas = []


def falla(texto):
    fallas.append(texto)
    print("FALLA " + texto)


m = json.load(open(os.path.join(RAIZ, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
for p in m["plugins"]:
    carpeta = os.path.normpath(os.path.join(RAIZ, p["source"]))
    manifiesto = os.path.join(carpeta, ".claude-plugin", "plugin.json")
    if not os.path.exists(manifiesto):
        falla(f"{p['name']}: no existe {p['source']}/.claude-plugin/plugin.json")
        continue
    pj = json.load(open(manifiesto, encoding="utf-8"))
    if pj.get("name") != p["name"]:
        falla(f"{p['name']}: plugin.json se llama {pj.get('name')}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", pj.get("version", "")):
        falla(f"{p['name']}: sin versión (sin subirla, los cambios no llegan)")
    if os.path.isdir(os.path.join(carpeta, "bin")):
        falla(f"{p['name']}: tiene bin/ arriba")
    mcp = os.path.join(carpeta, ".mcp.json")
    if os.path.exists(mcp):
        for nombre, s in json.load(open(mcp, encoding="utf-8")).get("mcpServers", {}).items():
            if s.get("type") != "http" or not s.get("url", "").startswith("https://") or re.search(r"/[A-Za-z0-9_-]{24,}/", s.get("url", "")):
                falla(f"{p['name']}: el conector {nombre} no es una dirección https fija sin clave")
    skills = os.path.join(carpeta, "skills")
    for s in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
        ruta = os.path.join(skills, s, "SKILL.md")
        texto = open(ruta, encoding="utf-8").read()
        cabeza = re.match(r"---\n(.*?)\n---\n", texto, re.S)
        if not cabeza or f"name: {s}\n" not in cabeza.group(1) + "\n" or "description: " not in cabeza.group(1):
            falla(f"{p['name']}/{s}: el encabezado no tiene name = carpeta y descripción")
        if p["name"] != "cortexdai-prueba" and "Las cifras salen siempre del conector de CortexDAI" not in texto:
            falla(f"{p['name']}/{s}: no dice que las cifras salen del conector")
        validas = HERRAMIENTAS_DEMO if p["name"] == "cortexdai-demo" else HERRAMIENTAS
        for h in set(PARECE_HERRAMIENTA.findall(texto)) - validas - CAMPOS - CAMPOS_DEMO:
            falla(f"{p['name']}/{s}: nombra `{h}`, que no es una herramienta del conector")
        if os.path.exists(mcp) and f"**Versión de esta skill:** {pj.get('displayName')} {pj.get('version')}." not in texto:
            falla(f"{p['name']}/{s}: no dice la versión del plugin (corre scripts/marcar-version.py)")
        for c in CIFRA.findall(texto):
            falla(f"{p['name']}/{s}: trae una cifra ({c})")

if fallas:
    print(f"{len(fallas)} FALLAS")
    sys.exit(1)
print("TODO OK · plugins listos para publicar")
