from _comun import C, M, numerica, unica, varias

U = "2. Estadística descriptiva"

LEER_ENCUESTA = 'encuesta = pd.read_csv("encuesta_medios.csv")'
LEER_SALARIOS = 'salarios = pd.read_csv("salarios_redaccion.csv")'

CUADERNOS = [
# ---------------------------------------------------------------------------
dict(
    num=5, slug="P05_tablas_de_frecuencias", unidad=U,
    titulo="Tablas de frecuencias: contar bien antes de publicar",
    datos=["encuesta_medios.csv"],
    intro="""«El 22 % de los encuestados se informa principalmente por redes sociales.» Detrás de esa frase hay una **tabla de frecuencias**: cuántas personas eligen cada opción y qué parte del total suponen. Es el resumen más sencillo y el más publicado.

**Qué necesitas saber antes**: el cuaderno 4 (leer y filtrar tablas).""",
    aprender=["Construir una tabla de frecuencias absolutas y relativas.",
              "Calcular frecuencias acumuladas en variables ordinales.",
              "Agrupar una variable cuantitativa en intervalos.",
              "Redactar porcentajes sin errores de base."],
    secciones=[
        dict(titulo="Frecuencias absolutas y relativas", celdas=[
            C(LEER_ENCUESTA),
            M("""- **Frecuencia absoluta** ($n_i$): cuántas veces aparece cada valor.
- **Frecuencia relativa** ($f_i = n_i / n$): qué proporción del total supone. Multiplicada por 100, es el **porcentaje**.

Las relativas siempre suman 1 (o 100 %)."""),
            C("""absoluta = encuesta["medio_principal"].value_counts()
relativa = encuesta["medio_principal"].value_counts(normalize=True)

tabla = pd.DataFrame({"personas": absoluta, "porcentaje": (relativa * 100).round(1)})
tabla"""),
            M("**Qué ha pasado**: con `normalize=True`, `value_counts()` divide cada recuento por el total. Hemos juntado las dos columnas en una tabla con `pd.DataFrame()`."),
            C("""print("Suma de porcentajes:", round(tabla["porcentaje"].sum(), 1))"""),
            M("Por el redondeo, la suma puede dar 99,9 o 100,1. Es normal; si publicas la tabla, añade una nota: «los porcentajes pueden no sumar 100 por redondeo»."),
        ], quiz=[
            numerica("Si 264 de 1.200 personas se informan por redes sociales, ¿qué porcentaje es? (un decimal)", 21.95, 22.05,
                     ok="¡Correcto! 264 / 1.200 × 100 = 22,0 %."),
        ]),
        dict(titulo="Frecuencias acumuladas en variables ordinales", celdas=[
            M("""Cuando las categorías tienen orden (estudios, nivel de confianza), tiene sentido **acumular**: «el 45 % tiene, como mucho, estudios secundarios». Hay que ordenar las categorías antes con `reindex()`."""),
            C("""orden = ["Primarios", "Secundarios", "FP", "Universitarios"]
fa = encuesta["estudios"].value_counts().reindex(orden)
tabla_est = pd.DataFrame({"n": fa, "%": (fa / fa.sum() * 100).round(1)})
tabla_est["% acumulado"] = tabla_est["%"].cumsum()
tabla_est"""),
            M("""**Cómo leerlo**: la última fila de la columna acumulada es siempre 100 %. La frase «el X % no tiene estudios universitarios» se lee en la fila de FP."""),
            M("La confianza en los medios (0 a 10) también es ordinal. Ordenamos por el valor con `sort_index()`:"),
            C("""conf = encuesta["confianza_medios"].value_counts().sort_index()
pd.DataFrame({"n": conf, "% acumulado": (conf.cumsum() / conf.sum() * 100).round(1)})"""),
        ], quiz=[
            unica("En la tabla de estudios, ¿qué significa el % acumulado de la fila «Secundarios»?",
                  "El porcentaje con estudios primarios o secundarios",
                  [("El porcentaje con estudios secundarios", "Eso es la frecuencia relativa simple."),
                   ("El porcentaje con estudios secundarios o superiores", "Se acumula desde la primera categoría hacia abajo.")]),
        ]),
        dict(titulo="Agrupar en intervalos", celdas=[
            M("""Con variables cuantitativas que toman muchos valores (la edad) una tabla valor a valor no se lee. Se agrupan en **intervalos** con `pd.cut()`. Los límites los decides tú: usa los habituales en tu fuente (el INE suele usar grupos de edad de 5 o 10 años)."""),
            C("""limites = [17, 29, 44, 64, 100]
etiquetas = ["18-29", "30-44", "45-64", "65 y más"]
encuesta["grupo_edad"] = pd.cut(encuesta["edad"], bins=limites, labels=etiquetas)
encuesta["grupo_edad"].value_counts(sort=False)"""),
            M("**Qué ha pasado**: `pd.cut()` asigna cada edad a su intervalo. Por defecto el límite derecho se incluye: 29 cae en «18-29» y 30 en «30-44». `sort=False` mantiene el orden de los grupos."),
        ], quiz=[
            unica("Con `bins=[17, 29, 44, 64, 100]`, ¿en qué grupo cae una persona de 44 años?", "30-44",
                  [("45-64", "El límite derecho (44) se incluye en el intervalo (29, 44]."), ("18-29", "29 es el límite de ese grupo.")]),
        ]),
        dict(titulo="Porcentajes sin trampas", celdas=[
            M("""Tres errores habituales en prensa:

1. **Confundir la base**: «el 60 % de los que comparten noticias ha creído un bulo» no es lo mismo que «el 60 % de los que han creído un bulo comparte noticias». Di siempre **sobre quién** se calcula el porcentaje.
2. **Porcentajes de grupos pequeños**: el 50 % de 4 personas son 2 personas. Publica también el número de casos.
3. **Puntos frente a porcentaje**: si un medio pasa del 20 % al 25 % de audiencia, sube **5 puntos**, que es un aumento del **25 %**. Lo verás en el cuaderno 14."""),
            C("""pago = encuesta[encuesta["suscripcion_pago"] == "Sí"]
print("Personas que pagan por noticias:", len(pago))
print("De ellas, con estudios universitarios (%):",
      round((pago["estudios"] == "Universitarios").mean() * 100, 1))"""),
        ], quiz=[
            unica("Un medio pasa del 20 % al 25 % de cuota de pantalla. ¿Qué frase es correcta?", "Sube 5 puntos",
                  [("Sube un 5 %", "Sube 5 puntos porcentuales, que es un 25 % más."), ("Sube un 50 %", "(25 − 20) / 20 = 25 %, no 50 %.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Haz la tabla de frecuencias absolutas y relativas (en %) de la provincia de residencia.",
             solucion='''n = encuesta["provincia"].value_counts()
pd.DataFrame({"n": n, "%": (n / n.sum() * 100).round(1)})'''),
        dict(seccion="sección 1", enunciado="¿Qué porcentaje de las personas entrevistadas afirma haber creído alguna vez un bulo?",
             solucion='''round((encuesta["ha_creido_bulo"] == "Sí").mean() * 100, 1)'''),
        dict(seccion="sección 2", enunciado="Con la tabla acumulada de confianza, ¿qué porcentaje de quienes contestaron da una confianza de 4 o menos?",
             solucion='''conf = encuesta["confianza_medios"].dropna()
round((conf <= 4).mean() * 100, 1)'''),
        dict(seccion="sección 3", enunciado="Agrupa `minutos_noticias_dia` en los intervalos [0, 15], (15, 30], (30, 60], (60, 120] y más de 120, y haz su tabla de frecuencias relativas.",
             solucion='''grupos = pd.cut(encuesta["minutos_noticias_dia"], bins=[-1, 15, 30, 60, 120, 1000],
                labels=["15 o menos", "16-30", "31-60", "61-120", "Más de 120"])
(grupos.value_counts(normalize=True, sort=False) * 100).round(1)''',
             comentario="Empezamos en −1 para que el 0 entre en el primer intervalo."),
        dict(seccion="sección 4", enunciado="Escribe un titular y un subtítulo con el dato de los jóvenes (18-29) que se informan sobre todo por redes. El subtítulo debe decir sobre cuántas personas se calcula.",
             comentario="Por ejemplo: «Seis de cada diez jóvenes se informan sobre todo por redes sociales». Subtítulo: «Entre las 202 personas de 18 a 29 años entrevistadas...». Comprueba la cifra con `value_counts(normalize=True)` sobre ese grupo."),
    ],
    resumen=["La **frecuencia absoluta** cuenta casos; la **relativa** es su proporción sobre el total (`normalize=True`).",
             "En variables **ordinales** tiene sentido la frecuencia **acumulada** (`cumsum()`), con las categorías en orden.",
             "Las variables cuantitativas con muchos valores se agrupan en **intervalos** con `pd.cut()`.",
             "Di siempre **sobre quién** se calcula un porcentaje y cuántos casos hay detrás.",
             "Diferencia entre **puntos porcentuales** y **porcentaje de variación**."],
    glosario=[("Frecuencia absoluta", "Número de veces que aparece un valor."), ("Frecuencia relativa", "Proporción del total que supone un valor."),
              ("Frecuencia acumulada", "Suma de las frecuencias hasta un valor, en variables ordenadas."),
              ("Intervalo de clase", "Rango de valores que se agrupan juntos."), ("Punto porcentual", "Diferencia entre dos porcentajes.")],
    errores=[("Las categorías salen desordenadas", "`value_counts()` ordena por frecuencia", "Usa `reindex(orden)` o `sort_index()`"),
             ("`pd.cut` deja valores como NaN", "Algún valor queda fuera de los límites", "Amplía el primer o el último límite")],
    seguir="En el cuaderno 6 convertirás estas tablas en gráficos y aprenderás a detectar gráficos engañosos.",
),
# ---------------------------------------------------------------------------
dict(
    num=6, slug="P06_graficos_cualitativas", unidad=U,
    titulo="Gráficos para variables cualitativas y gráficos que engañan",
    datos=["encuesta_medios.csv", "audiencias_tv.csv"],
    intro="""Un buen gráfico se entiende en tres segundos; uno malo, o no se entiende o, peor, **engaña**. En las redacciones se publican a diario gráficos de barras, de sectores y de columnas. Aquí aprenderás a hacerlos con matplotlib y, sobre todo, a reconocer los trucos que distorsionan los datos.

**Qué necesitas saber antes**: el cuaderno 5 (tablas de frecuencias).""",
    aprender=["Hacer gráficos de barras verticales y horizontales, ordenados y con etiquetas.",
              "Saber cuándo un gráfico de sectores funciona y cuándo no.",
              "Detectar ejes truncados y otras manipulaciones habituales."],
    secciones=[
        dict(titulo="El gráfico de barras", celdas=[
            C(LEER_ENCUESTA + '\naudiencias = pd.read_csv("audiencias_tv.csv")'),
            M("""Para una variable cualitativa, el gráfico más claro es el de **barras**. Tres reglas:
1. **Ordena** las barras de mayor a menor (salvo que la variable sea ordinal).
2. Usa barras **horizontales** si las etiquetas son largas.
3. El eje de las barras **empieza en cero**."""),
            C("""pct = (encuesta["medio_principal"].value_counts(normalize=True) * 100).sort_values()

fig, ax = plt.subplots()
ax.barh(pct.index, pct.values, color="steelblue")
for i, v in enumerate(pct.values):
    ax.text(v + 0.5, i, f"{v:.0f} %", va="center")       # etiqueta con el valor
ax.set_xlabel("% de personas")
ax.set_title("Medio principal para informarse\\nEncuesta simulada, n = 1.200")
ax.spines[["top", "right"]].set_visible(False)
plt.show()"""),
            M("**Qué ha pasado**: con `plt.subplots()` creamos la figura (`fig`) y los ejes (`ax`), y sobre `ax` dibujamos y ponemos títulos. Las etiquetas con el valor ahorran al lector buscar en el eje."),
        ], quiz=[
            varias("¿Qué buenas prácticas tiene el gráfico anterior?", [
                ("Barras ordenadas por tamaño", True, "¡Correcto!"), ("Eje que empieza en cero", True, "¡Correcto!"),
                ("Título con la fuente y el tamaño de muestra", True, "¡Correcto!"), ("Efecto 3D", False, "No tiene, y es mejor así: el 3D distorsiona.")]),
        ]),
        dict(titulo="Comparar grupos con barras", celdas=[
            M("**Qué vamos a hacer**: comparar el share medio de cada género de programa por cadena. `groupby()` agrupa y `unstack()` pone un grupo en columnas."),
            C("""share = audiencias.groupby(["genero", "cadena"])["share"].mean().unstack()
share.round(1)"""),
            C("""share.plot(kind="bar", figsize=(11, 4))
plt.ylabel("Share medio (%)")
plt.title("Share medio por género y cadena (datos simulados)")
plt.xticks(rotation=0)
plt.legend(title="Cadena", bbox_to_anchor=(1, 1))
plt.show()"""),
            M("Con cinco cadenas y cinco géneros el gráfico ya cuesta leerlo. A veces es mejor **elegir una historia**: por ejemplo, solo los informativos."),
            C("""share.loc["Informativo"].sort_values().plot(kind="barh", color="steelblue")
plt.xlabel("Share medio (%)")
plt.title("Share medio de los informativos por cadena (datos simulados)")
plt.show()"""),
        ], quiz=[
            unica("¿Qué hace `groupby(\"cadena\")[\"share\"].mean()`?", "Calcula el share medio de cada cadena",
                  [("Ordena las cadenas por share", "Eso sería sort_values()."), ("Cuenta los programas de cada cadena", "Eso sería value_counts() o size().")]),
        ]),
        dict(titulo="Sectores: casi nunca", celdas=[
            M("""El gráfico de **sectores** solo funciona si hay **pocas categorías** (2 o 3) que forman **un todo**. El ojo compara mal ángulos: con cinco categorías parecidas, las barras ganan siempre."""),
            C("""fig, axes = plt.subplots(1, 2, figsize=(12, 4))
pct.plot(kind="pie", ax=axes[0], autopct="%.0f%%")
axes[0].set_ylabel("")
axes[0].set_title("Sectores: ¿cuál es mayor, radio o papel?")
pct.plot(kind="barh", ax=axes[1], color="steelblue")
axes[1].set_title("Barras: se ve al instante")
plt.tight_layout()
plt.show()"""),
        ], quiz=[
            unica("¿Cuándo es razonable un gráfico de sectores?", "Con 2 o 3 categorías que suman el 100 %",
                  [("Con muchas categorías parecidas", "Ahí el ojo no distingue los ángulos."), ("Para comparar dos años", "Para comparar, mejor barras o líneas.")]),
        ]),
        dict(titulo="Gráficos que engañan", celdas=[
            M("""El truco más común es **truncar el eje**: empezar las barras en un valor distinto de cero hace que una diferencia pequeña parezca enorme."""),
            C("""cadenas = ["Cadena 1", "Cadena 2"]
valores = [14.2, 15.1]

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].bar(cadenas, valores, color=["grey", "firebrick"])
axes[0].set_ylim(14, 15.2)
axes[0].set_title("Eje truncado: «¡arrasa!»")
axes[1].bar(cadenas, valores, color=["grey", "firebrick"])
axes[1].set_ylim(0, 16)
axes[1].set_title("Eje desde cero: casi iguales")
plt.show()"""),
            M("""Otros trucos que debes vigilar (y no usar):

| Truco | Efecto |
| :-- | :-- |
| Eje truncado en barras | Exagera diferencias |
| Escalas distintas en dos gráficos comparados | Hace parecer iguales cosas distintas |
| Efecto 3D y perspectiva | Agranda lo que está delante |
| Iconos que crecen en área | Duplicar la altura cuadruplica el área |
| Elegir el periodo a conveniencia | Esconde la tendencia general |

En los **gráficos de líneas** sí se puede no empezar en cero, siempre que se indique claramente la escala."""),
        ], quiz=[
            unica("Un gráfico de barras muestra 14,2 frente a 15,1 con el eje empezando en 14. ¿Qué impresión da?",
                  "Que la diferencia es mucho mayor de lo que es",
                  [("La impresión correcta", "Con el eje en 14 la segunda barra parece ocho veces la primera."), ("Que son iguales", "Al contrario: exagera la diferencia.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Haz un gráfico de barras horizontales, ordenado, con el porcentaje de personas de cada nivel de estudios. Como es ordinal, mantén el orden Primarios → Universitarios.",
             solucion='''orden = ["Primarios", "Secundarios", "FP", "Universitarios"]
p = (encuesta["estudios"].value_counts(normalize=True) * 100).reindex(orden)
p.plot(kind="barh", color="steelblue")
plt.xlabel("%")
plt.title("Nivel de estudios (encuesta simulada, n = 1.200)")
plt.show()'''),
        dict(seccion="sección 2", enunciado="Calcula el número medio de espectadores (en miles) por franja horaria y represéntalo en un gráfico de barras ordenado.",
             solucion='''e = audiencias.groupby("franja")["espectadores_miles"].mean().sort_values()
e.plot(kind="barh", color="steelblue")
plt.xlabel("Miles de espectadores")
plt.show()'''),
        dict(seccion="sección 3", enunciado="Haz un gráfico de sectores con la variable `suscripcion_pago` (Sí/No). ¿Es este un caso en que el sector funciona?",
             solucion='''encuesta["suscripcion_pago"].value_counts().plot(kind="pie", autopct="%.0f%%")
plt.ylabel("")
plt.show()''',
             comentario="Sí: son dos categorías que suman el 100 %."),
        dict(seccion="sección 4", enunciado="Busca en la prensa de esta semana un gráfico con el eje truncado o con otro de los trucos de la tabla. Pega el enlace en una celda de texto y explica qué distorsiona.",
             comentario="Ejercicio abierto para comentar en clase."),
    ],
    resumen=["Para variables cualitativas usa **barras**: ordenadas, horizontales si hay etiquetas largas y con el **eje desde cero**.",
             "`groupby()` + `mean()` resume una variable por grupos; `unstack()` lo prepara para un gráfico de barras agrupadas.",
             "Los **sectores** solo valen con 2–3 categorías que forman un todo.",
             "Desconfía de ejes truncados, escalas distintas, 3D, iconos que crecen en área y periodos elegidos a conveniencia.",
             "Todo gráfico debe llevar **título, unidad, fuente y número de casos**."],
    glosario=[("Eje truncado", "Eje que no empieza en cero y exagera las diferencias."), ("`groupby`", "Agrupa las filas por los valores de una columna."),
              ("Leyenda", "Recuadro que explica colores o símbolos del gráfico.")],
    errores=[("El gráfico sale vacío o duplicado", "Se mezcla `plt` con `ax` sin crear la figura", "Crea `fig, ax = plt.subplots()` y dibuja sobre `ax`"),
             ("Las etiquetas del eje se solapan", "Son largas", "Usa `kind=\"barh\"` o `plt.xticks(rotation=45)`")],
    seguir="En el cuaderno 7 pasarás a las variables cuantitativas: histogramas.",
),
# ---------------------------------------------------------------------------
dict(
    num=7, slug="P07_graficos_cuantitativas", unidad=U,
    titulo="Gráficos para variables cuantitativas: el histograma",
    datos=["salarios_redaccion.csv", "encuesta_medios.csv"],
    intro="""¿Cómo se reparten los sueldos en una redacción? ¿Cuánto tiempo dedica la gente a las noticias? Para variables cuantitativas el gráfico de referencia es el **histograma**: muestra dónde se concentran los valores, si hay asimetría y si aparecen casos raros. Es lo primero que conviene mirar antes de calcular una media.

**Qué necesitas saber antes**: los cuadernos 5 y 6.""",
    aprender=["Hacer e interpretar un histograma.",
              "Elegir el número de intervalos y entender cómo cambia el gráfico.",
              "Reconocer distribuciones simétricas, asimétricas y bimodales.",
              "Comparar la distribución de dos grupos."],
    secciones=[
        dict(titulo="El histograma", celdas=[
            C(LEER_SALARIOS + "\n" + LEER_ENCUESTA),
            M("""Un **histograma** divide el rango de la variable en intervalos contiguos y dibuja una barra con el número de casos de cada uno. A diferencia del gráfico de barras, **las barras van pegadas**, porque el eje es continuo."""),
            C("""plt.hist(salarios["salario_bruto_anual"], bins=20, color="steelblue", edgecolor="white")
plt.xlabel("Salario bruto anual (€)")
plt.ylabel("Número de personas")
plt.title("Salarios en una redacción (datos simulados, n = 420)")
plt.show()"""),
            M("""**Cómo leerlo**: la mayoría cobra entre 20.000 y 35.000 euros, pero la cola derecha es larga: unos pocos sueldos muy altos (la dirección). Es una distribución **asimétrica a la derecha**, la forma típica de salarios, rentas y audiencias."""),
        ], quiz=[
            unica("¿En qué se diferencia un histograma de un gráfico de barras?",
                  "En el histograma las barras van pegadas porque el eje es una variable continua",
                  [("No hay diferencia", "El histograma es para cuantitativas y agrupa en intervalos."),
                   ("El histograma es para variables cualitativas", "Es al revés.")]),
        ]),
        dict(titulo="Cuántos intervalos", celdas=[
            M("El número de intervalos (`bins`) cambia mucho la imagen. Pocos ocultan detalles; demasiados dibujan ruido."),
            C("""fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), sharey=False)
for ax, b in zip(axes, [5, 20, 80]):
    ax.hist(salarios["salario_bruto_anual"], bins=b, color="steelblue", edgecolor="white")
    ax.set_title(f"bins = {b}")
plt.tight_layout()
plt.show()"""),
            M("No hay un número correcto: prueba varios y quédate con el que muestra la forma **sin inventar picos**. Una regla de partida es la raíz cuadrada del número de casos (√420 ≈ 20)."),
        ], quiz=[
            unica("Con 400 datos, ¿qué número de intervalos es un buen punto de partida según la regla de la raíz?", "20",
                  [("4", "Demasiado pocos: ocultaría la forma."), ("400", "Uno por dato: solo se vería ruido.")]),
        ]),
        dict(titulo="Formas de una distribución", celdas=[
            M("""Las formas que más verás:

- **Simétrica**: los valores se reparten igual a ambos lados del centro (la confianza en los medios, aproximadamente).
- **Asimétrica a la derecha**: cola larga hacia los valores altos (salarios, minutos de consumo, compartidos en redes).
- **Bimodal**: dos picos, señal de que se mezclan **dos grupos** distintos."""),
            C("""fig, axes = plt.subplots(1, 2, figsize=(12, 3.5))
axes[0].hist(encuesta["confianza_medios"].dropna(), bins=range(0, 12), color="steelblue", edgecolor="white", align="left")
axes[0].set_title("Confianza en los medios (0-10): casi simétrica")
axes[1].hist(encuesta["minutos_noticias_dia"].dropna(), bins=30, color="darkorange", edgecolor="white")
axes[1].set_title("Minutos al día con noticias: asimétrica a la derecha")
plt.tight_layout()
plt.show()"""),
            M("""Ahora mira qué pasa si dibujamos juntos los sueldos de la **dirección** y de los **community managers**: aparecen dos montañas separadas. Un histograma bimodal te avisa de que no tiene sentido dar una sola cifra resumen."""),
            C("""dos = salarios[salarios["puesto"].isin(["Community manager", "Dirección", "Redactor/a jefe"])]
plt.hist(dos["salario_bruto_anual"], bins=25, color="grey", edgecolor="white")
plt.title("Mezcla de puestos: más de un pico")
plt.xlabel("Salario bruto anual (€)")
plt.show()"""),
        ], quiz=[
            unica("Un histograma con dos picos claramente separados sugiere...", "que se mezclan dos grupos distintos",
                  [("que los datos son erróneos", "No necesariamente: puede ser una mezcla de grupos."), ("una distribución simétrica", "Puede ser simétrica y a la vez bimodal, pero lo importante son los dos grupos.")]),
        ]),
        dict(titulo="Comparar dos grupos", celdas=[
            M("**Qué vamos a hacer**: comparar los salarios de mujeres y hombres con dos histogramas superpuestos y semitransparentes (`alpha`). `density=True` pone los dos en la misma escala aunque los grupos tengan tamaños distintos."),
            C("""for sexo, color in [("Mujer", "purple"), ("Hombre", "teal")]:
    datos = salarios.loc[salarios["sexo"] == sexo, "salario_bruto_anual"]
    plt.hist(datos, bins=25, alpha=0.5, color=color, label=f"{sexo} (n = {len(datos)})", density=True)
plt.legend()
plt.xlabel("Salario bruto anual (€)")
plt.title("Distribución de salarios por sexo (datos simulados)")
plt.show()"""),
            M("Las dos distribuciones se solapan mucho; a simple vista cuesta ver diferencias. En los cuadernos 8 a 10 aprenderás a resumirlas con números, y en el 9 con un diagrama de caja, que compara grupos mucho mejor."),
        ], quiz=[
            unica("¿Para qué sirve `density=True` al comparar dos histogramas?", "Para que los grupos sean comparables aunque tengan distinto tamaño",
                  [("Para que las barras sean más gruesas", "Cambia la escala del eje vertical, no el grosor."), ("Para ordenar los datos", "No ordena nada.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Haz un histograma de la edad de las personas de la encuesta con intervalos de 5 años (`bins=range(15, 90, 5)`). ¿Qué forma tiene?",
             solucion='''plt.hist(encuesta["edad"], bins=range(15, 90, 5), color="steelblue", edgecolor="white")
plt.xlabel("Edad")
plt.show()''',
             comentario="Bastante plana (uniforme), porque los datos simulados reparten las edades por igual."),
        dict(seccion="sección 2", enunciado="Repite el histograma de minutos al día con 10, 30 y 100 intervalos. ¿Cuál elegirías para publicar?",
             solucion='''for b in [10, 30, 100]:
    plt.hist(encuesta["minutos_noticias_dia"].dropna(), bins=b)
    plt.title(f"bins = {b}")
    plt.show()'''),
        dict(seccion="sección 3", enunciado="Dibuja el histograma de los años de experiencia de la redacción. ¿Es simétrico?",
             solucion='''plt.hist(salarios["anios_experiencia"], bins=20, color="steelblue", edgecolor="white")
plt.show()''', comentario="Es asimétrico a la derecha: mucha gente con poca experiencia y pocos veteranos."),
        dict(seccion="sección 4", enunciado="Compara con histogramas superpuestos los minutos de noticias de quienes se informan sobre todo por televisión y por redes sociales.",
             solucion='''for m in ["Televisión", "Redes sociales"]:
    d = encuesta.loc[encuesta["medio_principal"] == m, "minutos_noticias_dia"].dropna()
    plt.hist(d, bins=25, alpha=0.5, density=True, label=m)
plt.legend()
plt.show()'''),
    ],
    resumen=["El **histograma** muestra cómo se reparten los valores de una variable cuantitativa; sus barras van pegadas.",
             "El número de intervalos cambia la imagen: prueba varios; √n es un buen punto de partida.",
             "Formas típicas: **simétrica**, **asimétrica a la derecha** (salarios, audiencias) y **bimodal** (mezcla de grupos).",
             "Para comparar grupos de distinto tamaño usa `density=True` y transparencia (`alpha`).",
             "Mira siempre la distribución **antes** de resumirla con una sola cifra."],
    glosario=[("Histograma", "Gráfico de barras pegadas que muestra la distribución de una variable cuantitativa."),
              ("Distribución", "Forma en que se reparten los valores de una variable."),
              ("Asimetría", "Falta de simetría; a la derecha si la cola larga va hacia valores altos."),
              ("Bimodal", "Distribución con dos picos.")],
    errores=[("`ValueError` en `plt.hist`", "La columna tiene NaN", "Usa `.dropna()` antes de dibujar")],
    seguir="En el cuaderno 8 resumirás estas distribuciones con medidas de centralización: media, mediana y moda.",
),
# ---------------------------------------------------------------------------
dict(
    num=8, slug="P08_media_mediana_moda", unidad=U,
    titulo="Medidas de centralización: media, mediana y moda",
    datos=["salarios_redaccion.csv", "encuesta_medios.csv"],
    intro="""«El salario medio en la redacción es de 29.300 euros.» Probablemente la mayoría de esa redacción cobra menos. La **media** es la medida más publicada y la más malinterpretada. En este cuaderno aprenderás qué cuenta cada medida de centralización y cuál elegir para no engañar.

**Qué necesitas saber antes**: el cuaderno 7 (histogramas y asimetría).""",
    aprender=["Calcular e interpretar la media, la mediana y la moda.",
              "Elegir la medida adecuada según la forma de la distribución.",
              "Calcular una media ponderada.",
              "Resumir una variable por grupos con `groupby()`."],
    secciones=[
        dict(titulo="Media y mediana", celdas=[
            C(LEER_SALARIOS),
            M("""- La **media** ($\\bar{x} = \\frac{\\sum x_i}{n}$) reparte el total a partes iguales: es lo que cobraría cada persona si se juntaran todos los sueldos y se dividieran.
- La **mediana** es el valor central cuando se ordenan los datos: la mitad cobra menos y la otra mitad más."""),
            C("""s = salarios["salario_bruto_anual"]
print("Media:  ", round(s.mean()))
print("Mediana:", round(s.median()))
print("Personas por debajo de la media (%):", round((s < s.mean()).mean() * 100, 1))"""),
            M("""**Qué ha pasado**: la media supera a la mediana en unos 2.500 euros, y más del 60 % de la plantilla cobra **menos que la media**. Los sueldos de dirección tiran de la media hacia arriba. Con distribuciones asimétricas a la derecha, **la mediana describe mejor al trabajador típico**."""),
            C("""plt.hist(s, bins=25, color="lightgrey", edgecolor="white")
plt.axvline(s.mean(), color="firebrick", label=f"Media {s.mean():,.0f} €")
plt.axvline(s.median(), color="steelblue", label=f"Mediana {s.median():,.0f} €")
plt.legend()
plt.title("La media se va hacia la cola (datos simulados)")
plt.show()"""),
        ], quiz=[
            unica("En una distribución muy asimétrica a la derecha (como los salarios), lo normal es que...", "la media sea mayor que la mediana",
                  [("la media sea menor que la mediana", "La cola de valores altos sube la media."), ("media y mediana coincidan", "Solo pasa en distribuciones simétricas.")]),
        ]),
        dict(titulo="La moda y las variables cualitativas", celdas=[
            M("""La **moda** es el valor más frecuente. Es la única medida de centralización que sirve para variables **nominales** (no hay «medio principal medio»)."""),
            C(LEER_ENCUESTA + """
print("Moda del medio principal:", encuesta["medio_principal"].mode()[0])
print("Moda de la confianza:", encuesta["confianza_medios"].mode()[0])"""),
            M("""¿Qué medida usar?

| Tipo de variable | Medida |
| :-- | :-- |
| Nominal | Moda |
| Ordinal | Mediana (y moda) |
| Cuantitativa simétrica | Media (≈ mediana) |
| Cuantitativa asimétrica o con valores extremos | Mediana |"""),
        ], quiz=[
            unica("¿Qué medida de centralización tiene sentido para la provincia de residencia?", "La moda",
                  [("La media", "No se puede promediar una categoría."), ("La mediana", "Las provincias no tienen orden.")]),
        ]),
        dict(titulo="Media ponderada", celdas=[
            M("""Cuando los datos tienen **distinto peso**, la media simple engaña. Ejemplo: el share medio de un programa a lo largo de la semana no es la media de los shares diarios si cada día lo ve un número de personas distinto.

$$\\bar{x}_w = \\frac{\\sum w_i x_i}{\\sum w_i}$$

Las encuestas también usan pesos para que la muestra represente a la población (lo verás en el cuaderno 25)."""),
            C("""share_dia = np.array([12.0, 11.5, 13.2, 12.8, 14.1, 9.0, 8.5])
espectadores_tv = np.array([9.5, 9.3, 9.6, 9.4, 8.8, 7.2, 7.5])   # millones viendo la tele a esa hora
print("Media simple:   ", round(share_dia.mean(), 2))
print("Media ponderada:", round(np.average(share_dia, weights=espectadores_tv), 2))"""),
            M("**Qué ha pasado**: el fin de semana el share es más bajo pero hay menos gente delante del televisor; ponderar le da menos peso y la media sube un poco."),
        ], quiz=[
            numerica("Notas 6 (peso 1) y 9 (peso 2). ¿Cuál es la media ponderada?", 7.99, 8.01, ok="¡Correcto! (6·1 + 9·2) / 3 = 8."),
        ]),
        dict(titulo="Comparar grupos", celdas=[
            M("**Qué vamos a hacer**: comparar media y mediana del salario por tipo de contrato y por sexo. `agg()` calcula varias medidas a la vez."),
            C("""salarios.groupby("contrato")["salario_bruto_anual"].agg(["count", "mean", "median"]).round(0)"""),
            C("""por_sexo = salarios.groupby("sexo")["salario_bruto_anual"].median()
brecha = (por_sexo["Hombre"] - por_sexo["Mujer"]) / por_sexo["Hombre"] * 100
print(por_sexo)
print(f"Brecha salarial (sobre la mediana masculina): {brecha:.1f} %")"""),
            M("""**Cuidado al publicarlo**: esta brecha compara a todas las mujeres con todos los hombres, sin tener en cuenta el puesto ni la experiencia. Es un dato real de la plantilla (simulada), pero no demuestra por sí solo que se pague distinto **por el mismo trabajo**. Lo correcto es decir qué se compara."""),
        ], quiz=[
            unica("¿Qué devuelve `salarios.groupby(\"puesto\")[\"salario_bruto_anual\"].median()`?", "La mediana del salario de cada puesto",
                  [("La mediana de todos los salarios", "groupby separa por puestos."), ("El puesto con salario mediano", "Devuelve una cifra por puesto.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula la media y la mediana de los minutos diarios dedicados a las noticias. ¿Cuál usarías en un titular?",
             solucion='''m = encuesta["minutos_noticias_dia"]
print(m.mean(), m.median())''', comentario="La mediana: la distribución es asimétrica a la derecha."),
        dict(seccion="sección 2", enunciado="¿Cuál es el tipo de medio más frecuente entre quienes pagan por noticias?",
             solucion='''encuesta.loc[encuesta["suscripcion_pago"] == "Sí", "medio_principal"].mode()[0]'''),
        dict(seccion="sección 3", enunciado="Un periódico tiene tres ediciones con 40.000, 12.000 y 8.000 lectores, y un tiempo medio de lectura de 6, 11 y 15 minutos. ¿Cuál es el tiempo medio de lectura del conjunto de lectores?",
             solucion='''np.average([6, 11, 15], weights=[40000, 12000, 8000])''',
             comentario="8,2 minutos; la media simple (10,7) daría el mismo peso a una edición con cinco veces menos lectores."),
        dict(seccion="sección 4", enunciado="Calcula el salario mediano por puesto, ordénalo de mayor a menor y represéntalo en un gráfico de barras horizontales.",
             solucion='''salarios.groupby("puesto")["salario_bruto_anual"].median().sort_values().plot(kind="barh")
plt.xlabel("Salario mediano (€)")
plt.show()'''),
        dict(seccion="sección 4", enunciado="Calcula la brecha salarial por sexo **solo entre redactores y redactoras**. ¿Cambia respecto a la de toda la plantilla?",
             solucion='''r = salarios[salarios["puesto"] == "Redactor/a"].groupby("sexo")["salario_bruto_anual"].median()
(r["Hombre"] - r["Mujer"]) / r["Hombre"] * 100'''),
    ],
    resumen=["La **media** reparte el total por igual; la **mediana** deja la mitad de los casos a cada lado; la **moda** es el valor más frecuente.",
             "Con distribuciones **asimétricas** o con valores extremos, la mediana describe mejor el caso típico.",
             "Para variables **nominales** solo tiene sentido la moda.",
             "Si los datos tienen distinto peso, usa la **media ponderada** (`np.average(x, weights=w)`).",
             "Al comparar grupos, di exactamente **qué** se compara (todas las mujeres frente a todos los hombres, o a igual puesto)."],
    glosario=[("Media", "Suma de los valores dividida por su número."), ("Mediana", "Valor que deja la mitad de los datos por debajo."),
              ("Moda", "Valor más frecuente."), ("Media ponderada", "Media en la que cada valor cuenta según su peso."),
              ("Brecha salarial", "Diferencia relativa entre los salarios de dos grupos.")],
    errores=[("`mode()` devuelve varios valores", "Hay empate en la moda", "Son todas modas; menciónalo o usa `mode()[0]`")],
    seguir="En el cuaderno 9 verás cuartiles, percentiles y el diagrama de caja.",
),
# ---------------------------------------------------------------------------
dict(
    num=9, slug="P09_cuartiles_y_diagrama_de_caja", unidad=U,
    titulo="Medidas de posición: cuartiles, percentiles y diagrama de caja",
    datos=["salarios_redaccion.csv", "audiencias_tv.csv"],
    intro="""«El 10 % de la plantilla que más cobra gana más que el 50 % que menos.» Esa frase usa **percentiles**. Las medidas de posición dicen dónde queda un valor respecto al resto y son la base del **diagrama de caja**, el mejor gráfico para comparar varios grupos de un vistazo.

**Qué necesitas saber antes**: el cuaderno 8 (mediana).""",
    aprender=["Calcular e interpretar cuartiles, deciles y percentiles.",
              "Situar un valor concreto en la distribución (su percentil).",
              "Construir y leer un diagrama de caja.",
              "Comparar grupos con diagramas de caja."],
    secciones=[
        dict(titulo="Cuartiles y percentiles", celdas=[
            C(LEER_SALARIOS + '\naudiencias = pd.read_csv("audiencias_tv.csv")\ns = salarios["salario_bruto_anual"]'),
            M("""El **percentil p** es el valor que deja por debajo el p % de los datos. Algunos tienen nombre propio:

- **Cuartiles**: $Q_1$ (percentil 25), $Q_2$ (percentil 50 = mediana) y $Q_3$ (percentil 75).
- **Deciles**: percentiles 10, 20, ..., 90."""),
            C("""print(s.quantile([0.25, 0.5, 0.75]))"""),
            M("**Cómo leerlo**: un cuarto de la plantilla cobra menos de $Q_1$ y otro cuarto más de $Q_3$. La mitad central está entre ambos."),
            C("""deciles = s.quantile([0.1, 0.9])
print(deciles)
print("Ratio P90/P10:", round(deciles[0.9] / deciles[0.1], 2))"""),
            M("El **ratio P90/P10** es un indicador de desigualdad muy usado en informes de salarios y renta: cuántas veces más cobra quien está en el percentil 90 que quien está en el 10."),
        ], quiz=[
            unica("Si el percentil 90 de los salarios es 40.000 €, ¿qué significa?", "El 90 % cobra 40.000 € o menos",
                  [("El 90 % cobra más de 40.000 €", "Es al revés: el 90 % queda por debajo."), ("La media es 40.000 €", "El percentil no es la media.")]),
        ]),
        dict(titulo="¿En qué posición está un valor?", celdas=[
            M("También podemos hacer la pregunta inversa: ¿qué percentil ocupa un sueldo de 30.000 euros? Basta con calcular qué proporción de datos está por debajo."),
            C("""valor = 30000
percentil = (s < valor).mean() * 100
print(f"Un salario de {valor} € está en el percentil {percentil:.0f}")"""),
            M("Es la forma correcta de contar en una noticia si un dato es alto o bajo: «cobra más que el 70 % de sus compañeros» se entiende mejor que cualquier media."),
        ], quiz=[
            unica("Si `(s < 30000).mean()` vale 0,70, ¿qué percentil ocupa 30.000 €?", "El 70",
                  [("El 30", "Un 70 % de los datos está por debajo."), ("El 0,70", "Hay que multiplicar por 100.")]),
        ]),
        dict(titulo="El diagrama de caja", celdas=[
            M("""El **diagrama de caja** (*boxplot*) resume cinco números en un dibujo:

- la **caja** va de $Q_1$ a $Q_3$ y la raya interior es la **mediana**;
- los **bigotes** llegan hasta el dato más extremo que no se aleja más de 1,5 veces el rango intercuartílico ($RIC = Q_3 - Q_1$);
- los puntos sueltos son **valores atípicos** (lo verás en el cuaderno 11)."""),
            C("""plt.boxplot(s, vert=False)
plt.xlabel("Salario bruto anual (€)")
plt.title("Salarios de la redacción (datos simulados)")
plt.show()"""),
            M("**Cómo leerlo**: la mediana está más cerca de $Q_1$ que de $Q_3$ y el bigote derecho es más largo: confirma la asimetría a la derecha. Los puntos de la derecha son los sueldos de dirección."),
        ], quiz=[
            unica("En un diagrama de caja, ¿qué representa la raya dentro de la caja?", "La mediana",
                  [("La media", "La media no se dibuja por defecto."), ("La moda", "No aparece en el diagrama de caja.")]),
        ]),
        dict(titulo="Comparar grupos con cajas", celdas=[
            M("**Qué vamos a hacer**: comparar el salario por tipo de medio. Con Pandas basta `boxplot(column=..., by=...)`."),
            C("""salarios.boxplot(column="salario_bruto_anual", by="tipo_medio", vert=False, grid=False, figsize=(10, 4))
plt.suptitle("")
plt.title("Salario según tipo de medio (datos simulados)")
plt.xlabel("Salario bruto anual (€)")
plt.show()"""),
            M("En un solo gráfico se comparan cinco grupos: dónde está su centro (mediana), cuánto varían (tamaño de la caja) y si tienen casos extremos. Hacer lo mismo con cinco histogramas sería mucho más difícil."),
            C("""audiencias.boxplot(column="share", by="franja", grid=False, figsize=(10, 4))
plt.suptitle("")
plt.title("Share por franja horaria (datos simulados)")
plt.ylabel("Share (%)")
plt.show()"""),
        ], quiz=[
            unica("Al comparar dos grupos con cajas, una caja más larga indica...", "más dispersión en la mitad central de los datos",
                  [("una mediana más alta", "La posición de la mediana es la raya, no la longitud de la caja."), ("más casos", "El tamaño de la caja no depende del número de casos.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula los cuartiles del share de los programas de televisión.",
             solucion='audiencias["share"].quantile([0.25, 0.5, 0.75])'),
        dict(seccion="sección 1", enunciado="Calcula el ratio P90/P10 de los salarios **solo de redactores y redactoras**. ¿Es mayor o menor que el de toda la plantilla? ¿Por qué?",
             solucion='''r = salarios.loc[salarios["puesto"] == "Redactor/a", "salario_bruto_anual"]
r.quantile(0.9) / r.quantile(0.1)''', comentario="Menor: dentro de un mismo puesto los salarios son más parecidos."),
        dict(seccion="sección 2", enunciado="Un programa tiene 1.900 miles de espectadores. ¿En qué percentil está dentro de todos los programas?",
             solucion='round((audiencias["espectadores_miles"] < 1900).mean() * 100)'),
        dict(seccion="sección 4", enunciado="Haz un diagrama de caja del salario según el tipo de contrato. ¿Qué grupo tiene la mediana más baja?",
             solucion='''salarios.boxplot(column="salario_bruto_anual", by="contrato", vert=False, grid=False)
plt.show()'''),
    ],
    resumen=["El **percentil p** deja por debajo el p % de los datos; los **cuartiles** son los percentiles 25, 50 y 75.",
             "El **ratio P90/P10** mide la desigualdad entre la parte alta y la baja de una distribución.",
             "Para situar un valor: `(serie < valor).mean() * 100` da su percentil.",
             "El **diagrama de caja** resume mediana, cuartiles, bigotes y atípicos, y es el mejor gráfico para **comparar grupos**."],
    glosario=[("Percentil", "Valor que deja por debajo un porcentaje dado de los datos."), ("Cuartil", "Percentiles 25, 50 y 75."),
              ("Rango intercuartílico (RIC)", "Q3 − Q1: amplitud de la mitad central."), ("Diagrama de caja", "Gráfico que resume la distribución con cinco números.")],
    errores=[("Aparece un título duplicado encima del boxplot", "Pandas añade un título por grupo", "Usa `plt.suptitle(\"\")`")],
    seguir="En el cuaderno 10 medirás la dispersión: rango, varianza, desviación típica y coeficiente de variación.",
),
# ---------------------------------------------------------------------------
dict(
    num=10, slug="P10_medidas_de_dispersion", unidad=U,
    titulo="Medidas de dispersión: ¿son los datos parecidos o muy distintos?",
    datos=["audiencias_tv.csv", "salarios_redaccion.csv"],
    intro="""Dos cadenas pueden tener el mismo share medio y comportamientos opuestos: una siempre igual, la otra con programas que arrasan y otros que no ve nadie. La media no lo dice; las **medidas de dispersión**, sí. Sin ellas, cualquier promedio es una media verdad.

**Qué necesitas saber antes**: los cuadernos 8 y 9.""",
    aprender=["Calcular el rango y el rango intercuartílico.",
              "Calcular e interpretar la varianza y la desviación típica.",
              "Comparar la dispersión de variables con distinta escala con el coeficiente de variación.",
              "Resumir una variable con media y desviación típica en una noticia."],
    secciones=[
        dict(titulo="Rango y rango intercuartílico", celdas=[
            C('audiencias = pd.read_csv("audiencias_tv.csv")\n' + LEER_SALARIOS),
            M("""- **Rango** = máximo − mínimo. Fácil, pero depende solo de los dos valores más extremos.
- **Rango intercuartílico** (RIC) = $Q_3 - Q_1$. Mide la amplitud de la mitad central y no le afectan los extremos."""),
            C("""sh = audiencias["share"]
print("Rango:", round(sh.max() - sh.min(), 1))
print("RIC:  ", round(sh.quantile(0.75) - sh.quantile(0.25), 1))"""),
        ], quiz=[
            unica("¿Qué medida de dispersión no se ve afectada por un valor extremo?", "El rango intercuartílico",
                  [("El rango", "Depende justo de los extremos."), ("La varianza", "También se ve muy afectada por los extremos.")]),
        ]),
        dict(titulo="Varianza y desviación típica", celdas=[
            M("""La **varianza** mide cuánto se alejan, de media, los datos de su media (al cuadrado):

$$s^2 = \\frac{\\sum (x_i - \\bar{x})^2}{n - 1}$$

Como está en unidades al cuadrado (puntos de share²), se usa su raíz, la **desviación típica** $s$, que está en las mismas unidades que los datos."""),
            M("**Qué vamos a hacer**: calcularla paso a paso con cinco programas y comprobarla con Pandas."),
            C("""x = np.array([12.0, 9.0, 15.0, 10.0, 14.0])
media = x.mean()
desvios = x - media
print("Desvíos respecto a la media:", desvios)
varianza = (desvios ** 2).sum() / (len(x) - 1)
print("Varianza:", varianza, "  Desviación típica:", round(np.sqrt(varianza), 2))
print("Con Pandas:", round(pd.Series(x).std(), 2))"""),
            M("""**Qué ha pasado**: los desvíos suman cero (siempre ocurre), por eso se elevan al cuadrado. La desviación típica de 2,5 puntos indica que estos programas se separan, en promedio, unos 2,5 puntos del share medio (12).

Se divide entre $n-1$ porque trabajamos con una **muestra**; es lo que hace Pandas por defecto."""),
            C("""por_cadena = audiencias.groupby("cadena")["share"].agg(["mean", "std"]).round(1)
por_cadena"""),
        ], quiz=[
            numerica("Datos: 4, 6, 8. Su media es 6. ¿Cuál es su varianza (dividiendo entre n − 1)?", 3.99, 4.01, ok="¡Correcto! (4 + 0 + 4) / 2 = 4."),
        ]),
        dict(titulo="Coeficiente de variación", celdas=[
            M("""Para comparar la dispersión de variables con **unidades o tamaños distintos** (share en % y espectadores en miles, o salarios de becarios y directivos) se usa el **coeficiente de variación**:

$$CV = \\frac{s}{\\bar{x}} \\times 100$$

No tiene unidades. Como orientación, un CV por debajo del 30 % indica datos bastante homogéneos."""),
            C("""def cv(serie):
    return round(serie.std() / serie.mean() * 100, 1)

print("CV del share:       ", cv(audiencias["share"]), "%")
print("CV de espectadores: ", cv(audiencias["espectadores_miles"]), "%")
salarios.groupby("puesto")["salario_bruto_anual"].apply(cv)"""),
            M("**Cómo leerlo**: los espectadores varían mucho más que el share, porque dependen también de la franja (a medianoche hay menos gente frente al televisor). Y dentro de cada puesto los salarios son bastante homogéneos."),
        ], quiz=[
            unica("¿Para qué sirve el coeficiente de variación?", "Para comparar la dispersión de variables con distinta escala o unidades",
                  [("Para medir el centro de los datos", "Eso es la media o la mediana."), ("Para detectar la moda", "No tiene relación con la moda.")]),
        ]),
        dict(titulo="Cómo contarlo", celdas=[
            M("""En una noticia la dispersión se cuenta mejor con **ejemplos y rangos** que con la palabra «desviación típica»:

- «La mitad de los programas tiene un share de entre 6 y 12 puntos» (cuartiles).
- «Los sueldos de la redacción van de menos de 15.000 a casi 120.000 euros» (rango).
- «Los informativos de la Cadena 3 son los más regulares: casi todos rondan el 13 %» (desviación típica pequeña).

En los gráficos, las barras de error o las cajas transmiten la dispersión sin fórmulas."""),
            C("""q1, q3 = audiencias["share"].quantile([0.25, 0.75])
print(f"La mitad de los programas tiene un share de entre {q1:.0f} y {q3:.0f} puntos.")"""),
        ], quiz=[
            unica("¿Qué frase transmite mejor la dispersión a un lector general?",
                  "«La mitad de los programas tiene entre 6 y 12 puntos de share»",
                  [("«La desviación típica es 4,2»", "Es correcto, pero muchos lectores no lo entenderán."), ("«El share medio es 10»", "Eso es el centro, no la dispersión.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula el rango y el RIC del salario. ¿Cuál describe mejor la variabilidad de la mayoría de la plantilla?",
             solucion='''s = salarios["salario_bruto_anual"]
print(s.max() - s.min(), s.quantile(0.75) - s.quantile(0.25))''', comentario="El RIC: el rango lo marcan los sueldos de dirección."),
        dict(seccion="sección 2", enunciado="¿Qué género de programa tiene el share más regular (menor desviación típica)?",
             solucion='audiencias.groupby("genero")["share"].std().sort_values()'),
        dict(seccion="sección 3", enunciado="Compara el CV de los salarios de autónomos y de indefinidos.",
             solucion='salarios.groupby("contrato")["salario_bruto_anual"].apply(lambda x: x.std() / x.mean() * 100)'),
        dict(seccion="sección 4", enunciado="Escribe con una f-string una frase del tipo «La mitad de la plantilla cobra entre X y Y euros».",
             solucion='''q1, q3 = salarios["salario_bruto_anual"].quantile([0.25, 0.75])
print(f"La mitad de la plantilla cobra entre {q1:,.0f} y {q3:,.0f} euros")'''),
    ],
    resumen=["El **rango** depende de los extremos; el **RIC** mide la mitad central y es robusto.",
             "La **desviación típica** mide la distancia típica de los datos a la media, en sus mismas unidades.",
             "El **coeficiente de variación** compara dispersiones de variables con escalas distintas.",
             "En prensa, cuenta la dispersión con **rangos y ejemplos**: «la mitad está entre X e Y»."],
    glosario=[("Rango", "Diferencia entre el máximo y el mínimo."), ("Varianza", "Media de los desvíos al cuadrado (dividiendo por n − 1)."),
              ("Desviación típica", "Raíz cuadrada de la varianza."), ("Coeficiente de variación", "Desviación típica dividida por la media, en %.")],
    errores=[("La desviación típica de NumPy no coincide con la de Pandas", "NumPy divide entre n y Pandas entre n − 1", "Usa `np.std(x, ddof=1)`")],
    seguir="En el cuaderno 11 verás cómo detectar valores atípicos y describir la forma de una distribución.",
),
# ---------------------------------------------------------------------------
dict(
    num=11, slug="P11_atipicos_y_forma", unidad=U,
    titulo="Valores atípicos, puntuaciones z y forma de la distribución",
    datos=["verificaciones.csv", "salarios_redaccion.csv", "audiencias_tv.csv"],
    intro="""Un bulo compartido 160.000 veces cuando la mitad de los contenidos no pasa de 1.200. Un sueldo cinco veces mayor que el resto. Los **valores atípicos** pueden ser un error de los datos o **la noticia**. Antes de borrarlos o de destacarlos hay que detectarlos con criterio.

**Qué necesitas saber antes**: los cuadernos 9 y 10.""",
    aprender=["Detectar valores atípicos con la regla del 1,5 × RIC.",
              "Calcular puntuaciones z para comparar valores de distribuciones distintas.",
              "Medir la asimetría de una distribución.",
              "Decidir qué hacer con un valor atípico."],
    secciones=[
        dict(titulo="La regla del 1,5 × RIC", celdas=[
            C('verif = pd.read_csv("verificaciones.csv")\n' + LEER_SALARIOS),
            M("""Un valor se considera **atípico** si queda por debajo de $Q_1 - 1{,}5 \\cdot RIC$ o por encima de $Q_3 + 1{,}5 \\cdot RIC$. Es la misma regla que usan los bigotes del diagrama de caja."""),
            C("""def limites_atipicos(serie):
    q1, q3 = serie.quantile([0.25, 0.75])
    ric = q3 - q1
    return q1 - 1.5 * ric, q3 + 1.5 * ric

inf, sup = limites_atipicos(salarios["salario_bruto_anual"])
atipicos = salarios[(salarios["salario_bruto_anual"] < inf) | (salarios["salario_bruto_anual"] > sup)]
print(f"Límites: {inf:,.0f} € y {sup:,.0f} €")
print("Número de atípicos:", len(atipicos))
atipicos["puesto"].value_counts()"""),
            M("**Qué ha pasado**: los atípicos son sueldos de dirección, jefaturas de redacción y algún editor. No son errores: son sueldos (simulados) de otro tipo de puesto."),
        ], quiz=[
            numerica("Si Q1 = 20 y Q3 = 30, ¿a partir de qué valor un dato es atípico por arriba?", 44.99, 45.01, ok="¡Correcto! 30 + 1,5 × 10 = 45."),
        ]),
        dict(titulo="Puntuaciones z", celdas=[
            M("""La **puntuación z** dice a cuántas desviaciones típicas está un valor de la media:

$$z = \\frac{x - \\bar{x}}{s}$$

Sirve para comparar valores de distribuciones distintas: ¿es más excepcional un programa con 20 puntos de share o uno con 3.000.000 de espectadores? Valores con $|z| > 3$ suelen considerarse muy raros (en distribuciones aproximadamente simétricas)."""),
            C("""s = salarios["salario_bruto_anual"]
salarios["z"] = (s - s.mean()) / s.std()
salarios.sort_values("z", ascending=False)[["puesto", "salario_bruto_anual", "z"]].head().round(2)"""),
        ], quiz=[
            unica("Un salario tiene z = 2. ¿Qué significa?", "Está dos desviaciones típicas por encima de la media",
                  [("Es el doble de la media", "z mide distancia en desviaciones típicas, no en veces la media."), ("Está en el percentil 2", "z no es un percentil.")]),
        ]),
        dict(titulo="Asimetría", celdas=[
            M("""El **coeficiente de asimetría** resume la forma: vale 0 si es simétrica, es positivo si la cola larga va a la derecha y negativo si va a la izquierda. Las veces que se comparte un contenido en redes son un ejemplo extremo de asimetría positiva."""),
            C("""print("Asimetría del salario:", round(salarios["salario_bruto_anual"].skew(), 2))
print("Asimetría de veces compartido:", round(verif["veces_compartido"].skew(), 2))
print(verif["veces_compartido"].describe().round(0))"""),
            M("Con una asimetría tan fuerte, el histograma normal no deja ver nada. Un truco habitual es usar una **escala logarítmica**, en la que cada marca del eje multiplica por 10:"),
            C("""fig, axes = plt.subplots(1, 2, figsize=(12, 3.5))
axes[0].hist(verif["veces_compartido"], bins=40, color="grey")
axes[0].set_title("Escala normal")
axes[1].hist(np.log10(verif["veces_compartido"]), bins=40, color="steelblue")
axes[1].set_title("Escala logarítmica (10³ = mil, 10⁴ = diez mil...)")
axes[1].set_xlabel("log10(veces compartido)")
plt.tight_layout()
plt.show()"""),
        ], quiz=[
            unica("Un coeficiente de asimetría de 4 indica...", "una cola muy larga hacia los valores altos",
                  [("una distribución simétrica", "Sería cercano a 0."), ("una cola hacia los valores bajos", "Sería negativo.")]),
        ]),
        dict(titulo="¿Qué hago con un atípico?", celdas=[
            M("""Antes de tocar un valor atípico pregúntate **por qué está ahí**:

| Situación | Qué hacer |
| :-- | :-- |
| Error de tecleo o de unidades (un sueldo de 2.500.000 €) | Comprobar con la fuente y corregir |
| Caso de otro tipo (la dirección en una tabla de redactores) | Analizarlo aparte |
| Caso real y extremo (un bulo viral) | **Es la noticia**: no lo borres; usa mediana y percentiles para el resto |

Nunca elimines datos solo porque «estropean» el resultado, y si los excluyes, dilo en la nota metodológica."""),
            C("""print("Bulo más compartido:")
verif.sort_values("veces_compartido", ascending=False).head(3)"""),
        ], quiz=[
            unica("En una tabla de sueldos aparece uno de 2.500.000 €/año para un redactor. ¿Qué haces primero?",
                  "Comprobarlo con la fuente: puede ser un error",
                  [("Borrarlo sin más", "Nunca sin comprobar."), ("Publicar que hay un redactor millonario", "Primero hay que verificar.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Aplica la regla del 1,5 × RIC a `veces_compartido`. ¿Qué porcentaje de contenidos son atípicos?",
             solucion='''inf, sup = limites_atipicos(verif["veces_compartido"])
round(((verif["veces_compartido"] > sup) | (verif["veces_compartido"] < inf)).mean() * 100, 1)'''),
        dict(seccion="sección 1", enunciado="¿Qué veredicto (Falso, Engañoso, Verdadero) tienen los contenidos atípicamente compartidos?",
             solucion='''verif[verif["veces_compartido"] > sup]["veredicto"].value_counts(normalize=True)'''),
        dict(seccion="sección 2", enunciado="Calcula la puntuación z de un programa con 20 puntos de share y de otro con 3.000 (miles) de espectadores, usando `audiencias_tv.csv`. ¿Cuál es más excepcional?",
             solucion='''aud = pd.read_csv("audiencias_tv.csv")
z1 = (20 - aud["share"].mean()) / aud["share"].std()
z2 = (3000 - aud["espectadores_miles"].mean()) / aud["espectadores_miles"].std()
print(z1, z2)'''),
        dict(seccion="sección 3", enunciado="Compara la asimetría de las veces compartido según el veredicto.",
             solucion='verif.groupby("veredicto")["veces_compartido"].skew()'),
    ],
    resumen=["Un valor es **atípico** si queda fuera de $[Q_1 - 1{,}5\\,RIC,\\; Q_3 + 1{,}5\\,RIC]$.",
             "La **puntuación z** indica a cuántas desviaciones típicas de la media está un valor y permite comparar escalas distintas.",
             "El **coeficiente de asimetría** es 0 si la distribución es simétrica y positivo si la cola va a la derecha; con asimetrías fuertes ayuda la **escala logarítmica**.",
             "Un atípico puede ser un **error**, un **caso de otro grupo** o **la noticia**: compruébalo antes de decidir."],
    glosario=[("Valor atípico", "Dato muy alejado del resto."), ("Puntuación z", "Distancia a la media medida en desviaciones típicas."),
              ("Coeficiente de asimetría", "Medida numérica de la falta de simetría."), ("Escala logarítmica", "Escala en la que cada marca multiplica por 10.")],
    errores=[("`np.log10` da `-inf`", "Hay valores 0", "Usa `np.log10(x + 1)` o filtra los ceros")],
    seguir="En el cuaderno 12 empezarás a estudiar relaciones entre variables: tablas de contingencia.",
),
# ---------------------------------------------------------------------------
dict(
    num=12, slug="P12_tablas_de_contingencia", unidad=U,
    titulo="Relación entre variables cualitativas: tablas de contingencia",
    datos=["encuesta_medios.csv"],
    intro="""¿Los jóvenes se informan más por redes? ¿Quien comparte noticias cae más en bulos? Para responder hay que cruzar dos variables en una **tabla de contingencia**. Saber leerla, y sobre todo saber **qué porcentaje calcular**, separa una buena noticia de un error de base.

**Qué necesitas saber antes**: el cuaderno 5 (frecuencias y porcentajes).""",
    aprender=["Construir una tabla de contingencia con `pd.crosstab()`.",
              "Calcular porcentajes por filas, por columnas y sobre el total, y elegir el adecuado.",
              "Representar la relación con barras apiladas al 100 %.",
              "Reconocer cuándo dos variables parecen relacionadas."],
    secciones=[
        dict(titulo="La tabla de contingencia", celdas=[
            C(LEER_ENCUESTA + """
encuesta["grupo_edad"] = pd.cut(encuesta["edad"], bins=[17, 29, 44, 64, 100],
                                labels=["18-29", "30-44", "45-64", "65 y más"])"""),
            M("Una **tabla de contingencia** cuenta cuántos casos hay en cada combinación de dos variables. `margins=True` añade los totales."),
            C("""pd.crosstab(encuesta["grupo_edad"], encuesta["medio_principal"], margins=True, margins_name="Total")"""),
            M("Con los recuentos brutos cuesta comparar, porque cada grupo de edad tiene un tamaño distinto. Hay que pasar a **porcentajes**."),
        ], quiz=[
            unica("¿Qué cuenta cada celda de `pd.crosstab(A, B)`?", "Cuántos casos tienen a la vez ese valor de A y ese valor de B",
                  [("La media de A para cada valor de B", "crosstab cuenta casos, no promedia."), ("El porcentaje de A", "Por defecto da recuentos.")]),
        ]),
        dict(titulo="¿Por filas o por columnas?", celdas=[
            M("""La pregunta decide el porcentaje:

- «¿Qué medio usan los jóvenes?» → dentro de cada **grupo de edad** (porcentajes **por fila**, `normalize="index"`).
- «¿Qué edad tiene la audiencia de las redes?» → dentro de cada **medio** (porcentajes **por columna**, `normalize="columns"`)."""),
            C("""por_fila = (pd.crosstab(encuesta["grupo_edad"], encuesta["medio_principal"], normalize="index") * 100).round(1)
por_fila"""),
            M("**Cómo leerlo**: cada fila suma 100. Entre los menores de 30, alrededor del 60 % se informa sobre todo por redes; entre los mayores de 65, apenas un 4 %."),
            C("""por_col = (pd.crosstab(encuesta["grupo_edad"], encuesta["medio_principal"], normalize="columns") * 100).round(1)
por_col"""),
            M("**Cómo leerlo**: ahora cada columna suma 100. De todas las personas que se informan por redes, ¿qué parte es joven? Es otra pregunta y otra cifra. Confundirlas es el error de base más común."),
        ], quiz=[
            unica("Quieres escribir «El X % de los mayores de 65 se informa por televisión». ¿Qué tabla usas?",
                  "Porcentajes por fila (dentro de cada grupo de edad)",
                  [("Porcentajes por columna", "Eso daría qué parte de la audiencia de televisión tiene más de 65."), ("Recuentos brutos", "Necesitas el porcentaje sobre los mayores de 65.")]),
        ]),
        dict(titulo="Gráficos de barras apiladas al 100 %", celdas=[
            M("Una tabla por filas se representa muy bien con barras apiladas al 100 %: cada barra es un grupo y los colores, su composición."),
            C("""por_fila.plot(kind="barh", stacked=True, figsize=(11, 4), colormap="tab10")
plt.xlabel("%")
plt.title("Medio principal según edad (encuesta simulada, n = 1.200)")
plt.legend(bbox_to_anchor=(1, 1))
plt.show()"""),
        ], quiz=[
            unica("En un gráfico de barras apiladas al 100 %, ¿qué suman los segmentos de cada barra?", "100 %",
                  [("El total de la muestra", "Cada barra se normaliza a su propio grupo."), ("Depende del grupo", "Siempre suman 100 %.")]),
        ]),
        dict(titulo="¿Hay relación?", celdas=[
            M("""Si dos variables **no** estuvieran relacionadas, los porcentajes por fila serían parecidos en todas las filas. Si cambian mucho de una fila a otra, hay **asociación**. Ejemplo: ¿quien comparte noticias ha creído más bulos?"""),
            C("""tabla = (pd.crosstab(encuesta["comparte_noticias"], encuesta["ha_creido_bulo"], normalize="index") * 100).round(1)
tabla"""),
            M("""**Cómo leerlo**: casi el 39 % de quienes comparten noticias reconoce haber creído un bulo, frente a algo menos del 20 % de quienes no comparten. Hay asociación.

⚠️ **Asociación no es causalidad**: compartir no tiene por qué *causar* creer bulos; puede que ambas cosas dependan de un tercer factor (por ejemplo, informarse por redes). En el cuaderno 30 verás cómo comprobar si una diferencia así puede deberse al azar."""),
        ], quiz=[
            unica("Si el porcentaje de «Sí» fuera el mismo en todas las filas de una tabla por filas, diríamos que...", "las dos variables no parecen relacionadas",
                  [("están muy relacionadas", "Al revés: la relación se ve cuando los porcentajes cambian."), ("hay un error", "Es un resultado perfectamente posible.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Haz la tabla de contingencia entre provincia y suscripción de pago, con totales.",
             solucion='pd.crosstab(encuesta["provincia"], encuesta["suscripcion_pago"], margins=True)'),
        dict(seccion="sección 2", enunciado="¿Qué porcentaje paga por noticias en cada nivel de estudios? Elige bien el tipo de porcentaje.",
             solucion='(pd.crosstab(encuesta["estudios"], encuesta["suscripcion_pago"], normalize="index") * 100).round(1)'),
        dict(seccion="sección 2", enunciado="Entre quienes han creído un bulo, ¿qué medio principal usan? ¿Es la misma pregunta que «¿qué porcentaje de los que usan redes ha creído un bulo?»?",
             solucion='''print((pd.crosstab(encuesta["ha_creido_bulo"], encuesta["medio_principal"], normalize="index") * 100).round(1))
print((pd.crosstab(encuesta["medio_principal"], encuesta["ha_creido_bulo"], normalize="index") * 100).round(1))''',
             comentario="No: son dos bases distintas (quienes creyeron un bulo frente a quienes usan cada medio)."),
        dict(seccion="sección 3", enunciado="Representa con barras apiladas al 100 % la confianza en los medios agrupada en «Baja (0-3)», «Media (4-6)» y «Alta (7-10)» según el medio principal.",
             solucion='''encuesta["conf_grupo"] = pd.cut(encuesta["confianza_medios"], bins=[-1, 3, 6, 10], labels=["Baja", "Media", "Alta"])
(pd.crosstab(encuesta["medio_principal"], encuesta["conf_grupo"], normalize="index") * 100).plot(kind="barh", stacked=True)
plt.show()'''),
    ],
    resumen=["Una **tabla de contingencia** (`pd.crosstab`) cruza dos variables cualitativas.",
             "La pregunta decide el porcentaje: **por fila** (`normalize=\"index\"`), **por columna** (`\"columns\"`) o sobre el **total** (`\"all\"`).",
             "Confundir la base del porcentaje es el error más común al publicar cruces.",
             "Si los porcentajes por fila cambian mucho entre filas, hay **asociación**; pero asociación no implica causalidad."],
    glosario=[("Tabla de contingencia", "Tabla de doble entrada con los recuentos de dos variables cualitativas."),
              ("Distribución condicionada", "Distribución de una variable dentro de un grupo de la otra."),
              ("Asociación", "Relación estadística entre dos variables."), ("Marginales", "Totales de filas y columnas.")],
    errores=[("Los porcentajes no suman 100 en las filas", "Has usado `normalize=\"columns\"` o `\"all\"`", "Usa `normalize=\"index\"`")],
    seguir="En el cuaderno 13 estudiarás la relación entre variables cuantitativas: correlación y recta de regresión.",
),
# ---------------------------------------------------------------------------
dict(
    num=13, slug="P13_correlacion_y_regresion", unidad=U,
    titulo="Relación entre variables cuantitativas: correlación y regresión",
    datos=["municipios.csv"],
    intro="""«Los municipios con más renta tienen más hogares conectados a internet.» «Donde más se lee la prensa, mayor es la edad media.» Las dos frases describen **correlaciones**. Este cuaderno enseña a medirlas, a dibujar la recta que las resume y, sobre todo, a no confundir correlación con causa.

**Qué necesitas saber antes**: los cuadernos 8 y 10 (media y desviación típica).""",
    aprender=["Dibujar e interpretar un diagrama de dispersión.",
              "Calcular e interpretar el coeficiente de correlación de Pearson.",
              "Ajustar una recta de regresión y usarla para describir la relación.",
              "Explicar por qué correlación no implica causalidad."],
    secciones=[
        dict(titulo="El diagrama de dispersión", celdas=[
            C('muni = pd.read_csv("municipios.csv")\nmuni.head()'),
            M("Cada punto es un municipio: su renta en el eje horizontal y el porcentaje de hogares con internet en el vertical."),
            C("""plt.scatter(muni["renta_media_persona"], muni["hogares_internet_pct"], alpha=0.6, color="steelblue")
plt.xlabel("Renta media por persona (€)")
plt.ylabel("Hogares con internet (%)")
plt.title("Renta e internet en 140 municipios (datos simulados)")
plt.show()"""),
            M("**Cómo leerlo**: la nube sube de izquierda a derecha: los municipios con más renta tienden a tener más hogares conectados. Es una relación **positiva** y aproximadamente **lineal**."),
        ], quiz=[
            unica("En un diagrama de dispersión, una nube que baja de izquierda a derecha indica...", "una relación negativa",
                  [("una relación positiva", "Positiva sería si sube."), ("que no hay relación", "Sin relación, la nube no tendría dirección.")]),
        ]),
        dict(titulo="El coeficiente de correlación", celdas=[
            M("""El **coeficiente de correlación de Pearson** ($r$) mide la fuerza de la relación **lineal**. Va de −1 a 1:

| $r$ | Lectura |
| :-- | :-- |
| cerca de 1 | relación positiva fuerte |
| cerca de 0 | sin relación lineal |
| cerca de −1 | relación negativa fuerte |"""),
            C("""print("Renta - internet:", round(muni["renta_media_persona"].corr(muni["hogares_internet_pct"]), 2))
print("Renta - paro:    ", round(muni["renta_media_persona"].corr(muni["tasa_paro"]), 2))
cols = ["renta_media_persona", "tasa_paro", "edad_media", "hogares_internet_pct", "lectores_prensa_pct"]
muni[cols].corr().round(2)"""),
            M("**Cómo leerlo**: la renta se relaciona positivamente con internet y negativamente con el paro. La edad media y los lectores de prensa tienen la correlación más fuerte de la tabla."),
            M("⚠️ $r$ solo mide relaciones **lineales**. Una relación en forma de U puede dar $r \\approx 0$. **Mira siempre el gráfico.**"),
        ], quiz=[
            unica("Si r = −0,66 entre renta y paro, ¿qué significa?", "Los municipios con más renta tienden a tener menos paro",
                  [("Más renta causa menos paro", "La correlación no demuestra causa."), ("No hay relación", "−0,66 es una relación moderada-fuerte.")]),
        ]),
        dict(titulo="La recta de regresión", celdas=[
            M("""La **recta de regresión** es la recta que mejor resume la nube: $y = a + b\\,x$. La **pendiente** $b$ dice cuánto cambia $y$, en promedio, cuando $x$ aumenta una unidad."""),
            C("""x = muni["renta_media_persona"]
y = muni["hogares_internet_pct"]
b, a = np.polyfit(x, y, 1)
print(f"Recta: internet = {a:.1f} + {b:.5f} × renta")
print(f"Por cada 1.000 € más de renta, {b * 1000:.1f} puntos más de hogares con internet")"""),
            C("""plt.scatter(x, y, alpha=0.5, color="steelblue")
xs = np.linspace(x.min(), x.max(), 100)
plt.plot(xs, a + b * xs, color="firebrick", label="Recta de regresión")
plt.xlabel("Renta media por persona (€)")
plt.ylabel("Hogares con internet (%)")
plt.legend()
plt.show()"""),
            M("""El **coeficiente de determinación** $R^2 = r^2$ indica qué parte de la variación de $y$ «se explica» por la recta. Si $r = 0{,}64$, entonces $R^2 \\approx 0{,}41$: la renta da cuenta de un 41 % de las diferencias de conexión entre municipios; el resto depende de otras cosas."""),
        ], quiz=[
            unica("La pendiente de una recta es 0,9 (paro en puntos frente a edad media en años). ¿Qué significa?",
                  "Por cada año más de edad media, el paro es 0,9 puntos mayor en promedio",
                  [("La correlación es 0,9", "La pendiente y la correlación son cosas distintas."), ("El 90 % del paro depende de la edad", "Eso sería un R² de 0,9.")]),
        ]),
        dict(titulo="Correlación no es causalidad", celdas=[
            M("""Los municipios con más lectores de prensa tienen más edad media. ¿Leer prensa envejece? Evidentemente no: la gente mayor lee más prensa. Y otras correlaciones esconden una **tercera variable** que mueve a las dos (una **variable de confusión**).

Antes de escribir que A causa B, pregúntate:
1. ¿Podría ser al revés (B causa A)?
2. ¿Hay una tercera variable que explique las dos?
3. ¿Es casualidad? (con muchos cruces, alguno sale por azar)

Solo un **experimento** o un diseño cuidadoso permite hablar de causas."""),
            C("""plt.scatter(muni["edad_media"], muni["lectores_prensa_pct"], alpha=0.6, color="darkorange")
plt.xlabel("Edad media (años)")
plt.ylabel("Lectores de prensa (%)")
plt.title(f"r = {muni['edad_media'].corr(muni['lectores_prensa_pct']):.2f}: ¿la prensa envejece?")
plt.show()"""),
        ], quiz=[
            varias("Encuentras que los municipios con más farmacias tienen más fallecimientos. ¿Qué explicaciones debes considerar?", [
                ("Una tercera variable: los municipios grandes tienen más farmacias y más fallecimientos", True, "¡Correcto! El tamaño de la población."),
                ("Las farmacias causan fallecimientos", False, "No hay ningún motivo para pensarlo."),
                ("Conviene usar tasas por habitante en lugar de cifras absolutas", True, "¡Correcto!")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Dibuja el diagrama de dispersión entre la renta media y la tasa de paro.",
             solucion='''plt.scatter(muni["renta_media_persona"], muni["tasa_paro"], alpha=0.6)
plt.xlabel("Renta"); plt.ylabel("Paro (%)")
plt.show()'''),
        dict(seccion="sección 2", enunciado="¿Qué pareja de variables de la tabla tiene la correlación más cercana a cero?",
             solucion='muni[cols].corr().round(2)'),
        dict(seccion="sección 3", enunciado="Ajusta la recta del paro en función de la renta. ¿Cuánto baja el paro, en promedio, por cada 1.000 € más de renta?",
             solucion='''b, a = np.polyfit(muni["renta_media_persona"], muni["tasa_paro"], 1)
b * 1000'''),
        dict(seccion="sección 3", enunciado="Calcula el R² de esa recta.",
             solucion='muni["renta_media_persona"].corr(muni["tasa_paro"]) ** 2'),
        dict(seccion="sección 4", enunciado="Escribe un titular honesto y otro engañoso con la correlación entre edad media y lectores de prensa.",
             comentario="Honesto: «Los municipios más envejecidos son los que más leen prensa». Engañoso: «Leer prensa hace que un municipio envejezca»."),
    ],
    resumen=["El **diagrama de dispersión** es el primer paso para estudiar dos variables cuantitativas.",
             "El **coeficiente de correlación** $r$ (de −1 a 1) mide la fuerza de la relación **lineal**; mira siempre el gráfico.",
             "La **recta de regresión** ($y = a + b\\,x$) resume la relación; la pendiente $b$ es el cambio medio de $y$ por unidad de $x$.",
             "$R^2 = r^2$ es la parte de la variación de $y$ asociada a $x$.",
             "**Correlación no implica causalidad**: piensa en la causa inversa, las variables de confusión y el azar."],
    glosario=[("Diagrama de dispersión", "Gráfico de puntos de dos variables cuantitativas."), ("Correlación de Pearson", "Medida de la relación lineal entre dos variables, de −1 a 1."),
              ("Recta de regresión", "Recta que mejor resume la relación lineal."), ("Variable de confusión", "Tercera variable que influye en las dos que se comparan."),
              ("R²", "Proporción de la variación explicada por la recta.")],
    errores=[("`np.polyfit` da error con NaN", "Hay datos que faltan", "Elimina antes las filas incompletas con `dropna()`")],
    seguir="Con esto termina la unidad 2. En el cuaderno 14 empieza la unidad de números índice: tasas de variación e índices simples.",
),
]
