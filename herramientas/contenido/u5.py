from _comun import C, M, numerica, unica, varias

U = "5. Conceptos básicos de inferencia estadística"

CUADERNOS = [
# ---------------------------------------------------------------------------
dict(
    num=25, slug="P25_poblacion_muestra_y_muestreo", unidad=U,
    titulo="Población, muestra y tipos de muestreo",
    datos=["encuesta_medios.csv"],
    intro="""Ningún instituto pregunta a todo el país: entrevista a 1.000 o 2.000 personas y de ahí saca conclusiones para millones. Que eso funcione depende de **cómo** se elige a esas personas. Una encuesta de 1.000 entrevistas bien hecha vale mucho más que una votación en redes con 50.000 respuestas. Este cuaderno explica por qué.

**Qué necesitas saber antes**: la unidad 4, en especial los cuadernos 20 y 23.""",
    aprender=["Distinguir población, muestra, parámetro y estadístico.",
              "Describir los principales tipos de muestreo y cuándo se usa cada uno.",
              "Reconocer los sesgos de selección, de no respuesta y de autoselección.",
              "Entender para qué sirve ponderar una muestra."],
    secciones=[
        dict(titulo="Población, muestra, parámetro y estadístico", celdas=[
            M("""| Concepto | Qué es | Ejemplo |
| :-- | :-- | :-- |
| **Población** | Todo el grupo sobre el que se quiere saber algo | Residentes mayores de 18 años en la Comunitat Valenciana |
| **Censo** | Estudiar a toda la población | Las elecciones son un censo de los votantes |
| **Muestra** | Parte de la población que se estudia | 1.200 personas entrevistadas |
| **Parámetro** | Valor (desconocido) en la población | % real que se informa por redes |
| **Estadístico** | Valor calculado en la muestra | % de los entrevistados que se informa por redes |

La **inferencia** consiste en usar el estadístico para decir algo del parámetro, **con una medida de su error**."""),
            M("""**Qué vamos a hacer**: para poder comprobar lo que hacemos, en este cuaderno trataremos las 1.200 personas de la encuesta como si fueran **toda la población**. Así conocemos el «parámetro» y podemos ver cuánto se equivocan distintas muestras."""),
            C("""poblacion = pd.read_csv("encuesta_medios.csv")
parametro = (poblacion["medio_principal"] == "Redes sociales").mean()
print(f"Parámetro (en la 'población'): {parametro:.3f}")"""),
        ], quiz=[
            unica("El 23 % de los 1.000 entrevistados en una encuesta dice informarse por redes. Ese 23 % es...", "un estadístico",
                  [("un parámetro", "El parámetro sería el porcentaje en toda la población, que no conocemos."), ("un censo", "Un censo estudiaría a toda la población.")]),
        ]),
        dict(titulo="Muestreo aleatorio simple y estratificado", celdas=[
            M("""En el **muestreo aleatorio simple** (MAS) cada persona tiene la misma probabilidad de ser elegida. Con Pandas: `sample(n)`."""),
            C("""rng = np.random.default_rng(25)
muestra = poblacion.sample(100, random_state=1)
print(f"Estadístico en una muestra de 100: {(muestra['medio_principal'] == 'Redes sociales').mean():.3f}")

estimaciones = [(poblacion.sample(100, random_state=i)["medio_principal"] == "Redes sociales").mean() for i in range(5)]
print("Cinco muestras distintas:", np.round(estimaciones, 3))"""),
            M("""Cada muestra da un resultado distinto: es el **error muestral**, que veremos en el cuaderno 26.

En el **muestreo estratificado** la población se divide en grupos (**estratos**: provincias, grupos de edad) y se extrae una muestra de cada uno. Garantiza que todos los grupos estén representados y suele reducir el error. Es lo que hacen el CIS y casi todos los institutos."""),
            C("""prop = poblacion["provincia"].value_counts(normalize=True)
n_total = 100
estratificada = pd.concat([poblacion[poblacion["provincia"] == prov].sample(round(n_total * p), random_state=1)
                           for prov, p in prop.items()])
print(estratificada["provincia"].value_counts())"""),
            M("""Otros tipos que verás en las fichas técnicas:

- **Por conglomerados**: se eligen al azar grupos enteros (municipios, secciones censales) y dentro de ellos a las personas. Abarata el trabajo de campo.
- **Por cuotas**: se fijan cuántas personas de cada sexo y edad hay que entrevistar, pero la elección final no es aleatoria.
- **Polietápico**: combina varios (primero municipios, luego hogares, luego personas)."""),
        ], quiz=[
            unica("Divides la población por provincias y sacas una muestra aleatoria de cada una, proporcional a su tamaño. Es un muestreo...", "estratificado",
                  [("por conglomerados", "Por conglomerados se eligen grupos enteros al azar."), ("aleatorio simple", "En el simple no se divide la población en grupos.")]),
        ]),
        dict(titulo="Sesgos: cuando la muestra no se parece a la población", celdas=[
            M("""Un **sesgo** es un error que va siempre en la misma dirección y **no disminuye aunque aumente la muestra**. Los más frecuentes:

| Sesgo | Qué pasa | Ejemplo |
| :-- | :-- | :-- |
| **De selección** | Algunos grupos tienen más probabilidad de entrar | Encuesta solo por teléfono fijo: faltan jóvenes |
| **De autoselección** | Las personas deciden si participan | Votaciones en redes o en la web del diario |
| **De no respuesta** | Quienes no contestan son distintos | Los más desconfiados no responden |
| **De deseabilidad social** | Se responde lo que «queda bien» | Se declara más lectura de la que hay |"""),
            M("""**Qué vamos a hacer**: simular una encuesta en redes sociales. Solo responde quien se informa por redes (que participa mucho más) o quien comparte noticias. Aunque recojamos muchas respuestas, el resultado está sesgado."""),
            C("""p_participar = np.where(poblacion["medio_principal"] == "Redes sociales", 0.6, 0.05)
p_participar = p_participar + np.where(poblacion["comparte_noticias"] == "Sí", 0.1, 0)
responde = rng.random(len(poblacion)) < p_participar
encuesta_redes = poblacion[responde]
print("Respuestas recogidas:", len(encuesta_redes))
print(f"% que se informa por redes según la encuesta en redes: {(encuesta_redes['medio_principal'] == 'Redes sociales').mean():.1%}")
print(f"Valor real (parámetro): {parametro:.1%}")"""),
            M("**Qué ha pasado**: la «encuesta» en redes multiplica por más de tres el porcentaje real. Más respuestas no lo arreglan: el problema es **quién** responde. Por eso una votación en redes **nunca** es una encuesta, y no debe publicarse como tal."),
        ], quiz=[
            unica("Un diario hace una votación en su web con 30.000 participantes. ¿Qué problema tiene?", "Autoselección: participan quienes quieren y no representan a la población",
                  [("Ninguno: 30.000 es una muestra enorme", "El tamaño no corrige el sesgo."), ("El margen de error es muy grande", "El problema no es el margen: el resultado está sesgado.")]),
        ]),
        dict(titulo="Ponderar una muestra", celdas=[
            M("""Si la muestra tiene, por ejemplo, demasiados universitarios, se puede **ponderar**: dar a cada persona un peso igual a (proporción en la población) / (proporción en la muestra). Así los grupos poco representados cuentan más. Corrige desequilibrios **conocidos**, pero no los sesgos de grupos que ni siquiera están en la muestra."""),
            C("""# Muestra con demasiados universitarios
rng_p = np.random.default_rng(1)
p_entrar = np.where(poblacion["estudios"] == "Universitarios", 0.9, 0.3)
sesgada = poblacion[rng_p.random(len(poblacion)) < p_entrar].copy()

prop_pob = poblacion["estudios"].value_counts(normalize=True)
prop_mue = sesgada["estudios"].value_counts(normalize=True)
sesgada["peso"] = sesgada["estudios"].map(prop_pob / prop_mue)

real = (poblacion["suscripcion_pago"] == "Sí").mean()
sin_pesos = (sesgada["suscripcion_pago"] == "Sí").mean()
con_pesos = np.average(sesgada["suscripcion_pago"] == "Sí", weights=sesgada["peso"])
print(f"% que paga por noticias. Real: {real:.1%}   Muestra sin ponderar: {sin_pesos:.1%}   Ponderada: {con_pesos:.1%}")"""),
        ], quiz=[
            unica("En la muestra hay un 50 % de universitarios y en la población un 33 %. ¿Qué peso reciben los universitarios al ponderar?", "Menos de 1 (0,33 / 0,50 = 0,66)",
                  [("Más de 1", "Están sobrerrepresentados: su peso debe bajar."), ("Exactamente 1", "Solo si las proporciones coinciden.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula en la «población» el parámetro «% que paga por noticias» y estímalo con una muestra aleatoria simple de 200 personas.",
             solucion='''print((poblacion["suscripcion_pago"] == "Sí").mean())
print((poblacion.sample(200, random_state=7)["suscripcion_pago"] == "Sí").mean())'''),
        dict(seccion="sección 2", enunciado="Extrae una muestra estratificada de 120 personas por grupo de estudios, proporcional al tamaño de cada grupo.",
             solucion='''prop = poblacion["estudios"].value_counts(normalize=True)
pd.concat([poblacion[poblacion["estudios"] == e].sample(round(120 * p), random_state=2) for e, p in prop.items()])["estudios"].value_counts()'''),
        dict(seccion="sección 3", enunciado="Busca la ficha técnica de una encuesta publicada este mes (CIS u otro instituto). Anota: universo, tamaño de muestra, tipo de muestreo, método de entrevista y fechas.",
             comentario="Ejercicio abierto. Si una noticia sobre una encuesta no da estos datos, el lector no puede valorar su calidad."),
        dict(seccion="sección 3", enunciado="Repite la simulación de la encuesta en redes con probabilidades de participación de 0,3 y 0,05. ¿Sigue habiendo sesgo?",
             solucion='''r = rng.random(len(poblacion)) < np.where(poblacion["medio_principal"] == "Redes sociales", 0.3, 0.05)
(poblacion[r]["medio_principal"] == "Redes sociales").mean()'''),
    ],
    resumen=["La **inferencia** usa un **estadístico** de una **muestra** para conocer un **parámetro** de la **población**.",
             "**Aleatorio simple**: todos con la misma probabilidad. **Estratificado**: una muestra por grupo. **Conglomerados**: grupos enteros al azar. **Cuotas**: no aleatorio.",
             "Un **sesgo** no se corrige aumentando la muestra; las votaciones en redes tienen **sesgo de autoselección**.",
             "**Ponderar** corrige desequilibrios conocidos de la muestra, no los grupos ausentes.",
             "Exige siempre la **ficha técnica**: universo, tamaño, tipo de muestreo, método y fechas."],
    glosario=[("Población", "Conjunto completo sobre el que se quiere saber algo."), ("Muestra", "Parte de la población que se observa."),
              ("Parámetro", "Valor en la población, normalmente desconocido."), ("Estadístico", "Valor calculado con la muestra."),
              ("Sesgo de autoselección", "Error que aparece cuando los participantes deciden ellos mismos si participan."),
              ("Ficha técnica", "Descripción de cómo se ha hecho una encuesta.")],
    seguir="En el cuaderno 26 verás cuánto se equivoca una muestra por puro azar: la distribución muestral y el error estadístico.",
),
# ---------------------------------------------------------------------------
dict(
    num=26, slug="P26_distribucion_muestral_y_error", unidad=U,
    titulo="Distribución muestral y error estadístico (simulación de Monte Carlo)",
    datos=["salarios_redaccion.csv", "verificaciones.csv"],
    intro="""Si cinco institutos hacen la misma encuesta el mismo día, darán cinco resultados distintos aunque todos trabajen bien. Esa variación es el **error muestral**, y se puede medir. En este cuaderno lo veremos con una **simulación de Monte Carlo**: repetir miles de veces una encuesta en el ordenador y mirar cómo se reparten sus resultados.

**Qué necesitas saber antes**: los cuadernos 24 y 25.""",
    aprender=["Simular la distribución muestral de una proporción y de una media.",
              "Calcular e interpretar el error típico.",
              "Ver cómo disminuye el error al aumentar la muestra.",
              "Entender el teorema central del límite."],
    secciones=[
        dict(titulo="Muchas encuestas imaginarias", celdas=[
            M("""**Qué vamos a hacer**: imaginar una población en la que el **34 %** votaría al partido A. Hacemos 10.000 encuestas de 1.000 personas y guardamos el porcentaje de A en cada una. Ese conjunto de resultados es la **distribución muestral** de la proporción."""),
            C("""rng = np.random.default_rng(26)
p_real = 0.34
n = 1000
resultados = rng.binomial(n, p_real, size=10_000) / n

plt.hist(resultados * 100, bins=40, color="steelblue", edgecolor="white")
plt.axvline(p_real * 100, color="firebrick", label="Valor real: 34 %")
plt.xlabel("% de voto a A en cada encuesta")
plt.ylabel("Número de encuestas")
plt.title("10.000 encuestas de 1.000 personas (simulación)")
plt.legend()
plt.show()
print(f"Media de las encuestas: {resultados.mean():.4f}   Desviación típica: {resultados.std():.4f}")"""),
            M("**Cómo leerlo**: las encuestas se reparten en forma de campana alrededor del 34 %. La mayoría cae entre el 31 % y el 37 %; muy pocas se alejan más. La desviación típica de esta distribución (unos 1,5 puntos) se llama **error típico**."),
        ], quiz=[
            unica("¿Qué es la distribución muestral de una proporción?", "Cómo se reparten las proporciones obtenidas en muchas muestras posibles",
                  [("La distribución de los datos de una muestra", "Eso es la distribución de la muestra, no del estadístico."), ("La proporción real en la población", "Eso es el parámetro.")]),
        ]),
        dict(titulo="El error típico", celdas=[
            M("""El **error típico** de una proporción se calcula sin simular:

$$EE(\\hat{p}) = \\sqrt{\\frac{p(1-p)}{n}}$$

y el de una media, $EE(\\bar{x}) = \\sigma / \\sqrt{n}$. Fíjate en la $\\sqrt{n}$: para **reducir el error a la mitad hay que cuadruplicar la muestra**."""),
            C("""print(f"Error típico teórico: {np.sqrt(p_real * (1 - p_real) / n):.4f}   simulado: {resultados.std():.4f}")
for n_ in [250, 1000, 4000]:
    print(f"n = {n_:>5}: error típico = {np.sqrt(p_real * (1 - p_real) / n_) * 100:.2f} puntos")"""),
            C("""for n_, color in [(250, "lightgrey"), (1000, "steelblue"), (4000, "navy")]:
    r = rng.binomial(n_, p_real, size=10_000) / n_ * 100
    plt.hist(r, bins=50, alpha=0.6, color=color, label=f"n = {n_}", density=True)
plt.axvline(34, color="firebrick")
plt.legend()
plt.xlabel("% de voto a A")
plt.title("Cuanto mayor la muestra, más estrecha la campana")
plt.show()"""),
        ], quiz=[
            unica("Si una encuesta pasa de 500 a 2.000 entrevistas, su error típico...", "se reduce a la mitad",
                  [("se reduce a la cuarta parte", "Se divide por √4 = 2, no por 4."), ("no cambia", "Disminuye con la raíz del tamaño.")]),
        ]),
        dict(titulo="El teorema central del límite", celdas=[
            M("""¿Y si la variable no es normal, como los salarios? El **teorema central del límite** dice que, con muestras suficientemente grandes, **la media de la muestra se distribuye aproximadamente como una normal**, sea cual sea la forma de la variable. Lo comprobamos con los salarios (muy asimétricos):"""),
            C("""sal = pd.read_csv("salarios_redaccion.csv")["salario_bruto_anual"]
fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))
axes[0].hist(sal, bins=30, color="grey")
axes[0].set_title("Salarios (asimétricos)")
for ax, n_ in zip(axes[1:], [5, 50]):
    medias = [sal.sample(n_, replace=True, random_state=i).mean() for i in range(3000)]
    ax.hist(medias, bins=40, color="steelblue")
    ax.set_title(f"Medias de muestras de {n_}")
plt.tight_layout()
plt.show()"""),
            M("**Qué ha pasado**: con muestras de 5 la distribución de la media aún arrastra algo de asimetría; con muestras de 50 ya es una campana. Por eso podemos usar la normal para calcular el error de medias y proporciones aunque los datos no sean normales."),
        ], quiz=[
            unica("Según el teorema central del límite, con muestras grandes...", "la media muestral sigue aproximadamente una normal",
                  [("los datos se vuelven normales", "Los datos siguen teniendo su forma; es la media la que se vuelve normal."), ("el error desaparece", "El error disminuye, pero no desaparece.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Simula 10.000 encuestas de 400 personas con un 50 % real de «sí». ¿Qué proporción de encuestas da un resultado por debajo del 45 %?",
             solucion='''r = rng.binomial(400, 0.5, size=10_000) / 400
(r < 0.45).mean()'''),
        dict(seccion="sección 2", enunciado="Calcula el error típico (en puntos) de una encuesta de 1.500 personas para un partido con un 10 % de voto y para otro con un 50 %. ¿Cuál tiene más error?",
             solucion='''for p_ in [0.1, 0.5]:
    print(p_, np.sqrt(p_ * (1 - p_) / 1500) * 100)''', comentario="El del 50 %: el error es máximo cuando p = 0,5."),
        dict(seccion="sección 2", enunciado="¿Cuántas entrevistas hacen falta para que el error típico de una proporción del 50 % sea de 1 punto? Prueba valores de n.",
             solucion='''for n_ in [1000, 2000, 2500, 3000]:
    print(n_, np.sqrt(0.25 / n_) * 100)'''),
        dict(seccion="sección 3", enunciado="Repite la simulación del teorema central del límite con la variable «veces compartido» de `verificaciones.csv`, aún más asimétrica, con muestras de 5, 50 y 500. ¿Con qué tamaño ves una campana?",
             solucion='''vc = pd.read_csv("verificaciones.csv")["veces_compartido"]
for n_ in [5, 50, 500]:
    medias = [vc.sample(n_, replace=True, random_state=i).mean() for i in range(2000)]
    plt.hist(medias, bins=40)
    plt.title(f"n = {n_}")
    plt.show()''',
             comentario="Con asimetrías extremas hace falta una muestra bastante mayor que con los salarios."),
    ],
    resumen=["La **distribución muestral** describe cómo varía un estadístico de una muestra a otra.",
             "Su desviación típica es el **error típico**: $\\sqrt{p(1-p)/n}$ para proporciones y $\\sigma/\\sqrt{n}$ para medias.",
             "El error disminuye con $\\sqrt{n}$: **cuadruplicar la muestra reduce el error a la mitad**.",
             "**Teorema central del límite**: con muestras grandes, la media muestral es aproximadamente normal.",
             "La **simulación de Monte Carlo** permite ver todo esto repitiendo miles de muestras imaginarias."],
    glosario=[("Distribución muestral", "Distribución de un estadístico en todas las muestras posibles."), ("Error típico", "Desviación típica de la distribución muestral."),
              ("Error muestral", "Diferencia entre el estadístico y el parámetro debida al azar del muestreo."),
              ("Teorema central del límite", "Con muestras grandes, la media muestral se distribuye aproximadamente como una normal."),
              ("Monte Carlo", "Método que usa simulaciones aleatorias para estudiar un problema.")],
    seguir="En el cuaderno 27 convertirás el error típico en el margen de error de una encuesta.",
),
# ---------------------------------------------------------------------------
dict(
    num=27, slug="P27_margen_de_error_de_una_encuesta", unidad=U,
    titulo="Intervalo de confianza para una proporción: el margen de error",
    datos=["sondeos.csv"], imports_extra="from scipy import stats\n",
    intro="""«Error muestral: ±3,1 puntos para un nivel de confianza del 95 %». Esa línea de la ficha técnica es la clave para leer cualquier encuesta. Con ella sabrás cuándo una diferencia es noticia y cuándo es un **empate técnico**, y por qué los resultados de un subgrupo (los jóvenes, una provincia) son mucho menos precisos que el total.

**Qué necesitas saber antes**: los cuadernos 24 y 26.""",
    aprender=["Calcular el margen de error y el intervalo de confianza de una proporción.",
              "Interpretar correctamente el nivel de confianza.",
              "Decidir cuándo dos resultados de una encuesta son un empate técnico.",
              "Calcular el margen de error de un subgrupo."],
    secciones=[
        dict(titulo="El margen de error", celdas=[
            M("""El **intervalo de confianza** al 95 % para una proporción es:

$$\\hat{p} \\pm 1{,}96 \\sqrt{\\frac{\\hat{p}(1-\\hat{p})}{n}}$$

La parte de la derecha es el **margen de error**. Las fichas técnicas suelen dar el margen «en el peor caso», con $p = 0{,}5$, que es el mayor posible."""),
            C("""def margen(p, n, confianza=0.95):
    z = stats.norm.ppf(1 - (1 - confianza) / 2)     # 1,96 para el 95 %
    return z * np.sqrt(p * (1 - p) / n)

def intervalo(p, n, confianza=0.95):
    e = margen(p, n, confianza)
    return p - e, p + e

print(f"Margen para n = 1.000, p = 0,5: ±{margen(0.5, 1000) * 100:.1f} puntos")
inf, sup = intervalo(0.34, 1000)
print(f"Partido con 34 % en 1.000 entrevistas: entre {inf:.1%} y {sup:.1%}")"""),
        ], quiz=[
            numerica("Calcula el margen de error (en puntos, un decimal) de una encuesta de 2.400 personas con p = 0,5 al 95 %.", 1.9, 2.05,
                     ok="¡Correcto! 1,96 × √(0,25 / 2.400) ≈ 0,020 → ±2,0 puntos."),
        ]),
        dict(titulo="Qué significa «95 % de confianza»", celdas=[
            M("""El 95 % **no** es la probabilidad de que el valor real esté en *este* intervalo concreto. Significa que, si repitiéramos la encuesta muchas veces, el **95 % de los intervalos** así calculados contendría el valor real. Lo vemos con 100 encuestas simuladas:"""),
            C("""rng = np.random.default_rng(27)
p_real, n = 0.34, 1000
fallan = 0
for i in range(100):
    p_hat = rng.binomial(n, p_real) / n
    lo, hi = intervalo(p_hat, n)
    acierta = lo <= p_real <= hi
    fallan += not acierta
    plt.plot([lo * 100, hi * 100], [i, i], color="steelblue" if acierta else "firebrick")
plt.axvline(34, color="black")
plt.xlabel("% de voto a A")
plt.title(f"100 intervalos al 95 %: {fallan} no contienen el valor real (en rojo)")
plt.show()"""),
            M("Subir la confianza al 99 % ensancha el intervalo (z = 2,58). Es un compromiso entre **seguridad** y **precisión**."),
            C("""for c in [0.90, 0.95, 0.99]:
    print(f"Confianza {c:.0%}: margen ±{margen(0.5, 1000, c) * 100:.1f} puntos")"""),
        ], quiz=[
            unica("¿Qué significa un intervalo de confianza al 95 %?", "Que el procedimiento acierta en el 95 % de las muestras posibles",
                  [("Que el 95 % de la población está dentro del intervalo", "El intervalo es para el parámetro, no para las personas."), ("Que el resultado es correcto al 95 %", "Es una propiedad del método, no del resultado concreto.")]),
        ]),
        dict(titulo="Empate técnico", celdas=[
            C('sondeos = pd.read_csv("sondeos.csv")\nsondeos.tail()'),
            M("""Si los intervalos de dos candidaturas **se solapan claramente**, la encuesta no permite decir quién va delante: es un **empate técnico**. (La forma exacta de comparar dos porcentajes de la misma encuesta la verás en el cuaderno 30; el solapamiento es una regla práctica y algo conservadora.)"""),
            C("""ultimo = sondeos.iloc[-1]
n = ultimo["tamano_muestra"]
for cand in ["A", "B"]:
    p = ultimo[f"pct_{cand}"] / 100
    lo, hi = intervalo(p, n)
    print(f"{cand}: {p:.1%}  (entre {lo:.1%} y {hi:.1%})")"""),
            C("""sondeos["margen"] = margen(0.5, sondeos["tamano_muestra"]) * 100
plt.errorbar(range(len(sondeos)), sondeos["pct_A"], yerr=sondeos["margen"], fmt="o", label="A", alpha=0.7)
plt.errorbar(np.arange(len(sondeos)) + 0.3, sondeos["pct_B"], yerr=sondeos["margen"], fmt="o", label="B", alpha=0.7)
plt.xlabel("Sondeo (en orden de fecha)")
plt.ylabel("% de voto")
plt.legend()
plt.title("Sondeos simulados con su margen de error")
plt.show()"""),
            M("**Cómo leerlo**: casi todos los sondeos tienen las barras de A y B solapadas. Un titular como «B adelanta a A» basado en uno solo de ellos sería engañoso; lo correcto es hablar de empate técnico o mirar la **media de muchos sondeos**."),
        ], quiz=[
            unica("Una encuesta da 36 % a A y 34 % a B con un margen de ±3 puntos. ¿Qué titular es correcto?", "«Empate técnico entre A y B»",
                  [("«A gana a B por dos puntos»", "La diferencia es menor que el margen."), ("«A gana por un 2 %»", "Además de ser un empate técnico, son puntos, no porcentaje.")]),
        ]),
        dict(titulo="Los subgrupos tienen más error", celdas=[
            M("""Si la encuesta tiene 1.000 entrevistas pero solo 150 son jóvenes, el margen para los jóvenes se calcula con **n = 150**, y es mucho mayor. Las noticias que destacan «lo que opinan los jóvenes» a partir de una encuesta general deben decirlo."""),
            C("""for grupo, n_g in [("Total", 1000), ("Mayores de 65", 260), ("De 18 a 29", 150), ("Castellón", 60)]:
    print(f"{grupo:>15} (n = {n_g:>4}): ±{margen(0.5, n_g) * 100:.1f} puntos")"""),
        ], quiz=[
            unica("En una encuesta de 1.200 personas, 80 son de una provincia pequeña. ¿Qué margen hay que usar para hablar de esa provincia?", "El calculado con n = 80, mucho mayor",
                  [("El de la encuesta total", "El total tiene más casos que la provincia."), ("No tiene margen", "Toda estimación muestral tiene margen de error.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula el intervalo al 95 % para un partido que obtiene el 12 % en una encuesta de 800 personas.",
             solucion='intervalo(0.12, 800)'),
        dict(seccion="sección 2", enunciado="Repite la simulación de los 100 intervalos al 90 %. ¿Cuántos fallan ahora, aproximadamente?",
             comentario="Cambia `intervalo(p_hat, n)` por `intervalo(p_hat, n, 0.90)`: deberían fallar unos 10 de cada 100."),
        dict(seccion="sección 3", enunciado="¿En cuántos sondeos la diferencia entre A y B es mayor que dos veces el margen (es decir, no se solapan los intervalos)?",
             solucion='((sondeos["pct_A"] - sondeos["pct_B"]).abs() > 2 * sondeos["margen"]).sum()'),
        dict(seccion="sección 3", enunciado="Calcula la media de todos los sondeos para A y B y su margen aproximado, sumando todas las muestras. ¿Sigue siendo un empate?",
             solucion='''n_tot = sondeos["tamano_muestra"].sum()
pa = np.average(sondeos["pct_A"], weights=sondeos["tamano_muestra"]) / 100
pb = np.average(sondeos["pct_B"], weights=sondeos["tamano_muestra"]) / 100
print(pa, pb, margen(0.5, n_tot))''',
             comentario="Promediar sondeos reduce mucho el margen, siempre que los sondeos no compartan el mismo sesgo."),
        dict(seccion="sección 4", enunciado="Redacta la frase de ficha técnica de una encuesta de 1.600 entrevistas al 95 %.",
             solucion='print(f"Error muestral: ±{margen(0.5, 1600) * 100:.1f} puntos para un nivel de confianza del 95 % y p = q = 0,5")'),
    ],
    resumen=["**Intervalo al 95 %** para una proporción: $\\hat{p} \\pm 1{,}96\\sqrt{\\hat{p}(1-\\hat{p})/n}$; la parte ± es el **margen de error**.",
             "La ficha técnica da el margen con **p = 0,5**, el mayor posible.",
             "«95 % de confianza» es una propiedad del **método**: acierta en el 95 % de las muestras posibles.",
             "Si las diferencias son menores que el margen, es un **empate técnico**.",
             "Los **subgrupos** tienen menos casos y **más margen** de error."],
    glosario=[("Intervalo de confianza", "Rango de valores plausibles para un parámetro."), ("Margen de error", "Semiamplitud del intervalo de confianza."),
              ("Nivel de confianza", "Proporción de intervalos que contendrían el parámetro si se repitiera el muestreo."),
              ("Empate técnico", "Situación en la que la diferencia entre dos resultados es menor que el error de la encuesta.")],
    errores=[("El margen sale en tanto por uno (0,031)", "Falta multiplicar por 100", "Multiplica por 100 para expresarlo en puntos")],
    seguir="En el cuaderno 28 harás intervalos para medias y calcularás cuántas entrevistas necesita una encuesta.",
),
# ---------------------------------------------------------------------------
dict(
    num=28, slug="P28_intervalo_para_una_media_y_tamano_de_muestra", unidad=U,
    titulo="Intervalo de confianza para una media y tamaño de muestra",
    datos=["encuesta_medios.csv"], imports_extra="from scipy import stats\n",
    intro="""«Los españoles dedican de media 54 minutos al día a las noticias.» ¿Con qué precisión? Y si un medio quiere encargar una encuesta con un margen de ±2 puntos, ¿cuántas entrevistas debe pagar? Este cuaderno responde a las dos preguntas: el **intervalo de confianza para una media** y el **cálculo del tamaño de muestra**.

**Qué necesitas saber antes**: el cuaderno 27.""",
    aprender=["Calcular un intervalo de confianza para una media con la t de Student.",
              "Comparar intervalos de varios grupos en un gráfico.",
              "Calcular el tamaño de muestra necesario para un margen de error dado.",
              "Entender por qué el tamaño de la población apenas influye."],
    secciones=[
        dict(titulo="Intervalo para una media", celdas=[
            M("""Para una media, el intervalo al 95 % es:

$$\\bar{x} \\pm t_{n-1} \\cdot \\frac{s}{\\sqrt{n}}$$

donde $t_{n-1}$ es un valor de la **t de Student** (muy parecido a 1,96 cuando $n$ es grande), porque además de la media estimamos la desviación típica."""),
            C("""enc = pd.read_csv("encuesta_medios.csv")
minutos = enc["minutos_noticias_dia"].dropna()
n = len(minutos)
media, s = minutos.mean(), minutos.std()
t = stats.t.ppf(0.975, df=n - 1)
ee = s / np.sqrt(n)
print(f"n = {n}, media = {media:.1f} min, s = {s:.1f}, t = {t:.3f}")
print(f"IC 95 %: entre {media - t * ee:.1f} y {media + t * ee:.1f} minutos")"""),
            M("Con `scipy` se obtiene directamente:"),
            C("""stats.t.interval(0.95, df=n - 1, loc=media, scale=ee)"""),
            M("**Cómo leerlo**: con 1.164 respuestas la media se conoce con una precisión de unos ±1,7 minutos. Fíjate en que el intervalo es para la **media**, no para cada persona: las personas varían muchísimo más."),
        ], quiz=[
            unica("Con muestras grandes, el valor de t para el 95 % es aproximadamente...", "1,96",
                  [("0,95", "0,95 es la confianza, no el valor crítico."), ("2,58", "Ese es el valor para el 99 %.")]),
        ]),
        dict(titulo="Comparar grupos con sus intervalos", celdas=[
            M("**Qué vamos a hacer**: calcular la media de minutos y su intervalo para cada medio principal y dibujarlos con barras de error."),
            C("""def ic_media(x, confianza=0.95):
    x = x.dropna()
    ee = x.std() / np.sqrt(len(x))
    t = stats.t.ppf(1 - (1 - confianza) / 2, df=len(x) - 1)
    return pd.Series({"n": len(x), "media": x.mean(), "margen": t * ee})

tabla = enc.groupby("medio_principal")["minutos_noticias_dia"].apply(ic_media).unstack().sort_values("media")
tabla.round(1)"""),
            C("""plt.errorbar(tabla["media"], tabla.index, xerr=tabla["margen"], fmt="o", color="steelblue", capsize=4)
plt.xlabel("Minutos al día con noticias (media e IC 95 %)")
plt.title("Consumo de noticias según el medio principal (encuesta simulada)")
plt.show()"""),
            M("Los grupos pequeños (radio, prensa en papel) tienen intervalos más anchos. Si los intervalos de dos grupos se solapan mucho, no podemos asegurar que sus medias sean distintas."),
        ], quiz=[
            unica("¿Por qué el intervalo de la prensa en papel es más ancho que el de la televisión?", "Porque hay menos personas en ese grupo",
                  [("Porque leen menos", "La anchura depende del tamaño y de la dispersión, no de la media."), ("Porque la confianza es menor", "Todos se calculan al 95 %.")]),
        ]),
        dict(titulo="¿Cuántas entrevistas necesito?", celdas=[
            M("""Despejando $n$ en la fórmula del margen de una proporción:

$$n = \\frac{z^2\\, p(1-p)}{e^2}$$

con $p = 0{,}5$ si no se sabe nada (peor caso) y $e$ el margen deseado en tanto por uno."""),
            C("""def tamano_muestra(margen, p=0.5, confianza=0.95):
    z = stats.norm.ppf(1 - (1 - confianza) / 2)
    return int(np.ceil(z**2 * p * (1 - p) / margen**2))

for e in [0.05, 0.03, 0.02, 0.01]:
    print(f"Margen ±{e * 100:.0f} puntos: {tamano_muestra(e):>6} entrevistas")"""),
            M("**Cómo leerlo**: pasar de ±3 a ±1 punto multiplica las entrevistas por 9. Por eso casi ninguna encuesta pública baja de ±2 puntos: sería carísima."),
        ], quiz=[
            unica("Para reducir el margen de error de ±4 a ±2 puntos, ¿cuántas veces más entrevistas hacen falta?", "4 veces más",
                  [("2 veces más", "El tamaño depende del cuadrado del margen."), ("8 veces más", "Es (4/2)² = 4.")]),
        ]),
        dict(titulo="¿Y el tamaño de la población?", celdas=[
            M("""Sorprendentemente, el tamaño de la población **casi no importa** salvo que la muestra sea una parte grande de ella. Una encuesta de 1.000 personas tiene prácticamente el mismo margen en Castellón que en toda España. Se ajusta con el **factor de corrección para poblaciones finitas**:

$$n_{ajustado} = \\frac{n}{1 + \\frac{n - 1}{N}}$$"""),
            C("""n0 = tamano_muestra(0.03)
for N in [500, 5_000, 50_000, 5_000_000, 48_000_000]:
    print(f"Población {N:>11,}: {int(np.ceil(n0 / (1 + (n0 - 1) / N))):>5} entrevistas para ±3 puntos")"""),
            M("Solo en poblaciones pequeñas (los socios de un club, la plantilla de una empresa) la corrección reduce de forma notable las entrevistas necesarias."),
        ], quiz=[
            unica("Para un margen de ±3 puntos, ¿necesita una encuesta en una ciudad de 300.000 habitantes muchas menos entrevistas que una nacional?", "No: necesita prácticamente las mismas",
                  [("Sí, unas diez veces menos", "El tamaño de la población apenas influye cuando es grande."), ("Sí, la mitad", "La corrección solo importa en poblaciones pequeñas.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula el intervalo al 95 % para la confianza media en los medios.",
             solucion='ic_media(enc["confianza_medios"])'),
        dict(seccion="sección 1", enunciado="Calcula el mismo intervalo al 99 %. ¿Es más ancho o más estrecho?",
             solucion='ic_media(enc["confianza_medios"], 0.99)'),
        dict(seccion="sección 2", enunciado="Haz el gráfico de medias con intervalos de la confianza en los medios según el nivel de estudios.",
             solucion='''t2 = enc.groupby("estudios")["confianza_medios"].apply(ic_media).unstack()
plt.errorbar(t2["media"], t2.index, xerr=t2["margen"], fmt="o", capsize=4)
plt.show()'''),
        dict(seccion="sección 3", enunciado="Un diario quiere estimar el porcentaje de lectores satisfechos con un margen de ±4 puntos. Cree que ronda el 80 %. ¿Cuántas encuestas necesita? ¿Y si no sabe nada (p = 0,5)?",
             solucion='print(tamano_muestra(0.04, p=0.8), tamano_muestra(0.04))'),
        dict(seccion="sección 4", enunciado="La plantilla de un grupo de comunicación tiene 1.200 personas. ¿Cuántas hay que encuestar para un margen de ±5 puntos?",
             solucion='''n0 = tamano_muestra(0.05)
int(np.ceil(n0 / (1 + (n0 - 1) / 1200)))'''),
    ],
    resumen=["**IC para una media**: $\\bar{x} \\pm t \\cdot s/\\sqrt{n}$; con muestras grandes $t \\approx 1{,}96$.",
             "Las **barras de error** permiten comparar las medias de varios grupos con su incertidumbre.",
             "**Tamaño de muestra** para una proporción: $n = z^2 p(1-p)/e^2$; usa $p = 0{,}5$ si no sabes nada.",
             "Dividir el margen por 2 exige **cuadruplicar** la muestra.",
             "El tamaño de la población **apenas influye** salvo que sea pequeña (corrección para poblaciones finitas)."],
    glosario=[("t de Student", "Distribución que se usa en lugar de la normal cuando se estima la desviación típica."),
              ("Barras de error", "Segmentos que representan el intervalo de confianza en un gráfico."),
              ("Tamaño de muestra", "Número de casos necesario para una precisión dada."),
              ("Población finita", "Población pequeña en la que la muestra es una parte apreciable.")],
    seguir="En el cuaderno 29 aprenderás la lógica de los contrastes de hipótesis y el famoso p-valor.",
),
# ---------------------------------------------------------------------------
dict(
    num=29, slug="P29_contrastes_de_hipotesis", unidad=U,
    titulo="Contrastes de hipótesis: la lógica del p-valor",
    datos=["encuesta_medios.csv"], imports_extra="from scipy import stats\n",
    intro="""«Un estudio demuestra que...»: detrás de muchas de estas noticias hay un **contraste de hipótesis** y un **p-valor**. Es la herramienta que usa la ciencia para decidir si un resultado puede deberse al azar. También es una de las más malinterpretadas. Entender su lógica te permitirá leer estudios con criterio y no repetir sus exageraciones.

**Qué necesitas saber antes**: los cuadernos 26 y 27.""",
    aprender=["Plantear una hipótesis nula y una alternativa.",
              "Calcular e interpretar un p-valor, por simulación y con fórmula.",
              "Distinguir los errores de tipo I y de tipo II.",
              "Reconocer usos engañosos: «significativo» no es «importante» y el p-hacking."],
    secciones=[
        dict(titulo="La lógica: un juicio a la hipótesis nula", celdas=[
            M("""Un contraste funciona como un juicio:

| Juicio | Contraste |
| :-- | :-- |
| Presunción de inocencia | **Hipótesis nula** $H_0$: no hay efecto, no hay diferencia, todo es azar |
| La acusación | **Hipótesis alternativa** $H_1$: sí hay efecto |
| Las pruebas | Los datos de la muestra |
| «Más allá de toda duda razonable» | El **p-valor** es muy pequeño |
| Absuelto no significa inocente | No rechazar $H_0$ no demuestra que $H_0$ sea cierta |

Ejemplo: una cabecera afirma que **más de la mitad** de sus lectores la prefiere en digital. En una muestra de 400 lectores, 222 (55,5 %) lo dicen. ¿Basta para afirmarlo, o podría ser azar con un 50 % real?

- $H_0$: $p = 0{,}5$ &nbsp;&nbsp; $H_1$: $p > 0{,}5$"""),
        ], quiz=[
            unica("En un contraste, la hipótesis nula suele afirmar...", "que no hay efecto o diferencia",
                  [("lo que el investigador quiere demostrar", "Eso suele ser la alternativa."), ("que los datos son erróneos", "No tiene que ver con errores en los datos.")]),
        ]),
        dict(titulo="El p-valor por simulación", celdas=[
            M("""El **p-valor** es la probabilidad de obtener un resultado **igual o más extremo** que el observado **si $H_0$ fuera cierta**. Lo calculamos simulando muchas muestras de 400 lectores con un 50 % real:"""),
            C("""rng = np.random.default_rng(29)
n, observados = 400, 222
sim = rng.binomial(n, 0.5, size=100_000)
p_valor_sim = (sim >= observados).mean()

plt.hist(sim, bins=50, color="lightgrey")
plt.axvline(observados, color="firebrick", label=f"Observado: {observados}")
plt.xlabel("Lectores que prefieren digital en muestras de 400 (si p = 0,5)")
plt.legend()
plt.title(f"p-valor simulado = {p_valor_sim:.4f}")
plt.show()"""),
            M("Con la fórmula exacta (`binomtest`) obtenemos casi lo mismo:"),
            C("""res = stats.binomtest(observados, n, p=0.5, alternative="greater")
print(f"p-valor exacto: {res.pvalue:.4f}")"""),
            M("""**Cómo leerlo**: si de verdad la preferencia fuera del 50 %, obtener 222 o más de 400 pasaría solo en torno a un 1,5 % de las muestras. Es poco probable, así que **rechazamos $H_0$** al nivel habitual del 5 %: los datos apoyan que más de la mitad prefiere el digital.

El umbral (normalmente 0,05) se llama **nivel de significación** $\\alpha$. Si p < α, se dice que el resultado es **estadísticamente significativo**."""),
        ], quiz=[
            unica("Un p-valor de 0,03 significa que...", "si H0 fuera cierta, un resultado tan extremo saldría en el 3 % de las muestras",
                  [("hay un 3 % de probabilidad de que H0 sea cierta", "Es la interpretación errónea más común."), ("el efecto es del 3 %", "El p-valor no mide el tamaño del efecto.")]),
        ]),
        dict(titulo="Dos tipos de error", celdas=[
            M("""| | $H_0$ es cierta | $H_0$ es falsa |
| :-- | :-- | :-- |
| **Rechazo $H_0$** | Error de **tipo I** (falso positivo), probabilidad α | Acierto |
| **No rechazo $H_0$** | Acierto | Error de **tipo II** (falso negativo) |

Con α = 0,05, **1 de cada 20** contrastes en los que no hay ningún efecto saldrá «significativo» por puro azar."""),
            M("**Qué vamos a hacer**: simular 100 estudios en los que **no hay ningún efecto real** y ver cuántos salen significativos. Esperamos unos 5."),
            C("""significativos = 0
for estudio in range(100):
    grupo_a = rng.normal(50, 10, 100)
    grupo_b = rng.normal(50, 10, 100)          # misma media: no hay efecto
    p = stats.ttest_ind(grupo_a, grupo_b).pvalue
    significativos += p < 0.05
print(f"Estudios 'significativos' sin ningún efecto real: {significativos} de 100")"""),
        ], quiz=[
            unica("Un error de tipo I es...", "concluir que hay un efecto cuando no lo hay",
                  [("no detectar un efecto que sí existe", "Eso es un error de tipo II."), ("equivocarse al calcular el p-valor", "No es un error de cálculo, sino de decisión.")]),
        ]),
        dict(titulo="Significativo no es importante", celdas=[
            M("""Dos trampas que verás en notas de prensa de estudios:

1. **Con muestras enormes, cualquier diferencia minúscula es significativa.** Un p-valor pequeño dice que el efecto probablemente **existe**, no que sea **grande** ni **importante**. Pregunta siempre por el **tamaño del efecto** y su intervalo de confianza.
2. **P-hacking**: si se prueban 20 cruces de variables, alguno saldrá significativo por azar (lo acabas de ver). Desconfía de los estudios que «descubren» un efecto sin haberlo planteado de antemano."""),
            C("""for n_ in [100, 10_000, 1_000_000]:
    a = rng.normal(50.0, 10, n_)
    b = rng.normal(50.3, 10, n_)                # diferencia real minúscula: 0,3 puntos
    print(f"n = {n_:>9,} por grupo: diferencia = {b.mean() - a.mean():.2f}, p-valor = {stats.ttest_ind(a, b).pvalue:.4f}")"""),
            M("> **Para la noticia**: «el estudio encuentra una diferencia estadísticamente significativa, aunque pequeña: de 0,3 puntos sobre 100». Mejor eso que «un estudio demuestra que...»."),
        ], quiz=[
            varias("¿Qué afirmaciones sobre el p-valor son correctas?", [
                ("Un p-valor pequeño no implica que el efecto sea grande", True, "¡Correcto!"),
                ("p > 0,05 demuestra que no hay efecto", False, "No rechazar H0 no demuestra que sea cierta."),
                ("Si se hacen muchos contrastes, alguno saldrá significativo por azar", True, "¡Correcto!"),
                ("El p-valor es la probabilidad de que H0 sea cierta", False, "Es la probabilidad de los datos (o más extremos) suponiendo H0.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 2", enunciado="En la encuesta (n = 1.200), ¿hay evidencia de que **más del 25 %** ha creído alguna vez un bulo? Plantea las hipótesis y calcula el p-valor con `binomtest`.",
             solucion='''enc = pd.read_csv("encuesta_medios.csv")
k = (enc["ha_creido_bulo"] == "Sí").sum()
stats.binomtest(k, len(enc), p=0.25, alternative="greater").pvalue'''),
        dict(seccion="sección 2", enunciado="Repite el ejemplo de los lectores con una muestra de 100 y 55 respuestas a favor (también el 55 %). ¿Es significativo? ¿Por qué cambia?",
             solucion='stats.binomtest(55, 100, p=0.5, alternative="greater").pvalue', comentario="No: con 100 casos, un 55 % es compatible con el azar. El mismo porcentaje con más datos da más evidencia."),
        dict(seccion="sección 3", enunciado="Repite la simulación de los estudios sin efecto 1.000 veces en lugar de 20. ¿Qué proporción sale significativa?",
             solucion='''sig = 0
for _ in range(1000):
    sig += stats.ttest_ind(rng.normal(50, 10, 100), rng.normal(50, 10, 100)).pvalue < 0.05
sig / 1000'''),
        dict(seccion="sección 4", enunciado="Busca una noticia reciente que diga «un estudio demuestra...». ¿Indica el tamaño del efecto, el tamaño de la muestra y si fue un experimento?",
             comentario="Ejercicio abierto para comentar en clase."),
    ],
    resumen=["Un **contraste** plantea $H_0$ (no hay efecto) frente a $H_1$ y usa los datos para decidir.",
             "El **p-valor** es la probabilidad de un resultado tan extremo o más **si $H_0$ fuera cierta**; si es menor que α (0,05), se rechaza $H_0$.",
             "**Error de tipo I**: falso positivo (probabilidad α). **Error de tipo II**: falso negativo.",
             "«Significativo» **no** es «importante»: pide el tamaño del efecto y su intervalo.",
             "Muchos contrastes producen falsos positivos (**p-hacking**)."],
    glosario=[("Hipótesis nula", "Afirmación de que no hay efecto, que se pone a prueba."), ("p-valor", "Probabilidad de un resultado igual o más extremo si H0 es cierta."),
              ("Nivel de significación", "Umbral α por debajo del cual se rechaza H0."), ("Error de tipo I", "Rechazar H0 siendo cierta."),
              ("Error de tipo II", "No rechazar H0 siendo falsa."), ("P-hacking", "Probar muchos análisis hasta encontrar uno significativo.")],
    errores=[("`AttributeError: binom_test`", "Esa función se eliminó de SciPy", "Usa `stats.binomtest(...).pvalue`")],
    seguir="En el cuaderno 30, el último, compararás dos grupos: proporciones, tablas de contingencia y medias.",
),
# ---------------------------------------------------------------------------
dict(
    num=30, slug="P30_comparar_dos_grupos", unidad=U,
    titulo="Comparar dos grupos: proporciones, tablas y medias",
    datos=["encuesta_medios.csv", "salarios_redaccion.csv"], imports_extra="from scipy import stats\n",
    intro="""¿Creen más bulos quienes comparten noticias? ¿Cobran distinto mujeres y hombres en la redacción? ¿Es real la diferencia entre dos provincias? Casi todas las preguntas periodísticas con datos acaban siendo **comparaciones entre grupos**. En este último cuaderno juntarás todo lo aprendido para contestarlas con rigor y redactar el resultado.

**Qué necesitas saber antes**: los cuadernos 12, 27 y 29.""",
    aprender=["Comparar dos proporciones con un intervalo y un contraste.",
              "Contrastar la independencia en una tabla de contingencia (chi-cuadrado).",
              "Comparar dos medias con la t de Student.",
              "Redactar una comparación con su incertidumbre."],
    secciones=[
        dict(titulo="Dos proporciones", celdas=[
            C('enc = pd.read_csv("encuesta_medios.csv")\nsal = pd.read_csv("salarios_redaccion.csv")'),
            M("""Pregunta: ¿es mayor la proporción de personas que han creído un bulo entre quienes comparten noticias?

El intervalo para la **diferencia de proporciones** es $(\\hat{p}_1 - \\hat{p}_2) \\pm 1{,}96\\sqrt{\\frac{\\hat{p}_1(1-\\hat{p}_1)}{n_1} + \\frac{\\hat{p}_2(1-\\hat{p}_2)}{n_2}}$."""),
            C("""g1 = enc[enc["comparte_noticias"] == "Sí"]["ha_creido_bulo"] == "Sí"
g2 = enc[enc["comparte_noticias"] == "No"]["ha_creido_bulo"] == "Sí"
p1, p2, n1, n2 = g1.mean(), g2.mean(), len(g1), len(g2)
dif = p1 - p2
ee = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
print(f"Comparten: {p1:.1%} (n = {n1})   No comparten: {p2:.1%} (n = {n2})")
print(f"Diferencia: {dif * 100:.1f} puntos, IC 95 %: de {(dif - 1.96 * ee) * 100:.1f} a {(dif + 1.96 * ee) * 100:.1f}")"""),
            M("El intervalo está muy lejos de 0: la diferencia es real (en esta muestra simulada). El contraste correspondiente ($H_0$: $p_1 = p_2$) da un p-valor minúsculo:"),
            C("""p_comun = (g1.sum() + g2.sum()) / (n1 + n2)
z = dif / np.sqrt(p_comun * (1 - p_comun) * (1 / n1 + 1 / n2))
print(f"z = {z:.2f}, p-valor (bilateral) = {2 * (1 - stats.norm.cdf(abs(z))):.2e}")"""),
        ], quiz=[
            unica("Si el intervalo al 95 % de una diferencia de proporciones va de −1,5 a 4,2 puntos, ¿qué concluyes?", "No hay evidencia de diferencia, porque el intervalo incluye el 0",
                  [("El primer grupo es mayor", "El 0 está dentro: la diferencia podría ser nula o incluso negativa."), ("La diferencia es de 4,2 puntos", "4,2 es solo el extremo superior.")]),
        ]),
        dict(titulo="Tablas de contingencia: la prueba chi-cuadrado", celdas=[
            M("""Con más de dos categorías se usa la **prueba chi-cuadrado de independencia**: compara la tabla observada con la que esperaríamos **si las variables fueran independientes** (cuaderno 21).

- $H_0$: las dos variables son independientes."""),
            C("""tabla = pd.crosstab(enc["provincia"], enc["ha_creido_bulo"])
chi2, p, gl, esperadas = stats.chi2_contingency(tabla)
print(tabla)
print(f"\\nChi-cuadrado = {chi2:.2f}, grados de libertad = {gl}, p-valor = {p:.3f}")
print("Frecuencias esperadas si fueran independientes:")
print(pd.DataFrame(esperadas, index=tabla.index, columns=tabla.columns).round(1))"""),
            M("""**Cómo leerlo**: en el cuaderno 21 Castellón parecía tener más personas que habían creído un bulo (33 % frente a 25–26 %). Pero el p-valor (0,16) es mayor que 0,05: con solo 160 personas de Castellón en la muestra, esa diferencia es compatible con el azar. Titular «Castellón, la provincia más crédula» sería un error.

Ahora, una relación clara:"""),
            C("""tabla2 = pd.crosstab(enc["medio_principal"], enc["comparte_noticias"])
print(f"Medio principal y compartir noticias: p-valor = {stats.chi2_contingency(tabla2)[1]:.2e}")"""),
        ], quiz=[
            unica("La prueba chi-cuadrado de independencia contrasta...", "si dos variables cualitativas están relacionadas",
                  [("si dos medias son iguales", "Para eso se usa la t de Student."), ("si una variable es normal", "No es su objetivo.")]),
        ]),
        dict(titulo="Dos medias: la t de Student", celdas=[
            M("""Para comparar las medias de una variable cuantitativa en dos grupos se usa la **prueba t** (en la versión de Welch, que no supone varianzas iguales). Comparemos el salario de mujeres y hombres **dentro del mismo puesto** (redactores y redactoras), para no mezclar puestos distintos."""),
            C("""red = sal[sal["puesto"] == "Redactor/a"]
m = red.loc[red["sexo"] == "Mujer", "salario_bruto_anual"]
h = red.loc[red["sexo"] == "Hombre", "salario_bruto_anual"]
res = stats.ttest_ind(h, m, equal_var=False)
dif = h.mean() - m.mean()
ee = np.sqrt(h.var() / len(h) + m.var() / len(m))
print(f"Hombres: {h.mean():,.0f} € (n = {len(h)})   Mujeres: {m.mean():,.0f} € (n = {len(m)})")
print(f"Diferencia: {dif:,.0f} €, IC 95 % aprox.: de {dif - 1.96 * ee:,.0f} a {dif + 1.96 * ee:,.0f} €")
print(f"p-valor = {res.pvalue:.4f}")"""),
            M("""**Cómo leerlo**: los redactores cobran de media unos 1.700 € más que las redactoras. El p-valor está justo por debajo de 0,05 y el intervalo va de casi 0 a unos 3.400 €: hay indicios de diferencia, pero la estimación es muy imprecisa. Con datos reales habría que tener en cuenta también la experiencia y el tipo de contrato."""),
            C("""red.boxplot(column="salario_bruto_anual", by="sexo", vert=False, grid=False)
plt.suptitle("")
plt.title("Salario de redactores y redactoras (datos simulados)")
plt.show()"""),
        ], quiz=[
            unica("¿Por qué comparamos solo a redactores y redactoras y no a toda la plantilla?", "Para no mezclar el efecto del sexo con el del puesto",
                  [("Porque la t solo admite un puesto", "La t admite cualquier grupo; es una decisión de diseño."), ("Porque hay más datos", "Al contrario: hay menos datos, pero la comparación es más justa.")]),
        ]),
        dict(titulo="Cómo contarlo: lista de comprobación final", celdas=[
            M("""Antes de publicar una comparación con datos, repasa esta lista. Resume todo el curso:

1. **¿De dónde salen los datos?** Fuente, fecha y ficha técnica (cuadernos 1 y 25).
2. **¿Qué se compara exactamente?** Grupos comparables, mismo periodo, misma definición (8 y 30).
3. **¿Media o mediana? ¿Puntos o porcentaje?** (8 y 14).
4. **¿Sobre quién se calcula el porcentaje?** (5, 12 y 21).
5. **¿Cuántos casos hay en cada grupo y cuál es el margen de error?** (27 y 28).
6. **¿Puede ser azar?** Intervalo de confianza o p-valor (29 y 30).
7. **¿Es grande la diferencia, además de significativa?** (29).
8. **¿Correlación o causa?** ¿Hay variables de confusión? (13).
9. **¿Es estacional o real?** ¿Está en euros reales? (16 y 19).
10. **¿El gráfico es honesto?** Eje, escala, título y fuente (6)."""),
            C("""print(f"Entre las personas que comparten noticias, el {p1:.0%} reconoce haber creído alguna vez un bulo,")
print(f"frente al {p2:.0%} de quienes no comparten (encuesta simulada a {len(enc)} personas; diferencia de")
print(f"{(p1 - p2) * 100:.0f} puntos, con un margen de error de ±{1.96 * np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2) * 100:.0f} puntos).")"""),
        ], quiz=[
            varias("Una noticia dice: «Las mujeres cobran un 6 % menos en las redacciones, según una encuesta a 120 periodistas». ¿Qué preguntas harías antes de publicarla?", [
                ("¿Se compara a igual puesto y experiencia?", True, "¡Correcto!"), ("¿Cuál es el margen de error con 120 personas?", True, "¡Correcto!"),
                ("¿Es media o mediana?", True, "¡Correcto!"), ("Ninguna: 6 % es un dato claro", False, "Un dato sin contexto puede engañar.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="¿Pagan por noticias en mayor proporción las personas con estudios universitarios que el resto? Calcula la diferencia y su intervalo.",
             solucion='''u = enc["estudios"] == "Universitarios"
a = enc.loc[u, "suscripcion_pago"] == "Sí"
b = enc.loc[~u, "suscripcion_pago"] == "Sí"
d = a.mean() - b.mean()
e = 1.96 * np.sqrt(a.mean() * (1 - a.mean()) / len(a) + b.mean() * (1 - b.mean()) / len(b))
print(d, d - e, d + e)'''),
        dict(seccion="sección 2", enunciado="Haz la prueba chi-cuadrado entre el nivel de estudios y haber creído un bulo.",
             solucion='stats.chi2_contingency(pd.crosstab(enc["estudios"], enc["ha_creido_bulo"]))[1]'),
        dict(seccion="sección 3", enunciado="Compara el salario medio de personas con contrato indefinido y temporal. ¿Es significativa la diferencia?",
             solucion='''i = sal.loc[sal["contrato"] == "Indefinido", "salario_bruto_anual"]
t = sal.loc[sal["contrato"] == "Temporal", "salario_bruto_anual"]
print(i.mean() - t.mean(), stats.ttest_ind(i, t, equal_var=False).pvalue)'''),
        dict(seccion="sección 4", enunciado="**Trabajo final (como el de la evaluación continua)**: elige una comparación con los datos del curso, compruébala con la lista de la sección 4 y escribe una pieza de 250 palabras con un gráfico honesto y la frase metodológica.",
             comentario="La guía docente evalúa: claridad periodística, contenido estadístico riguroso y creatividad en la elección del estadístico y los parámetros."),
    ],
    resumen=["**Dos proporciones**: intervalo para la diferencia; si no incluye el 0, hay evidencia de diferencia.",
             "**Chi-cuadrado** (`stats.chi2_contingency`): contrasta la independencia en una tabla de contingencia.",
             "**Dos medias**: prueba t de Welch (`stats.ttest_ind(..., equal_var=False)`), comparando grupos **comparables**.",
             "Publica la diferencia **con su incertidumbre** (margen o intervalo) y el número de casos.",
             "Usa la **lista de comprobación** antes de publicar cualquier comparación con datos."],
    glosario=[("Diferencia de proporciones", "Resta de las proporciones de dos grupos."), ("Chi-cuadrado", "Prueba de independencia entre variables cualitativas."),
              ("Frecuencias esperadas", "Recuentos que habría en una tabla si las variables fueran independientes."),
              ("Prueba t de Welch", "Prueba para comparar dos medias sin suponer varianzas iguales.")],
    seguir="**¡Enhorabuena!** Has terminado el curso. Para seguir: practica con datos reales del [INE](https://www.ine.es), del [CIS](https://www.cis.es) y de [datos.gob.es](https://datos.gob.es), y revisa los cuadernos de SIMUSTAT para ampliar (regresión múltiple, ANOVA).",
),
]
