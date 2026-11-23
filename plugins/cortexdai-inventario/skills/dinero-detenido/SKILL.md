---
name: dinero-detenido
description: Encuentra cuánto dinero está detenido en el almacén y dónde — por antigüedad, sede y producto — con las cifras de la empresa en CortexDAI, y dice qué liquidar primero. Úsala cuando pregunten por stock viejo, inventario parado, «¿cuánto dinero tengo en el almacén?», «¿qué liquido?» o por el inventario de una sede.
---

# Dinero detenido en el almacén

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de ninguna
empresa.

**Versión de esta skill:** CortexDAI · Inventario 0.3.0. Si las instrucciones del conector de CortexDAI dicen otra versión vigente para `cortexdai-inventario`, termina tu respuesta con esta línea: «Hay una versión nueva de CortexDAI · Inventario. Para tenerla: en claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»

## Pasos

1. `stock_por_antiguedad` (con `unidades` si piden una sede, con `productos` si piden un producto).
2. Si `hay_datos` es falso o no hay inventario cargado, dilo y termina.
3. Para saber si lo viejo se vende o no: `evolucion` de los últimos tres meses con `separar_por = "producto"`
   (y la sede, si piden una).

## Cómo responder

- **La cifra de arriba:** cuánta cantidad y cuánto dinero hay de más de 90 días (los tramos «91 a 120 días» y
  «Más de 120 días») y qué parte del almacén es. Con la moneda y la fecha de la foto (`al`).
- **Dónde está:** las combinaciones de sede y producto con más dinero de más de 90 días, de mayor a menor, como
  mucho diez filas.
- **Qué liquidar primero:** lo que tiene más dinero viejo **y** casi no se vendió en los últimos meses. Si se
  vende bien, no es para liquidar: es inventario que rota lento; dilo así.
- Los tramos de antigüedad son una referencia general de DObs (lo dice la `nota`): si la empresa usa otros, que
  lo diga y se ajusta.
- Todo cálculo tuyo (porcentajes, sumas) se hace solo con cifras del conector y se dice cómo se hizo.
