from _comun import C, M, numerica, unica, varias

U = "1. Introducción"

CUADERNOS = [
# ---------------------------------------------------------------------------
dict(
    num=1, slug="P01_estadistica_y_periodismo", unidad=U,
    titulo="Estadística para contar historias: Colab y primeros datos",
    datos=["encuesta_medios.csv"],
    intro="""Casi cualquier noticia lleva números: el paro baja un 2 %, la mitad de los jóvenes se informa por redes, una encuesta da empate técnico. Un periodista que no sabe leer esas cifras **las repite**; uno que sabe, **las comprueba, las explica y encuentra la historia que esconden**.

La Estadística es la herramienta para eso: resumir muchos datos en pocas cifras honestas, ver si una diferencia es real o casualidad, y medir cuánto nos podemos fiar de una muestra. En este curso la aprenderemos haciendo **periodismo de datos** con Python, en cuadernos como este.

**Qué necesitas saber antes**: nada. Este es el primer cuaderno.""",
    aprender=["Explicar para qué sirve la Estadística en el trabajo periodístico.",
              "Usar Google Colab: celdas de texto y de código, ejecutar y guardar.",
              "Cargar una tabla de datos y obtener tu primer recuento y tu primer gráfico."],
    secciones=[
        dict(titulo="Por qué un periodista necesita Estadística", celdas=[
            M("""Mira estos titulares inventados, pero muy parecidos a los reales:

| Titular | Qué hay que preguntar |
| :-- | :-- |
| «El salario medio de los periodistas supera los 29.000 euros» | ¿Media o mediana? Unos pocos sueldos altos suben mucho la media. |
| «Los delitos se disparan un 50 %» | ¿De 2 a 3 casos o de 2.000 a 3.000? ¿Porcentaje o puntos? |
| «El partido A gana: 34 % frente a 33 %» | Con 1.000 entrevistas el margen de error es de unos ±3 puntos: es un empate. |
| «Quien lee prensa vive más» | ¿Causa o simple asociación? Quizá ambas cosas dependen de la renta. |

Cada fila es un tema de este curso: **medidas de centralización**, **tasas de variación y números índice**, **margen de error** y **correlación frente a causalidad**."""),
            M("""La guía docente organiza la asignatura en cinco unidades, y estos 30 cuadernos las siguen en orden:

1. **Introducción** (cuadernos 1–4): Colab, Python mínimo y tablas de datos.
2. **Estadística descriptiva** (5–13): resumir y representar datos.
3. **Números índice y series cronológicas** (14–19): IPC, términos reales, tendencias.
4. **Probabilidad** (20–24): azar, probabilidad condicionada, binomial y normal.
5. **Inferencia** (25–30): muestras, encuestas, margen de error y contrastes."""),
        ], quiz=[
            unica("Una encuesta con 1.000 entrevistas da 34 % al partido A y 33 % al partido B. ¿Qué titular es más correcto?",
                  "«Empate técnico entre A y B»",
                  [("«A gana a B»", "La diferencia (1 punto) es menor que el margen de error de una muestra así."),
                   ("«B se hunde»", "Nada en los datos dice que B baje."),
                   ("«A supera a B por un 3 %»", "La diferencia es de 1 punto, no de un 3 %.")]),
        ]),
        dict(titulo="Google Colab en cinco minutos", celdas=[
            M("""Un **cuaderno** mezcla dos tipos de celdas:

- **Celdas de texto** (como esta): explicaciones con formato. Haz doble clic para editarlas.
- **Celdas de código**: instrucciones en Python. Se ejecutan con el botón ▶ o con **Mayús + Intro**, y el resultado aparece debajo.

Colab se ejecuta en un ordenador de Google: no hay que instalar nada. Para guardar tus cambios usa **Archivo → Guardar una copia en Drive**."""),
            M("**Qué vamos a hacer**: ejecutar nuestra primera celda de código. Python puede funcionar como calculadora."),
            C("""# Esto es un comentario: Python ignora todo lo que va detrás de #
3200 / 4000 * 100"""),
            M("**Qué ha pasado**: Python ha calculado qué porcentaje son 3.200 lectores de un total de 4.000: un 80 %. La última línea de una celda se muestra siempre como resultado."),
            M("Con `print()` podemos mostrar varios resultados y añadir texto:"),
            C("""print("Lectores de pago:", 3200)
print("Porcentaje:", 3200 / 4000 * 100, "%")"""),
        ], quiz=[
            varias("¿Qué afirmaciones sobre Colab son ciertas?", [
                ("Las celdas de código se ejecutan con Mayús + Intro", True, "¡Correcto!"),
                ("Hay que instalar Python en el ordenador", False, "No: Colab se ejecuta en servidores de Google."),
                ("Si Colab se desconecta hay que volver a ejecutar la configuración", True, "¡Correcto! Los ficheros descargados se borran."),
                ("Lo que va detrás de # se ejecuta como código", False, "No: es un comentario y Python lo ignora."),
            ]),
        ]),
        dict(titulo="Tu primer análisis: ¿por dónde se informa la gente?", celdas=[
            M("""Vamos a usar una **encuesta simulada** a 1.200 personas de la Comunitat Valenciana sobre cómo consumen noticias. Cada **fila** es una persona entrevistada y cada **columna** una pregunta.

**Qué vamos a hacer**: leer el fichero con la librería *Pandas* y ver las cinco primeras filas."""),
            C("""encuesta = pd.read_csv("encuesta_medios.csv")
encuesta.head()"""),
            M("**Qué ha pasado**: `pd.read_csv()` ha leído el fichero y lo ha guardado con el nombre `encuesta`. `head()` muestra las primeras filas. Ya verás estas funciones con calma en el cuaderno 4."),
            M("Ahora contamos cuántas personas eligen cada medio como fuente principal, con `value_counts()`:"),
            C("""encuesta["medio_principal"].value_counts()"""),
            M("Y lo convertimos en un gráfico de barras, que es como mejor se lee un recuento:"),
            C("""recuento = encuesta["medio_principal"].value_counts()
recuento.plot(kind="barh", color="steelblue")
plt.title("Medio principal para informarse (encuesta simulada, n = 1.200)")
plt.xlabel("Número de personas")
plt.show()"""),
            M("""**Cómo leerlo**: la televisión sigue siendo el medio más citado, seguida de la prensa digital y las redes sociales. Fíjate en que el título del gráfico dice **qué** se mide, **de dónde** sale y **cuántas** personas: es lo mínimo que debe llevar cualquier gráfico que publiques."""),
        ], quiz=[
            unica("En la tabla `encuesta`, ¿qué representa cada fila?",
                  "Una persona entrevistada",
                  [("Un medio de comunicación", "No: los medios son los valores de la columna medio_principal."),
                   ("Una pregunta de la encuesta", "No: las preguntas son las columnas."),
                   ("Una provincia", "No: la provincia es una columna más.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 2", enunciado="Calcula con Python qué porcentaje representan 264 personas sobre un total de 1.200.",
             solucion="264 / 1200 * 100"),
        dict(seccion="sección 3", enunciado="Cuenta cuántas personas hay de cada provincia en la encuesta.",
             solucion='encuesta["provincia"].value_counts()'),
        dict(seccion="sección 3", enunciado="Haz un gráfico de barras horizontales con el nivel de estudios de las personas entrevistadas. Ponle un título que diga qué se mide y de dónde salen los datos.",
             solucion='''encuesta["estudios"].value_counts().plot(kind="barh", color="steelblue")
plt.title("Nivel de estudios (encuesta simulada, n = 1.200)")
plt.show()'''),
        dict(seccion="sección 1", enunciado="Escribe en una celda de texto (botón **+ Texto**) un titular honesto con el resultado del gráfico de medios, y debajo una frase que diga qué precaución tendría que mencionar la noticia.",
             comentario="Por ejemplo: «La televisión sigue siendo la primera fuente de noticias para más de un tercio de la población». Precaución: es una encuesta (una muestra), así que las cifras tienen margen de error; y aquí, además, los datos son simulados."),
    ],
    resumen=["La Estadística sirve al periodista para **comprobar, resumir y explicar** cifras, y para no repetir errores ajenos.",
             "Un cuaderno de Colab combina **texto** y **código**; el código se ejecuta con ▶ o Mayús + Intro.",
             "En una tabla de datos, **cada fila es un caso** (una persona) y **cada columna una variable** (una pregunta).",
             "`value_counts()` cuenta cuántas veces aparece cada valor; `plot(kind=\"barh\")` lo dibuja.",
             "Todo gráfico publicado debe decir **qué se mide, de dónde salen los datos y cuántos casos hay**."],
    glosario=[("Cuaderno (notebook)", "Documento que mezcla texto y código ejecutable."),
              ("Celda", "Bloque de texto o de código dentro de un cuaderno."),
              ("Caso", "Cada unidad sobre la que se recogen datos (una persona, un municipio, un día)."),
              ("Variable", "Cada característica que se mide de los casos (edad, medio principal...)."),
              ("Periodismo de datos", "Periodismo que obtiene, analiza y visualiza datos para contar historias.")],
    seguir="En el cuaderno 2 aprenderás lo mínimo de Python que necesitas: números, textos, listas y condiciones.",
),
# ---------------------------------------------------------------------------
dict(
    num=2, slug="P02_python_minimo_1", unidad=U,
    titulo="Python mínimo (I): números, textos, listas y condiciones",
    datos=[], imports=False,
    intro="""No hace falta ser programador para hacer periodismo de datos, pero sí manejar cuatro piezas de Python: **variables**, **textos**, **listas** y **condiciones**. Con ellas ya puedes calcular una tasa de variación, escribir un titular automático o separar los municipios que superan un umbral.

**Qué necesitas saber antes**: el cuaderno 1 (cómo ejecutar celdas).""",
    aprender=["Guardar valores en variables y operar con ellas.",
              "Escribir textos con cifras usando *f-strings* y redondear correctamente.",
              "Guardar varios datos en una lista y calcular con ella.",
              "Tomar decisiones con `if`, `elif` y `else`."],
    secciones=[
        dict(titulo="Variables y operaciones", celdas=[
            M("""Una **variable** es un nombre que guarda un valor. Se crea con `=`. Elige nombres que expliquen qué guardan, sin tildes ni espacios (`parados_enero`, no `p1`)."""),
            C("""parados_enero = 182450
parados_febrero = 179630

diferencia = parados_febrero - parados_enero
print("Diferencia absoluta:", diferencia)"""),
            M("""Las operaciones básicas son `+`, `-`, `*`, `/` y `**` (potencia). Con ellas calculamos la **tasa de variación**, la cifra más usada en prensa:

$$\\text{tasa de variación (\\%)} = \\frac{\\text{valor final} - \\text{valor inicial}}{\\text{valor inicial}} \\times 100$$"""),
            C("""tasa = (parados_febrero - parados_enero) / parados_enero * 100
print("Tasa de variación:", tasa, "%")
print("Redondeada:", round(tasa, 1), "%")"""),
            M("""**Qué ha pasado**: el paro ha bajado un 1,5 %. `round(valor, 1)` deja un decimal: en prensa casi nunca se publican más de uno o dos.

⚠️ Python usa **punto** como separador decimal (`1.5`), no coma."""),
        ], quiz=[
            numerica("Una cabecera pasa de 12.500 a 15.000 suscriptores. ¿Cuál es su tasa de variación en %? (escribe solo el número)",
                     19.99, 20.01, ok="¡Correcto! (15000 − 12500) / 12500 × 100 = 20 %."),
        ]),
        dict(titulo="Textos y titulares automáticos", celdas=[
            M("""Los textos (tipo `str`) van entre comillas. Una **f-string** (una `f` delante de las comillas) permite meter variables dentro del texto con llaves `{}`. Así se escriben los titulares automáticos de muchas redacciones."""),
            C("""provincia = "Alicante"
tasa = -1.53
titular = f"El paro baja un {abs(tasa):.1f} % en {provincia}"
print(titular)"""),
            M("""**Qué ha pasado**: `{abs(tasa):.1f}` escribe el valor absoluto de la tasa con un decimal. `abs()` quita el signo porque el verbo «baja» ya lo indica."""),
            M("Algunas operaciones útiles con textos:"),
            C("""medio = "  prensa Digital "
print(medio.strip())          # quita espacios al principio y al final
print(medio.strip().lower())  # todo en minúsculas
print(medio.strip().title())  # Mayúscula Inicial
print(len("Estadística"))     # número de caracteres"""),
            M("Limpiar textos así es habitual: en los datos reales «Prensa digital», «prensa digital » y «PRENSA DIGITAL» serían tres categorías distintas si no los unificamos."),
        ], quiz=[
            unica("¿Qué escribe `print(f\"Sube un {12.345:.1f} %\")`?", "Sube un 12.3 %",
                  [("Sube un 12.345 %", "`.1f` deja un solo decimal."),
                   ("Sube un {12.345:.1f} %", "Con la f delante, lo que va entre llaves se sustituye por su valor."),
                   ("Sube un 12 %", "`.1f` deja un decimal, no cero.")]),
        ]),
        dict(titulo="Listas: varios datos juntos", celdas=[
            M("""Una **lista** guarda varios valores en orden, entre corchetes. Es la forma más sencilla de guardar, por ejemplo, la audiencia de una semana."""),
            C("""audiencia = [1520, 1610, 1480, 1730, 1390, 980, 1100]   # miles de espectadores, de lunes a domingo
print("Días:", len(audiencia))
print("Total semanal:", sum(audiencia))
print("Máximo:", max(audiencia), "Mínimo:", min(audiencia))
print("Media diaria:", round(sum(audiencia) / len(audiencia), 1))"""),
            M("""Cada elemento tiene una **posición** que empieza en **0**. `audiencia[0]` es el lunes y `audiencia[-1]` el último (domingo). Con `[a:b]` se toma un trozo, desde `a` hasta `b` **sin incluir** `b`."""),
            C("""print("Lunes:", audiencia[0])
print("Domingo:", audiencia[-1])
print("Fin de semana:", audiencia[5:7])"""),
            M("Para añadir un dato usamos `append()`:"),
            C("""audiencia.append(1650)   # el lunes siguiente
print(audiencia)"""),
        ], quiz=[
            unica("Con `audiencia = [1520, 1610, 1480, 1730, 1390, 980, 1100]`, ¿qué devuelve `audiencia[1:3]`?",
                  "[1610, 1480]",
                  [("[1520, 1610, 1480]", "La posición 0 no está incluida, porque empezamos en 1."),
                   ("[1610, 1480, 1730]", "El final (posición 3) no se incluye."),
                   ("[1520, 1610]", "Las posiciones empiezan en 0: la 1 es el martes.")]),
        ]),
        dict(titulo="Condiciones: decidir con los datos", celdas=[
            M("""Con `if` el código hace una cosa u otra según se cumpla una condición. Las comparaciones son `>`, `<`, `>=`, `<=`, `==` (igual) y `!=` (distinto). Las líneas que dependen del `if` van **sangradas** (con 4 espacios)."""),
            C("""tasa = -1.53

if tasa > 0:
    verbo = "sube"
elif tasa < 0:
    verbo = "baja"
else:
    verbo = "se mantiene"

print(f"El paro {verbo} un {abs(tasa):.1f} %")"""),
            M("**Qué ha pasado**: como la tasa es negativa, se cumple la segunda condición y el verbo es «baja». Prueba a cambiar `tasa` por `2.4` o por `0` y vuelve a ejecutar."),
            M("Las condiciones se combinan con `and` (las dos) y `or` (al menos una):"),
            C("""share = 14.2
franja = "Prime time"
if share > 12 and franja == "Prime time":
    print("Programa líder en su franja")"""),
        ], quiz=[
            unica("Si `share = 9.5`, ¿qué imprime este código?\n\n`if share >= 10: print('Éxito')` / `else: print('Por debajo')`",
                  "Por debajo", [("Éxito", "9,5 no es mayor ni igual que 10."), ("Nada", "Siempre se ejecuta una de las dos ramas.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Un diario tenía 48.200 lectores en 2023 y 51.900 en 2024. Calcula la tasa de variación con un decimal.",
             solucion="round((51900 - 48200) / 48200 * 100, 1)"),
        dict(seccion="sección 2", enunciado="Con la variable `ciudad = \"Elche\"` y `tasa = 3.27`, escribe el titular «La audiencia sube un 3,3 % en Elche» con una f-string.",
             solucion='''ciudad = "Elche"
tasa = 3.27
print(f"La audiencia sube un {tasa:.1f} % en {ciudad}")''',
             comentario="Python escribe el decimal con punto (3.3). En el cuaderno 4 verás cómo dar formato español a las cifras."),
        dict(seccion="sección 3", enunciado="Guarda en una lista las visitas web de una semana: 41200, 43900, 40500, 39800, 42100, 35300, 36800. Calcula la media diaria y la diferencia entre el día con más y el día con menos visitas.",
             solucion='''visitas = [41200, 43900, 40500, 39800, 42100, 35300, 36800]
print(sum(visitas) / len(visitas))
print(max(visitas) - min(visitas))'''),
        dict(seccion="sección 4", enunciado="Escribe un código que, dada una variable `tasa`, imprima «Fuerte subida» si es mayor que 5, «Subida» si está entre 0 y 5, y «Bajada» si es negativa.",
             solucion='''tasa = 3.1
if tasa > 5:
    print("Fuerte subida")
elif tasa >= 0:
    print("Subida")
else:
    print("Bajada")'''),
    ],
    resumen=["Una **variable** guarda un valor: `nombre = valor`. Usa nombres descriptivos.",
             "La **tasa de variación** es (final − inicial) / inicial × 100. Redondea con `round()`.",
             "Las **f-strings** (`f\"... {variable:.1f} ...\"`) meten cifras en un texto con el formato que quieras.",
             "Una **lista** guarda datos en orden; las posiciones empiezan en **0** y en `[a:b]` el final no se incluye.",
             "`if` / `elif` / `else` ejecutan un bloque u otro según una condición; el bloque va sangrado."],
    glosario=[("Variable", "Nombre que guarda un valor."), ("`str`", "Tipo de dato de texto."),
              ("f-string", "Texto con `f` delante donde lo que va entre llaves se sustituye por su valor."),
              ("Lista", "Colección ordenada de valores entre corchetes."),
              ("Tasa de variación", "Cambio relativo entre dos valores, en porcentaje.")],
    errores=[("`SyntaxError` con una coma decimal", "Has escrito `1,5` en lugar de `1.5`", "Usa el punto como separador decimal"),
             ("`IndentationError`", "El bloque del `if` no está sangrado", "Pon 4 espacios delante de las líneas del bloque"),
             ("`IndexError: list index out of range`", "Pides una posición que no existe", "Recuerda que la última posición es `len(lista) - 1`")],
    seguir="En el cuaderno 3 verás bucles, funciones y diccionarios, y aprenderás a usar librerías.",
),
# ---------------------------------------------------------------------------
dict(
    num=3, slug="P03_python_minimo_2", unidad=U,
    titulo="Python mínimo (II): bucles, funciones, diccionarios y librerías",
    datos=[], imports=False,
    intro="""Cuando tengas que calcular la misma tasa para 140 municipios no lo harás a mano: escribirás una **función** y la repetirás con un **bucle**. Y cuando quieras guardar datos con etiqueta (municipio → población) usarás un **diccionario**. Con esto y las **librerías** de Python ya tienes todo lo necesario para el resto del curso.

**Qué necesitas saber antes**: el cuaderno 2.""",
    aprender=["Repetir una operación con un bucle `for`.",
              "Escribir tus propias funciones con `def`.",
              "Guardar datos con etiqueta en un diccionario.",
              "Importar y usar librerías: `math`, `statistics`, Pandas y matplotlib."],
    secciones=[
        dict(titulo="Bucles: repetir sin copiar y pegar", celdas=[
            M("""Un bucle `for` recorre los elementos de una lista y ejecuta el bloque sangrado una vez para cada uno."""),
            C("""cadenas = ["Cadena 1", "Cadena 2", "Cadena 3"]
for cadena in cadenas:
    print("Analizando", cadena)"""),
            M("""**Qué vamos a hacer**: calcular la tasa de variación mensual del paro para varios meses seguidos. `range(1, n)` genera los números 1, 2, ..., n−1."""),
            C("""parados = [182450, 179630, 176200, 171900, 168050]
meses = ["enero", "febrero", "marzo", "abril", "mayo"]

for i in range(1, len(parados)):
    tasa = (parados[i] - parados[i - 1]) / parados[i - 1] * 100
    print(f"{meses[i]}: {tasa:.1f} %")"""),
            M("**Qué ha pasado**: en cada vuelta `i` vale 1, 2, 3 y 4, y comparamos cada mes con el anterior (`i - 1`). Enero no tiene tasa porque no hay mes previo."),
        ], quiz=[
            unica("¿Cuántas veces se ejecuta el bloque de `for i in range(1, 5):`?", "4 veces (i = 1, 2, 3, 4)",
                  [("5 veces", "`range(1, 5)` no incluye el 5."), ("1 vez", "El bucle se repite para cada valor del rango.")]),
        ]),
        dict(titulo="Funciones: cálculos que reutilizas", celdas=[
            M("""Una **función** guarda un cálculo con un nombre. Se define con `def`, recibe **argumentos** entre paréntesis y devuelve un resultado con `return`."""),
            C("""def tasa_variacion(inicial, final):
    \"\"\"Devuelve la tasa de variación en %, con un decimal.\"\"\"
    return round((final - inicial) / inicial * 100, 1)

print(tasa_variacion(12500, 15000))
print(tasa_variacion(182450, 179630))"""),
            M("Una función puede usar a otra. Esta escribe el titular completo:"),
            C("""def titular_paro(lugar, inicial, final):
    t = tasa_variacion(inicial, final)
    verbo = "sube" if t > 0 else "baja"
    return f"El paro {verbo} un {abs(t)} % en {lugar}"

print(titular_paro("Alicante", 182450, 179630))
print(titular_paro("Castellón", 41200, 42150))"""),
            M("**Qué ha pasado**: `verbo = \"sube\" if t > 0 else \"baja\"` es una forma corta del `if` en una sola línea. Con dos funciones ya hemos automatizado un titular."),
        ], quiz=[
            unica("¿Qué devuelve `tasa_variacion(200, 150)`?", "-25.0",
                  [("25.0", "El valor baja, así que la tasa es negativa."), ("-50.0", "Se divide entre el valor inicial (200), no entre el final."),
                   ("33.3", "Revisa qué valor va en el denominador.")]),
        ]),
        dict(titulo="Diccionarios: datos con etiqueta", celdas=[
            M("""Un **diccionario** guarda pares **clave → valor** entre llaves. Es ideal para datos con nombre, como la población de cada ciudad."""),
            C("""poblacion = {"Alicante": 349282, "Elche": 235580, "Torrevieja": 89000}
print(poblacion["Elche"])
poblacion["Orihuela"] = 80000          # añadir una clave nueva
for ciudad, habitantes in poblacion.items():
    print(f"{ciudad}: {habitantes} habitantes")"""),
            M("⚠️ Las cifras de población de este ejemplo son aproximadas y solo sirven para practicar."),
        ], quiz=[
            unica("Con `d = {\"A\": 10, \"B\": 20}`, ¿cómo se obtiene el 20?", "d[\"B\"]",
                  [("d[1]", "En un diccionario se accede por clave, no por posición."), ("d(\"B\")", "Se usan corchetes, no paréntesis.")]),
        ]),
        dict(titulo="Librerías: no reinventes la rueda", celdas=[
            M("""Una **librería** es un conjunto de funciones ya escritas. Se cargan con `import`. Las que usaremos en todo el curso son:

| Librería | Para qué | Cómo se importa |
| :-- | :-- | :-- |
| `statistics` | Medidas sencillas (media, mediana) | `import statistics` |
| NumPy | Cálculo con muchos números | `import numpy as np` |
| Pandas | Tablas de datos | `import pandas as pd` |
| matplotlib | Gráficos | `import matplotlib.pyplot as plt` |"""),
            C("""import statistics
sueldos = [21000, 23500, 24800, 26100, 27000, 31000, 95000]
print("Media:", round(statistics.mean(sueldos)))
print("Mediana:", statistics.median(sueldos))"""),
            M("**Qué ha pasado**: un solo sueldo muy alto (95.000) arrastra la media hasta 35.486, mientras que la mediana (26.100) describe mejor al trabajador típico. Lo estudiaremos en el cuaderno 8."),
            C("""import pandas as pd
import matplotlib.pyplot as plt

serie = pd.Series(sueldos, name="sueldo")
serie.plot(kind="bar", color="steelblue")
plt.title("Siete sueldos inventados")
plt.show()"""),
        ], quiz=[
            varias("¿Qué instrucciones importan correctamente una librería?", [
                ("import pandas as pd", True, "¡Correcto!"), ("import statistics", True, "¡Correcto!"),
                ("pandas import pd", False, "El orden es `import librería as alias`."),
                ("import matplotlib.pyplot as plt", True, "¡Correcto!")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Con la lista `share = [11.2, 12.5, 10.8, 13.1, 9.7]` (cinco programas), recorre la lista con un bucle e imprime «Por encima» si el share supera el 11 % y «Por debajo» si no.",
             solucion='''share = [11.2, 12.5, 10.8, 13.1, 9.7]
for s in share:
    print(s, "Por encima" if s > 11 else "Por debajo")'''),
        dict(seccion="sección 2", enunciado="Escribe una función `porcentaje(parte, total)` que devuelva el porcentaje con un decimal. Pruébala con 264 de 1.200.",
             solucion='''def porcentaje(parte, total):
    return round(parte / total * 100, 1)

porcentaje(264, 1200)'''),
        dict(seccion="sección 3", enunciado="Crea un diccionario con los espectadores (en miles) de tres informativos: «Noticias 1»: 2100, «Noticias 2»: 1850, «Noticias 3»: 1230. Recórrelo e imprime el porcentaje de cada uno sobre el total de los tres.",
             solucion='''espect = {"Noticias 1": 2100, "Noticias 2": 1850, "Noticias 3": 1230}
total = sum(espect.values())
for prog, e in espect.items():
    print(prog, round(e / total * 100, 1), "%")'''),
        dict(seccion="sección 4", enunciado="Importa `statistics` y calcula la media y la mediana de los minutos diarios que dedican a las noticias estas personas: 15, 20, 20, 25, 30, 35, 240. ¿Cuál describe mejor a la persona típica?",
             solucion='''import statistics
m = [15, 20, 20, 25, 30, 35, 240]
print(statistics.mean(m), statistics.median(m))''',
             comentario="La mediana (25 minutos): el valor 240 infla la media hasta unos 55 minutos."),
    ],
    resumen=["Un bucle **`for`** repite un bloque para cada elemento; `range(a, b)` va de a hasta b−1.",
             "Una **función** (`def nombre(argumentos): ... return resultado`) guarda un cálculo para reutilizarlo.",
             "Un **diccionario** guarda pares clave → valor y se consulta con `d[clave]`.",
             "Las **librerías** se cargan con `import`; en el curso usaremos `pd`, `np` y `plt`.",
             "Con valores extremos, la **mediana** describe mejor el caso típico que la media."],
    glosario=[("Bucle", "Instrucción que repite un bloque de código."), ("Función", "Bloque de código con nombre que recibe datos y devuelve un resultado."),
              ("Argumento", "Dato que se le pasa a una función."), ("Diccionario", "Colección de pares clave → valor."),
              ("Librería", "Conjunto de funciones listas para usar.")],
    errores=[("`KeyError` en un diccionario", "La clave no existe o está escrita distinta", "Revisa mayúsculas y tildes con `d.keys()`"),
             ("La función no devuelve nada (`None`)", "Falta el `return`", "Añade `return resultado` al final de la función")],
    seguir="En el cuaderno 4 empezarás a trabajar con tablas de datos reales... simuladas: leer, explorar, filtrar y limpiar con Pandas.",
),
# ---------------------------------------------------------------------------
dict(
    num=4, slug="P04_tablas_de_datos_con_pandas", unidad=U,
    titulo="Tablas de datos con Pandas: leer, explorar, filtrar y limpiar",
    datos=["encuesta_medios.csv", "salarios_redaccion.csv"],
    intro="""Los datos de un periodista llegan casi siempre en forma de **tabla**: una hoja de cálculo del portal de transparencia, un CSV del INE, la base de datos de una encuesta. *Pandas* es la librería de Python para trabajar con esas tablas, que llama **dataframes**.

Antes de contar ninguna historia con una tabla hay que **conocerla**: cuántas filas tiene, qué significa cada columna, qué datos faltan. Este cuaderno es esa rutina.

**Qué necesitas saber antes**: los cuadernos 2 y 3.""",
    aprender=["Leer un fichero CSV como dataframe y ver su tamaño y sus columnas.",
              "Distinguir los tipos de variable estadística: cuantitativas y cualitativas.",
              "Seleccionar columnas y filtrar filas que cumplen una condición.",
              "Detectar y tratar datos que faltan (`NaN`)."],
    secciones=[
        dict(titulo="Leer y conocer la tabla", celdas=[
            M("**Qué vamos a hacer**: leer la encuesta de consumo de noticias y hacer las cuatro comprobaciones de rutina: tamaño, primeras filas, tipos y nombres de columna."),
            C("""encuesta = pd.read_csv("encuesta_medios.csv")
print("Filas y columnas:", encuesta.shape)
encuesta.head()"""),
            C("""encuesta.info()"""),
            M("""**Cómo leer `info()`**: hay 1.200 filas. Casi todas las columnas tienen 1.200 valores no nulos, pero `minutos_noticias_dia` y `confianza_medios` tienen menos: **faltan respuestas**. `object` significa texto; `int64` y `float64`, números enteros y decimales."""),
        ], quiz=[
            unica("Si `encuesta.shape` devuelve `(1200, 11)`, ¿qué significa?", "1.200 filas (personas) y 11 columnas (variables)",
                  [("11 personas y 1.200 preguntas", "El orden es (filas, columnas)."), ("1.200 personas con 11 respuestas que faltan", "shape no informa de datos faltantes.")]),
        ]),
        dict(titulo="Tipos de variables", celdas=[
            M("""En Estadística las variables se clasifican según **qué información recogen**, y de eso depende qué resumen y qué gráfico usar:

| Tipo | Subtipo | Ejemplo en la encuesta |
| :-- | :-- | :-- |
| **Cuantitativa** (números con sentido de cantidad) | Discreta (se cuenta) | edad en años, minutos al día |
| | Continua (admite decimales) | salario, share |
| **Cualitativa** (categorías) | Nominal (sin orden) | provincia, medio principal |
| | Ordinal (con orden) | nivel de estudios, confianza de 0 a 10 |
| | Binaria (dos valores) | comparte noticias sí/no |

⚠️ Una variable puede estar guardada con números y ser cualitativa: un código postal o un «1 = sí, 0 = no»."""),
            M("`describe()` resume las variables numéricas, y con `exclude=\"number\"` las de texto:"),
            C("""encuesta.describe().round(1)"""),
            C("""encuesta.describe(exclude="number")"""),
            M("**Cómo leerlo**: para las numéricas da recuento, media, desviación típica, mínimo, cuartiles y máximo (los verás en los cuadernos 8 a 10). Para las de texto, cuántos valores distintos hay (`unique`), cuál es el más frecuente (`top`) y cuántas veces aparece (`freq`)."),
        ], quiz=[
            varias("¿Cuáles de estas variables son cualitativas?", [
                ("Provincia de residencia", True, "¡Correcto! Nominal."), ("Minutos al día viendo noticias", False, "Es cuantitativa."),
                ("Nivel de estudios", True, "¡Correcto! Ordinal."), ("Código postal", True, "¡Correcto! Aunque sea un número, no tiene sentido sumarlo.")]),
        ]),
        dict(titulo="Seleccionar y filtrar", celdas=[
            M("""Una columna se selecciona con su nombre entre corchetes. Varias columnas, con una **lista** de nombres (por eso hay dobles corchetes)."""),
            C("""encuesta[["edad", "medio_principal", "confianza_medios"]].head()"""),
            M("""**Filtrar** es quedarse con las filas que cumplen una condición. Es la pregunta periodística más habitual: «¿y entre los jóvenes?»."""),
            C("""jovenes = encuesta[encuesta["edad"] < 30]
print("Menores de 30:", len(jovenes))
jovenes["medio_principal"].value_counts()"""),
            M("""**Qué ha pasado**: entre los menores de 30 años, las **redes sociales** son el primer medio, cuando en el total de la encuesta eran el tercero. Esa diferencia ya es una historia.

Para combinar condiciones se usa `&` (y) y `|` (o), con cada condición entre paréntesis:"""),
            C("""filtro = (encuesta["edad"] < 30) & (encuesta["provincia"] == "Alicante")
print("Jóvenes de Alicante:", filtro.sum())"""),
            M("Y para ordenar, `sort_values()`. Estos son los cinco salarios más altos de la redacción simulada:"),
            C("""salarios = pd.read_csv("salarios_redaccion.csv")
salarios.sort_values("salario_bruto_anual", ascending=False).head()"""),
        ], quiz=[
            unica("¿Qué código selecciona a las personas de 65 años o más?", "encuesta[encuesta[\"edad\"] >= 65]",
                  [("encuesta[\"edad\" >= 65]", "La condición se aplica a la columna: encuesta[\"edad\"] >= 65."),
                   ("encuesta[encuesta[\"edad\"] > 65]", "> 65 deja fuera a quienes tienen exactamente 65.")]),
        ]),
        dict(titulo="Datos que faltan", celdas=[
            M("""En una encuesta siempre hay quien no contesta. Pandas marca esos huecos con **`NaN`** (*Not a Number*). Antes de publicar una cifra hay que saber **cuántos faltan y por qué**."""),
            C("""encuesta.isnull().sum()"""),
            M("""**Cómo leerlo**: faltan 36 respuestas de minutos al día y 60 de confianza. Las funciones de Pandas, como `mean()`, **ignoran** los `NaN` automáticamente, así que la media de confianza se calcula sobre 1.140 personas, no sobre 1.200. Conviene decirlo en la noticia («entre quienes contestaron...»)."""),
            C("""print("Personas con dato de confianza:", encuesta["confianza_medios"].count())
print("Confianza media:", round(encuesta["confianza_medios"].mean(), 2))

completos = encuesta.dropna()
print("Filas sin ningún hueco:", len(completos))"""),
            M("""`dropna()` elimina las filas con algún `NaN`. Úsalo con cuidado: si quienes no contestan son distintos de quienes sí lo hacen (por ejemplo, desconfían más), quitar los huecos **sesga** el resultado."""),
        ], quiz=[
            unica("Si 60 de 1.200 personas no contestan la confianza, ¿sobre cuántas calcula Pandas la media?", "1.140",
                  [("1.200", "`mean()` ignora los NaN."), ("60", "Esas son las que faltan.")]),
        ]),
    ],
    reto=[
        dict(seccion="sección 1", enunciado="Lee `salarios_redaccion.csv` y muestra su tamaño, sus 5 primeras filas y el tipo de cada columna.",
             solucion='''salarios = pd.read_csv("salarios_redaccion.csv")
print(salarios.shape)
print(salarios.dtypes)
salarios.head()'''),
        dict(seccion="sección 2", enunciado="Clasifica las columnas de `salarios` según su tipo estadístico (cuantitativa discreta o continua, cualitativa nominal u ordinal).",
             comentario="`anios_experiencia`: cuantitativa discreta; `salario_bruto_anual`: cuantitativa continua; `puesto`, `tipo_medio`, `sexo` y `contrato`: cualitativas nominales; `id`: identificador, no se analiza."),
        dict(seccion="sección 3", enunciado="¿Cuántas personas de la redacción trabajan como autónomas? ¿Y cuántas son mujeres con contrato temporal?",
             solucion='''print((salarios["contrato"] == "Autónomo").sum())
print(((salarios["sexo"] == "Mujer") & (salarios["contrato"] == "Temporal")).sum())'''),
        dict(seccion="sección 3", enunciado="Muestra los 10 salarios más bajos de los redactores y redactoras (`puesto == \"Redactor/a\"`), con su experiencia y tipo de contrato.",
             solucion='''red = salarios[salarios["puesto"] == "Redactor/a"]
red.sort_values("salario_bruto_anual")[["salario_bruto_anual", "anios_experiencia", "contrato"]].head(10)'''),
        dict(seccion="sección 4", enunciado="En la encuesta, calcula qué porcentaje de personas no contestó a los minutos diarios de noticias. ¿Lo mencionarías en una noticia?",
             solucion='''round(encuesta["minutos_noticias_dia"].isnull().mean() * 100, 1)''',
             comentario="Un 3 %. Es poco, pero la nota metodológica de la noticia debería decir sobre cuántas respuestas se calcula cada cifra."),
    ],
    resumen=["Al recibir una tabla: **`shape`**, **`head()`**, **`info()`** y **`describe()`**.",
             "Las variables pueden ser **cuantitativas** (discretas o continuas) o **cualitativas** (nominales, ordinales o binarias); un número no siempre es una cantidad.",
             "Una columna se selecciona con `df[\"col\"]`; varias, con `df[[\"a\", \"b\"]]`; las filas, con `df[condición]`, combinando condiciones con `&` y `|`.",
             "Los datos que faltan aparecen como **`NaN`**: cuéntalos con `isnull().sum()` y di en la noticia sobre cuántos casos se calcula cada cifra.",
             "Eliminar filas incompletas con `dropna()` puede **sesgar** los resultados."],
    glosario=[("DataFrame", "Tabla de Pandas: filas (casos) y columnas (variables)."), ("CSV", "Fichero de texto con valores separados por comas."),
              ("`NaN`", "Marca de dato que falta."), ("Filtrar", "Quedarse con las filas que cumplen una condición."),
              ("Sesgo", "Error sistemático que desvía un resultado en una dirección.")],
    errores=[("Todo sale en una sola columna al leer un CSV", "El separador no es la coma", "Usa `pd.read_csv(fichero, sep=\";\")`"),
             ("`KeyError` al seleccionar una columna", "El nombre no coincide exactamente", "Revisa los nombres con `df.columns`"),
             ("`ValueError: The truth value of a Series is ambiguous`", "Has usado `and`/`or` con columnas", "Usa `&` y `|` y pon cada condición entre paréntesis")],
    seguir="Con esto termina la unidad 1. En el cuaderno 5 empieza la Estadística descriptiva: tablas de frecuencias.",
),
]
