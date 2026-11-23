---
name: como-vamos
description: Responde cómo va el mes contra la meta con las cifras de la empresa en CortexDAI — cuánto se lleva, cuánto tocaba a la fecha, qué sedes o tiendas van en meta y cuáles no, y qué productos las frenan. Úsala cuando pregunten «¿cómo vamos?», «¿cómo va el mes?», «¿llegamos a la meta?», «¿qué sede va peor?» o pidan el resumen del mes.
---

# Cómo vamos este mes

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de ninguna
empresa. No estimes ni completes una cifra que falte: si no está, dilo.

**Versión de esta skill:** CortexDAI · Comercial 0.4.0. Si las instrucciones del conector de CortexDAI dicen otra versión vigente para `cortexdai-comercial`, termina tu respuesta con esta línea: «Hay una versión nueva de CortexDAI · Comercial. Para tenerla: en claude.ai, Plugins → Add → Manage marketplaces → ⋯ → Check for updates.»

## Pasos

1. `como_vamos` (sin `periodo`: el mes vigente). Si piden otro mes, `periodo = "AAAA-MM"`.
2. Si `hay_datos` es falso, di que todavía no hay datos cargados y qué hacer (lo dice la respuesta). Termina ahí.
3. Para cada sede o tienda en `rojo` o `ambar` (las `unidades` de la respuesta), `avance_contra_meta` con
   `unidades = [esa sede]`: qué productos explican la brecha. Llámalas en paralelo.

## Cómo responder

- **Primera línea: la conclusión.** Cuánto se lleva contra la meta **que toca a la fecha**
  (`cumplimiento_a_la_fecha_pct`), cuántas sedes van en meta y cuántas no. El mes y si está cerrado.
- **No confundas los dos porcentajes.** `cumplimiento_pct` es contra la meta del mes completo; a mitad de mes
  siempre es bajo. El que dice si se va bien es `cumplimiento_a_la_fecha_pct`.
- **Las sedes que no llegan**, de la peor a la mejor: valor, meta a la fecha, brecha y los dos o tres productos
  que más pesan en esa brecha.
- **Salvedades.** Si la respuesta trae `salvedades`, `firme: false` o `aviso`, dilo junto a la cifra, con sus
  palabras. Un mes sin cerrar va a subir: dilo.
- Usa los colores en palabras (`en_palabras`): «en meta», «cerca de la meta», «por debajo de la meta».
- Si la empresa tiene comparación con el año anterior (`variacion_anual_pct`), dila. Si no viene, no la inventes.
- Usa los nombres exactos de sedes y productos que devuelve el conector.

Si piden un archivo (Word, Excel, PowerPoint), arma el contenido con estas mismas cifras y usa la skill de
archivos que tenga la persona. Pon en el archivo el periodo y la fecha de los datos.
