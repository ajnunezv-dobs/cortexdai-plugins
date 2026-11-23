---
name: plan-de-accion-por-sede
description: Convierte el atraso de una sede en un plan de acción para lo que queda del mes — cuántas cajas faltan por línea, qué productos liquidar, cuáles dejar de pedir y cuáles pedir — y lo entrega como una hoja de Excel con responsable y fecha, ya con la marca de DObs (logotipo y colores), con los datos de CortexDAI (demo Distribuidora Andina, datos ficticios). Úsala cuando pidan «el plan para Cusco», «¿qué hago con esta sede?», «un plan de acción», «¿cómo cierro el mes?» o una lista de tareas para un jefe de sede. También cuando lo pidan en Google Sheets: se arma el mismo archivo con marca y se abre en Google.
---

# Plan de acción por sede

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

Un jefe comercial no necesita otro reporte: necesita saber **qué hace mañana cada persona**. Esta skill entrega
una hoja de Excel con una fila por acción.

## Pasos

Con la sede que pidan (si no dicen cuál, usa la de peor `cierre_proyectado_pct` de `como_vamos_este_mes`):

1. `como_vamos_este_mes` con `sedes = [sede]` — estado, `faltan_cajas` y cierre proyectado de la sede.
2. `como_vamos_este_mes` con `sedes = [sede]` y `por_linea = true` — qué líneas están por debajo de lo esperado
   a la fecha (`cajas_vendidas` menor que `esperado_a_la_fecha`).
3. `que_pedir` con `sedes = [sede]` — productos por `liquidar`, `sin_venta`, `sobrestock` y `pedir`.
4. `stock_por_antiguedad` con `sedes = [sede]` — cajas de más de 120 días y dinero detenido por línea.
5. `objetivos` con `solo_en_riesgo = true` — quién es el responsable de la sede y de cada línea atrasada.

## El archivo de Excel (con la marca de DObs)

**No armes el Excel a mano ni con otra librería.** La marca (franja con el logotipo, colores, encabezados y pie) la
pone el programa `scripts/crear_plan.py`; tú solo escribes el contenido.

1. Escribe el contenido en `contenido.json`, con la forma que explica el encabezado de `scripts/crear_plan.py`
   (hay un ejemplo completo en `ejemplo.json`). Las cajas van como número. El `aviso` es siempre
   «Datos ficticios · demostración de CortexDAI».
2. Ejecuta, desde la carpeta de esta skill:
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/crear_plan.py contenido.json plan-{sede}-{AAAA-MM}.xlsx
   ```
   Si falta la librería: `pip install openpyxl pillow`. Si el programa se niega, dice qué corregir.
3. Entrega ese archivo. No lo abras para cambiarle colores, letras ni el logotipo.

El programa arma dos hojas con lo que le des:

**Hoja «Plan»** — una fila por acción, ordenadas por cajas (de más a menos). Máximo 12 filas.

| Columna | Qué lleva |
|---|---|
| Nº | 1, 2, 3… |
| Acción | Un verbo y un objeto: «Liquidar [producto]», «Dejar de pedir [producto]», «Pedir [producto]» |
| Línea | La línea del producto |
| Cajas | Las cajas que mueve la acción (del conector, sin redondear) |
| Por qué | La cifra que la justifica: «[N] días de cobertura; [N] cajas con más de 120 días» |
| Responsable | El de `objetivos` para esa línea o sede. Si no hay, escribe «Sin responsable»: no inventes un nombre |
| Fecha límite | Dentro del mes en curso. Lo que se acaba (`se_acaba = true`) vence antes que su plazo de reposición |
| Estado | «Pendiente» en todas |

El programa las ordena por cajas, inmoviliza el encabezado y pone el estado «Pendiente».

**Hoja «Meta del mes»** — una fila por línea de la sede: vendido, meta, esperado a la fecha, cierre proyectado y
cajas que faltan para la meta. Una última fila con el `total` del conector (no lo sumes tú).
Debajo, una línea: «Faltan {faltan_cajas} cajas para la meta de {mes}, con datos al {datos_al}».

El aviso de datos ficticios lo pone el programa en las dos hojas.

## En el chat

Después del archivo, cinco líneas como máximo: estado de la sede, las tres acciones que más cajas mueven y lo
que el plan **no** alcanza a cubrir (si las acciones no suman lo que falta, dilo con la cifra).

## Reglas

- Di al inicio que son datos ficticios de la demostración de CortexDAI.
- No prometas ventas: liquidar o trasladar cajas no es vender. La columna «Cajas» dice cuántas cajas mueve la
  acción, no cuánto sube la venta.
- Los nombres de los responsables de la demo son inventados.
- Las reglas de pedido y los tramos de días son «propuesta de DObs, por confirmar»: dilo una vez.
- No pongas descuentos ni precios: el conector no trae el precio al que se puede liquidar.
- Si además piden otro archivo distinto de este (Word, Excel, PowerPoint o de Google), usa la skill
  `documentos-con-marca-dobs`: ningún archivo sale sin la marca de DObs.

## Si lo piden en Google Sheets

Quien lo pide así trabaja en Google: quiere el archivo **en su Google Drive**, no un archivo de Office para
subirlo a mano.

1. Arma el archivo de Excel con el mismo programa, sin cambiar nada: es la única forma de que lleve la marca.
2. **Súbelo tú a su Google Drive** con el conector de Google Drive de la conversación, pidiendo que se convierta
   a Hojas de cálculo de Google. Si no indicaron carpeta, va a la raíz de «Mi unidad».
3. Responde con **el enlace** al archivo ya en Google. No entregues además el archivo de Office, salvo que lo pidan.

Solo si no hay conector de Google Drive, o si la subida falla, entrega el archivo de Excel y dilo en una
línea: «No pude subirlo a tu Drive (di el motivo). Súbelo y ábrelo con Hojas de cálculo de Google: conserva la marca».

No crees un archivo de Google en blanco para escribir el contenido dentro: saldría sin la marca.
