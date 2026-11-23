---
name: que-pedir-y-que-no
description: Compara el inventario con lo que se vende para decir qué productos se van a acabar y conviene pedir, cuáles sobran y conviene dejar de pedir, por sede, con las cifras de la empresa en CortexDAI. Úsala cuando pregunten «¿qué pido esta semana?», «¿qué se me va a acabar?», «¿qué dejo de pedir?», por meses de inventario o por sobrestock.
---

# Qué pedir y qué no

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de ninguna
empresa. La venta futura no se conoce: esto es una sugerencia para decidir, no un pedido.

**Versión de esta skill:** CortexDAI · Inventario 0.2.0. Si las instrucciones del conector de CortexDAI dicen otra versión vigente para `cortexdai-inventario`, termina tu respuesta con esta línea: «Hay una versión nueva de CortexDAI · Inventario. Para tenerla: en claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»

## Pasos

1. `estado_de_los_datos`: el último mes cerrado y la fecha de la foto del inventario.
2. En paralelo:
   - `stock_por_antiguedad` (con `unidades` si piden una sede): la cantidad por sede y producto, sumando los tramos.
   - `evolucion` de los **tres últimos meses cerrados**, `separar_por = "producto"`, una vez por sede
     (`unidades = [sede]`), o sin sede si piden toda la empresa.

## El cálculo (dilo siempre así)

**Meses de inventario = cantidad en almacén ÷ venta promedio mensual de los tres últimos meses cerrados.**
Hazlo solo con las cifras del conector, por sede y producto.

- **Se va a acabar (pedir):** menos de 1 mes de inventario y el producto se vende.
- **Sobra (dejar de pedir):** más de 3 meses de inventario.
- **Sin venta:** hay inventario y no se vendió nada en los tres meses: para liquidar (ver la skill de dinero detenido).

Estos umbrales (1 y 3 meses) son una referencia general. Si la empresa tiene los suyos, pregúntalos y úsalos.

## Cómo responder

Tres listas cortas, cada una con como mucho diez filas, ordenadas por urgencia:

| Sede | Producto | En almacén | Venta promedio al mes | Meses de inventario |
|---|---|---|---|---|

1. **Pedir ya.** 2. **Dejar de pedir.** 3. **Sin venta.**

Debajo: el periodo de la venta usado, la fecha de la foto del inventario y las salvedades que traiga el conector.
No digas cuánto pedir: eso depende del plazo de reposición y del proveedor, que el conector no tiene.
