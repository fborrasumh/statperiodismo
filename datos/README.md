# Datos del curso

**Todos los ficheros son simulados** con `herramientas/generar_datos.py` (semilla fija 1200, así que se regeneran idénticos). Imitan la forma de fuentes reales, pero **ninguna cifra es real**: no los cites como datos de ningún organismo.

| Fichero | Filas | Qué simula | Columnas | Cuadernos |
| :-- | --: | :-- | :-- | :-- |
| `encuesta_medios.csv` | 1.200 | Encuesta de consumo de noticias en la Comunitat Valenciana | id, edad, sexo, provincia, estudios, medio_principal, minutos_noticias_dia, confianza_medios (0-10), comparte_noticias, ha_creido_bulo, suscripcion_pago | P01, P04–P08, P12, P21, P24, P25, P28–P30 |
| `salarios_redaccion.csv` | 420 | Plantilla de medios de comunicación | id, puesto, anios_experiencia, tipo_medio, sexo, contrato, salario_bruto_anual (€) | P04, P07–P11, P26, P30 |
| `audiencias_tv.csv` | 160 | Audiencias de programas de televisión en una semana | programa, cadena, genero, franja, duracion_min, share (%), espectadores_miles | P06, P09–P11 |
| `verificaciones.csv` | 900 | Contenidos revisados por una agencia de verificación | id, plataforma, tema, formato, veredicto, veces_compartido | P11, P21, P26 |
| `municipios.csv` | 140 | Indicadores municipales | municipio, comarca, poblacion, renta_media_persona, tasa_paro, edad_media, hogares_internet_pct, lectores_prensa_pct | P13, P20 |
| `paro_mensual.csv` | 120 | Paro registrado mensual en una provincia, 2016-2025 | fecha (AAAA-MM), parados | P14, P18, P19 |
| `ipc_simulado.csv` | 132 | Índice de precios mensual por grupos, base 2021 = 100, 2015-2025 | fecha, alimentos, vivienda, transporte, ocio_cultura, resto, general | P16, P17 |
| `ipc_ponderaciones.csv` | 5 | Ponderaciones de los grupos del índice | grupo, ponderacion | P16 |
| `salario_medio.csv` | 11 | Salario medio nominal anual, 2015-2025 | anio, salario_medio_nominal (€) | P16 |
| `cesta_compra.csv` | 8 | Precios y cantidades de una cesta en 2020 y 2024 | producto, precio_2020, cantidad_2020, precio_2024, cantidad_2024 | P15 |
| `visitas_diario.csv` | 1.096 | Visitas diarias a un diario digital, 2022-2024 | fecha, visitas | P18, P19 |
| `sondeos.csv` | 36 | Sondeos semanales de intención de voto (candidaturas A y B) | fecha, empresa, tamano_muestra, pct_A, pct_B | P27 |

Las relaciones que se descubren en los cuadernos (más redes sociales entre los jóvenes, salarios asimétricos, estacionalidad del paro, más bulos en WhatsApp...) están incluidas a propósito en la simulación para que haya historias que contar.
