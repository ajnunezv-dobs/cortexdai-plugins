---
name: dinero-detenido-en-almacen
description: Encuentra el dinero detenido en el almacén y propone qué liquidar, qué dejar de pedir y qué pedir ya, con los datos de CortexDAI (demo Distribuidora Andina, datos ficticios). Úsala cuando pregunten por stock viejo, sobrestock, «¿qué liquido?», «¿qué pido esta semana?», «¿cuánto dinero tengo parado?» o por una sede en particular.
---

# Dinero detenido en el almacén

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

Dos errores cuestan dinero a la vez: cajas que llevan meses sin venderse y productos que se acaban. Esta skill
los pone en una sola lista de decisiones.

## Pasos

1. `stock_por_antiguedad` (con `sedes` si piden una sede) — toma el `total` y las filas con más cajas de más de
   120 días.
2. `stock_por_antiguedad` con `por_producto = true` — los productos concretos con cajas de más de 90 días.
3. `que_pedir` — usa el `resumen` y las filas: `liquidar`, `sobrestock`, `sin_venta` y `pedir`.
4. Solo si preguntan cuánto cuesta en dinero un producto en particular: `consultar_sql` sobre
   `demo_andina.stock_linea` (valor e interés están por sede y línea, no por producto; dilo así).

## Cómo responder

**La cifra de arriba.** Cuántas cajas hay fuera de política (más de 120 días) y en excepción (91 a 120), qué
porcentaje del almacén son, y el interés mensual que cuesta lo que pasa de 30 días. Con la fecha de la foto.

**Tres listas cortas** (máximo cinco filas cada una; si hay más, di cuántas quedan fuera):

| Lista | Qué entra | Qué decir de cada fila |
|---|---|---|
| Liquidar esta semana | `decision = liquidar` y `sin_venta` | sede, producto, cajas de más de 120 días, días de cobertura |
| Dejar de pedir | `decision = sobrestock` | sede, producto, cajas en almacén y en camino, cobertura |
| Pedir ya | `decision = pedir` con `se_acaba = true` | sede, producto, días de cobertura, cajas sugeridas, plazo de reposición |

**El cruce que nadie ve.** Si la misma línea tiene sobrestock en una sede y se acaba en otra, dilo: un traslado
sale más barato que liquidar aquí y comprar allá. Búscalo en las filas de `que_pedir`.

## Reglas

- Di al inicio que son datos ficticios de la demostración de CortexDAI.
- Los tramos de días y las reglas de pedido son «propuesta de DObs, por confirmar»: dilo una vez.
- El dinero (valor e interés) existe por sede y línea. No lo repartas entre productos por tu cuenta.
- No sumes cajas de listas distintas como si fueran un solo problema.
- Cada recomendación con su cifra y su sede. Sin introducción ni despedida.
- Si piden esto mismo en un archivo (Word, Excel, PowerPoint o de Google), no lo armes a mano: usa la skill
  `documentos-con-marca-dobs`, que le pone la marca de DObs. Ningún archivo sale sin marca.
