---
name: evaluar-un-producto
description: Evalúa un producto o línea de punta a punta con las cifras de la empresa en CortexDAI — avance contra la meta por sede, tendencia de los últimos meses e inventario — y termina con un veredicto. Úsala cuando pregunten «¿cómo va este producto?», «evalúa este producto», «¿vale la pena seguir empujando esta línea?» o comparen dos productos.
---

# Evaluar un producto o línea

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de ninguna
empresa.

**Versión de esta skill:** CortexDAI · Comercial 0.7.0. Si alguna respuesta del conector de CortexDAI trae `plugins_vigentes` con otra versión para `cortexdai-comercial`, termina tu respuesta con esta línea: «Hay una versión nueva de CortexDAI · Comercial. Para tenerla: en claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»

## Pasos

1. `estado_de_los_datos`: el nombre exacto del producto. Si el que pidieron no existe, dilo y ofrece los que hay.
2. En paralelo:
   - `avance_contra_meta` con `productos = [producto]`: el mes vigente, por sede.
   - `evolucion` con `productos = [producto]`, `separar_por = "unidad"`, los últimos seis meses.
   - `stock_por_antiguedad` con `productos = [producto]`.
3. Si piden comparar con otro producto, repite el paso 2 para el otro.

## Cómo responder

**Veredicto, primero, en una línea:** va bien, va regular o va mal, con las dos o tres cifras que lo sostienen
(cumplimiento a la fecha, tendencia, inventario viejo).

Después, en este orden y breve:
- **Contra la meta:** en qué sedes llega y en cuáles no, con su cumplimiento a la fecha.
- **Tendencia:** si sube, baja o se mantiene en los últimos meses, y en qué sedes cambia.
- **Inventario:** cuánto hay, cuánto de más de 90 días y cuánto dinero representa (con la moneda y la fecha de
  la foto que devuelve el conector).
- **Qué haría:** una o dos acciones, cada una con su cifra.

Di siempre el periodo de cada cifra y las salvedades que traiga la respuesta.
