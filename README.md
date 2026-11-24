# Plugins de CortexDAI

Repositorio privado de DObs. Cada carpeta de `plugins/` es un plugin para claude.ai con las skills de un cliente.
Se agrega una vez en claude.ai (Personalizar > Plugins > Agregar marketplace) y los cambios llegan solos.

Reglas: las skills no llevan cifras ni datos del cliente; nada de claves ni enlaces con clave en este repositorio;
cada publicación sube el `version` del `plugin.json`.

## Plugins

| Plugin | Qué trae |
|---|---|
| `cortexdai-comercial` | Cómo va el mes, plan para cerrar el mes, evaluar un producto, informe de la semana |
| `cortexdai-inventario` | Dinero detenido, qué pedir y qué no |
| `cortexdai-demo` | Las skills de la demostración con Distribuidora Andina (datos ficticios); usan el conector de la demo, que se agrega a mano |

Comercial e Inventario traen el conector único `https://mcp.cortexdai.dobservability.com/mcp`: el inicio de sesión decide el ambiente
de cada cliente. Las skills solo usan las siete herramientas fijas del conector.

Antes de publicar: `python scripts/validar.py` y subir el `version` del plugin que cambió.

## Cómo llegan los cambios

Con un marketplace agregado por una persona (Customize → Plugins → Add marketplace), «Sync automatically» no trajo los
cambios por sí solo en la prueba del 2026-11-23: llegan con **Manage marketplaces → ⋯ → Check for updates**, un clic que
actualiza todos los plugins. En Team y Enterprise el administrador sincroniza el repositorio para toda la empresa (sin probar).

## Plugins propios de un cliente (su marca, sus plantillas, sus grupos)

    python scripts/generar-cliente.py <carpeta privada del cliente>

La carpeta del cliente (con `cliente.json`, sus logotipos y sus plantillas) **no va en este repositorio**: vive en
`D:\Proyectos\DObs\cortexdai-plugins-clientes\<cliente>`. El generador toma las skills de Comercial e Inventario, les
pone la versión del cliente, agrega `documentos-con-marca` con su marca (`plantillas/documentos-con-marca`) y deja un
plugin por grupo, con su .zip para «Upload plugin». El formato de la ficha está al inicio de `scripts/generar-cliente.py`.
