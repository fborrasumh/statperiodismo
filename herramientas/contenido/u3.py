from _comun import C, M, numerica, unica, varias

U = "3. Números índice y series cronológicas"

CUADERNOS = [
# ---------------------------------------------------------------------------
dict(
    num=14, slug="P14_tasas_de_variacion_e_indices_simples", unidad=U,
    titulo="Tasas de variación e índices simples",
    datos=["paro_mensual.csv"],
    intro="""«El paro baja un 2 %», «la factura de la luz sube un 30 %», «el IPC se modera». Las tasas de variación y los números índice son el idioma de la información económica. Mal usados, producen los errores más repetidos de la prensa: confundir puntos con porcentajes, o celebrar una subida que solo es un **efecto base**.

**Qué necesitas saber antes**: los cuadernos 2 y 4.""",
    aprender=["Calcular tasas de variación entre dos periodos y diferenciar puntos de porcentajes.",
              "Construir un índice simple con base 100.",
              "Calcular la tasa media anual acumulativa.",
              "Reconocer el efecto base."],
    secciones=[
        dict(titulo="Tasas de variación", celdas=[
            C('paro = pd.read_csv("paro_mensual.csv")\nparo.tail()'),
            M("""La **tasa de variación** entre un periodo inicial (0) y uno final (t) es:

$$TV = \\frac{x_t - x_0}{x_0} \\times 100$$

Con Pandas, `pct_change()` la calcula respecto a la fila anterior, y `pct_change(12)` respecto a 12 filas antes (el mismo mes del año anterior: **tasa interanual**)."""),
            C("""paro["tasa_mensual"] = (paro["parados"].pct_change() * 100).round(2)
paro["tasa_interanual"] = (paro["parados"].pct_change(12) * 100).round(2)
paro.tail(6)"""),
            M("**Cómo leerlo**: la tasa mensual compara con el mes anterior (y se ve muy afectada por la temporada); la interanual compara con el mismo mes del año anterior y es la que se usa para hablar de **tendencia**."),
        ], quiz=[
            numerica("El paro pasa de 150.000 a 144.000 personas. ¿Cuál es la tasa de variación en %?", -4.01, -3.99, ok="¡Correcto! (144.000 − 150.000) / 150.000 × 100 = −4 %."),
        ]),
        dict(titulo="Puntos frente a porcentaje", celdas=[
            M("""Cuando la variable **ya es un porcentaje** (tasa de paro, cuota de pantalla, intención de voto), hay dos formas de medir el cambio:

- **Diferencia en puntos porcentuales**: 12 % → 15 % son **3 puntos**.
- **Tasa de variación**: (15 − 12) / 12 = **25 %**.

Las dos son correctas, pero no intercambiables. «La tasa de paro sube un 3 %» cuando ha pasado del 12 % al 15 % es un error."""),
            C("""antes, despues = 12.0, 15.0
print("Diferencia:", despues - antes, "puntos")
print("Tasa de variación:", round((despues - antes) / antes * 100, 1), "%")"""),
        ], quiz=[
            unica("La intención de voto de un partido pasa del 10 % al 12 %. ¿Qué frase es correcta?", "«Sube dos puntos»",
                  [("«Sube un 2 %»", "Sube 2 puntos, que es un 20 % más."), ("«Sube un 12 %»", "12 % es el valor final, no el cambio.")]),
        ]),
        dict(titulo="Índices simples", celdas=[
            M("""Un **índice simple** compara cada valor con el de un periodo de referencia (**periodo base**), al que se da el valor 100:

$$I_t = \\frac{x_t}{x_{base}} \\times 100$$

Un índice de 108 significa un 8 % más que en la base; uno de 95, un 5 % menos. Permite comparar series de tamaños muy distintos en la misma escala."""),
            C("""paro["anio"] = paro["fecha"].str[:4].astype(int)
anual = paro.groupby("anio")["parados"].mean().round()
indice = (anual / anual.loc[2016] * 100).round(1)
pd.DataFrame({"parados (media anual)": anual, "índice 2016 = 100": indice})"""),
            C("""indice.plot(marker="o", color="steelblue")
plt.axhline(100, color="grey", lw=0.8)
plt.title("Paro registrado, índice 2016 = 100 (datos simulados)")
plt.ylabel("Índice")
plt.show()"""),
        ], quiz=[
            unica("Un índice de precios vale 112 (base 2020 = 100). ¿Qué significa?", "Los precios son un 12 % más altos que en 2020",
                  [("Los precios han subido 112 €", "Un índice no tiene unidades monetarias."), ("La inflación de este año es del 12 %", "Es el aumento acumulado desde 2020, no el de un año.")]),
        ]),
        dict(titulo="Tasa media anual y efecto base", celdas=[
            M("""Para resumir el crecimiento de varios años no se promedian las tasas: se usa la **tasa media anual acumulativa**:

$$TMA = \\left(\\frac{x_{final}}{x_{inicial}}\\right)^{1/n} - 1$$

donde $n$ es el número de años transcurridos."""),
            C("""ini, fin = anual.loc[2016], anual.loc[2025]
n = 2025 - 2016
tma = ((fin / ini) ** (1 / n) - 1) * 100
print(f"Tasa media anual 2016-2025: {tma:.2f} %")"""),
            M("""El **efecto base** aparece cuando el periodo de comparación fue excepcional. Si el paro se disparó en 2020, la tasa interanual de 2021 parecerá una gran mejora aunque solo se vuelva a la normalidad. Antes de titular «récord», mira **contra qué** se compara."""),
            C("""ventana = paro[(paro["fecha"] >= "2020-01") & (paro["fecha"] <= "2022-06")]
plt.plot(ventana["fecha"], ventana["tasa_interanual"], marker=".")
plt.axhline(0, color="grey", lw=0.8)
plt.xticks(ventana["fecha"][::3], rotation=45)
plt.title("Tasa interanual del paro: el salto de 2020 y su efecto base en 2021")
plt.ylabel("%")
plt.show()"""),
        ], quiz=[
            unica("Un indicador cayó mucho en 2020 y en 2021 vuelve a su nivel de 2019. ¿Qué mostrará la tasa interanual de 2021?",
                  "Una subida grande, por efecto base",
                  [("Ningún cambio", "Compara con 2020, que fue anormalmente bajo."), ("Una bajada", "Al volver al nivel normal, sube respecto a 2020.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="¿Cuál fue el mes con la mayor caída mensual del paro en toda la serie?",
             solucion='paro.loc[paro["tasa_mensual"].idxmin(), ["fecha", "tasa_mensual"]]'),
        dict(seccion="sección 2", enunciado="La cuota de pantalla de un informativo pasa del 14,5 % al 11,6 %. Escribe la frase correcta en puntos y en porcentaje.",
             solucion='''print(11.6 - 14.5, "puntos")
print(round((11.6 - 14.5) / 14.5 * 100, 1), "%")''', comentario="Baja 2,9 puntos, es decir, un 20 %."),
        dict(seccion="sección 3", enunciado="Construye el índice de paro con base 2019 = 100 y di cuánto ha cambiado el paro entre 2019 y 2025.",
             solucion='(anual / anual.loc[2019] * 100).round(1)'),
        dict(seccion="sección 4", enunciado="Un diario digital pasó de 2,1 millones de usuarios únicos en 2020 a 3,4 millones en 2024. Calcula la tasa media anual acumulativa.",
             solucion='((3.4 / 2.1) ** (1 / 4) - 1) * 100', comentario="Algo menos del 13 % anual. Promediar las tasas de cada año daría otro resultado."),
    ],
    resumen=["**Tasa de variación** = (final − inicial) / inicial × 100; `pct_change()` la calcula en Pandas.",
             "La **tasa interanual** (`pct_change(12)` en datos mensuales) elimina el efecto de la temporada.",
             "Si la variable ya es un %, distingue **puntos** de **porcentaje de variación**.",
             "Un **índice simple** divide cada valor por el del periodo base y multiplica por 100.",
             "Resume varios años con la **tasa media anual acumulativa** y vigila el **efecto base**."],
    glosario=[("Tasa de variación", "Cambio relativo entre dos periodos."), ("Tasa interanual", "Tasa respecto al mismo periodo del año anterior."),
              ("Punto porcentual", "Diferencia entre dos porcentajes."), ("Índice simple", "Valor relativo a un periodo base que vale 100."),
              ("Efecto base", "Distorsión de una tasa por la excepcionalidad del periodo de comparación.")],
    errores=[("La primera fila de `pct_change()` es NaN", "No hay periodo anterior", "Es lo esperado; no es un error")],
    seguir="En el cuaderno 15 construirás índices que combinan varios precios: Laspeyres y Paasche.",
),
# ---------------------------------------------------------------------------
dict(
    num=15, slug="P15_indices_compuestos", unidad=U,
    titulo="Índices compuestos: la cesta de la compra (Laspeyres y Paasche)",
    datos=["cesta_compra.csv"],
    intro="""«La cesta de la compra es un 25 % más cara que en 2020.» ¿Qué cesta? Si el aceite se triplica pero apenas se compra, ¿cuánto pesa en el total? Los **índices compuestos** combinan muchos precios en una sola cifra, ponderando cada uno según su importancia. Son la base del IPC.

**Qué necesitas saber antes**: el cuaderno 14 (índices simples) y el 8 (media ponderada).""",
    aprender=["Calcular índices simples de varios productos y su media sin ponderar.",
              "Calcular los índices de precios de Laspeyres y de Paasche.",
              "Explicar la diferencia entre ambos y por qué el IPC usa una variante de Laspeyres."],
    secciones=[
        dict(titulo="Índices de cada producto", celdas=[
            C('cesta = pd.read_csv("cesta_compra.csv")\ncesta'),
            M("La cesta (simulada) tiene precios y cantidades mensuales de un hogar en 2020 (base) y 2024. Empezamos por el índice simple de precios de cada producto:"),
            C("""cesta["indice_precio"] = (cesta["precio_2024"] / cesta["precio_2020"] * 100).round(1)
cesta[["producto", "precio_2020", "precio_2024", "indice_precio"]].sort_values("indice_precio")"""),
            M("**Cómo leerlo**: el aceite de oliva tiene un índice de 228,6 (su precio se ha multiplicado por 2,3). El pan ha subido un 15 %. La media simple de los índices daría a todos los productos el mismo peso, como si gastáramos lo mismo en café que en pollo."),
            C("""print("Media simple de los índices:", round(cesta["indice_precio"].mean(), 1))"""),
        ], quiz=[
            unica("¿Por qué no basta con la media simple de los índices de precios?", "Porque no tiene en cuenta cuánto se gasta en cada producto",
                  [("Porque los índices no se pueden promediar", "Se pueden promediar, pero ponderando."), ("Porque hay que usar la mediana", "El problema es el peso, no la medida.")]),
        ]),
        dict(titulo="Índice de Laspeyres", celdas=[
            M("""El **índice de Laspeyres** compara lo que costaría **la cesta del año base** a los precios actuales con lo que costaba en el año base:

$$L = \\frac{\\sum p_t \\, q_0}{\\sum p_0 \\, q_0} \\times 100$$

Responde a: «¿cuánto más cuesta hoy comprar lo mismo que comprábamos en 2020?»."""),
            C("""gasto_base = (cesta["precio_2020"] * cesta["cantidad_2020"]).sum()
misma_cesta_hoy = (cesta["precio_2024"] * cesta["cantidad_2020"]).sum()
laspeyres = misma_cesta_hoy / gasto_base * 100
print(f"Gasto en 2020: {gasto_base:.2f} €   Misma cesta en 2024: {misma_cesta_hoy:.2f} €")
print(f"Índice de Laspeyres: {laspeyres:.1f}")"""),
            M("""Es equivalente a una **media ponderada** de los índices simples, con pesos iguales al gasto de cada producto en el año base:"""),
            C("""pesos = cesta["precio_2020"] * cesta["cantidad_2020"]
print(round(np.average(cesta["indice_precio"], weights=pesos), 1))"""),
        ], quiz=[
            unica("¿Qué cantidades usa el índice de Laspeyres?", "Las del periodo base",
                  [("Las del periodo actual", "Esas las usa Paasche."), ("La media de ambos periodos", "No: fija la cesta del año base.")]),
        ]),
        dict(titulo="Índice de Paasche", celdas=[
            M("""El **índice de Paasche** usa la cesta **actual**:

$$P = \\frac{\\sum p_t \\, q_t}{\\sum p_0 \\, q_t} \\times 100$$

Si los hogares han reaccionado comprando menos de lo que más ha subido (menos aceite, menos periódicos de papel), Paasche dará una subida **menor** que Laspeyres."""),
            C("""paasche = (cesta["precio_2024"] * cesta["cantidad_2024"]).sum() / (cesta["precio_2020"] * cesta["cantidad_2024"]).sum() * 100
fisher = np.sqrt(laspeyres * paasche)
print(f"Laspeyres: {laspeyres:.1f}   Paasche: {paasche:.1f}   Fisher (media geométrica): {fisher:.1f}")"""),
            M("""**Por qué el IPC usa Laspeyres (encadenado)**: solo necesita conocer las cantidades del periodo base, que se obtienen de una encuesta de gasto cara y lenta; los precios sí se recogen cada mes. Para que la cesta no se quede vieja, el INE actualiza las ponderaciones cada año (**Laspeyres encadenado**)."""),
        ], quiz=[
            unica("Si los hogares sustituyen los productos que más suben por otros, ¿qué suele ocurrir?", "Paasche da una subida menor que Laspeyres",
                  [("Laspeyres da una subida menor", "Laspeyres mantiene la cesta antigua, con más peso de lo que subió."), ("Dan siempre lo mismo", "Solo si las cantidades no cambian.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="¿Qué producto ha subido más y cuál menos? Represéntalo en un gráfico de barras horizontales de los índices.",
             solucion='''cesta.set_index("producto")["indice_precio"].sort_values().plot(kind="barh")
plt.axvline(100, color="grey")
plt.show()'''),
        dict(seccion="sección 2", enunciado="Calcula qué parte del gasto de 2020 suponía cada producto (su peso en el Laspeyres).",
             solucion='(pesos / pesos.sum() * 100).round(1)'),
        dict(seccion="sección 2", enunciado="Recalcula el Laspeyres quitando el periódico de la cesta. ¿Cambia mucho?",
             solucion='''c = cesta[cesta["producto"] != "Periódico (ud.)"]
(c["precio_2024"] * c["cantidad_2020"]).sum() / (c["precio_2020"] * c["cantidad_2020"]).sum() * 100'''),
        dict(seccion="sección 3", enunciado="Escribe un titular con el Laspeyres y otro con el Paasche. ¿Cuál describe mejor «lo que nota el bolsillo»?",
             comentario="Laspeyres responde a «comprar lo mismo que antes cuesta X % más»; Paasche refleja la cesta que se compra ahora. Para el bolsillo, Laspeyres es lo que más se usa, pero exagera algo si la gente ha cambiado de productos."),
    ],
    resumen=["Un **índice compuesto** combina varios precios ponderando cada uno por su importancia.",
             "**Laspeyres** usa las cantidades del **año base**: ¿cuánto cuesta hoy la cesta de antes?",
             "**Paasche** usa las cantidades **actuales**; con efecto sustitución da subidas menores.",
             "Laspeyres equivale a una media de índices simples ponderada por el **gasto en el año base**.",
             "El **IPC** es un Laspeyres encadenado con ponderaciones que se actualizan cada año."],
    glosario=[("Índice compuesto", "Índice que resume la evolución de varios precios o cantidades."), ("Laspeyres", "Índice ponderado con las cantidades del periodo base."),
              ("Paasche", "Índice ponderado con las cantidades del periodo actual."), ("Efecto sustitución", "Cambio de las compras hacia productos que suben menos.")],
    seguir="En el cuaderno 16 trabajarás con un IPC (simulado): inflación, tasas interanuales y euros reales.",
),
# ---------------------------------------------------------------------------
dict(
    num=16, slug="P16_ipc_y_terminos_reales", unidad=U,
    titulo="El IPC: inflación, tasas interanuales y euros reales",
    datos=["ipc_simulado.csv", "ipc_ponderaciones.csv", "salario_medio.csv"],
    intro="""«Los salarios suben un 4 %»: buena noticia... salvo que los precios hayan subido un 6 %. Para saber si alguien gana o pierde poder de compra hay que **deflactar**: pasar de euros corrientes a **euros constantes**. Es una de las operaciones más útiles (y menos hechas) en información económica.

**Qué necesitas saber antes**: los cuadernos 14 y 15.""",
    aprender=["Leer una serie del IPC y calcular la inflación interanual y la media anual.",
              "Entender el IPC general como media ponderada de sus grupos.",
              "Deflactar una serie: pasar de euros corrientes a euros constantes.",
              "Calcular la variación del poder adquisitivo."],
    secciones=[
        dict(titulo="La serie del IPC", celdas=[
            C('ipc = pd.read_csv("ipc_simulado.csv")\nipc["fecha"] = pd.to_datetime(ipc["fecha"])\nipc = ipc.set_index("fecha")\nipc.tail()'),
            M("""Es un IPC **simulado**, con base 2021 = 100 (como el IPC real del INE). La **inflación** que se publica cada mes es la **tasa interanual** del índice general."""),
            C("""ipc["inflacion"] = ipc["general"].pct_change(12) * 100
ipc["inflacion"].plot(color="firebrick")
plt.axhline(0, color="grey", lw=0.8)
plt.title("Inflación interanual (IPC simulado)")
plt.ylabel("%")
plt.show()"""),
            M("""También se publica la **inflación media anual**: la tasa entre la media del índice de un año y la del anterior. Con datos mensuales, `resample("YE")` agrupa por año."""),
            C("""media_anual = ipc["general"].resample("YE").mean()
media_anual.index = media_anual.index.year
(media_anual.pct_change() * 100).round(1)"""),
        ], quiz=[
            unica("¿Qué es la «inflación» que se publica cada mes?", "La tasa de variación interanual del IPC general",
                  [("El valor del índice", "El índice es el nivel; la inflación es su variación."), ("La tasa respecto al mes anterior", "Esa es la tasa mensual, muy afectada por la temporada.")]),
        ]),
        dict(titulo="El IPC general como media ponderada", celdas=[
            C('pond = pd.read_csv("ipc_ponderaciones.csv")\npond'),
            M("El índice general es (aproximadamente) la media de los índices de cada grupo, ponderada por el peso de ese grupo en el gasto de los hogares:"),
            C("""grupos = pond["grupo"].tolist()
reconstruido = (ipc[grupos] * pond.set_index("grupo")["ponderacion"]).sum(axis=1)
pd.DataFrame({"general": ipc["general"], "reconstruido": reconstruido.round(3)}).tail(3)"""),
            M("Coinciden porque así se generó el índice simulado. En el IPC real coinciden de forma aproximada, porque el INE encadena las ponderaciones de cada año. Comparemos cómo ha subido cada grupo:"),
            C("""(ipc[grupos].iloc[-1] - 100).sort_values().plot(kind="barh", color="steelblue")
plt.xlabel("Variación desde la media de 2021 (%)")
plt.title("¿Qué ha subido más desde 2021? (IPC simulado)")
plt.show()"""),
        ], quiz=[
            unica("Si la vivienda pesa el 13 % del IPC y su índice sube un 10 %, ¿cuánto aporta aproximadamente al IPC general?", "Alrededor de 1,3 puntos",
                  [("10 puntos", "Hay que multiplicar por su peso."), ("13 puntos", "13 % es el peso, no la subida.")]),
        ]),
        dict(titulo="Deflactar: euros corrientes y euros constantes", celdas=[
            M("""Para comparar euros de años distintos hay que quitar el efecto de los precios. Si el IPC es $I_t$ (base 100), el **valor real** en euros del año base es:

$$\\text{valor real}_t = \\frac{\\text{valor nominal}_t}{I_t} \\times 100$$"""),
            C("""sal = pd.read_csv("salario_medio.csv").set_index("anio")
sal["ipc_medio"] = media_anual.round(2)
sal["salario_real_2021"] = (sal["salario_medio_nominal"] / sal["ipc_medio"] * 100).round(0)
sal"""),
            C("""sal[["salario_medio_nominal", "salario_real_2021"]].plot(marker="o")
plt.title("Salario medio nominal y real, en euros de 2021 (datos simulados)")
plt.ylabel("€")
plt.show()"""),
            M("""**Cómo leerlo**: el salario nominal sube todos los años. El real, no: entre 2020 y 2023 los precios subieron más que los sueldos y el poder de compra **cayó**, aunque la nómina fuera mayor."""),
        ], quiz=[
            numerica("Un salario de 30.000 € con un IPC de 120 (base 2021 = 100), ¿a cuántos euros de 2021 equivale?", 24999, 25001, ok="¡Correcto! 30.000 / 120 × 100 = 25.000 €."),
        ]),
        dict(titulo="Poder adquisitivo", celdas=[
            M("""La variación del **poder adquisitivo** es la tasa de variación del salario real. Una aproximación rápida, útil para tasas pequeñas, es: variación del salario − inflación."""),
            C("""sal["var_nominal"] = (sal["salario_medio_nominal"].pct_change() * 100).round(1)
sal["inflacion_media"] = (sal["ipc_medio"].pct_change() * 100).round(1)
sal["var_real"] = (sal["salario_real_2021"].pct_change() * 100).round(1)
sal[["var_nominal", "inflacion_media", "var_real"]]"""),
            M("Un titular honesto con estos datos sería del tipo: «Los salarios suben un X %, pero pierden poder de compra por tercer año» (ajústalo a lo que digan las cifras)."),
        ], quiz=[
            unica("Los salarios suben un 3 % y la inflación es del 5 %. ¿Qué pasa con el poder adquisitivo?", "Baja, aproximadamente un 2 %",
                  [("Sube un 3 %", "Esa es la subida nominal."), ("Sube un 8 %", "Hay que restar, no sumar, la inflación.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="¿En qué mes se alcanzó la inflación interanual más alta de la serie y cuánto fue?",
             solucion='ipc["inflacion"].idxmax(), round(ipc["inflacion"].max(), 1)'),
        dict(seccion="sección 2", enunciado="Calcula la tasa interanual del grupo «vivienda» y compárala en un gráfico con la del índice general.",
             solucion='''(ipc[["general", "vivienda"]].pct_change(12) * 100).plot()
plt.ylabel("%")
plt.show()'''),
        dict(seccion="sección 3", enunciado="Expresa el salario real en euros de 2015 en lugar de euros de 2021.",
             solucion='(sal["salario_medio_nominal"] / sal["ipc_medio"] * sal.loc[2015, "ipc_medio"]).round(0)'),
        dict(seccion="sección 4", enunciado="¿Entre 2015 y 2025 el salario real acumulado subió o bajó? ¿Cuánto?",
             solucion='round((sal.loc[2025, "salario_real_2021"] / sal.loc[2015, "salario_real_2021"] - 1) * 100, 1)'),
    ],
    resumen=["La **inflación** que se publica es la **tasa interanual** del IPC general; la **media anual** compara medias de años.",
             "El IPC general es una **media ponderada** de los índices de sus grupos.",
             "**Deflactar**: valor real = valor nominal / IPC × 100 (en euros del año base).",
             "El **poder adquisitivo** cambia según la variación del salario real ≈ subida salarial − inflación.",
             "Una subida en euros corrientes puede ser una **pérdida** en euros constantes."],
    glosario=[("IPC", "Índice de Precios de Consumo: mide la evolución de los precios que pagan los hogares."),
              ("Inflación", "Aumento generalizado de los precios; se mide con la tasa interanual del IPC."),
              ("Deflactar", "Eliminar el efecto de los precios para expresar valores en euros constantes."),
              ("Euros corrientes", "Euros de cada año, sin corregir."), ("Euros constantes", "Euros de un año de referencia.")],
    errores=[("`resample` da error", "El índice no es de fechas", "Convierte con `pd.to_datetime` y usa `set_index`")],
    seguir="En el cuaderno 17 aprenderás a cambiar la base de un índice y a enlazar series.",
),
# ---------------------------------------------------------------------------
dict(
    num=17, slug="P17_cambio_de_base_y_enlace", unidad=U,
    titulo="Cambio de base y enlace de series",
    datos=["ipc_simulado.csv"],
    intro="""Cada cierto tiempo los institutos de estadística **cambian la base** de sus índices y las series antiguas dejan de enlazar con las nuevas. Si quieres contar cómo han evolucionado los precios desde 2015, o comparar dos índices con bases distintas, tendrás que hacer un **cambio de base** o un **enlace**. Son dos operaciones sencillas que evitan errores muy visibles.

**Qué necesitas saber antes**: los cuadernos 14 y 16.""",
    aprender=["Cambiar la base de un índice a otro periodo.",
              "Enlazar dos tramos de una serie publicados con bases distintas.",
              "Calcular la variación entre dos fechas directamente con el índice."],
    secciones=[
        dict(titulo="Cambiar la base", celdas=[
            C('ipc = pd.read_csv("ipc_simulado.csv")\nipc["fecha"] = pd.to_datetime(ipc["fecha"])\nipc = ipc.set_index("fecha")'),
            M("""Para pasar un índice a una nueva base, se divide toda la serie por el valor (o la media) del nuevo periodo base y se multiplica por 100:

$$I^{nueva}_t = \\frac{I_t}{I_{nueva\\ base}} \\times 100$$

Las **tasas de variación no cambian**: solo cambia la referencia."""),
            C("""base_2015 = ipc["general"]["2015"].mean()
ipc["general_b2015"] = (ipc["general"] / base_2015 * 100).round(2)
print(ipc[["general", "general_b2015"]].iloc[[0, 72, -1]])"""),
            C("""tasa_b2021 = ipc["general"].pct_change(12).iloc[-1] * 100
tasa_b2015 = ipc["general_b2015"].pct_change(12).iloc[-1] * 100
print(f"Inflación con base 2021: {tasa_b2021:.2f} %   con base 2015: {tasa_b2015:.2f} %")"""),
        ], quiz=[
            unica("Al cambiar la base de un índice, ¿qué ocurre con sus tasas de variación?", "No cambian",
                  [("Se multiplican por 100", "Solo cambia el nivel de referencia."), ("Cambian de signo", "No: cambiar la base no altera la evolución.")]),
        ]),
        dict(titulo="Variación entre dos fechas", celdas=[
            M("Con un índice se calcula directamente cuánto han subido los precios entre dos fechas cualesquiera, sin importar la base:"),
            C("""def variacion(serie, desde, hasta):
    return (serie[hasta] / serie[desde] - 1) * 100

print(f"Precios enero 2015 - diciembre 2025: +{variacion(ipc['general'], '2015-01-01', '2025-12-01'):.1f} %")
print(f"Lo mismo con base 2015:           +{variacion(ipc['general_b2015'], '2015-01-01', '2025-12-01'):.1f} %")"""),
            M("⚠️ Un error frecuente es **restar** los índices: pasar de 105 a 115 no es «un 10 % más», sino (115 / 105 − 1) × 100 = 9,5 %. Restar solo da el porcentaje correcto si el punto de partida vale 100."),
        ], quiz=[
            numerica("Un índice pasa de 105 a 115. ¿Cuál es la variación en % (un decimal)?", 9.5, 9.55, ok="¡Correcto! 115 / 105 − 1 = 9,5 %."),
        ]),
        dict(titulo="Enlazar dos tramos de una serie", celdas=[
            M("""Imagina que un organismo publicó la serie hasta 2020 con base 2016 y desde 2021 con base 2021. Para tener una sola serie se busca un **periodo de solapamiento** (un mes que esté en las dos) y se calcula un **coeficiente de enlace**."""),
            C("""general = ipc["general"]
antigua = (general[:"2021-01-01"] / general["2016"].mean() * 100).round(2)     # publicada en base 2016
nueva = general["2021-01-01":].round(3)                                      # publicada en base 2021
print("Mes común (enero 2021):  antigua =", antigua["2021-01-01"], "  nueva =", nueva["2021-01-01"])"""),
            C("""coef = nueva["2021-01-01"] / antigua["2021-01-01"]
antigua_enlazada = antigua * coef
serie_enlazada = pd.concat([antigua_enlazada[:"2020-12-01"], nueva])
print("Coeficiente de enlace:", round(coef, 4))
serie_enlazada.plot(color="steelblue")
plt.title("Serie enlazada en base 2021 (IPC simulado)")
plt.show()"""),
            M("**Qué ha pasado**: hemos reescalado el tramo antiguo para que coincida con el nuevo en el mes común. Los institutos oficiales suelen publicar ya las series enlazadas; cuando lo hagan, úsalas en lugar de fabricarlas tú."),
        ], quiz=[
            unica("¿Qué se necesita para enlazar dos tramos de una serie con bases distintas?", "Al menos un periodo en el que existan los dos tramos",
                  [("Que tengan el mismo número de datos", "No es necesario."), ("Que las dos bases sean el mismo año", "Entonces no haría falta enlazar.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Pon el índice de alimentos en base enero 2020 = 100.",
             solucion='(ipc["alimentos"] / ipc.loc["2020-01-01", "alimentos"] * 100).round(1)'),
        dict(seccion="sección 2", enunciado="¿Cuánto han subido los alimentos y la vivienda entre enero de 2021 y diciembre de 2025?",
             solucion='''for g in ["alimentos", "vivienda"]:
    print(g, round(variacion(ipc[g], "2021-01-01", "2025-12-01"), 1))'''),
        dict(seccion="sección 3", enunciado="Enlaza los tramos usando como mes común junio de 2021 en lugar de enero. ¿Cambia el resultado?",
             solucion='''a = general[:"2021-06-01"] / general["2016"].mean() * 100
n = general["2021-06-01":]
(a * n["2021-06-01"] / a["2021-06-01"]).tail(3)''',
             comentario="No cambia, porque los dos tramos salen aquí de la misma serie. Con series oficiales reales puede haber pequeñas diferencias según el mes de enlace."),
    ],
    resumen=["**Cambio de base**: dividir la serie por el valor del nuevo periodo base y multiplicar por 100; las tasas no cambian.",
             "La variación entre dos fechas es **cociente − 1**, no la resta de índices (salvo que el inicio valga 100).",
             "Para **enlazar** dos tramos con bases distintas se usa un periodo común y un coeficiente de enlace.",
             "Si el organismo publica series enlazadas oficiales, úsalas."],
    glosario=[("Periodo base", "Periodo cuyo índice vale 100."), ("Cambio de base", "Reexpresar un índice respecto a otro periodo base."),
              ("Enlace", "Unión de dos tramos de una serie publicados con bases distintas.")],
    seguir="En el cuaderno 18 empieza el análisis de series cronológicas: componentes y gráficos.",
),
# ---------------------------------------------------------------------------
dict(
    num=18, slug="P18_series_cronologicas", unidad=U,
    titulo="Series cronológicas: componentes y lectura de gráficos temporales",
    datos=["paro_mensual.csv", "visitas_diario.csv"],
    intro="""«El paro baja en julio» es casi siempre verdad... y casi nunca es noticia: pasa todos los años por la temporada turística. Una **serie cronológica** (los datos de una variable ordenados en el tiempo) mezcla una **tendencia**, un patrón **estacional** que se repite y un componente **irregular**. Distinguirlos es imprescindible para no confundir lo habitual con lo excepcional.

**Qué necesitas saber antes**: el cuaderno 14 (tasas interanuales).""",
    aprender=["Representar una serie cronológica con un gráfico de líneas.",
              "Identificar tendencia, estacionalidad, ciclo e irregularidad.",
              "Agregar datos diarios a semanas o meses.",
              "Comparar cada periodo con el mismo periodo del año anterior."],
    secciones=[
        dict(titulo="El gráfico de líneas", celdas=[
            C('paro = pd.read_csv("paro_mensual.csv")\nparo["fecha"] = pd.to_datetime(paro["fecha"])\nparo = paro.set_index("fecha")\nparo.head()'),
            M("En una serie el eje horizontal es **el tiempo** y los puntos se unen con líneas. A diferencia de las barras, aquí el eje vertical **no tiene por qué empezar en cero**, siempre que se vea la escala."),
            C("""paro["parados"].plot(color="steelblue", figsize=(11, 4))
plt.title("Paro registrado mensual (datos simulados)")
plt.ylabel("Personas")
plt.show()"""),
        ], quiz=[
            unica("¿Qué gráfico es el adecuado para una serie temporal larga?", "Un gráfico de líneas",
                  [("Un gráfico de sectores", "No muestra la evolución."), ("Un histograma", "Mostraría la distribución de los valores, no su evolución.")]),
        ]),
        dict(titulo="Componentes de una serie", celdas=[
            M("""Una serie se piensa como la combinación de:

| Componente | Qué es | En el paro |
| :-- | :-- | :-- |
| **Tendencia** | Evolución a largo plazo | Baja durante años |
| **Ciclo** | Oscilaciones de varios años | Crisis y recuperaciones |
| **Estacionalidad** | Patrón que se repite cada año (o semana) | Baja en verano, sube en otoño |
| **Irregular** | Lo que queda: ruido y sucesos puntuales | Una huelga, un temporal |

El salto de 2020 es un componente irregular muy grande (o un cambio de ciclo)."""),
            M("**Qué vamos a hacer**: ver la estacionalidad poniendo cada año en una línea, con los meses en el eje horizontal."),
            C("""tabla = paro.assign(anio=paro.index.year, mes=paro.index.month).pivot(index="mes", columns="anio", values="parados")
tabla.plot(figsize=(11, 4), colormap="viridis", legend=False)
plt.xticks(range(1, 13), ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
plt.title("Cada línea es un año: el patrón estacional se repite")
plt.ylabel("Parados")
plt.show()"""),
            M("**Cómo leerlo**: todos los años el paro baja de primavera a verano y sube en otoño. Ese movimiento **no es noticia**; lo que lo es, es que un julio baje más o menos de lo habitual."),
        ], quiz=[
            unica("El paro baja todos los veranos y sube cada otoño. ¿Qué componente es?", "La estacionalidad",
                  [("La tendencia", "La tendencia es la evolución a largo plazo."), ("El componente irregular", "Es un patrón que se repite, no algo puntual.")]),
        ]),
        dict(titulo="Comparar con el mismo periodo del año anterior", celdas=[
            M("Para quitar la estacionalidad sin fórmulas, se compara cada mes con el **mismo mes del año anterior** (tasa interanual):"),
            C("""paro["var_mensual"] = paro["parados"].diff()
paro["var_interanual"] = paro["parados"].diff(12)
paro.loc["2025-05-01":"2025-09-01", ["parados", "var_mensual", "var_interanual"]]"""),
            M("""**Cómo leerlo**: el paro de julio baja respecto a junio (efecto verano), pero lo relevante es si baja respecto a julio del año anterior. Así se escribe: «el paro baja en julio en X personas, la mayor caída interanual desde...»."""),
        ], quiz=[
            unica("¿Qué compara `diff(12)` en una serie mensual?", "Cada mes con el mismo mes del año anterior",
                  [("Cada mes con el anterior", "Eso es diff() o diff(1)."), ("Los 12 primeros meses", "diff resta valores separados 12 posiciones.")]),
        ]),
        dict(titulo="De datos diarios a semanales o mensuales", celdas=[
            C('visitas = pd.read_csv("visitas_diario.csv")\nvisitas["fecha"] = pd.to_datetime(visitas["fecha"])\nvisitas = visitas.set_index("fecha")["visitas"]'),
            M("Los datos diarios tienen mucho ruido y una estacionalidad **semanal** (los fines de semana se lee menos). `resample()` agrega por semana (`\"W\"`) o por mes (`\"MS\"`)."),
            C("""fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
visitas.plot(ax=axes[0], lw=0.6, title="Diario")
visitas.resample("W").sum().plot(ax=axes[1], title="Semanal (suma)")
visitas.resample("MS").sum().plot(ax=axes[2], marker="o", title="Mensual (suma)")
plt.tight_layout()
plt.show()"""),
            C("""dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
media_dia = visitas.groupby(visitas.index.dayofweek).mean()
media_dia.index = dias
media_dia.round(0)"""),
            M("**Cómo leerlo**: en la serie diaria se ven picos informativos (grandes noticias) y la caída de agosto; la serie mensual muestra mejor la tendencia creciente. El sábado es el día con menos visitas."),
        ], quiz=[
            unica("¿Qué hace `visitas.resample(\"MS\").sum()`?", "Suma las visitas de cada mes",
                  [("Calcula la media diaria de cada mes", "Para eso sería .mean()."), ("Ordena los meses", "resample agrupa por periodos de tiempo.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Dibuja la serie de paro solo desde 2022.",
             solucion='paro.loc["2022":, "parados"].plot()\nplt.show()'),
        dict(seccion="sección 2", enunciado="¿En qué mes del año suele haber menos parados? Calcula la media de cada mes del año a lo largo de toda la serie.",
             solucion='paro.groupby(paro.index.month)["parados"].mean().round()'),
        dict(seccion="sección 3", enunciado="¿Cuál fue la mayor caída interanual del paro y en qué mes?",
             solucion='paro["var_interanual"].idxmin(), paro["var_interanual"].min()'),
        dict(seccion="sección 4", enunciado="Busca los cinco días con más visitas del diario. ¿Qué tienen en común?",
             solucion='visitas.sort_values(ascending=False).head()', comentario="Son picos informativos: en los datos reales coincidirían con grandes noticias."),
    ],
    resumen=["Una **serie cronológica** se representa con **líneas**; el eje vertical puede no empezar en cero si la escala está clara.",
             "Componentes: **tendencia**, **ciclo**, **estacionalidad** e **irregular**.",
             "Lo estacional se repite cada año y **no es noticia**; compara con el **mismo periodo del año anterior** (`diff(12)`, `pct_change(12)`).",
             "`resample()` agrega datos diarios a semanas o meses y reduce el ruido."],
    glosario=[("Serie cronológica", "Valores de una variable ordenados en el tiempo."), ("Tendencia", "Evolución a largo plazo."),
              ("Estacionalidad", "Patrón que se repite con periodo fijo."), ("Componente irregular", "Variación no sistemática."),
              ("Variación interanual", "Diferencia con el mismo periodo del año anterior.")],
    errores=[("`resample` da `TypeError`", "El índice no es de tipo fecha", "Usa `pd.to_datetime` y `set_index`")],
    seguir="En el cuaderno 19 aislarás la tendencia con medias móviles y medirás la estacionalidad.",
),
# ---------------------------------------------------------------------------
dict(
    num=19, slug="P19_tendencia_y_estacionalidad", unidad=U,
    titulo="Tendencia con medias móviles y desestacionalización",
    datos=["paro_mensual.csv", "visitas_diario.csv"],
    intro="""Los organismos estadísticos publican a menudo dos cifras: la «original» y la «desestacionalizada». La segunda quita el efecto de la temporada para ver si la situación mejora o empeora de verdad. Aquí aprenderás la versión sencilla de ese proceso: **medias móviles** para la tendencia e **índices de variación estacional** para medir y quitar la estacionalidad.

**Qué necesitas saber antes**: el cuaderno 18.""",
    aprender=["Calcular medias móviles y usarlas para ver la tendencia.",
              "Calcular índices de variación estacional.",
              "Desestacionalizar una serie y leer la serie corregida."],
    secciones=[
        dict(titulo="Medias móviles", celdas=[
            C('paro = pd.read_csv("paro_mensual.csv")\nparo["fecha"] = pd.to_datetime(paro["fecha"])\nparo = paro.set_index("fecha")\nvisitas = pd.read_csv("visitas_diario.csv")\nvisitas["fecha"] = pd.to_datetime(visitas["fecha"])\nvisitas = visitas.set_index("fecha")["visitas"]'),
            M("""Una **media móvil** de orden $k$ sustituye cada valor por la media de $k$ valores consecutivos. Si $k$ coincide con el periodo estacional (7 días, 12 meses), la estacionalidad desaparece y queda la **tendencia**. `rolling(k, center=True)` la calcula centrada."""),
            C("""fig, ax = plt.subplots(figsize=(11, 4))
visitas.plot(ax=ax, lw=0.5, alpha=0.5, label="Diario")
visitas.rolling(7, center=True).mean().plot(ax=ax, label="Media móvil 7 días")
visitas.rolling(91, center=True).mean().plot(ax=ax, lw=2, label="Media móvil 91 días")
ax.legend()
ax.set_title("Visitas al diario: el ruido y la tendencia (datos simulados)")
plt.show()"""),
            M("**Qué ha pasado**: la media de 7 días quita el efecto del fin de semana; la de 91 días (un trimestre) deja ver la tendencia creciente. Las «medias de 7 días» se popularizaron en prensa durante la pandemia precisamente para eso."),
        ], quiz=[
            unica("Para eliminar la estacionalidad semanal de datos diarios, ¿qué media móvil usarías?", "De 7 días",
                  [("De 3 días", "No cubre una semana completa."), ("De 30 días", "Quita también lo semanal, pero suaviza mucho más de lo necesario.")]),
        ]),
        dict(titulo="Índices de variación estacional", celdas=[
            M("""Los **índices de variación estacional** (IVE) dicen cuánto se aparta cada mes, en promedio, de la tendencia. Método sencillo (de razón a la media móvil):

1. Calcular la tendencia con una media móvil centrada de 12 meses.
2. Dividir cada dato por su tendencia.
3. Promediar esos cocientes para cada mes del año."""),
            C("""tendencia = paro["parados"].rolling(12, center=True).mean()
razon = paro["parados"] / tendencia
ive = razon.groupby(razon.index.month).mean()
ive = ive / ive.mean() * 100            # que su media sea 100
ive.round(1)"""),
            C("""ive.plot(kind="bar", color=["firebrick" if v > 100 else "steelblue" for v in ive])
plt.axhline(100, color="grey", lw=0.8)
plt.xticks(range(12), ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"], rotation=0)
plt.title("Índice de variación estacional del paro (100 = mes normal)")
plt.show()"""),
            M("**Cómo leerlo**: un IVE de 93,5 en julio significa que en julio el paro suele estar un 6,5 % por debajo de su tendencia. Enero y febrero están por encima (104)."),
        ], quiz=[
            unica("Un índice de variación estacional de 104 en enero significa...", "que en enero el valor suele estar un 4 % por encima de la tendencia",
                  [("que en enero el paro ha subido un 4 % este año", "El IVE es un promedio de muchos años, no el dato de este año."), ("que enero tiene 104 parados", "Es un índice, no una cantidad.")]),
        ]),
        dict(titulo="Desestacionalizar", celdas=[
            M("Para **desestacionalizar** se divide cada dato por el IVE de su mes (y se multiplica por 100):"),
            C("""paro["desestacionalizado"] = paro["parados"] / paro.index.month.map(ive) * 100
paro[["parados", "desestacionalizado"]].plot(figsize=(11, 4))
plt.title("Paro original y desestacionalizado (datos simulados)")
plt.show()"""),
            C("""ultimos = paro[["parados", "desestacionalizado"]].diff().tail(6).round()
ultimos.columns = ["variación mensual original", "variación mensual desestacionalizada"]
ultimos"""),
            M("""**Cómo leerlo**: la serie original baja en verano y sube en otoño; la desestacionalizada muestra si, quitando la temporada, el paro mejora o empeora. Los organismos oficiales usan métodos más sofisticados (como TRAMO-SEATS o X-13), pero la idea es la misma.

> En una noticia: «el paro sube en octubre por el fin de la temporada, pero en términos desestacionalizados baja por quinto mes consecutivo» (si los datos lo dicen)."""),
        ], quiz=[
            unica("El paro sube en septiembre, pero el dato desestacionalizado baja. ¿Qué titular es más correcto?",
                  "«El paro sube en septiembre por la temporada, aunque la tendencia sigue a la baja»",
                  [("«El paro se dispara en septiembre»", "La subida es la habitual de la temporada."), ("«El paro baja en septiembre»", "El dato original sube; hay que explicar la diferencia.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula y representa la media móvil centrada de 12 meses del paro sobre la serie original.",
             solucion='''paro["parados"].plot()
paro["parados"].rolling(12, center=True).mean().plot()
plt.show()'''),
        dict(seccion="sección 2", enunciado="¿Qué mes tiene el IVE más bajo y cuál el más alto?",
             solucion='ive.idxmin(), ive.idxmax()'),
        dict(seccion="sección 2", enunciado="Calcula los índices de variación estacional **semanal** de las visitas al diario (día de la semana), con una media móvil de 7 días.",
             solucion='''t = visitas.rolling(7, center=True).mean()
r = (visitas / t).groupby(visitas.index.dayofweek).mean()
(r / r.mean() * 100).round(1)'''),
        dict(seccion="sección 3", enunciado="Escribe el titular del último mes de la serie usando a la vez el dato original y el desestacionalizado.",
             comentario="Usa la tabla `ultimos`: di qué pasa con la cifra original y qué dice la desestacionalizada."),
    ],
    resumen=["Una **media móvil** de orden igual al periodo estacional elimina la estacionalidad y deja ver la tendencia.",
             "Los **índices de variación estacional** miden cuánto se aparta, de media, cada mes de la tendencia (100 = normal).",
             "**Desestacionalizar**: dato / IVE × 100.",
             "En prensa, combina el dato original con el **desestacionalizado** para separar temporada y tendencia."],
    glosario=[("Media móvil", "Media de k valores consecutivos que se va desplazando."), ("IVE", "Índice de variación estacional: desviación media de cada periodo respecto a la tendencia."),
              ("Serie desestacionalizada", "Serie a la que se ha quitado el componente estacional.")],
    errores=[("Los primeros y últimos valores de la media móvil son NaN", "No hay suficientes datos alrededor", "Es normal en las medias centradas")],
    seguir="Con esto termina la unidad 3. En el cuaderno 20 empieza la Probabilidad: azar y simulación.",
),
]
