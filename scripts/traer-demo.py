"""Trae las skills de la demo (Distribuidora Andina) desde el repositorio de la plataforma, donde se prueban contra
el conector de la demo (tests/test_mcp_demo.py). Esa carpeta es la fuente; aquí solo se publican.

    python scripts/traer-demo.py <carpeta del lakehouse, rama cortex-generico>

Después: python scripts/validar.py, subir el `version` de plugins/cortexdai-demo y publicar.
"""
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
origen = os.path.join(sys.argv[1], "mcp_demo", "skills")
destino = os.path.join(RAIZ, "plugins", "cortexdai-demo", "skills")
if not os.path.isdir(origen):
    sys.exit(f"No existe {origen}")
shutil.rmtree(destino, ignore_errors=True)
shutil.copytree(origen, destino, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
# En un plugin, los programas de la skill se llaman por su carpeta: ${CLAUDE_SKILL_DIR}.
for s in os.listdir(destino):
    ruta = os.path.join(destino, s, "SKILL.md")
    t = open(ruta, encoding="utf-8").read()
    t = re.sub(r"(\n\s*)python scripts/", r"\1python ${CLAUDE_SKILL_DIR}/scripts/", t)
    open(ruta, "w", encoding="utf-8", newline="\n").write(t)
print("Traídas:", ", ".join(sorted(os.listdir(destino))))
