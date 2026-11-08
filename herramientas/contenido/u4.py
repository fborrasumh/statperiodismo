from _comun import C, M, numerica, unica, varias

U = "4. Probabilidad"

CUADERNOS = [
# ---------------------------------------------------------------------------
dict(
    num=20, slug="P20_azar_y_probabilidad", unidad=U,
    titulo="Azar y probabilidad: experimentos, sucesos y simulación",
    datos=["municipios.csv"],
    intro="""«El pueblo con más cáncer de España»: cada año aparece un titular así sobre algún municipio pequeño. Muchas veces no hay ninguna causa: en poblaciones pequeñas **el azar produce valores extremos**. Entender el azar es la base para no confundir casualidad con noticia y, más adelante, para calcular márgenes de error.

**Qué necesitas saber antes**: los cuadernos 2 a 5.""",
    aprender=["Definir experimento aleatorio, suceso y probabilidad.",
              "Calcular probabilidades con la regla de Laplace y las reglas del complementario y de la unión.",
              "Simular experimentos aleatorios con NumPy.",
              "Explicar la ley de los grandes números y su lado periodístico: los extremos de las muestras pequeñas."],
    secciones=[
        dict(titulo="Experimentos, sucesos y probabilidad", celdas=[
            M("""- Un **experimento aleatorio** es aquel cuyo resultado no se puede predecir con certeza (lanzar un dado, elegir al azar a una persona para una encuesta).
- Un **suceso** es un conjunto de resultados («sale par», «la persona elegida se informa por redes»).
- La **probabilidad** de un suceso es un número entre 0 (imposible) y 1 (seguro).

Si todos los resultados son **igual de probables**, se usa la **regla de Laplace**:

$$P(A) = \\frac{\\text{casos favorables}}{\\text{casos posibles}}$$"""),
            M("Reglas básicas:\n\n- **Complementario**: $P(\\text{no } A) = 1 - P(A)$.\n- **Unión** de sucesos que no pueden ocurrir a la vez: $P(A \\text{ o } B) = P(A) + P(B)$.\n- **Unión** en general: $P(A \\text{ o } B) = P(A) + P(B) - P(A \\text{ y } B)$."),
            C("""# Elegimos al azar a una persona de una encuesta con estos recuentos
recuento = {"Televisión": 418, "Prensa digital": 294, "Redes sociales": 264, "Radio": 121, "Prensa en papel": 103}
total = sum(recuento.values())
p_redes = recuento["Redes sociales"] / total
p_prensa = (recuento["Prensa digital"] + recuento["Prensa en papel"]) / total
print(f"P(redes) = {p_redes:.3f}")
print(f"P(no redes) = {1 - p_redes:.3f}")
print(f"P(prensa, digital o papel) = {p_prensa:.3f}")"""),
        ], quiz=[
            numerica("En una urna hay 3 bolas rojas y 7 azules. ¿Cuál es la probabilidad de sacar una roja? (en tanto por uno)", 0.299, 0.301, ok="¡Correcto! 3 / 10 = 0,3."),
        ]),
        dict(titulo="Simular el azar", celdas=[
            M("""Cuando un cálculo es difícil, se puede **simular**: repetir el experimento muchas veces con el ordenador y contar. NumPy tiene un generador de números aleatorios; fijar una **semilla** (`seed`) hace que los resultados se puedan repetir."""),
            C("""rng = np.random.default_rng(seed=1)
dado = rng.integers(1, 7, size=10)      # 10 lanzamientos de un dado
print(dado)
print("Proporción de seises:", (dado == 6).mean())"""),
            M("Con 10 lanzamientos la proporción de seises puede alejarse mucho de 1/6 ≈ 0,167. ¿Y con más?"),
            C("""for n in [10, 100, 1_000, 10_000, 100_000]:
    tiradas = rng.integers(1, 7, size=n)
    print(f"n = {n:>7}: proporción de seises = {(tiradas == 6).mean():.4f}")"""),
        ], quiz=[
            unica("¿Para qué sirve fijar una semilla (`seed`) en una simulación?", "Para que los resultados se puedan repetir exactamente",
                  [("Para que los resultados sean más exactos", "No cambia la exactitud, solo hace reproducible el azar."), ("Para que no haya azar", "Sigue siendo aleatorio, pero repetible.")]),
        ]),
        dict(titulo="La ley de los grandes números", celdas=[
            M("""La **ley de los grandes números** dice que, al repetir un experimento muchas veces, la **frecuencia relativa** de un suceso se acerca a su **probabilidad**. Es lo que hace fiables las encuestas grandes."""),
            C("""n = 5000
tiradas = rng.integers(1, 7, size=n)
frec_acumulada = np.cumsum(tiradas == 6) / np.arange(1, n + 1)
plt.plot(frec_acumulada, color="steelblue")
plt.axhline(1 / 6, color="firebrick", ls="--", label="Probabilidad 1/6")
plt.xscale("log")
plt.xlabel("Número de lanzamientos (escala logarítmica)")
plt.ylabel("Proporción de seises")
plt.legend()
plt.show()"""),
        ], quiz=[
            unica("Según la ley de los grandes números, al aumentar el número de repeticiones...", "la frecuencia relativa se acerca a la probabilidad",
                  [("la probabilidad cambia", "La probabilidad es fija; lo que se estabiliza es la frecuencia."), ("el número de éxitos se iguala al de fracasos", "Solo si la probabilidad fuera 0,5, y aun así lo que se iguala son las proporciones.")]),
        ]),
        dict(titulo="El lado oscuro: los extremos de lo pequeño", celdas=[
            M("""**Qué vamos a hacer**: imaginar que en todos los municipios la probabilidad de una enfermedad es **exactamente la misma** (1 por 1.000 habitantes al año). Simulamos los casos y miramos qué municipios salen con las tasas más altas."""),
            C("""muni = pd.read_csv("municipios.csv")
p = 0.001
muni["casos"] = rng.binomial(muni["poblacion"], p)          # azar puro: misma probabilidad en todos
muni["tasa_por_1000"] = muni["casos"] / muni["poblacion"] * 1000
muni.sort_values("tasa_por_1000", ascending=False)[["municipio", "poblacion", "casos", "tasa_por_1000"]].head(5)"""),
            C("""plt.scatter(muni["poblacion"], muni["tasa_por_1000"], alpha=0.6)
plt.axhline(1, color="firebrick", ls="--", label="Tasa real en todos: 1 por 1.000")
plt.xscale("log")
plt.xlabel("Población (escala logarítmica)")
plt.ylabel("Tasa simulada por 1.000")
plt.legend()
plt.title("Solo azar: los extremos aparecen en los municipios pequeños")
plt.show()"""),
            M("""**Qué ha pasado**: aunque el riesgo es idéntico en todas partes, los municipios pequeños dan tasas muy altas (o cero), y los grandes se quedan cerca de 1. Esto es la **ley de los pequeños números**. Antes de titular «el pueblo con más...», mira su **población** y piensa si el azar basta para explicarlo."""),
        ], quiz=[
            unica("Un pueblo de 300 habitantes tiene la tasa de una enfermedad más alta de la provincia. ¿Qué es lo primero que hay que considerar?",
                  "Que con tan poca población el azar produce tasas extremas",
                  [("Que hay una causa ambiental", "Puede haberla, pero el azar es la primera explicación a descartar."), ("Que los datos están mal", "No necesariamente: el azar basta para explicarlo.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Con el diccionario `recuento`, calcula la probabilidad de que una persona elegida al azar **no** se informe ni por televisión ni por radio.",
             solucion='1 - (recuento["Televisión"] + recuento["Radio"]) / total'),
        dict(seccion="sección 2", enunciado="Simula 10.000 lanzamientos de dos dados y estima la probabilidad de que la suma sea 7. Compárala con el valor exacto (6/36).",
             solucion='''d1 = rng.integers(1, 7, 10000)
d2 = rng.integers(1, 7, 10000)
print(((d1 + d2) == 7).mean(), 6 / 36)'''),
        dict(seccion="sección 3", enunciado="Simula una encuesta en la que el 30 % de la población prefiere un medio: elige al azar 50 personas y luego 5.000 (`rng.random(n) < 0.3`). ¿Cuál se acerca más al 30 %?",
             solucion='''for n in [50, 5000]:
    print(n, (rng.random(n) < 0.3).mean())'''),
        dict(seccion="sección 4", enunciado="Repite la simulación de la sección 4 cambiando la semilla. ¿Son los mismos municipios los que salen en cabeza?",
             solucion='''rng2 = np.random.default_rng(99)
muni["casos2"] = rng2.binomial(muni["poblacion"], p)
(muni["casos2"] / muni["poblacion"] * 1000).sort_values(ascending=False).head()''',
             comentario="No: cambian cada vez. Si un municipio fuera de verdad distinto, saldría en cabeza año tras año."),
    ],
    resumen=["Un **experimento aleatorio** no tiene resultado predecible; la **probabilidad** mide entre 0 y 1 lo posible que es un suceso.",
             "**Laplace**: casos favorables / casos posibles (si todos son igual de probables). Complementario: 1 − P(A).",
             "Se puede **simular** el azar con NumPy; fija la semilla para poder repetirlo.",
             "**Ley de los grandes números**: con muchas repeticiones, la frecuencia relativa se acerca a la probabilidad.",
             "En **muestras o poblaciones pequeñas** el azar produce extremos: no los confundas con noticias."],
    glosario=[("Experimento aleatorio", "Proceso cuyo resultado no se puede predecir con certeza."), ("Suceso", "Conjunto de resultados de un experimento."),
              ("Regla de Laplace", "Probabilidad = favorables / posibles, con resultados equiprobables."),
              ("Ley de los grandes números", "La frecuencia relativa tiende a la probabilidad al aumentar las repeticiones."),
              ("Semilla", "Número que inicializa el generador aleatorio para poder repetir la simulación.")],
    seguir="En el cuaderno 21 verás la probabilidad condicionada y uno de los errores más graves en información judicial: la falacia del fiscal.",
),
# ---------------------------------------------------------------------------
dict(
    num=21, slug="P21_probabilidad_condicionada", unidad=U,
    titulo="Probabilidad condicionada e independencia",
    datos=["verificaciones.csv", "encuesta_medios.csv"],
    intro="""«El 70 % de los bulos se difunde por WhatsApp» y «el 70 % de lo que circula por WhatsApp es un bulo» son frases muy distintas, aunque usen el mismo número. La **probabilidad condicionada** formaliza la idea de «porcentaje sobre un grupo» que viste con las tablas de contingencia, y permite decidir si dos características son **independientes**.

**Qué necesitas saber antes**: los cuadernos 12 (tablas de contingencia) y 20.""",
    aprender=["Calcular probabilidades condicionadas a partir de una tabla.",
              "Distinguir $P(A \\mid B)$ de $P(B \\mid A)$ y reconocer la falacia del fiscal.",
              "Usar la regla del producto.",
              "Comprobar si dos sucesos son independientes."],
    secciones=[
        dict(titulo="Probabilidad condicionada", celdas=[
            C('verif = pd.read_csv("verificaciones.csv")\nverif["es_bulo"] = np.where(verif["veredicto"] == "Verdadero", "No", "Sí")   # falso o engañoso\ntabla = pd.crosstab(verif["plataforma"], verif["es_bulo"], margins=True)\ntabla'),
            M("""La **probabilidad de A condicionada a B** es la probabilidad de A **sabiendo que** ha ocurrido B:

$$P(A \\mid B) = \\frac{P(A \\text{ y } B)}{P(B)}$$

En una tabla: los casos con A y B, divididos por los casos con B. Es exactamente un **porcentaje por fila** (o por columna)."""),
            C("""wa = verif[verif["plataforma"] == "WhatsApp"]
p_bulo_dado_wa = (wa["es_bulo"] == "Sí").mean()
print(f"P(bulo | WhatsApp) = {p_bulo_dado_wa:.3f}")

bulos = verif[verif["es_bulo"] == "Sí"]
p_wa_dado_bulo = (bulos["plataforma"] == "WhatsApp").mean()
print(f"P(WhatsApp | bulo) = {p_wa_dado_bulo:.3f}")"""),
            M("**Cómo leerlo**: de los contenidos de WhatsApp revisados, más de 9 de cada 10 eran bulos; pero de todos los bulos, solo un tercio venía de WhatsApp. Las dos cifras son ciertas y responden a preguntas distintas."),
        ], quiz=[
            unica("En una tabla, ¿cómo se calcula P(bulo | TikTok)?", "Bulos de TikTok / total de contenidos de TikTok",
                  [("Bulos de TikTok / total de bulos", "Eso es P(TikTok | bulo)."), ("Bulos de TikTok / total de contenidos", "Eso es P(bulo y TikTok).")]),
        ]),
        dict(titulo="La falacia del fiscal", celdas=[
            M("""Confundir $P(A \\mid B)$ con $P(B \\mid A)$ se llama **falacia del fiscal**, porque aparece en juicios: «la probabilidad de que el ADN coincida por casualidad es de 1 entre 10.000» **no** significa que la probabilidad de que el acusado sea inocente sea de 1 entre 10.000.

Ejemplo numérico: en una ciudad de 500.000 habitantes, si la coincidencia casual es de 1/10.000, unas **50 personas** coincidirían por azar. Sin más pruebas, el acusado es solo uno de ellos."""),
            C("""poblacion = 500_000
p_coincidencia_inocente = 1 / 10_000
coincidencias_casuales = poblacion * p_coincidencia_inocente
print("Personas que coincidirían por azar:", int(coincidencias_casuales))
print(f"P(culpable | coincide), si solo hay un culpable y nada más: {1 / (coincidencias_casuales + 1):.3f}")"""),
        ], quiz=[
            unica("«El 80 % de los detenidos por un delito eran reincidentes.» ¿Qué NO se puede deducir?", "Que el 80 % de los reincidentes vuelve a ser detenido",
                  [("Que la mayoría de los detenidos tenía antecedentes", "Eso sí dice la frase."), ("Que 8 de cada 10 detenidos eran reincidentes", "Es la misma afirmación.")]),
        ]),
        dict(titulo="Regla del producto", celdas=[
            M("""Despejando la fórmula de la condicionada se obtiene la **regla del producto**:

$$P(A \\text{ y } B) = P(B) \\cdot P(A \\mid B)$$

Sirve para encadenar probabilidades: si el 22 % de las personas se informa por redes y, de ellas, el 65 % comparte noticias, el 0,22 × 0,65 ≈ 14 % de **toda** la población se informa por redes y comparte."""),
            C("""enc = pd.read_csv("encuesta_medios.csv")
p_redes = (enc["medio_principal"] == "Redes sociales").mean()
p_comparte_dado_redes = (enc.loc[enc["medio_principal"] == "Redes sociales", "comparte_noticias"] == "Sí").mean()
print(f"P(redes) × P(comparte | redes) = {p_redes:.3f} × {p_comparte_dado_redes:.3f} = {p_redes * p_comparte_dado_redes:.3f}")
print("Comprobación directa:", round(((enc["medio_principal"] == "Redes sociales") & (enc["comparte_noticias"] == "Sí")).mean(), 3))"""),
        ], quiz=[
            numerica("P(B) = 0,4 y P(A | B) = 0,5. ¿Cuánto vale P(A y B)?", 0.199, 0.201, ok="¡Correcto! 0,4 × 0,5 = 0,2."),
        ]),
        dict(titulo="Independencia", celdas=[
            M("""Dos sucesos son **independientes** si saber que ha ocurrido uno no cambia la probabilidad del otro:

$$P(A \\mid B) = P(A) \\quad \\Longleftrightarrow \\quad P(A \\text{ y } B) = P(A) \\cdot P(B)$$

En una tabla: si las variables fueran independientes, los porcentajes por fila serían **iguales** al porcentaje del total."""),
            C("""print("P(bulo) general:", round((verif["es_bulo"] == "Sí").mean(), 3))
(pd.crosstab(verif["plataforma"], verif["es_bulo"], normalize="index")["Sí"]).round(3)"""),
            C("""print("P(bulo) general:", round((verif["es_bulo"] == "Sí").mean(), 3))
(pd.crosstab(verif["tema"], verif["es_bulo"], normalize="index")["Sí"]).round(3)"""),
            M("""**Cómo leerlo**: la probabilidad de bulo cambia bastante según la plataforma (no parecen independientes), pero apenas cambia según el tema (parecen independientes). En datos de muestras nunca saldrán exactamente iguales; en el cuaderno 30 verás cómo decidir si la diferencia es mayor de lo que produciría el azar."""),
        ], quiz=[
            unica("Si P(A) = 0,3 y P(A | B) = 0,3, ¿qué podemos decir?", "A y B son independientes",
                  [("A y B son incompatibles", "Incompatibles significaría que no pueden ocurrir a la vez."), ("B causa A", "Al contrario: saber B no cambia la probabilidad de A.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Calcula P(bulo | formato = Audio) y P(Audio | bulo).",
             solucion='''print((verif.loc[verif["formato"] == "Audio", "es_bulo"] == "Sí").mean())
print((verif.loc[verif["es_bulo"] == "Sí", "formato"] == "Audio").mean())'''),
        dict(seccion="sección 2", enunciado="Redacta dos titulares, uno con cada probabilidad del ejercicio anterior, que no se puedan confundir.",
             comentario="Por ejemplo: «Más de 9 de cada 10 audios virales revisados eran falsos o engañosos» frente a «Solo 1 de cada 10 bulos verificados era un audio»."),
        dict(seccion="sección 3", enunciado="Con la encuesta, calcula por la regla del producto la probabilidad de que una persona tenga estudios universitarios y pague por noticias. Compruébalo directamente.",
             solucion='''pu = (enc["estudios"] == "Universitarios").mean()
pp_u = (enc.loc[enc["estudios"] == "Universitarios", "suscripcion_pago"] == "Sí").mean()
print(pu * pp_u, ((enc["estudios"] == "Universitarios") & (enc["suscripcion_pago"] == "Sí")).mean())'''),
        dict(seccion="sección 4", enunciado="¿Parecen independientes la provincia y haber creído un bulo en la encuesta?",
             solucion='''print((enc["ha_creido_bulo"] == "Sí").mean())
pd.crosstab(enc["provincia"], enc["ha_creido_bulo"], normalize="index")'''),
    ],
    resumen=["$P(A \\mid B)$ es la probabilidad de A **dentro del grupo B**: un porcentaje por fila o por columna.",
             "$P(A \\mid B)$ y $P(B \\mid A)$ suelen ser muy distintas; confundirlas es la **falacia del fiscal**.",
             "**Regla del producto**: $P(A \\text{ y } B) = P(B) \\cdot P(A \\mid B)$.",
             "A y B son **independientes** si $P(A \\mid B) = P(A)$: los porcentajes por fila son iguales al total."],
    glosario=[("Probabilidad condicionada", "Probabilidad de un suceso sabiendo que ha ocurrido otro."), ("Falacia del fiscal", "Confundir P(A | B) con P(B | A)."),
              ("Regla del producto", "P(A y B) = P(B) · P(A | B)."), ("Independencia", "Situación en la que saber un suceso no cambia la probabilidad del otro.")],
    seguir="En el cuaderno 22 usarás el teorema de Bayes para entender por qué un detector de bulos «con un 95 % de acierto» puede equivocarse mucho.",
),
# ---------------------------------------------------------------------------
dict(
    num=22, slug="P22_teorema_de_bayes", unidad=U,
    titulo="Teorema de Bayes: ¿cuánto acierta un detector de bulos?",
    datos=[],
    intro="""Una empresa anuncia un **detector automático de bulos con un 95 % de acierto**. ¿Si marca una noticia como falsa, hay un 95 % de probabilidad de que lo sea? Casi nunca: depende de **cuántos bulos hay** entre lo que se analiza. El **teorema de Bayes** da la respuesta correcta y explica también por qué fallan los cribados masivos o los sistemas de reconocimiento facial.

**Qué necesitas saber antes**: el cuaderno 21.""",
    aprender=["Calcular una probabilidad total con un árbol.",
              "Aplicar el teorema de Bayes para invertir una probabilidad condicionada.",
              "Entender sensibilidad, especificidad y valor predictivo de un sistema de detección.",
              "Explicar el papel de la prevalencia (la frecuencia de lo que se busca)."],
    secciones=[
        dict(titulo="Sensibilidad, especificidad y prevalencia", celdas=[
            M("""Cualquier sistema que clasifica en «sí/no» (un detector de bulos, una prueba médica, un filtro de spam) tiene dos tipos de acierto:

| Medida | Qué es | Ejemplo |
| :-- | :-- | :-- |
| **Sensibilidad** | P(marca bulo \\| es bulo) | detecta el 95 % de los bulos |
| **Especificidad** | P(marca verdadero \\| es verdadero) | deja pasar el 95 % de lo verdadero |
| **Prevalencia** | P(es bulo) | el 2 % de lo que se analiza son bulos |

Lo que le interesa al periodista es otra cosa: el **valor predictivo positivo**, P(es bulo \\| marca bulo)."""),
        ], quiz=[
            unica("La sensibilidad de un detector es...", "la probabilidad de marcar como bulo algo que sí es un bulo",
                  [("la probabilidad de que algo marcado como bulo lo sea", "Eso es el valor predictivo positivo."), ("la proporción de bulos que circulan", "Eso es la prevalencia.")]),
        ]),
        dict(titulo="Probabilidad total con un árbol", celdas=[
            M("""¿Qué proporción de noticias marcará el detector como bulo? Hay dos caminos: ser bulo y ser detectado, o ser verdadera y ser marcada por error.

$$P(\\text{marca}) = P(\\text{bulo})\\,P(\\text{marca} \\mid \\text{bulo}) + P(\\text{verdad})\\,P(\\text{marca} \\mid \\text{verdad})$$"""),
            C("""prevalencia = 0.02
sensibilidad = 0.95
especificidad = 0.95

p_marca = prevalencia * sensibilidad + (1 - prevalencia) * (1 - especificidad)
print(f"P(el detector marca bulo) = {p_marca:.4f}")"""),
            M("**Qué ha pasado**: aunque solo el 2 % son bulos, el detector marca cerca del **7 %** de las noticias, porque el 5 % de error sobre el 98 % de noticias verdaderas es una cantidad grande."),
        ], quiz=[
            numerica("Prevalencia 0,1, sensibilidad 0,9, especificidad 0,8. ¿Cuánto vale P(marca)?", 0.269, 0.271, ok="¡Correcto! 0,1·0,9 + 0,9·0,2 = 0,27."),
        ]),
        dict(titulo="El teorema de Bayes", celdas=[
            M("""El **teorema de Bayes** invierte la condicionada:

$$P(\\text{bulo} \\mid \\text{marca}) = \\frac{P(\\text{bulo})\\, P(\\text{marca} \\mid \\text{bulo})}{P(\\text{marca})}$$"""),
            C("""vpp = prevalencia * sensibilidad / p_marca
print(f"P(es bulo | el detector lo marca) = {vpp:.3f}")"""),
            M("""**Qué ha pasado**: ¡solo el 28 % de lo marcado es realmente un bulo! Con una prevalencia baja, la mayoría de las alarmas son **falsos positivos**. Un titular como «el algoritmo detecta bulos con un 95 % de fiabilidad» es, por tanto, engañoso si no dice cuántos bulos hay en lo que analiza."""),
            M("Lo comprobamos con frecuencias naturales, que se entienden mejor que las fórmulas. Imagina 10.000 noticias:"),
            C("""n = 10_000
bulos = n * prevalencia
verdaderas = n - bulos
bulos_detectados = bulos * sensibilidad
falsas_alarmas = verdaderas * (1 - especificidad)
print(f"De {n} noticias: {bulos:.0f} bulos y {verdaderas:.0f} verdaderas")
print(f"Marcadas como bulo: {bulos_detectados:.0f} bulos de verdad + {falsas_alarmas:.0f} falsas alarmas")
print(f"Proporción de marcadas que son bulo: {bulos_detectados / (bulos_detectados + falsas_alarmas):.3f}")"""),
        ], quiz=[
            unica("Con una prevalencia muy baja, aunque el detector sea bueno, la mayoría de las alarmas suelen ser...", "falsos positivos",
                  [("bulos reales", "Al haber pocos bulos, los errores sobre las noticias verdaderas pesan más."), ("imposibles de calcular", "Se calculan con Bayes.")]),
        ]),
        dict(titulo="La prevalencia lo cambia todo", celdas=[
            M("**Qué vamos a hacer**: calcular el valor predictivo positivo para distintas prevalencias, con el mismo detector."),
            C("""def valor_predictivo(prev, sens=0.95, esp=0.95):
    return prev * sens / (prev * sens + (1 - prev) * (1 - esp))

prevs = np.linspace(0.005, 0.6, 100)
plt.plot(prevs * 100, [valor_predictivo(p) * 100 for p in prevs], color="steelblue")
plt.xlabel("Prevalencia: % de bulos en lo analizado")
plt.ylabel("% de alarmas que son bulos de verdad")
plt.title("El mismo detector (95 % / 95 %) según cuántos bulos haya")
plt.grid(alpha=0.3)
plt.show()

for p in [0.01, 0.1, 0.5]:
    print(f"Prevalencia {p:.0%}: valor predictivo {valor_predictivo(p):.1%}")"""),
            M("Si el detector se aplica solo a contenidos ya sospechosos (alta prevalencia), sus alarmas son mucho más fiables. Lo mismo pasa con las pruebas médicas: no es igual aplicarlas a toda la población que a personas con síntomas."),
        ], quiz=[
            unica("Si el mismo detector se aplica a contenidos ya denunciados por los usuarios (donde la mitad son bulos), su valor predictivo...", "aumenta mucho",
                  [("se mantiene", "Depende de la prevalencia, que ha subido."), ("baja", "Al haber más bulos, las alarmas son más fiables.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 3", enunciado="Un sistema de reconocimiento facial tiene un 99 % de sensibilidad y un 99 % de especificidad. Se aplica a 100.000 personas en un estadio, entre las que hay 10 buscadas. ¿Qué proporción de las alarmas corresponde a personas buscadas?",
             solucion='valor_predictivo(10 / 100_000, sens=0.99, esp=0.99)', comentario="Menos del 1 %: casi todas las alarmas son falsas."),
        dict(seccion="sección 3", enunciado="Repite el cálculo con frecuencias naturales (cuántas alarmas verdaderas y cuántas falsas).",
             solucion='''print(10 * 0.99, (100_000 - 10) * 0.01)'''),
        dict(seccion="sección 4", enunciado="¿Qué especificidad necesitaría el detector de bulos (con sensibilidad 0,95 y prevalencia 0,02) para que el 80 % de sus alarmas fueran bulos reales? Prueba valores con un bucle.",
             solucion='''for esp in [0.95, 0.98, 0.99, 0.995, 0.999]:
    print(esp, round(valor_predictivo(0.02, 0.95, esp), 3))'''),
        dict(seccion="sección 1", enunciado="Escribe un párrafo para una noticia que explique, sin fórmulas, por qué «95 % de acierto» no significa que el 95 % de las alarmas sean ciertas.",
             comentario="Usa frecuencias naturales: «de cada 10.000 noticias...»."),
    ],
    resumen=["**Sensibilidad** = P(detecta | es); **especificidad** = P(no detecta | no es); **prevalencia** = P(es).",
             "**Probabilidad total**: se suman los caminos del árbol que llevan a un resultado.",
             "**Bayes** invierte la condicionada: P(es | detecta) = P(es) · P(detecta | es) / P(detecta).",
             "Con **prevalencia baja**, hasta un buen detector da mayoría de **falsos positivos**.",
             "Explica estos resultados con **frecuencias naturales** («de cada 10.000...»)."],
    glosario=[("Sensibilidad", "Proporción de positivos reales que el sistema detecta."), ("Especificidad", "Proporción de negativos reales que el sistema reconoce como tales."),
              ("Prevalencia", "Proporción de casos positivos en la población analizada."), ("Valor predictivo positivo", "Probabilidad de que un caso marcado sea realmente positivo."),
              ("Falso positivo", "Caso marcado como positivo que en realidad no lo es.")],
    seguir="En el cuaderno 23 verás las distribuciones binomial y de Poisson.",
),
# ---------------------------------------------------------------------------
dict(
    num=23, slug="P23_binomial_y_poisson", unidad=U,
    titulo="Variables aleatorias discretas: binomial y Poisson",
    datos=[], imports_extra="from scipy import stats\n",
    intro="""Si el 30 % de la población lee prensa digital y entrevistas a 20 personas, ¿cuántas lo harán? Si una agencia recibe de media 4 alertas de bulos por hora, ¿qué probabilidad hay de recibir 10 en una hora? Estas preguntas se responden con **modelos de probabilidad**: la **binomial** para contar éxitos en un número fijo de intentos y la **Poisson** para contar sucesos en un intervalo de tiempo.

**Qué necesitas saber antes**: los cuadernos 20 y 21.""",
    aprender=["Explicar qué es una variable aleatoria discreta y su distribución.",
              "Calcular probabilidades con la distribución binomial.",
              "Calcular probabilidades con la distribución de Poisson.",
              "Usar `scipy.stats` y comprobarlo con simulación."],
    secciones=[
        dict(titulo="Variables aleatorias", celdas=[
            M("""Una **variable aleatoria** asigna un número a cada resultado de un experimento aleatorio: el número de personas que leen prensa en una muestra, el número de alertas en una hora. Es **discreta** si toma valores que se cuentan (0, 1, 2...).

Su **distribución** dice la probabilidad de cada valor, y tiene una **media** (o esperanza, lo que sale «en promedio») y una **desviación típica**."""),
        ], quiz=[
            varias("¿Cuáles son variables aleatorias discretas?", [
                ("Número de lectores en una muestra de 20 personas", True, "¡Correcto!"), ("Número de bulos recibidos en una hora", True, "¡Correcto!"),
                ("Tiempo que tarda en hacerse viral un vídeo", False, "Es continua: puede tomar cualquier valor."), ("Número de goles en un partido", True, "¡Correcto!")]),
        ]),
        dict(titulo="La distribución binomial", celdas=[
            M("""La **binomial** $B(n, p)$ cuenta el número de **éxitos** en $n$ intentos **independientes**, cada uno con probabilidad $p$ de éxito.

- Media: $n \\cdot p$. Desviación típica: $\\sqrt{n\\,p\\,(1-p)}$.
- Ejemplo: número de personas que leen prensa digital entre 20 entrevistadas, si el 30 % lo hace: $B(20; 0{,}3)$."""),
            C("""n, p = 20, 0.3
X = stats.binom(n, p)
print("Media:", X.mean(), "  Desviación típica:", round(X.std(), 2))
print("P(X = 6)  =", round(X.pmf(6), 4))        # pmf: probabilidad de un valor concreto
print("P(X <= 3) =", round(X.cdf(3), 4))        # cdf: probabilidad acumulada
print("P(X >= 10) =", round(1 - X.cdf(9), 4))"""),
            C("""valores = np.arange(0, n + 1)
plt.bar(valores, X.pmf(valores), color="steelblue")
plt.xlabel("Número de lectores de prensa digital entre 20 personas")
plt.ylabel("Probabilidad")
plt.title("Distribución binomial B(20; 0,3)")
plt.show()"""),
            M("**Cómo leerlo**: lo más probable es encontrar unas 6 personas (la media), pero obtener 3 o 9 tampoco es raro. Por eso **una muestra pequeña puede dar porcentajes muy distintos del real**."),
        ], quiz=[
            numerica("Si X sigue una B(100; 0,4), ¿cuál es su media?", 39.99, 40.01, ok="¡Correcto! n · p = 100 · 0,4 = 40."),
        ]),
        dict(titulo="Comprobación por simulación", celdas=[
            M("Simulamos 10.000 encuestas de 20 personas y comparamos con la fórmula:"),
            C("""rng = np.random.default_rng(23)
muestras = rng.binomial(n, p, size=10_000)
print("P(X <= 3) simulada:", (muestras <= 3).mean(), "   exacta:", round(X.cdf(3), 4))"""),
        ], quiz=[
            unica("¿Por qué la probabilidad simulada no coincide exactamente con la exacta?", "Porque la simulación tiene su propio error aleatorio",
                  [("Porque la fórmula está mal", "La fórmula es exacta."), ("Porque la binomial no sirve", "Sirve; la diferencia viene del azar de la simulación.")]),
        ]),
        dict(titulo="La distribución de Poisson", celdas=[
            M("""La **Poisson** $P(\\lambda)$ cuenta sucesos que ocurren **al azar en un intervalo** (de tiempo o de espacio), con una media de $\\lambda$ por intervalo: alertas por hora, accidentes por fin de semana, cartas al director por día.

- Media y varianza: $\\lambda$."""),
            C("""lam = 4
Y = stats.poisson(lam)
print("P(Y = 4)   =", round(Y.pmf(4), 4))
print("P(Y >= 10) =", round(1 - Y.cdf(9), 5))
vals = np.arange(0, 15)
plt.bar(vals, Y.pmf(vals), color="darkorange")
plt.xlabel("Alertas de bulos en una hora")
plt.ylabel("Probabilidad")
plt.title("Poisson con media 4 alertas por hora")
plt.show()"""),
            M("""**Para qué sirve en una redacción**: si un fin de semana hay 9 accidentes mortales en una provincia donde la media es 4, ¿es algo excepcional? Con la Poisson, P(Y ≥ 9) ≈ 2 %: es raro, pero sucede alguna vez al año por puro azar. Antes de hablar de «repunte» hay que mirar más fines de semana."""),
            C("""print("P(9 o más accidentes | media 4) =", round(1 - stats.poisson(4).cdf(8), 4))"""),
        ], quiz=[
            unica("¿Qué distribución usarías para el número de llamadas que recibe una redacción en una hora?", "Poisson",
                  [("Binomial", "No hay un número fijo de intentos."), ("Ninguna", "La Poisson es el modelo clásico para sucesos en un intervalo.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 2", enunciado="En un municipio, el 60 % de los hogares tiene una suscripción digital. Si eliges 15 hogares al azar, ¿qué probabilidad hay de que **menos de la mitad** (7 o menos) tengan suscripción?",
             solucion='stats.binom(15, 0.6).cdf(7)'),
        dict(seccion="sección 2", enunciado="Dibuja las distribuciones B(10; 0,5) y B(100; 0,5) en dos gráficos. ¿Qué cambia en la forma?",
             solucion='''for n_ in [10, 100]:
    v = np.arange(0, n_ + 1)
    plt.bar(v, stats.binom(n_, 0.5).pmf(v))
    plt.title(f"B({n_}; 0,5)")
    plt.show()''', comentario="Con n grande la forma se parece a una campana: es la distribución normal del siguiente cuaderno."),
        dict(seccion="sección 4", enunciado="Una web recibe de media 2,5 denuncias de usuarios por día. ¿Qué probabilidad hay de que un día no reciba ninguna? ¿Y de que reciba 6 o más?",
             solucion='''Z = stats.poisson(2.5)
print(Z.pmf(0), 1 - Z.cdf(5))'''),
        dict(seccion="sección 4", enunciado="Simula 52 fines de semana con una media de 4 accidentes. ¿Cuántos tienen 9 o más?",
             solucion='(rng.poisson(4, size=52) >= 9).sum()'),
    ],
    resumen=["Una **variable aleatoria discreta** toma valores que se cuentan; su **distribución** da la probabilidad de cada uno.",
             "**Binomial** $B(n, p)$: éxitos en $n$ intentos independientes; media $np$.",
             "**Poisson** $P(\\lambda)$: sucesos al azar en un intervalo; media $\\lambda$.",
             "En `scipy.stats`: `pmf` (probabilidad de un valor), `cdf` (acumulada) y `1 - cdf` (cola superior).",
             "Un valor «excepcional» puede ser puro azar: calcula su probabilidad antes de titular «repunte»."],
    glosario=[("Variable aleatoria", "Número asociado al resultado de un experimento aleatorio."), ("Binomial", "Distribución del número de éxitos en n intentos independientes."),
              ("Poisson", "Distribución del número de sucesos en un intervalo."), ("Esperanza", "Media de una variable aleatoria."),
              ("`pmf` / `cdf`", "Función de probabilidad / función de distribución acumulada.")],
    errores=[("`P(X >= k)` sale mal", "Se ha usado `1 - cdf(k)`", "En discretas, P(X ≥ k) = 1 − cdf(k − 1)")],
    seguir="En el cuaderno 24 estudiarás la distribución más importante: la normal.",
),
# ---------------------------------------------------------------------------
dict(
    num=24, slug="P24_distribucion_normal", unidad=U,
    titulo="La distribución normal",
    datos=["encuesta_medios.csv"], imports_extra="from scipy import stats\n",
    intro="""La campana de Gauss aparece en las alturas, en los errores de medida y, sobre todo, en **las encuestas**: si repitiéramos muchas veces una encuesta, sus resultados formarían una campana alrededor del valor real. Por eso la **distribución normal** es la base del margen de error. Este cuaderno es el puente entre la probabilidad y la inferencia.

**Qué necesitas saber antes**: los cuadernos 10 (desviación típica), 11 (puntuaciones z) y 23.""",
    aprender=["Describir la distribución normal y sus parámetros.",
              "Usar la regla 68–95–99,7.",
              "Calcular probabilidades y percentiles con `scipy.stats.norm`.",
              "Ver cómo la binomial se aproxima a la normal cuando n es grande."],
    secciones=[
        dict(titulo="La campana", celdas=[
            M("""Una variable **normal** $N(\\mu, \\sigma)$ es continua, simétrica y con forma de campana. Queda totalmente determinada por su **media** $\\mu$ (el centro) y su **desviación típica** $\\sigma$ (la anchura).

En una variable continua no tiene sentido la probabilidad de un valor exacto: se calcula la probabilidad de un **intervalo**, que es el **área bajo la curva**."""),
            C("""x = np.linspace(-4, 4, 400)
for mu, sigma in [(0, 1), (0, 2), (1.5, 0.7)]:
    plt.plot(x, stats.norm(mu, sigma).pdf(x), label=f"N({mu}, {sigma})")
plt.legend()
plt.title("Tres normales: la media mueve, la desviación típica ensancha")
plt.show()"""),
        ], quiz=[
            unica("¿Qué parámetro de la normal controla su anchura?", "La desviación típica σ",
                  [("La media μ", "La media desplaza la campana."), ("El tamaño de muestra", "No es un parámetro de la normal.")]),
        ]),
        dict(titulo="La regla 68–95–99,7", celdas=[
            M("""En cualquier normal:

- el **68 %** de los valores está a menos de 1 σ de la media;
- el **95 %**, a menos de 2 σ (más exactamente 1,96 σ);
- el **99,7 %**, a menos de 3 σ."""),
            C("""Z = stats.norm(0, 1)            # normal estándar
for k in [1, 1.96, 2, 3]:
    print(f"P(-{k} < Z < {k}) = {Z.cdf(k) - Z.cdf(-k):.4f}")"""),
            C("""xs = np.linspace(-4, 4, 400)
plt.plot(xs, Z.pdf(xs), color="black")
plt.fill_between(xs, Z.pdf(xs), where=np.abs(xs) <= 1.96, color="steelblue", alpha=0.4, label="95 % central")
plt.legend()
plt.title("El 95 % del área está entre −1,96 y 1,96")
plt.show()"""),
            M("Este **1,96** volverá a aparecer en el margen de error de las encuestas (cuaderno 27)."),
        ], quiz=[
            unica("En una normal, ¿qué porcentaje de valores queda a más de 2 desviaciones típicas de la media (por cualquiera de los dos lados)?", "Alrededor del 5 %",
                  [("Alrededor del 32 %", "Eso es fuera de 1 σ."), ("Alrededor del 0,3 %", "Eso es fuera de 3 σ.")]),
        ]),
        dict(titulo="Calcular probabilidades y percentiles", celdas=[
            M("""Para calcular con cualquier normal se **tipifica** (como en el cuaderno 11): $z = (x - \\mu) / \\sigma$. Con `scipy` no hace falta: `cdf(x)` da $P(X \\le x)$ y `ppf(q)` da el valor que deja por debajo la proporción $q$."""),
            C("""enc = pd.read_csv("encuesta_medios.csv")
conf = enc["confianza_medios"].dropna()
mu, sigma = conf.mean(), conf.std()
print(f"Confianza: media {mu:.2f}, desviación típica {sigma:.2f}")

modelo = stats.norm(mu, sigma)
print("P(confianza <= 3) según la normal:", round(modelo.cdf(3.5), 3))   # 3,5: corrección por ser valores enteros
print("Proporción real en los datos:      ", round((conf <= 3).mean(), 3))
print("Percentil 90 según la normal:", round(modelo.ppf(0.9), 1))"""),
            M("**Cómo leerlo**: la normal describe bastante bien la confianza en los medios (que es casi simétrica). En variables asimétricas, como los salarios, el modelo normal daría resultados malos: compruébalo siempre con un histograma."),
        ], quiz=[
            unica("¿Qué devuelve `stats.norm(0, 1).ppf(0.975)`?", "Aproximadamente 1,96",
                  [("0,975", "ppf devuelve un valor de x, no una probabilidad."), ("0,025", "Eso sería la cola superior.")]),
        ]),
        dict(titulo="La binomial se vuelve normal", celdas=[
            M("""Cuando $n$ es grande, la binomial $B(n, p)$ se parece mucho a una normal con la misma media ($np$) y la misma desviación típica ($\\sqrt{np(1-p)}$). Es lo que pasa con el número de «síes» en una encuesta grande, y la razón de que el margen de error use la normal."""),
            C("""n, p = 1000, 0.34
B = stats.binom(n, p)
N = stats.norm(n * p, np.sqrt(n * p * (1 - p)))
k = np.arange(280, 400)
plt.bar(k, B.pmf(k), color="lightgrey", label="Binomial B(1000; 0,34)")
plt.plot(k, N.pdf(k), color="firebrick", label="Normal aproximada")
plt.legend()
plt.xlabel("Personas que votarían a A entre 1.000 entrevistadas")
plt.show()

print(f"Entre el {(n*p - 1.96*np.sqrt(n*p*(1-p)))/n:.1%} y el {(n*p + 1.96*np.sqrt(n*p*(1-p)))/n:.1%} de los votos, con un 95 % de probabilidad")"""),
            M("**Qué ha pasado**: si el 34 % de la población votara a A, una encuesta de 1.000 personas daría un resultado entre el 31 % y el 37 % en el 95 % de las ocasiones. Esa horquilla de unos ±3 puntos es el **margen de error** del que hablaremos en la unidad 5."),
        ], quiz=[
            unica("¿Por qué la normal es tan importante para las encuestas?", "Porque los resultados de encuestas grandes repetidas se reparten como una normal",
                  [("Porque las opiniones de la gente son normales", "Las opiniones pueden tener cualquier forma; lo normal es la distribución del resultado de la encuesta."), ("Porque todas las variables son normales", "Muchas no lo son, como los salarios.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 2", enunciado="Si la altura de una población sigue una N(170, 8) cm, ¿qué porcentaje mide más de 186 cm? Hazlo primero con la regla 68–95–99,7 y luego con `scipy`.",
             solucion='1 - stats.norm(170, 8).cdf(186)', comentario="186 es la media + 2σ: queda fuera alrededor de un 2,5 % (la mitad del 5 %)."),
        dict(seccion="sección 3", enunciado="Con el modelo normal de la confianza, ¿qué valor deja por encima al 10 % de las personas más confiadas?",
             solucion='modelo.ppf(0.9)'),
        dict(seccion="sección 3", enunciado="Dibuja el histograma de la confianza (con `density=True`) y encima la curva normal ajustada.",
             solucion='''plt.hist(conf, bins=range(0, 12), density=True, align="left", color="lightgrey")
xs = np.linspace(0, 10, 200)
plt.plot(xs, modelo.pdf(xs), color="firebrick")
plt.show()'''),
        dict(seccion="sección 4", enunciado="Repite la horquilla del 95 % para una encuesta de 400 personas y otra de 4.000 (con p = 0,34). ¿Qué le pasa al margen?",
             solucion='''for n_ in [400, 4000]:
    e = 1.96 * np.sqrt(p * (1 - p) / n_)
    print(n_, round(p - e, 3), round(p + e, 3))''', comentario="Al multiplicar por 10 el tamaño, el margen se divide por √10 ≈ 3,2."),
    ],
    resumen=["La **normal** $N(\\mu, \\sigma)$ es simétrica, con forma de campana; $\\mu$ la centra y $\\sigma$ la ensancha.",
             "Regla **68–95–99,7**: a 1, 2 y 3 desviaciones típicas de la media; el 95 % exacto está a ±1,96 σ.",
             "En `scipy.stats.norm`: `cdf` da probabilidades acumuladas y `ppf` percentiles.",
             "Con $n$ grande, la **binomial** se aproxima por una normal: es la base del **margen de error**.",
             "Antes de usar la normal como modelo, comprueba con un histograma que los datos son aproximadamente simétricos."],
    glosario=[("Distribución normal", "Distribución continua simétrica en forma de campana."), ("Normal estándar", "Normal con media 0 y desviación típica 1."),
              ("Tipificar", "Restar la media y dividir por la desviación típica."), ("`ppf`", "Función que devuelve el valor de un percentil.")],
    seguir="Con esto termina la unidad 4. En el cuaderno 25 empieza la inferencia: población, muestra y tipos de muestreo.",
),
]
