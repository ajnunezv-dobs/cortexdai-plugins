---
name: documentos-con-marca-dobs
description: Pone la marca de DObs (logotipo, colores, tipografías y pie) a CUALQUIER archivo que se entregue a partir de una conversación con CortexDAI — Word, Excel, PowerPoint, Google Docs, Google Sheets o Google Slides — con datos de la demo Distribuidora Andina (datos ficticios). Úsala SIEMPRE que pidan un archivo o documento («pásalo a Word», «dame un Excel», «hazme unas láminas», «súbelo a Google Docs», «expórtalo», «un informe para enviar», «un reporte») y también cuando otra skill de CortexDAI termine en un archivo y no traiga su propio programa de marca. Tiene prioridad sobre las skills generales de archivos (xlsx, docx, pptx, pdf) siempre que el contenido venga del conector de CortexDAI: esas no ponen la marca. Solo para la demo Distribuidora Andina: si los datos son de Incamotors (su conector CortexDAI, sus sedes o sus marcas de autos), NO uses esta skill: usa incamotors-marca, que pone la marca de Incamotors.
---

# Documentos con la marca de DObs

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

**Cuál marca va.** Esta skill es para la demo Distribuidora Andina y para documentos propios de DObs. Si los
datos son de Incamotors (su conector CortexDAI, sus sedes o sus marcas de autos), el archivo lleva la marca
de Incamotors: usa la skill `incamotors-marca` y no esta. Nunca mezcles las dos marcas en un archivo.

**Regla única: de una conversación con la demo de CortexDAI no sale ningún archivo sin la marca de DObs.** Tú decides
qué se dice; la marca (logotipo, colores, tipografías, franja y pie) la ponen los programas de `scripts/` y no
se elige ni se ajusta a mano.

No armes un Word, un Excel ni un PowerPoint con otra librería, con otra skill (tampoco las generales `xlsx`,
`docx` o `pptx`) ni «a tu manera», aunque sea más rápido: saldría sin marca. Si lo que piden no cabe en estos programas, dilo y ofrece la forma más cercana.

## Qué programa usar

| Piden | Programa | Ejemplo de contenido |
|---|---|---|
| Word, documento, informe, resumen, acta, **Google Docs** | `scripts/crear_documento.py` | `ejemplos/documento.json` |
| Excel, hoja de cálculo, tabla para trabajar, **Google Sheets** | `scripts/crear_hoja.py` | `ejemplos/hoja.json` |
| PowerPoint, láminas, presentación, **Google Slides** | `scripts/crear_presentacion.py` | `ejemplos/presentacion.json` |

Si existe una skill de CortexDAI específica para lo que piden (`presentacion-de-comite`, `plan-de-accion-por-sede`,
`brief-de-campana`), úsala a ella: ya trae la misma marca y además sabe qué preguntar al conector.

## Pasos

1. **Las cifras.** Usa las que ya están en la conversación. Si falta alguna, pídela al conector de CortexDAI;
   no calcules lo que el conector ya entrega calculado ni completes de memoria.
2. **El contenido.** Escríbelo en `contenido.json`, con la forma que explica el encabezado del programa elegido
   (ábrelo: lo dice arriba, y hay un ejemplo completo en `ejemplos/`).
   - `aviso` es siempre «Datos ficticios · demostración de CortexDAI». Sin él, el programa se niega.
   - El título es la conclusión, no el tema: «[Mes] cerraría en [N] % de la meta», no «Avance de octubre».
   - En Excel las cifras van como número, no como texto.
3. **El archivo.** Desde la carpeta de esta skill:
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/crear_documento.py contenido.json nombre.docx
   python ${CLAUDE_SKILL_DIR}/scripts/crear_hoja.py contenido.json nombre.xlsx
   python ${CLAUDE_SKILL_DIR}/scripts/crear_presentacion.py contenido.json nombre.pptx
   ```
   Si falta una librería: `pip install python-docx openpyxl pillow python-pptx`. Si el programa se niega, dice
   qué corregir: corrige el contenido y repite. No toques el programa.
4. **Entrega** el archivo tal como salió. No lo abras para cambiarle colores, letras ni el logotipo.

## Si piden Google Docs, Sheets o Slides

Quien lo pide así trabaja en Google: quiere el archivo **en su Google Drive**, no un archivo de Office para
subirlo a mano.

1. Arma el archivo de Office (`.docx`, `.xlsx` o `.pptx`) con el mismo programa, sin cambiar nada: es la única forma de que lleve la marca.
2. **Súbelo tú a su Google Drive** con el conector de Google Drive de la conversación, pidiendo que se convierta
   a Documentos, Hojas de cálculo o Presentaciones de Google. Si no indicaron carpeta, va a la raíz de «Mi unidad».
3. Responde con **el enlace** al archivo ya en Google. No entregues además el archivo de Office, salvo que lo pidan.

Solo si no hay conector de Google Drive, o si la subida falla, entrega el archivo de Office (`.docx`, `.xlsx` o `.pptx`) y dilo en una
línea: «No pude subirlo a tu Drive (di el motivo). Súbelo y ábrelo con Documentos, Hojas de cálculo o Presentaciones de Google: conserva la marca».

No crees un archivo de Google en blanco para escribir el contenido dentro: saldría sin la marca.

Google puede reemplazar las tipografías por otras parecidas; los colores y el logotipo no cambian. Dilo solo si
preguntan.

## Reglas

- Di al inicio que son datos ficticios de la demostración de CortexDAI.
- Toda cifra con su periodo y su comparación; el mes en curso va a medias.
- Una idea por lámina, una tabla por hoja, una conclusión por documento. Si no cabe, sobran palabras.
- La marca se cambia en un solo sitio: el bloque `MARCA` de cada programa y los logotipos de `recursos/`. Para
  otra empresa se cambian esos dos y todo lo que salga de aquí sale con su marca.
