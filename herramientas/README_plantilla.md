# SIMUSTAT Periodismo · Estadística con Python para el Grado en Periodismo

Curso completo de **Estadística (1200)**, 1.º del Grado en Periodismo de la Universidad Miguel Hernández de Elche, en **30 cuadernos de Google Colab**: uno por cada hora teórica de la asignatura. Todos los ejemplos son de **periodismo de datos**: encuestas, audiencias, salarios de redacciones, IPC, paro, sondeos electorales y verificación de bulos.

Es la primera adaptación por grado de [SIMUSTAT](https://unidigitalsimustat.umh.es/), el laboratorio de Estadística con Python de la UMH. Sigue el mismo formato y los mismos principios, y sirve de ejemplo para adaptarlo a otras titulaciones.

- **Sin instalar nada**: cada cuaderno se abre en Colab con un clic y descarga solo sus datos.
- **Un cuaderno, una sesión**: introducción, objetivos, secciones con código explicado, autoevaluaciones interactivas, **reto aprendiz** con soluciones plegadas, resumen, glosario y errores frecuentes.
- **Alineado con la guía docente 2026/27**: las cinco unidades y los once resultados de aprendizaje de la asignatura (ver [GUIA_PROFESORADO.md](GUIA_PROFESORADO.md)).
- **Probado**: los 30 cuadernos y todas las soluciones del reto se ejecutan sin errores (`herramientas/probar.py`).

> ⚠️ **Todos los datos son simulados** con fines docentes. Imitan la forma de fuentes reales, pero ninguna cifra es real. Ver [datos/README.md](datos/README.md).

## Cuadernos
{{INDICE}}

## Estructura del repositorio

```
cuadernos/          30 cuadernos .ipynb (P01 ... P30)
datos/              11 ficheros CSV simulados y su diccionario
autoeval/           115 preguntas de autoevaluación (formato jupyterquiz)
herramientas/
  contenido/        texto y código de cada cuaderno, por unidades (u1.py ... u5.py)
  construir.py      genera los cuadernos y las preguntas a partir del contenido
  generar_datos.py  genera los datos simulados (semilla fija: reproducible)
  probar.py         ejecuta todos los cuadernos y las soluciones del reto
  indice.py         regenera este README
GUIA_PROFESORADO.md planificación, evaluación y cómo adaptar el curso
```

## Cómo modificar o adaptar los cuadernos

Los cuadernos **no se editan a mano**: se generan desde `herramientas/contenido/`. Para cambiar un ejemplo, una pregunta o un reto:

```bash
pip install pandas numpy matplotlib scipy nbformat nbclient ipykernel jupyterquiz
python herramientas/generar_datos.py   # solo si cambias los datos
python herramientas/construir.py       # regenera cuadernos y preguntas
python herramientas/probar.py          # comprueba que todo se ejecuta
python herramientas/indice.py          # actualiza el README
```

Para adaptar el curso a **otro grado**, copia el repositorio, cambia los datos y los textos de `contenido/` y la constante `REPO` de `construir.py`. La estructura (núcleo común de probabilidad e inferencia + contexto propio del grado) se mantiene.

## Autoría y licencia

**Adaptación para el Grado en Periodismo**: Fernando Borrás Rocher ([ORCID 0000-0002-5519-4573](https://orcid.org/0000-0002-5519-4573)), Departamento de Estadística, Matemáticas e Informática, UMH.

**Basado en SIMUSTAT**, de Fernando Borrás, Federico Botella, Inés Hernández, M.ª Asunción Martínez Mayoral, Josep Moltó y Javier Morales, desarrollado en el marco del proyecto UNIDIGITAL-UMH.

Contenido publicado con licencia [Creative Commons Atribución-CompartirIgual 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.es), la misma que SIMUSTAT. Puedes copiarlo, adaptarlo y redistribuirlo citando la autoría y manteniendo la misma licencia. Ver [LICENSE](LICENSE) y [CITATION.cff](CITATION.cff).
