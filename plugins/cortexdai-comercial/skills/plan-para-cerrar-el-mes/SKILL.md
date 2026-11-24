---
name: plan-para-cerrar-el-mes
description: Convierte la brecha contra la meta en un plan para lo que queda del mes — cuánto falta por sede y por producto, qué empujar, qué inventario usar y quién lo hace — con las cifras de la empresa en CortexDAI. Úsala cuando pidan «¿cómo cerramos el mes?», «un plan para esta sede», «¿qué hago con esta sede?», «¿dónde está la brecha?» o una lista de tareas para un jefe de sede.
---

# Plan para cerrar el mes

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de ninguna
empresa. Un plan sin cifra no es un plan: cada acción lleva la suya.

**Versión de esta skill:** CortexDAI · Comercial 0.6.0. Si alguna respuesta del conector de CortexDAI trae `plugins_vigentes` con otra versión para `cortexdai-comercial`, termina tu respuesta con esta línea: «Hay una versión nueva de CortexDAI · Comercial. Para tenerla: en claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»

## Pasos

1. `como_vamos`: el estado del mes y qué sedes van en `rojo` o `ambar`. Si piden una sede, trabaja solo con ella.
2. `avance_contra_meta` con `unidades = [sede]`: los productos de esa sede, de lo peor a lo mejor, con su brecha.
3. `stock_por_antiguedad` con `unidades = [sede]`: qué hay en el almacén de esa sede para vender.
4. `evolucion` con `unidades = [sede]`, `separar_por = "producto"`, los últimos seis meses: si la caída es de
   este mes o viene de antes.

Llama en paralelo lo que no depende de otra respuesta.

## El plan

Una tabla, ordenada por brecha (lo que más falta primero), con como mucho diez filas:

| Acción | Sede | Producto | Cifra que la justifica | Responsable | Fecha |
|---|---|---|---|---|---|

- **Acción:** un verbo y un objeto («Empujar [producto] con el inventario de más de 90 días»), nunca «revisar».
- **Cifra:** la brecha del producto y, si aplica, cuánto inventario hay y de qué antigüedad.
- **Responsable y fecha:** si la persona no los dio, deja «Por definir». No inventes nombres.
- Debajo de la tabla, en una línea: cuánto falta en total para la meta y qué parte cubren las acciones. Si no
  alcanzan, dilo: las acciones mueven ventas, no las prometen.
- Si la caída viene de varios meses (paso 4), dilo: no es un problema de este mes.

Si piden el plan en Excel, arma la misma tabla con la skill de archivos que tenga la persona, con el periodo y
la fecha de los datos en el título.
