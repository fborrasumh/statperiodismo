"""Ejecuta los cuadernos en una carpeta temporal con los datos y preguntas locales.
Uso: python herramientas/probar.py [P01 P02 ...]"""
import shutil, sys, tempfile
from pathlib import Path
import nbformat
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parent.parent
filtro = sys.argv[1:]
fallos = 0
for nb_path in sorted((RAIZ / "cuadernos").glob("P*.ipynb")):
    if filtro and not any(nb_path.name.startswith(f) for f in filtro):
        continue
    with tempfile.TemporaryDirectory() as tmp:
        for d in ("datos", "autoeval"):
            for f in (RAIZ / d).iterdir():
                shutil.copy(f, tmp)
        nb = nbformat.read(nb_path, as_version=4)
        import re
        sols = []
        for c in nb.cells:
            if c.cell_type == "markdown" and "Ver solución" in c.source:
                sols += re.findall(r"```python\n(.*?)\n```", c.source, re.S)
        nb.cells += [nbformat.v4.new_code_cell(x) for x in sols]
        try:
            NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": tmp}}).execute()
            print("OK  ", nb_path.name)
            nbformat.write(nb, Path(tmp) / "x.ipynb")
            out = RAIZ / "herramientas" / "_ejecutados"
            out.mkdir(exist_ok=True)
            nbformat.write(nb, out / nb_path.name)
        except Exception as e:
            fallos += 1
            print("FALLO", nb_path.name, str(e).splitlines()[-1][:300] if str(e) else e)
            print(str(e)[-1500:])
print("Fallos:", fallos)
