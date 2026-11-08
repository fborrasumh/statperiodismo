# Guía para el profesorado

Esta guía explica cómo está organizado el curso, cómo encaja con la guía docente de **Estadística (1200)** del Grado en Periodismo y cómo usarlo, evaluarlo y adaptarlo.

## 1. Encaje con la guía docente 2026/27

La asignatura tiene 6 ECTS (3 de teoría y 3 de práctica), 60 horas dirigidas en 15 semanas. Los 30 cuadernos cubren las **30 horas de teoría**, uno por hora, y siguen las cinco unidades didácticas de la guía.

| Unidad de la guía | Cuadernos |
| :-- | :-- |
| 1. Introducción | P01–P04 |
| 2. Estadística descriptiva | P05–P13 |
| 3. Números índice y series cronológicas | P14–P19 |
| 4. Probabilidad | P20–P24 |
| 5. Conceptos básicos de inferencia estadística | P25–P30 |

| Resultado de aprendizaje de la guía | Cuadernos |
| :-- | :-- |
| Describir bancos de datos categóricos y numéricos con descriptores numéricos y gráficos | P04–P11 |
| Describir relaciones entre diferentes tipos de datos | P12, P13 |
| Conocer y aplicar los números índice sobre aplicaciones reales | P14–P17 |
| Identificar y describir los elementos básicos de las series cronológicas | P18, P19 |
| Identificar el azar y los elementos probabilísticos básicos | P20 |
| Aplicar la dependencia e independencia probabilística | P21, P22 |
| Identificar las distribuciones notables y calcular probabilidades | P23, P24 |
| Conocer población, parámetros, censos, muestras, variables y estimadores | P25, P26 |
| Conocer y aplicar los tipos básicos de muestreo | P25 |
| Resolver problemas sencillos de estimación | P26–P28 |
| Resolver contrastes sencillos y calcular el tamaño de muestra | P28–P30 |

La guía incluye «análisis de encuestas»: se trabaja de forma transversal en P05, P12, P25, P27, P28 y P30.

## 2. Calendario propuesto

Dos cuadernos por semana (las dos horas de teoría semanales).

| Semana | Cuadernos | Semana | Cuadernos |
| :-: | :-- | :-: | :-- |
| 1 | P01, P02 | 9 | P17, P18 |
| 2 | P03, P04 | 10 | P19, P20 |
| 3 | P05, P06 | 11 | P21, P22 |
| 4 | P07, P08 | 12 | P23, P24 |
| 5 | P09, P10 | 13 | P25, P26 |
| 6 | P11, P12 | 14 | P27, P28 |
| 7 | P13, P14 | 15 | P29, P30 |
| 8 | P15, P16 | | |

## 3. Cómo usar un cuaderno en clase

1. **Antes de clase**: el estudiantado abre el cuaderno desde el README (botón *Open in Colab*) y ejecuta la celda de configuración.
2. **En clase**: el profesor ejecuta las secciones en directo y comenta los bloques *Qué vamos a hacer*, *Qué ha pasado* y *Cómo leerlo*. Las **autoevaluaciones** sirven como preguntas rápidas al grupo (se responden en el propio cuaderno, sin plataforma externa).
3. **Después de clase**: el **reto aprendiz** es trabajo autónomo. Las soluciones están plegadas; si se quieren usar como entregable, elimina los bloques `<details>` en tu copia (o en `herramientas/contenido/`).
4. **Prácticas (3 ECTS)**: los retos, los ejercicios abiertos (buscar gráficos engañosos, fichas técnicas, noticias con «un estudio demuestra») y el trabajo final de P30 dan material para las sesiones prácticas.

Requisitos: una cuenta de Google (Colab es gratuito) y un navegador. También funcionan en Jupyter local.

## 4. Evaluación

La guía fija un trabajo práctico (45 %), un examen teórico (50 %) y asistencia y tutorías (5 %). El cuaderno P30 termina con el **trabajo final** en el formato de la guía: «presentación de un estadístico que describa comparaciones a través de una muestra». Rúbrica sugerida, con los tres criterios de la guía:

| Criterio | Qué se valora |
| :-- | :-- |
| Claridad periodística | Titular y texto correctos, comprensibles, sin exagerar; gráfico honesto con título, unidad, fuente y n |
| Contenido estadístico riguroso y completo | Medida adecuada (media/mediana, puntos/%), base del porcentaje, margen de error o intervalo, grupos comparables |
| Creatividad en las decisiones | Elección de la pregunta, del estadístico y de los parámetros; uso de la lista de comprobación de P30 |

## 5. Del software actual a Python

La guía 2026/27 lista Microsoft Office y UMH Statistics. Equivalencias rápidas:

| Tarea | Excel / UMH Statistics | Python (Pandas) | Cuaderno |
| :-- | :-- | :-- | :-: |
| Abrir datos | Abrir el fichero | `pd.read_csv("f.csv")` | P04 |
| Tabla de frecuencias | Tabla dinámica / Frecuencias | `df["v"].value_counts(normalize=True)` | P05 |
| Tabla de contingencia | Tabla dinámica con filas y columnas | `pd.crosstab(df["a"], df["b"], normalize="index")` | P12 |
| Media, mediana, cuartiles | `PROMEDIO`, `MEDIANA`, `CUARTIL` | `mean()`, `median()`, `quantile()` | P08–P09 |
| Desviación típica | `DESVEST.M` | `std()` | P10 |
| Correlación y recta | `COEF.DE.CORREL`, línea de tendencia | `corr()`, `np.polyfit(x, y, 1)` | P13 |
| Tasa interanual | Fórmula celda a celda | `pct_change(12)` | P14 |
| Media móvil | Fórmula arrastrada | `rolling(12, center=True).mean()` | P19 |
| Binomial, normal | `DISTR.BINOM.N`, `DISTR.NORM.N` | `stats.binom`, `stats.norm` | P23–P24 |
| Intervalo y contraste | Asistentes de UMH Statistics | `stats.t.interval`, `stats.binomtest`, `stats.ttest_ind` | P27–P30 |

## 6. Usar datos reales

Los 11 conjuntos de datos son simulados (ver [datos/README.md](datos/README.md)) para que las cifras y las conclusiones sean estables año tras año. Para trabajar con datos reales basta con sustituir un CSV manteniendo los nombres de columna, o leer la fuente directamente en el cuaderno. Fuentes naturales para cada bloque:

| Bloque | Fuente real |
| :-- | :-- |
| Encuestas de opinión y de consumo de medios | Barómetros y microdatos del CIS |
| IPC, salarios, población | INE (INEbase) |
| Paro registrado | Ministerio de Trabajo / SEPE |
| Datos municipales | INE (padrón, Atlas de distribución de renta de los hogares) |
| Datos abiertos en general | datos.gob.es y portales autonómicos |

Si cambias los datos, revisa los párrafos *Cómo leerlo*: describen los resultados de los datos simulados.

## 7. Mantenimiento

Todo el contenido está en `herramientas/contenido/u1.py` … `u5.py`. Tras cualquier cambio:

```bash
python herramientas/construir.py   # regenera cuadernos y preguntas
python herramientas/probar.py      # ejecuta los 30 cuadernos y las soluciones
python herramientas/indice.py      # actualiza el README
```
