"""Escribe README.md con el índice de cuadernos y sus botones de Colab."""
from construir import COLAB, RAIZ, cargar

BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

cs = cargar()
filas = []
unidad = None
for c in cs:
    if c["unidad"] != unidad:
        unidad = c["unidad"]
        filas.append(f"\n### Unidad {unidad}\n\n| Sesión | Cuaderno | Abrir |\n| :-: | :-- | :-: |")
    filas.append(f"| {c['num']} | {c['titulo']} | [![Abrir en Colab]({BADGE})]({COLAB}{c['slug']}.ipynb) |")

plantilla = (RAIZ / "herramientas" / "README_plantilla.md").read_text(encoding="utf8")
(RAIZ / "README.md").write_text(plantilla.replace("{{INDICE}}", "\n".join(filas)), encoding="utf8")
print("README.md escrito")
