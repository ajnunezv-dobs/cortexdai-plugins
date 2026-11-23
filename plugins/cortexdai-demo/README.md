# CortexDAI · Demo

Las skills que se muestran a un prospecto con la empresa ficticia Distribuidora Andina. Usan el conector de la demo,
que tiene sus propias herramientas (`que_pedir`, `objetivos`, `competencia`…) y se agrega a mano: su dirección lleva
clave y por eso no está en este repositorio.

Fuente: `mcp_demo/skills` del repositorio de la plataforma, donde se prueban contra el conector de la demo. Para
traer cambios: `python scripts/traer-demo.py <carpeta del lakehouse>`, `python scripts/validar.py`, subir `version`.

Fuera de una demo, apaga este plugin: sus skills son para la demo y no sirven con los datos de un cliente.
