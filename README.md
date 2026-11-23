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
| `cortexdai-prueba` | Solo para comprobar que las actualizaciones llegan solas |

Comercial e Inventario traen el conector único `https://mcp.cortexdai.dobservability.com/mcp`: el inicio de sesión decide el ambiente
de cada cliente. Las skills solo usan las siete herramientas fijas del conector.

Antes de publicar: `python scripts/validar.py` y subir el `version` del plugin que cambió.
