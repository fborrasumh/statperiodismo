"""Genera index.html (portada del curso para el estudiantado) a partir del contenido.
Uso: python herramientas/pagina.py"""
import html
import json

from construir import COLAB, RAIZ, REPO, cargar

GANCHOS = {
    1: "¿Por dónde se informa la gente? Tu primer gráfico en cinco minutos.",
    2: "Escribe titulares automáticos con cifras dentro.",
    3: "Calcula la misma tasa para 140 municipios sin copiar y pegar.",
    4: "Abre una encuesta de 1.200 personas y descubre qué respuestas faltan.",
    5: "«El 22 %»... ¿de quién? Porcentajes sin errores de base.",
    6: "Detecta el eje truncado antes de que te engañe a ti.",
    7: "¿Cómo se reparten de verdad los sueldos de una redacción?",
    8: "Por qué casi todo el mundo cobra menos que el «salario medio».",
    9: "«Cobra más que el 70 % de sus compañeros»: percentiles y cajas.",
    10: "Dos cadenas con el mismo share medio y nada en común.",
    11: "Un dato rarísimo: ¿error en la tabla o noticia del día?",
    12: "¿Creen más bulos quienes comparten noticias?",
    13: "Leer prensa no envejece: correlación no es causa.",
    14: "«Sube 5 puntos» no es «sube un 5 %».",
    15: "¿Cuánto más cara está la cesta de la compra? Depende de qué cesta.",
    16: "Tu sueldo sube un 4 % y puedes comprar menos: euros reales.",
    17: "Compara precios de 2015 y de hoy aunque el índice haya cambiado de base.",
    18: "«El paro baja en julio» casi nunca es noticia.",
    19: "Quita el efecto de la temporada y mira la tendencia.",
    20: "El pueblo con más casos de España... por puro azar.",
    21: "La falacia del fiscal: el número que más se confunde en los juicios.",
    22: "Un detector de bulos «del 95 %» cuyas alarmas fallan 7 de cada 10 veces.",
    23: "Nueve accidentes en un fin de semana: ¿repunte o mala suerte?",
    24: "La campana que hay detrás de cada encuesta.",
    25: "Por qué una votación en redes no es una encuesta.",
    26: "Cinco institutos, cinco resultados: el error muestral.",
    27: "¿Empate técnico o ventaja real?",
    28: "¿Cuántas entrevistas hacen falta para un margen de ±2 puntos?",
    29: "«Un estudio demuestra...»: aprende a leer el p-valor.",
    30: "Compara dos grupos y publícalo con su margen de error.",
}

UNIDADES = {
    "1. Introducción": "Colab, lo mínimo de Python y tu primera tabla de datos.",
    "2. Estadística descriptiva": "Resumir y dibujar datos sin engañar a nadie.",
    "3. Números índice y series cronológicas": "IPC, inflación, euros reales y tendencias.",
    "4. Probabilidad": "El azar, las probabilidades que se confunden y la campana de Gauss.",
    "5. Conceptos básicos de inferencia estadística": "Muestras, encuestas, margen de error y contrastes.",
}

e = html.escape
cs = cargar()
bloques = []
unidad = None
for c in cs:
    if c["unidad"] != unidad:
        if unidad is not None:
            bloques.append("</ol></section>")
        unidad = c["unidad"]
        num_u, nombre_u = unidad.split(". ", 1)
        bloques.append(
            f'<section class="unidad" aria-labelledby="u{num_u}">'
            f'<header class="unidad-cab"><span class="unidad-num" aria-hidden="true">{num_u}</span>'
            f'<div><h3 id="u{num_u}">{e(nombre_u)}</h3><p>{e(UNIDADES[unidad])}</p></div>'
            f'<span class="unidad-prog" data-unidad="{num_u}"></span></header><ol class="sesiones">')
    url = f"{COLAB}{c['slug']}.ipynb"
    texto_busqueda = e((c["titulo"] + " " + GANCHOS[c["num"]]).lower())
    bloques.append(
        f'<li class="sesion" data-num="{c["num"]}" data-unidad="{unidad.split(".")[0]}" data-busca="{texto_busqueda}">'
        f'<span class="s-num">{c["num"]}</span>'
        f'<div class="s-texto"><a class="s-titulo" href="{url}" target="_blank" rel="noopener">{e(c["titulo"])}</a>'
        f'<p class="s-gancho">{e(GANCHOS[c["num"]])}</p></div>'
        f'<label class="s-hecha"><input type="checkbox" data-num="{c["num"]}"><span>Hecha</span></label></li>')
bloques.append("</ol></section>")

primera = f"{COLAB}{cs[0]['slug']}.ipynb"
plantilla = (RAIZ / "herramientas" / "index_plantilla.html").read_text(encoding="utf8")
salida = (plantilla.replace("{{SESIONES}}", "\n".join(bloques))
          .replace("{{PRIMERA}}", primera)
          .replace("{{REPO}}", f"https://github.com/{REPO}")
          .replace("{{TOTAL}}", str(len(cs))))
(RAIZ / "index.html").write_text(salida, encoding="utf8")
print("index.html escrito")
