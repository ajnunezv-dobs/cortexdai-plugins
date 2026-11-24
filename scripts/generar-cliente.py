"""Arma los plugins de un cliente: las skills de CortexDAI con su marca, sus plantillas y, si tiene grupos, un plugin
por grupo. La ficha del cliente vive FUERA de este repositorio (es público): en una carpeta privada.

    python scripts/generar-cliente.py <carpeta del cliente>

La carpeta del cliente trae `cliente.json`, sus logotipos y, si quiere, sus plantillas:

    {
      "id": "ejemplo-sac",                 minúsculas y guiones: va en el nombre del plugin
      "nombre": "Ejemplo SAC",             como se ve
      "version": "1.0.0",                  subirla en cada entrega
      "marca": {
        "oscuro": "1B2A41",                el color de las franjas y los títulos
        "acento": "E07A1F",                el color que destaca (barras, cifra principal)
        "acento_texto": "8A4510",          el acento cuando va como letra sobre blanco (que se lea)
        "tipografia": "Segoe UI",          una que esté en toda PC con Office
        "logo_sobre_oscuro": "logo-blanco.png",
        "logo_sobre_claro": "logo-color.png",
        "verde": "3F8F4E"                  opcional: el color de «en meta» (por omisión, un verde)
      },
      "plantillas": {"informe-de-la-semana": "plantilla-informe.md"},
      "grupos": {                          sin «grupos»: un solo plugin con todas las skills
        "gerencia": ["como-vamos", "informe-de-la-semana", "dinero-detenido"],
        "sedes": ["como-vamos", "plan-para-cerrar-el-mes", "que-pedir-y-que-no"]
      }
    }

Sale en `<carpeta del cliente>/plugins/`: una carpeta y un .zip por plugin, listos para «Upload plugin» en claude.ai
(Organization settings › Plugins & skills; los grupos se asignan con «Group access…», solo en Enterprise). Todo plugin
lleva además `documentos-con-marca`, con los programas de Word, Excel y PowerPoint de este repositorio y la marca del
cliente. Las skills salen de los plugins públicos (Comercial e Inventario): una mejora ahí llega al cliente al volver
a generar.
"""
import json
import os
import re
import shutil
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLICOS = ("cortexdai-comercial", "cortexdai-inventario")
MARCA_SKILL = "documentos-con-marca"
HEX = re.compile(r"[0-9A-Fa-f]{6}")
NOMBRE = re.compile(r"[a-z0-9][a-z0-9-]{1,40}")
LOGOS = {"logo_sobre_oscuro": "logo-sobre-oscuro.png", "logo_sobre_claro": "logo-sobre-claro.png"}


class FichaInvalida(Exception):
    pass


def skills_publicas() -> dict:
    """{nombre de la skill: su carpeta} de los plugins públicos."""
    hay = {}
    for p in PUBLICOS:
        base = os.path.join(RAIZ, "plugins", p, "skills")
        for s in sorted(os.listdir(base)):
            hay[s] = os.path.join(base, s)
    return hay


def leer_ficha(carpeta: str) -> dict:
    ruta = os.path.join(carpeta, "cliente.json")
    if not os.path.exists(ruta):
        raise FichaInvalida(f"Falta {ruta}")
    f = json.load(open(ruta, encoding="utf-8"))
    fallas = []
    if not NOMBRE.fullmatch(f.get("id", "")):
        fallas.append("`id`: minúsculas, números y guiones")
    if not f.get("nombre"):
        fallas.append("falta `nombre`")
    if not re.fullmatch(r"\d+\.\d+\.\d+", f.get("version", "")):
        fallas.append("`version` como 1.0.0")
    m = f.get("marca") or {}
    for clave in ("oscuro", "acento", "acento_texto"):
        if not HEX.fullmatch(m.get(clave, "")):
            fallas.append(f"`marca.{clave}`: un color de 6 cifras hexadecimales, sin #")
    for clave in LOGOS:
        if not m.get(clave) or not os.path.exists(os.path.join(carpeta, m[clave])):
            fallas.append(f"`marca.{clave}`: falta el archivo del logotipo")
    hay = skills_publicas()
    for g, lista in (f.get("grupos") or {}).items():
        if not NOMBRE.fullmatch(g):
            fallas.append(f"grupo «{g}»: minúsculas y guiones")
        for s in lista:
            if s not in hay and s != MARCA_SKILL:
                fallas.append(f"grupo «{g}»: no existe la skill «{s}» (hay: {', '.join(sorted(hay))})")
    for s, archivo in (f.get("plantillas") or {}).items():
        if s not in hay:
            fallas.append(f"plantilla para «{s}», que no es una skill")
        elif not os.path.exists(os.path.join(carpeta, archivo)):
            fallas.append(f"falta la plantilla {archivo}")
    if fallas:
        raise FichaInvalida("La ficha del cliente tiene problemas:\n  · " + "\n  · ".join(fallas))
    return f


def _marca_en_programa(texto: str, f: dict) -> str:
    """Cambia el bloque MARCA de un programa por la marca del cliente. El resto del programa no se toca."""
    m = f["marca"]
    fuente = m.get("tipografia") or "Segoe UI"
    valores = {"tinta": m["oscuro"], "pistacho": m["acento"], "pistacho_texto": m["acento_texto"],
               "titulos": fuente, "texto": fuente, "firma": f["nombre"], "fondo_suave": m.get("fondo_suave") or "F4F5F7",
               "logo_sobre_oscuro": LOGOS["logo_sobre_oscuro"], "logo_sobre_claro": LOGOS["logo_sobre_claro"],
               "logo_sobre_acento": LOGOS["logo_sobre_claro"]}
    i = texto.index("MARCA = {")
    j = texto.index("\n}\n", i)
    bloque = texto[i:j]
    for clave, valor in valores.items():
        bloque = re.sub(rf'("{clave}": )"[^"]*"', lambda x: f'{x.group(1)}"{valor}"', bloque)
    # El acento de la marca de DObs (pistacho) es verdoso y por eso también pinta «en meta». El de un cliente puede ser
    # naranja o rojo: el estado «en meta» lleva un verde propio, siempre.
    verde = m.get("verde") or "3F8F4E"
    bloque = bloque.rstrip().rstrip(",") + f',\n    "verde": "{verde}",'
    texto = texto[:i] + bloque + texto[j:]
    texto = texto.replace('"verde": "pistacho"', '"verde": "verde"')
    texto = re.sub(r"todo (documento|archivo) de la demo dice que los datos son ficticios",
                   "todo archivo dice de dónde salen sus cifras y su fecha", texto)
    return texto


def _skill_de_marca(destino: str, carpeta: str, f: dict) -> None:
    origen = os.path.join(RAIZ, "plantillas", MARCA_SKILL)
    os.makedirs(os.path.join(destino, "scripts"))
    os.makedirs(os.path.join(destino, "recursos"))
    skill = open(os.path.join(origen, "SKILL.md"), encoding="utf-8").read().replace("{{EMPRESA}}", f["nombre"])
    open(os.path.join(destino, "SKILL.md"), "w", encoding="utf-8", newline="\n").write(skill)
    for p in sorted(os.listdir(os.path.join(origen, "scripts"))):
        if p.endswith(".py"):
            t = open(os.path.join(origen, "scripts", p), encoding="utf-8").read()
            open(os.path.join(destino, "scripts", p), "w", encoding="utf-8", newline="\n").write(_marca_en_programa(t, f))
    for clave, nombre in LOGOS.items():
        shutil.copyfile(os.path.join(carpeta, f["marca"][clave]), os.path.join(destino, "recursos", nombre))


def _version_del_cliente(texto: str, nombre_plugin: str, visible: str, version: str) -> str:
    """Las skills públicas dicen su versión de Comercial o Inventario; en el plugin del cliente dicen la suya."""
    return re.sub(r"\*\*Versión de esta skill:\*\*.*?(?=\n\n)",
                  lambda _: (f"**Versión de esta skill:** {visible} {version}. Si alguna respuesta del conector de CortexDAI "
                             f"trae `plugins_vigentes` con otra versión para `{nombre_plugin}`, termina tu respuesta con esta "
                             f"línea: «Hay una versión nueva de {visible}. Pídele a quien administra Claude en tu empresa que "
                             "la suba.»"), texto, count=1, flags=re.S)


def generar(carpeta: str) -> list:
    f = leer_ficha(carpeta)
    hay = skills_publicas()
    grupos = f.get("grupos") or {"": sorted(hay)}
    salida = os.path.join(carpeta, "plugins")
    shutil.rmtree(salida, ignore_errors=True)
    hechos = []
    for grupo, lista in grupos.items():
        nombre = f"cortexdai-{f['id']}" + (f"-{grupo}" if grupo else "")
        visible = f"{f['nombre']} · CortexDAI" + (f" · {grupo.replace('-', ' ').capitalize()}" if grupo else "")
        base = os.path.join(salida, nombre)
        os.makedirs(os.path.join(base, ".claude-plugin"))
        json.dump({"name": nombre, "displayName": visible, "version": f["version"],
                   "description": f"Las skills de CortexDAI para {f['nombre']}" + (f", grupo {grupo}" if grupo else "")
                                  + ": cifras verificadas desde tu IA, con la marca de la empresa.",
                   "author": {"name": "DObs", "url": "https://dobservability.com"}},
                  open(os.path.join(base, ".claude-plugin", "plugin.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
        shutil.copyfile(os.path.join(RAIZ, "plugins", PUBLICOS[0], ".mcp.json"), os.path.join(base, ".mcp.json"))
        for s in [x for x in lista if x != MARCA_SKILL]:
            destino = os.path.join(base, "skills", s)
            shutil.copytree(hay[s], destino)
            ruta = os.path.join(destino, "SKILL.md")
            t = _version_del_cliente(open(ruta, encoding="utf-8").read(), nombre, visible, f["version"])
            plantilla = (f.get("plantillas") or {}).get(s)
            if plantilla:
                shutil.copyfile(os.path.join(carpeta, plantilla), os.path.join(destino, "plantilla.md"))
            open(ruta, "w", encoding="utf-8", newline="\n").write(t)
        _skill_de_marca(os.path.join(base, "skills", MARCA_SKILL), carpeta, f)
        zipeado = base + ".zip"
        with zipfile.ZipFile(zipeado, "w", zipfile.ZIP_DEFLATED) as z:
            for r, _, archivos in os.walk(base):
                for a in sorted(archivos):
                    p = os.path.join(r, a)
                    z.write(p, os.path.join(nombre, os.path.relpath(p, base)).replace(os.sep, "/"))
        hechos.append((nombre, visible, sorted(os.listdir(os.path.join(base, "skills"))), zipeado))
    return hechos


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    try:
        for nombre, visible, skills, zipeado in generar(sys.argv[1]):
            print(f"{visible}  ({nombre})\n  skills: {', '.join(skills)}\n  archivo: {zipeado}")
    except FichaInvalida as e:
        sys.exit(str(e))
