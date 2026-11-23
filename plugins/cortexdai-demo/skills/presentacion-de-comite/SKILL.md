---
name: presentacion-de-comite
description: Solo para la demo de CortexDAI con Distribuidora Andina, con su conector activo. Arma la presentación del comité en PowerPoint, ya con la marca de DObs (colores, logotipo, tipografías y pie en cada lámina), a partir de los datos de CortexDAI (demo Distribuidora Andina, datos ficticios). Úsala cuando pidan «la presentación para el comité», «pásalo a láminas», «un PowerPoint con esto», «la presentación del lunes» o quieran llevar a una reunión lo que se acaba de analizar. También cuando lo pidan en Google Slides: se arma el mismo archivo con marca y se abre en Google. Solo para la demo Distribuidora Andina: si los datos son de Incamotors (su conector CortexDAI, sus sedes o sus marcas de autos), NO uses esta skill: usa incamotors-marca, que pone la marca de Incamotors.
---

# Presentación de comité con la marca de DObs

**Solo con el conector de la demo.** Usa esta skill únicamente si en esta conversación está activo el conector de la demo de Distribuidora Andina (sus herramientas incluyen `que_pedir`, `objetivos` y `competencia`). Si el conector activo es el de una empresa real, no la uses: para eso están los plugins CortexDAI · Comercial e Inventario.

**Las cifras salen siempre del conector de CortexDAI, en esta conversación.** Esta skill no trae cifras de la empresa: los ejemplos son solo de formato, con sedes, líneas y valores inventados («Sede A», «Línea 1»). Nunca copies una cifra, una sede ni un producto de un ejemplo.

Entrega un archivo `.pptx` de seis a ocho láminas listo para proyectar. Tú decides **qué se dice**; la marca
(colores, logotipo, tipografías, dónde va cada cosa) la pone el programa `scripts/crear_presentacion.py` y no
se discute ni se ajusta a mano.

## Pasos

1. **Las cifras.** Si en la conversación ya están las cifras del tema (porque se acaba de analizar), úsalas tal
   cual. Si no, pídelas al conector de CortexDAI: `estado_de_los_datos`, `como_vamos_este_mes`,
   `objetivos` con `solo_en_riesgo = true`, `stock_por_antiguedad` y, si el tema es una sede o una línea, las
   mismas herramientas con ese filtro. No calcules lo que el conector ya entrega calculado.
2. **El guion.** Escribe el contenido en un archivo `contenido.json` con la forma que explica el encabezado de
   `scripts/crear_presentacion.py` (hay un ejemplo completo en `ejemplo.json`). Orden recomendado:
   1. portada — el título es la conclusión, no el tema («[Mes] cerraría en [N] % de la meta», no «Avance de octubre»);
   2. `cifras` — las tres o cuatro cifras que sostienen la conclusión; una sola `destacada`;
   3. `tabla` — el detalle por sede o por línea, con su estado;
   4. `vinetas` — por qué pasa, solo con lo que los datos muestran;
   5. `frase` — la única idea que el comité debe recordar (una por presentación, no más);
   6. `cierre` — dos o tres decisiones, cada una con sede, producto o responsable y su cifra.
3. **El archivo.** Ejecuta:
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/crear_presentacion.py contenido.json comite-AAAA-MM-DD.pptx
   ```
   Si falta la librería: `pip install python-pptx`. Si el programa se niega, dice qué lámina no cabe: acorta o
   parte esa lámina y vuelve a ejecutar. No edites el programa para que acepte más texto.
4. **La entrega.** Da el archivo y, en tres líneas, qué dice cada lámina. Nada más.

## Reglas del contenido

- `aviso` es obligatorio y va en el pie de todas las láminas. En la demo: «Datos ficticios · demostración de
  CortexDAI». Nunca lo quites ni lo acortes.
- **Cifra + periodo + comparación**, siempre juntos: «[N] cajas al cierre de [mes], contra una meta de
  [M]». El periodo va en el rótulo o en la `nota` de la lámina.
- Octubre va a medias: se compara contra lo esperado a la fecha y con el cierre proyectado, nunca contra la
  meta entera sin decirlo.
- Las metas, los tramos de días y las reglas de pedido son «propuesta de DObs, por confirmar»: dilo en la `nota`
  de la lámina donde aparezcan.
- Estados de las tablas: `verde` (en ritmo o cumple), `ambar` (en riesgo), `rojo` (atrasada o no cumple),
  `sin_dato`. Vacío no es cero: una celda sin dato lleva `{"estado": "sin_dato", "texto": "Sin dato"}`.
- Títulos de menos de 90 caracteres. Topes por lámina: 4 cifras, 5 viñetas, 8 filas, 6 columnas.
- No inventes causas. Si los datos no explican por qué cae algo, la viñeta dice qué dato faltaría.
- Palabras que no van: insights, KPIs, data-driven, «la data».

## La marca

Está en el bloque `MARCA` del programa y en `recursos/`: marino `#071832`, pistacho `#B3CC5C` y blanco; el
logotipo de DObs y la firma «CortexDAI» en el pie; el pistacho nunca como texto sobre blanco. Para la
presentación de otra empresa se cambian ese bloque y los logotipos: el contenido y las reglas son los mismos.
- Si además piden otro archivo distinto de este (Word, Excel, PowerPoint o de Google), usa la skill
  `documentos-con-marca-dobs`: ningún archivo sale sin la marca de DObs.

## Si lo piden en Google Slides

Quien lo pide así trabaja en Google: quiere el archivo **en su Google Drive**, no un archivo de Office para
subirlo a mano.

1. Arma el archivo de PowerPoint con el mismo programa, sin cambiar nada: es la única forma de que lleve la marca.
2. **Súbelo tú a su Google Drive** con el conector de Google Drive de la conversación, pidiendo que se convierta
   a Presentaciones de Google. Si no indicaron carpeta, va a la raíz de «Mi unidad».
3. Responde con **el enlace** al archivo ya en Google. No entregues además el archivo de Office, salvo que lo pidan.

Solo si no hay conector de Google Drive, o si la subida falla, entrega el archivo de PowerPoint y dilo en una
línea: «No pude subirlo a tu Drive (di el motivo). Súbelo y ábrelo con Presentaciones de Google: conserva la marca».

No crees un archivo de Google en blanco para escribir el contenido dentro: saldría sin la marca.
