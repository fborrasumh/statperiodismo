"""Construye los cuadernos .ipynb y las autoevaluaciones a partir del contenido en herramientas/contenido/.

Cada unidad (u1.py ... u5.py) define una lista CUADERNOS con diccionarios.
Uso:  python herramientas/construir.py
"""
import base64
import importlib.util
import json
from pathlib import Path

import nbformat as nbf

RAIZ = Path(__file__).resolve().parent.parent
REPO = "fborrasumh/statperiodismo"
RAMA = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{RAMA}/"
COLAB = f"https://colab.research.google.com/github/{REPO}/blob/{RAMA}/cuadernos/"
QUIZ_VERSION = "2.9.6.4"

AUTORIA = """**Adaptación para el Grado en Periodismo**: Fernando Borrás Rocher (f.borras@umh.es)

**Basado en SIMUSTAT**, de Fernando Borrás, Federico Botella, Inés Hernández, M.ª Asunción Martínez Mayoral, Josep Moltó y Javier Morales.
Departamento de Estadística, Matemáticas e Informática. Universidad Miguel Hernández de Elche.

**Asignatura**: Estadística (1200), 1.º curso, Grado en Periodismo.

**Licencia**: <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="CC BY-SA 4.0" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a> Creative Commons Atribución-CompartirIgual 4.0.

> ⚠️ **Los datos de este curso son simulados.** Imitan la forma de fuentes reales (INE, CIS, audímetros, agencias de verificación), pero ninguna cifra es real. Úsalos para aprender; para publicar, ve siempre a la fuente oficial."""

ERRORES_COMUNES = [
    ("`NameError: name 'pd' is not defined`", "No se ejecutó la celda de importación", "Ejecuta las celdas desde el principio, en orden"),
    ("`FileNotFoundError` al leer un fichero", "No se ejecutó la configuración o Colab se reinició", "Ejecuta la celda *Configura el cuaderno*"),
    ("La pregunta de autoevaluación no aparece", "Falta la configuración", "Ejecuta la celda de configuración y luego la pregunta"),
]


def md(texto):
    return nbf.v4.new_markdown_cell(texto.strip("\n"))


def code(texto):
    return nbf.v4.new_code_cell(texto.strip("\n"))


def h(texto, nivel=2):
    return md(f"{'#' * nivel} <font color='steelblue'>{texto}</font>")


def nombre_quiz(slug, i):
    return f"q_{slug.split('_')[0]}_{i}.json"


def celda_config(c, quizzes):
    datos = c.get("datos", [])
    return code(f'''#@title <font color="steelblue" size="+1"> Ejecutar configuración {{ display-mode: "form" }}
import os, sys, json, base64, subprocess, urllib.request

RAW = "{RAW}"
DATOS = {json.dumps(datos)}
PREGUNTAS = {json.dumps(quizzes)}

try:
    from jupyterquiz import display_quiz
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "jupyterquiz=={QUIZ_VERSION}"], check=True)
    from jupyterquiz import display_quiz

for carpeta, ficheros in (("datos/", DATOS), ("autoeval/", PREGUNTAS)):
    for f in ficheros:
        if not os.path.exists(f):
            urllib.request.urlretrieve(RAW + carpeta + f, f)

def pregunta(fichero):
    """Muestra una pregunta interactiva de autoevaluación."""
    display_quiz(json.loads(base64.b64decode(open(fichero, "rb").read()).decode("utf8")))

print("Cuaderno configurado")''')


def construir(c, siguiente):
    slug = c["slug"]
    celdas = []
    quizzes = []
    n_quiz = 0
    # Cabecera
    celdas.append(md(f"# <font color=\"steelblue\">{c['num']:02d}. {c['titulo']}</font>\n\n"
                     f"*Unidad {c['unidad']}* · Sesión teórica {c['num']} de 30\n\n{AUTORIA}"))
    celdas.append(h("Antes de empezar: configura el cuaderno"))
    lista_datos = ", ".join(f"`{d}`" for d in c.get("datos", [])) or "ninguno"
    celdas.append(md(f"Ejecuta **una vez** la celda de abajo (botón ▶). Instala la librería de las preguntas, "
                     f"descarga los datos ({lista_datos}) y las preguntas de autoevaluación. "
                     "Si todo va bien verás **`Cuaderno configurado`**.\n\n"
                     "> 💡 Si Colab se desconecta, los ficheros se borran: vuelve a ejecutar esta celda."))
    idx_config = len(celdas)
    celdas.append(None)  # se rellena al final, cuando sepamos cuántas preguntas hay
    celdas.append(h("Introducción"))
    celdas.append(md(c["intro"]))
    celdas.append(h("Qué vas a aprender"))
    celdas.append(md("Al terminar este cuaderno sabrás:\n\n" + "\n".join(f"{i}. {o}" for i, o in enumerate(c["aprender"], 1))))
    celdas.append(h("Contenidos"))
    celdas.append(md("\n".join(f"{i}. {s['titulo']}" for i, s in enumerate(c["secciones"], 1))))
    if c.get("imports", True):
        celdas.append(code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n"
                           + c.get("imports_extra", "")
                           + "\nplt.rcParams['figure.figsize'] = (10, 4)\npd.set_option('display.max_columns', 20)"))
    for i, s in enumerate(c["secciones"], 1):
        celdas.append(h(f"{i}. {s['titulo']}"))
        for tipo, texto in s["celdas"]:
            celdas.append(md(texto) if tipo == "md" else code(texto))
        for q in s.get("quiz", []):
            n_quiz += 1
            nombre = nombre_quiz(slug, n_quiz)
            quizzes.append((nombre, q))
            celdas.append(h("Autoevaluación", 3))
            tipo = q.get("type", "multiple_choice")
            aviso = {"multiple_choice": "escoge la respuesta correcta (**solo hay una**)",
                     "many_choice": "marca **todas** las respuestas correctas",
                     "numeric": "escribe el número y pulsa Enter"}[tipo]
            celdas.append(md(f"Ejecuta la celda y {aviso}:"))
            celdas.append(code(f"#@title <font color='steelblue'> Pregunta interactiva {{ display-mode: \"form\" }}\npregunta(\"{nombre}\")"))
    # Reto aprendiz
    celdas.append(h("Reto aprendiz"))
    celdas.append(md(c.get("reto_intro", "Resuelve estos ejercicios en la celda vacía de debajo de cada enunciado. "
                                          "Si te atascas, vuelve a la sección indicada. La solución está plegada: "
                                          "**inténtalo antes de mirarla**.")))
    for j, e in enumerate(c["reto"], 1):
        texto = f"### **Ejercicio {j}**" + (f" *({e['seccion']})*" if e.get("seccion") else "") + f"\n\n{e['enunciado'].strip()}"
        if e.get("solucion"):
            texto += f"\n\n<details><summary>Ver solución</summary>\n\n```python\n{e['solucion'].strip()}\n```\n"
            if e.get("comentario"):
                texto += f"\n{e['comentario'].strip()}\n"
            texto += "</details>"
        elif e.get("comentario"):
            texto += f"\n\n<details><summary>Ver idea clave</summary>\n\n{e['comentario'].strip()}\n</details>"
        celdas.append(md(texto))
        celdas.append(code("\n\n\n"))
    celdas.append(h("Resumen: ideas clave"))
    celdas.append(md("\n".join(f"- {r}" for r in c["resumen"])))
    if c.get("glosario"):
        celdas.append(h("Glosario"))
        celdas.append(md("| Término | Significado |\n| :-- | :-- |\n" + "\n".join(f"| **{t}** | {d} |" for t, d in c["glosario"])))
    celdas.append(h("Errores frecuentes y cómo resolverlos"))
    errores = c.get("errores", []) + ERRORES_COMUNES
    celdas.append(md("| Síntoma | Causa probable | Solución |\n| :-- | :-- | :-- |\n" + "\n".join(f"| {a} | {b} | {d} |" for a, b, d in errores)))
    celdas.append(h("Para seguir"))
    sig = ""
    if siguiente:
        sig = f"\n\n**Siguiente cuaderno**: [{siguiente['num']:02d}. {siguiente['titulo']}]({COLAB}{siguiente['slug']}.ipynb)"
    celdas.append(md(c.get("seguir", "").strip() + sig))
    celdas[idx_config] = celda_config(c, [q[0] for q in quizzes])

    nb = nbf.v4.new_notebook()
    nb.cells = celdas
    nb.metadata = {"colab": {"provenance": [], "toc_visible": True},
                   "kernelspec": {"name": "python3", "display_name": "Python 3"},
                   "language_info": {"name": "python"}}
    nbf.write(nb, RAIZ / "cuadernos" / f"{slug}.ipynb")
    for nombre, q in quizzes:
        texto = json.dumps([q], ensure_ascii=False)
        (RAIZ / "autoeval" / nombre).write_bytes(base64.b64encode(texto.encode("utf8")))
    return len(quizzes)


def cargar():
    import sys
    sys.path.insert(0, str(RAIZ / "herramientas" / "contenido"))
    todos = []
    for f in sorted((RAIZ / "herramientas" / "contenido").glob("u*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        todos.extend(mod.CUADERNOS)
    return sorted(todos, key=lambda c: c["num"])


if __name__ == "__main__":
    cs = cargar()
    total = 0
    for i, c in enumerate(cs):
        total += construir(c, cs[i + 1] if i + 1 < len(cs) else None)
    print(f"{len(cs)} cuadernos, {total} preguntas")
