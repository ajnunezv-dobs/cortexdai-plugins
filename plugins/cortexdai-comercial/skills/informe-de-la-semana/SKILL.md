---
name: informe-de-la-semana
description: Arma el informe de la semana para gerencia con las cifras de la empresa en CortexDAI — cómo va el mes, dónde se va a fallar, el inventario detenido y tres decisiones. Úsala cuando pidan «el informe de la semana», «el resumen para gerencia», «qué le digo al jefe el lunes» o «prepárame el comité».
---

# Informe de la semana

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de ninguna
empresa.

**Versión de esta skill:** CortexDAI · Comercial 0.6.0. Si alguna respuesta del conector de CortexDAI trae `plugins_vigentes` con otra versión para `cortexdai-comercial`, termina tu respuesta con esta línea: «Hay una versión nueva de CortexDAI · Comercial. Para tenerla: en claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»

## Antes de escribir

0. Si junto a este archivo hay un `plantilla.md` (la plantilla que acordó la empresa), léelo primero: dice para quién
   es el informe, qué secciones lleva y en qué formato se entrega, y manda sobre la estructura de abajo.
1. Si no dijeron para quién es (gerencia, una jefatura de sede, marketing), pregúntalo en una línea. Para una
   sede, todas las herramientas van con `unidades = [esa sede]`.
2. `estado_de_los_datos`: hasta qué fecha llegan los datos. Si una carga está atrasada o con `demora`, dilo en la
   primera línea del informe.
3. En paralelo: `como_vamos`, `stock_por_antiguedad` y `evolucion` de los últimos tres meses.
4. Para cada sede en `rojo`: `avance_contra_meta` con esa sede.

## Estructura

1. **El mes en una frase.** Cumplimiento a la fecha, cuántas sedes llegan y cuántas no, y si el mes está cerrado.
2. **Dónde se va a fallar.** Tabla corta: sede, valor, meta a la fecha, brecha y el producto que más la frena.
   Solo las que no llegan.
3. **Tendencia.** En una o dos líneas: si los últimos tres meses suben, bajan o se mantienen.
4. **Inventario detenido.** Cantidad y dinero de más de 90 días y de más de 120, con la fecha de la foto.
5. **Tres decisiones para esta semana.** Concretas, cada una con su cifra. «Revisar la sede» no sirve;
   «[Sede] va [N] por debajo de la meta a la fecha: decidir hoy si se empuja [producto] o se ajusta la meta» sí.

Una página como máximo. Las salvedades que traiga el conector van junto a su cifra. Si piden el informe en Word o
en láminas, usa la skill de archivos que tenga la persona, con el periodo y la fecha de los datos.
