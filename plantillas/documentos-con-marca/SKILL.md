---
name: documentos-con-marca
description: Pone la marca de {{EMPRESA}} (logotipo, colores, tipografías y pie) a CUALQUIER archivo que se entregue con las cifras de CortexDAI — Word, Excel, PowerPoint, Google Docs, Google Sheets o Google Slides. Úsala SIEMPRE que pidan un archivo o documento («pásalo a Word», «dame un Excel», «hazme unas láminas», «súbelo a Google Docs», «un informe para enviar») con datos del conector CortexDAI, y cuando otra skill de CortexDAI termine en un archivo. Tiene prioridad sobre las skills generales de archivos (xlsx, docx, pptx, pdf), que no ponen la marca.
---

# Documentos con la marca de {{EMPRESA}}

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras: solo pone
la marca. Los ejemplos de los programas son de formato, con valores inventados; nunca copies una cifra de ellos.

**Regla única: de una conversación con CortexDAI no sale ningún archivo sin la marca de {{EMPRESA}}.** Tú decides qué
se dice; la marca (logotipo, colores, tipografías, franja y pie) la ponen los programas de `scripts/` y no se
elige ni se ajusta a mano. No armes un Word, un Excel ni un PowerPoint con otra librería ni con otra skill.

## Qué programa usar

| Piden | Programa |
|---|---|
| Word, documento, informe, resumen, acta, **Google Docs** | `scripts/crear_documento.py` |
| Excel, hoja de cálculo, tabla para trabajar, **Google Sheets** | `scripts/crear_hoja.py` |
| PowerPoint, láminas, presentación, **Google Slides** | `scripts/crear_presentacion.py` |

## Pasos

1. **Las cifras.** Usa las que ya están en la conversación. Si falta alguna, pídela al conector de CortexDAI.
2. **El contenido.** Escríbelo en `contenido.json`, con la forma que explica el encabezado del programa elegido.
   - `aviso` dice de dónde salen las cifras y su fecha: «Cifras de CortexDAI · datos al [fecha]». Sin él, el
     programa se niega.
   - El título es la conclusión, no el tema: «[Mes] cerraría en [N] % de la meta», no «Avance del mes».
   - En Excel las cifras van como número, no como texto.
3. **El archivo.**
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/crear_documento.py contenido.json nombre.docx
   python ${CLAUDE_SKILL_DIR}/scripts/crear_hoja.py contenido.json nombre.xlsx
   python ${CLAUDE_SKILL_DIR}/scripts/crear_presentacion.py contenido.json nombre.pptx
   ```
   Si falta una librería: `pip install python-docx openpyxl pillow python-pptx`. Si el programa se niega, dice qué
   corregir: corrige el contenido y repite. No toques el programa.
4. **Entrega** el archivo tal como salió.

## Si piden Google Docs, Sheets o Slides

Arma el archivo de Office con el mismo programa y **súbelo tú a su Google Drive** con el conector de Google Drive
de la conversación, pidiendo que se convierta al formato de Google. Responde con el enlace. Solo si no hay
conector de Google Drive, entrega el archivo de Office y dilo en una línea.

## Reglas

- Toda cifra con su periodo y su comparación; el mes en curso va a medias.
- Una idea por lámina, una tabla por hoja, una conclusión por documento.
