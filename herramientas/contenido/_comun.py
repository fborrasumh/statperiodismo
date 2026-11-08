"""Ayudas para escribir el contenido de los cuadernos."""


def M(texto):
    return ("md", texto)


def C(texto):
    return ("code", texto)


def unica(pregunta, correcta, incorrectas, codigo=None, ok="¡Correcto!"):
    """Pregunta con una sola respuesta correcta. incorrectas = [(texto, feedback), ...]."""
    q = {"question": pregunta, "type": "multiple_choice",
         "answers": [{"answer": correcta, "correct": True, "feedback": ok}]
         + [{"answer": t, "correct": False, "feedback": f} for t, f in incorrectas]}
    if codigo:
        q["code"] = codigo
    return q


def varias(pregunta, opciones, codigo=None):
    """Pregunta con varias correctas. opciones = [(texto, es_correcta, feedback), ...]."""
    q = {"question": pregunta, "type": "many_choice",
         "answers": [{"answer": t, "correct": c, "feedback": f} for t, c, f in opciones]}
    if codigo:
        q["code"] = codigo
    return q


def numerica(pregunta, minimo, maximo, ok="¡Correcto!", mal="No es correcto, revisa el cálculo.", precision=4):
    return {"question": pregunta, "type": "numeric", "precision": precision,
            "answers": [{"type": "range", "range": [minimo, maximo], "correct": True, "feedback": ok},
                        {"type": "default", "feedback": mal}]}
