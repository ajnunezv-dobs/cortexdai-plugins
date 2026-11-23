---
name: evaluar-una-linea
description: Solo para la demo de CortexDAI con Distribuidora Andina, con su conector activo. Evalúa una línea de productos de punta a punta con los datos de CortexDAI (demo Distribuidora Andina, datos ficticios) — ventas y margen contra el año anterior, avance contra la meta por sede, almacén y pedido sugerido — y termina con un veredicto. Úsala cuando pregunten «¿cómo va Snacks?», «evalúa la línea de Bebidas», «¿vale la pena seguir empujando Limpieza?» o comparen dos líneas.
---

# Evaluar una línea

**Solo con el conector de la demo.** Usa esta skill únicamente si en esta conversación está activo el conector de la demo de Distribuidora Andina (sus herramientas incluyen `que_pedir`, `objetivos` y `competencia`). Si el conector activo es el de una empresa real, no la uses: para eso están los plugins CortexDAI · Comercial e Inventario.

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

Responde una sola pregunta: **¿esta línea va bien, y qué hay que hacer con ella?** Cruza cuatro miradas que
normalmente viven en cuatro reportes distintos.

Las líneas que existen las da el conector (`ventas` con `agrupar_por = "linea"`). Si piden una que no está,
dilo y ofrece las que hay.

## Pasos

Llama en paralelo, siempre con `lineas = [la línea]`:

1. `ventas` con `agrupar_por = "sede"` — el año hasta el último mes cerrado, contra el año anterior, con margen.
2. `ventas` con `agrupar_por = "linea"` y **sin** filtro de línea — para saber cómo le va frente a las otras cinco
   (su lugar en cajas, en crecimiento y en margen).
3. `avance_contra_meta` — último mes cerrado, por sede.
4. `como_vamos_este_mes` — el mes en curso, por sede, con el `total` de la línea.
5. `stock_por_antiguedad` — cajas por tramo de días y dinero detenido.
6. `que_pedir` — qué productos de la línea hay que pedir, liquidar o tienen sobrestock.

## Cómo responder

**Veredicto, primero.** Una línea: «[Línea] va mal: cae [N] % contra el año anterior, no llega a la meta en [N] de [N] sedes y
tiene [N] cajas fuera de política». Va bien / va regular / va mal, con las dos o tres cifras que lo sostienen.

**Las cuatro miradas**, cada una en dos o tres líneas con sus cifras:

- **Venta y margen.** Cajas y variación contra el año anterior; margen y su lugar entre las seis líneas.
- **Contra la meta.** Mes cerrado: en cuántas sedes cumplió. Mes en curso: cierre proyectado de la línea contra
  su meta (del `total`), y qué sedes la sostienen y cuáles la hunden.
- **Almacén.** Cajas con más de 90 y de 120 días y en qué sedes están. Una línea que no vende y además se
  acumula es otro problema que una que no vende pero rota.
- **Pedido.** Productos por pedir, por liquidar y en sobrestock. Si hay productos que se acaban (`se_acaba`),
  nómbralos.

**Qué hacer.** Dos o tres acciones concretas, cada una con sede, producto y cifra.

## Reglas

- Di al inicio que son datos ficticios de la demostración de CortexDAI.
- Toda cifra con su periodo. El mes en curso va a medias: se compara contra lo esperado a la fecha.
- Las metas y las reglas de pedido son «propuesta de DObs, por confirmar».
- La meta de la línea en la red es la suma de sus sedes (el `total`); no promedies cumplimientos.
- Si comparan dos líneas, repite los pasos para cada una y cierra con una tabla lado a lado.
- No inventes causas: si los datos no explican por qué cae una línea, di qué dato faltaría.
- Si piden esto mismo en un archivo (Word, Excel, PowerPoint o de Google), no lo armes a mano: usa la skill
  `documentos-con-marca-dobs`, que le pone la marca de DObs. Ningún archivo sale sin marca.
