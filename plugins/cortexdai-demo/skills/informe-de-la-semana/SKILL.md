---
name: informe-de-la-semana
description: Solo para la demo de CortexDAI con Distribuidora Andina, con su conector activo. Arma el informe semanal para la gerencia con los datos de CortexDAI (demo Distribuidora Andina, datos ficticios) — cómo va el mes contra la meta, qué objetivos están en riesgo, qué pasa en el almacén y tres decisiones para esta semana. Úsala cuando pidan «el informe de la semana», «el resumen para gerencia», «cómo vamos» o «qué tengo que mirar el lunes».
---

# Informe de la semana

**Solo con el conector de la demo.** Usa esta skill únicamente si en esta conversación está activo el conector de la demo de Distribuidora Andina (sus herramientas incluyen `que_pedir`, `objetivos` y `competencia`). Si el conector activo es el de una empresa real, no la uses: para eso están los plugins CortexDAI · Comercial e Inventario.

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

Produce, en una página, lo que un gerente general necesita leer el lunes. Las cifras salen del conector de
CortexDAI; tú no calculas nada que el conector ya entregue calculado.

## Pasos

1. Llama a `estado_de_los_datos`. Anota `datos_al` y `fecha_foto`. Si `coincide_con_la_pantalla` es falso o la
   respuesta trae un aviso que empieza por «ATENCIÓN», dilo en la primera línea del informe y sigue.
2. Llama, en paralelo, a:
   - `ventas` con `agrupar_por = "total"`, `desde` y `hasta` iguales al último mes cerrado — cómo cerró el mes contra
     el mismo mes del año anterior;
   - `competencia` — si algún competidor anuncia más barato que nosotros (brecha negativa);
   - `como_vamos_este_mes` — las seis sedes y el `total` de la red;
   - `objetivos` con `solo_en_riesgo = true`;
   - `stock_por_antiguedad` — usa el `total`.
3. Si alguna sede está `atrasada` o `en_riesgo`, llama a `como_vamos_este_mes` con esa sede y
   `por_linea = true` para decir qué línea la frena. Máximo dos sedes: las de peor `cierre_proyectado_pct`.
4. Escribe el informe con la estructura de abajo.

## Estructura del informe

**Encabezado.** «Informe de la semana · Distribuidora Andina · datos al {datos_al}» y, debajo, en una línea:
«Datos ficticios de la demostración de CortexDAI».

**1 · El mes en una frase.** Vendido, meta y cierre proyectado de la red (del `total`), y cuántas sedes van en
ritmo, en riesgo y atrasadas. El mes va a medias: compara contra lo esperado a la fecha, no contra la meta entera.

**2 · Dónde se va a fallar.** Una tabla corta: sede, cierre proyectado, meta, % y la línea que más la frena.
Solo las sedes que no llegan.

**3 · Objetivos sin dueño.** Los objetivos en rojo o ámbar con `sin_accion_en_curso = true`: nombre, área,
responsable, meta y valor real. Estos son los que piden una decisión.

**4 · Almacén.** Cajas con más de 120 días y entre 91 y 120, con su porcentaje, y el valor del almacén.

**5 · Tres decisiones para esta semana.** Concretas, con responsable (el del objetivo) y con la cifra que las
justifica. Nada genérico: «Revisar [sede]» no sirve; «[Sede] cerraría en [N] contra [M]: decidir hoy si se
empuja [línea] o se ajusta la meta» sí.

## Reglas

- Toda cifra va con su periodo y su comparación.
- Las metas y los tramos de días son «propuesta de DObs, por confirmar»: dilo una vez, al pie.
- No sumes objetivos entre sí ni promedies porcentajes: usa los totales que entrega el conector.
- Si una herramienta devuelve vacío, dilo; vacío no es cero.
- Nunca presentes estas cifras como las de una empresa real.
- Largo: una página. Sin introducción ni despedida.
- Si piden esto mismo en un archivo (Word, Excel, PowerPoint o de Google), no lo armes a mano: usa la skill
  `documentos-con-marca-dobs`, que le pone la marca de DObs. Ningún archivo sale sin marca.
