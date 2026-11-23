---
name: brief-de-campana
description: Escribe el brief de una campaña de marketing en una página — qué línea empujar, en qué sedes, con qué productos, contra qué competidor y cómo se medirá — y lo entrega como documento de Word ya con la marca de DObs (logotipo, colores y tipografías), con los datos de CortexDAI (demo Distribuidora Andina, datos ficticios). Úsala cuando pidan «un brief», «una campaña para Snacks», «¿qué promociono este mes?», «¿cómo respondo a la competencia?» o un encargo para la agencia. También cuando lo pidan en Google Docs: se arma el mismo archivo con marca y se abre en Google.
---

# Brief de campaña

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

Marketing suele recibir el encargo sin las cifras. Este brief las pone primero: la campaña sale de dónde se
pierde venta y de qué producto sobra, no de una idea.

## Pasos

Con la línea que pidan (si no dicen cuál, usa la de peor variación contra el año anterior en `ventas` con
`agrupar_por = "linea"`):

1. `ventas` con `agrupar_por = "sede"` y `lineas = [línea]` — dónde cae y cuánto margen deja en cada sede.
2. `ventas` con `agrupar_por = "linea"` — su margen frente a las otras líneas: cuánto espacio hay para una oferta.
3. `como_vamos_este_mes` con `lineas = [línea]` — meta y cierre proyectado del mes, por sede y en el `total`.
4. `stock_por_antiguedad` con `lineas = [línea]` — en qué sedes sobra producto y en cuáles apenas alcanza.
5. `que_pedir` con `lineas = [línea]` — los productos concretos por liquidar o sin venta.
6. `competencia` con `lineas = [línea]` y `objetivos` con `area = "Marketing"` — a qué precio anuncia el competidor y qué objetivo de
   participación está en riesgo.

## El documento (una página, Word, con la marca de DObs)

**No armes el Word a mano ni con otra librería.** La marca (franja con el logotipo, colores, tipografías y pie) la
pone el programa `scripts/crear_brief.py`; tú solo escribes el contenido.

1. Escribe el contenido en `contenido.json`, con la forma que explica el encabezado de `scripts/crear_brief.py`
   (hay un ejemplo completo en `ejemplo.json`). El `aviso` es siempre «Datos ficticios · demostración de CortexDAI».
2. Ejecuta, desde la carpeta de esta skill:
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/crear_brief.py contenido.json brief-{línea}-{AAAA-MM}.docx
   ```
   Si falta la librería: `pip install python-docx`. Si el programa se niega, dice qué sobra: acorta y repite.
3. Entrega ese archivo. No lo abras para cambiarle colores, letras ni el logotipo.

Las seis secciones, en este orden:

1. **Por qué ahora.** Dos frases con cifra, periodo y comparación: cuánto cae la línea, en qué sedes, y qué
   anuncia la competencia.
2. **Dónde.** Las dos o tres sedes de la campaña, cada una con su cifra. Sede con producto de sobra y venta que
   cae = campaña. Sede con un mes o menos de inventario = no se promociona: se quedaría sin producto.
3. **Qué productos.** Hasta cinco, con sus cajas en almacén y sus días de cobertura.
4. **Qué se puede ofrecer.** El margen de la línea en esas sedes, y cuánto quedaría si se igualara el precio de
   la competencia. Si el margen no alcanza, dilo: la respuesta no es precio.
5. **Cómo sabremos si funcionó.** Una sola medida, con su punto de partida y su fecha: «[línea] en [sede]: de
   [cajas proyectadas este mes] a [lo esperado a la fecha] al cierre del mes siguiente».
6. **Lo que no sabemos.** Lo que el brief necesita y los datos no traen (precio de lista del competidor por
   producto, presupuesto, canales). Va siempre, aunque sea una línea.

## Reglas

- Di al inicio que son datos ficticios de la demostración de CortexDAI. El competidor de la demo también es
  inventado.
- No escribas el anuncio ni el lema: el brief es el encargo, no la pieza.
- No inventes presupuesto, canales ni audiencias: van en «Lo que no sabemos».
- El margen existe por sede y línea, no por producto: no lo repartas entre productos.
- Una página. Si no cabe, sobran palabras, no faltan hojas.
- Si además piden otro archivo distinto de este (Word, Excel, PowerPoint o de Google), usa la skill
  `documentos-con-marca-dobs`: ningún archivo sale sin la marca de DObs.

## Si lo piden en Google Docs

Quien lo pide así trabaja en Google: quiere el archivo **en su Google Drive**, no un archivo de Office para
subirlo a mano.

1. Arma el archivo de Word con el mismo programa, sin cambiar nada: es la única forma de que lleve la marca.
2. **Súbelo tú a su Google Drive** con el conector de Google Drive de la conversación, pidiendo que se convierta
   a Documentos de Google. Si no indicaron carpeta, va a la raíz de «Mi unidad».
3. Responde con **el enlace** al archivo ya en Google. No entregues además el archivo de Office, salvo que lo pidan.

Solo si no hay conector de Google Drive, o si la subida falla, entrega el archivo de Word y dilo en una
línea: «No pude subirlo a tu Drive (di el motivo). Súbelo y ábrelo con Documentos de Google: conserva la marca».

No crees un archivo de Google en blanco para escribir el contenido dentro: saldría sin la marca.
