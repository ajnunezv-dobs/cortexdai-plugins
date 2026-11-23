"""Escribe en cada skill la versión de su plugin (la de plugin.json) y el aviso de versión nueva.

La conexión única anuncia en `initialize` la versión vigente de cada plugin (PLUGINS_VIGENTES). Si la skill trae otra,
le dice a la persona que pulse «Check for updates». Solo para los plugins que usan la conexión única (con .mcp.json).
"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = re.compile(r"\n\*\*Versión de esta skill:\*\*.*?(?=\n\n)", re.S)


def bloque(nombre, visible, version):
    return (f"\n**Versión de esta skill:** {visible} {version}. Si las instrucciones del conector de CortexDAI dicen otra versión "
            f"vigente para `{nombre}`, termina tu respuesta con esta línea: «Hay una versión nueva de {visible}. Para tenerla: en "
            "claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»")


def vigentes():
    for p in sorted(os.listdir(os.path.join(RAIZ, "plugins"))):
        carpeta = os.path.join(RAIZ, "plugins", p)
        if os.path.exists(os.path.join(carpeta, ".mcp.json")):
            pj = json.load(open(os.path.join(carpeta, ".claude-plugin", "plugin.json"), encoding="utf-8"))
            yield carpeta, pj


if __name__ == "__main__":
    for carpeta, pj in vigentes():
        for s in sorted(os.listdir(os.path.join(carpeta, "skills"))):
            ruta = os.path.join(carpeta, "skills", s, "SKILL.md")
            t = open(ruta, encoding="utf-8").read()
            nuevo = bloque(pj["name"], pj["displayName"], pj["version"])
            if MARCA.search(t):
                t = MARCA.sub(lambda _: nuevo, t, count=1)
            else:   # va justo después del párrafo de las cifras
                i = t.index("\n\n", t.index("Las cifras salen siempre del conector de CortexDAI"))
                t = t[:i] + "\n" + nuevo + t[i:]
            open(ruta, "w", encoding="utf-8", newline="\n").write(t)
        print(f"{pj['name']} {pj['version']}")
