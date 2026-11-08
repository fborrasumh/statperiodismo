"""Genera los conjuntos de datos SIMULADOS del curso de Estadística para Periodismo.

Todos los datos son ficticios, creados con fines docentes. Imitan la forma de
fuentes reales (INE, CIS, EGM, observatorios de verificación), pero ninguna
cifra es real. Para usar datos reales, sustituye cada CSV por la descarga
oficial manteniendo los nombres de columna.

Uso:  python herramientas/generar_datos.py   (escribe en ./datos)
"""
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(1200)  # 1200 = código de la asignatura
OUT = Path(__file__).resolve().parent.parent / "datos"
OUT.mkdir(exist_ok=True)


def encuesta_medios(n=1200):
    """Encuesta sobre consumo de noticias en la Comunitat Valenciana."""
    edad = RNG.integers(18, 86, n)
    sexo = RNG.choice(["Mujer", "Hombre"], n, p=[0.51, 0.49])
    provincia = RNG.choice(["Alicante", "Valencia", "Castellón"], n, p=[0.37, 0.51, 0.12])
    estudios = RNG.choice(["Primarios", "Secundarios", "FP", "Universitarios"], n,
                          p=[0.15, 0.30, 0.22, 0.33])
    medios = ["Televisión", "Prensa digital", "Redes sociales", "Radio", "Prensa en papel"]
    medio = []
    for e in edad:
        if e < 30:
            p = [0.12, 0.25, 0.55, 0.05, 0.03]
        elif e < 50:
            p = [0.28, 0.35, 0.25, 0.08, 0.04]
        elif e < 65:
            p = [0.45, 0.25, 0.10, 0.12, 0.08]
        else:
            p = [0.58, 0.10, 0.04, 0.15, 0.13]
        medio.append(RNG.choice(medios, p=p))
    medio = np.array(medio)
    minutos = np.round(np.clip(RNG.gamma(2.2, 18, n) + (edad - 18) * 0.35, 0, 300))
    confianza = np.clip(np.round(RNG.normal(5.2, 2.0, n) - (medio == "Redes sociales") * 0.8), 0, 10).astype(int)
    p_comparte = np.where(medio == "Redes sociales", 0.62, 0.30)
    comparte = np.where(RNG.random(n) < p_comparte, "Sí", "No")
    p_bulo = 0.18 + 0.20 * (comparte == "Sí") + 0.08 * (estudios == "Primarios")
    bulo = np.where(RNG.random(n) < p_bulo, "Sí", "No")
    p_pago = 0.06 + 0.10 * (estudios == "Universitarios") + 0.05 * (edad > 45)
    pago = np.where(RNG.random(n) < p_pago, "Sí", "No")
    df = pd.DataFrame({
        "id": np.arange(1, n + 1), "edad": edad, "sexo": sexo, "provincia": provincia,
        "estudios": estudios, "medio_principal": medio, "minutos_noticias_dia": minutos.astype(int),
        "confianza_medios": confianza, "comparte_noticias": comparte,
        "ha_creido_bulo": bulo, "suscripcion_pago": pago,
    })
    # Huecos realistas: algunas personas no contestan
    for col, frac in [("minutos_noticias_dia", 0.03), ("confianza_medios", 0.05)]:
        idx = RNG.choice(n, int(n * frac), replace=False)
        df.loc[idx, col] = np.nan
    df.to_csv(OUT / "encuesta_medios.csv", index=False)


def salarios_redaccion(n=420):
    """Salarios brutos anuales de una plantilla de medios (distribución asimétrica)."""
    puestos = ["Redactor/a", "Redactor/a jefe", "Editor/a", "Fotoperiodista", "Community manager", "Dirección"]
    p = [0.48, 0.12, 0.12, 0.10, 0.15, 0.03]
    puesto = RNG.choice(puestos, n, p=p)
    base = {"Redactor/a": 24000, "Redactor/a jefe": 36000, "Editor/a": 31000,
            "Fotoperiodista": 23000, "Community manager": 21000, "Dirección": 70000}
    exp = np.clip(np.round(RNG.gamma(2.0, 4.5, n)), 0, 40).astype(int)
    tipo = RNG.choice(["Digital nativo", "Prensa tradicional", "Televisión", "Radio", "Agencia"], n,
                      p=[0.30, 0.25, 0.20, 0.12, 0.13])
    sexo = RNG.choice(["Mujer", "Hombre"], n, p=[0.55, 0.45])
    contrato = RNG.choice(["Indefinido", "Temporal", "Autónomo"], n, p=[0.58, 0.25, 0.17])
    sal = np.array([base[x] for x in puesto]) * np.exp(RNG.normal(0, 0.18, n)) * (1 + 0.018 * exp)
    sal *= np.where(sexo == "Mujer", 0.93, 1.0) * np.where(contrato == "Autónomo", 0.85, 1.0)
    df = pd.DataFrame({"id": np.arange(1, n + 1), "puesto": puesto, "anios_experiencia": exp,
                       "tipo_medio": tipo, "sexo": sexo, "contrato": contrato,
                       "salario_bruto_anual": np.round(sal, -1).astype(int)})
    df.to_csv(OUT / "salarios_redaccion.csv", index=False)


def audiencias(n=160):
    """Audiencias de programas de televisión en una semana."""
    cadenas = ["Cadena 1", "Cadena 2", "Cadena 3", "Cadena 4", "Autonómica"]
    generos = ["Informativo", "Entretenimiento", "Deportes", "Ficción", "Debate"]
    franjas = ["Mañana", "Sobremesa", "Tarde", "Prime time", "Late night"]
    filas = []
    for i in range(n):
        cad, gen, fr = RNG.choice(cadenas), RNG.choice(generos), RNG.choice(franjas)
        mult = {"Mañana": 0.6, "Sobremesa": 1.1, "Tarde": 0.8, "Prime time": 1.6, "Late night": 0.5}[fr]
        share = np.clip(RNG.normal(10, 4) * (1.2 if gen == "Informativo" else 1.0) * (0.7 if cad == "Autonómica" else 1), 1.0, 30)
        espect = share * 85 * mult * np.exp(RNG.normal(0, 0.25))
        filas.append({"programa": f"Programa {i + 1:03d}", "cadena": cad, "genero": gen, "franja": fr,
                      "duracion_min": int(RNG.choice([30, 45, 60, 90, 120])),
                      "share": round(float(share), 1), "espectadores_miles": int(round(espect))})
    pd.DataFrame(filas).to_csv(OUT / "audiencias_tv.csv", index=False)


def ipc():
    """Índice de precios ficticio, base 2021 = 100, mensual 2015-2025, por grupos."""
    fechas = pd.date_range("2015-01-01", "2025-12-01", freq="MS")
    t = np.arange(len(fechas))
    grupos = {"alimentos": (0.0020, 0.30, 0.0060), "vivienda": (0.0015, 0.20, 0.0120),
              "transporte": (0.0018, 0.45, 0.0090), "ocio_cultura": (0.0010, 0.10, 0.0040)}
    pesos = {"alimentos": 0.23, "vivienda": 0.13, "transporte": 0.14, "ocio_cultura": 0.08}
    df = pd.DataFrame({"fecha": fechas.strftime("%Y-%m")})
    for g, (tend, estac, ruido) in grupos.items():
        shock = np.cumsum(np.where((fechas >= "2021-06-01") & (fechas <= "2022-12-01"), 0.008 + (g == "vivienda") * 0.01, 0))
        nivel = np.exp(tend * t + shock + RNG.normal(0, ruido, len(t)).cumsum() * 0.3)
        nivel *= 1 + estac / 100 * np.sin(2 * np.pi * (fechas.month - 1) / 12)
        df[g] = nivel
    resto = 1 - sum(pesos.values())
    df["resto"] = np.exp(0.0016 * t + RNG.normal(0, 0.002, len(t)).cumsum())
    df["general"] = sum(df[g] * w for g, w in pesos.items()) + df["resto"] * resto
    base = df[df["fecha"].str.startswith("2021")].drop(columns="fecha").mean()
    for c in df.columns[1:]:
        df[c] = (df[c] / base[c] * 100).round(3)
    df.to_csv(OUT / "ipc_simulado.csv", index=False)
    pd.DataFrame({"grupo": list(pesos) + ["resto"],
                  "ponderacion": list(pesos.values()) + [round(resto, 2)]}).to_csv(OUT / "ipc_ponderaciones.csv", index=False)


def cesta():
    """Precios y cantidades de una cesta de la compra en dos años (para Laspeyres y Paasche)."""
    prod = ["Pan (kg)", "Leche (l)", "Aceite de oliva (l)", "Huevos (docena)", "Pollo (kg)",
            "Tomates (kg)", "Café (kg)", "Periódico (ud.)"]
    p0 = [2.40, 0.85, 4.20, 1.90, 5.10, 1.70, 9.50, 1.50]
    q0 = [6, 12, 2, 3, 3, 4, 0.5, 20]
    p1 = [2.75, 1.05, 9.60, 2.45, 5.90, 2.20, 11.40, 1.80]
    q1 = [6, 12, 1, 3, 3.5, 4, 0.5, 14]
    pd.DataFrame({"producto": prod, "precio_2020": p0, "cantidad_2020": q0,
                  "precio_2024": p1, "cantidad_2024": q1}).to_csv(OUT / "cesta_compra.csv", index=False)


def salario_nominal():
    """Salario medio nominal ficticio (euros/año) para deflactar con el IPC."""
    anios = np.arange(2015, 2026)
    sal = 22800 * np.cumprod(np.r_[1, 1 + RNG.normal(0.018, 0.008, len(anios) - 1)])
    sal[-4:] *= [1.02, 1.035, 1.05, 1.06]
    pd.DataFrame({"anio": anios, "salario_medio_nominal": np.round(sal).astype(int)}).to_csv(OUT / "salario_medio.csv", index=False)


def visitas_web():
    """Visitas diarias a un diario digital: tendencia + semana + verano + picos informativos."""
    fechas = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    t = np.arange(len(fechas))
    tendencia = 40000 + 18 * t
    semana = np.array([1.08, 1.06, 1.05, 1.04, 1.00, 0.86, 0.91])[fechas.dayofweek]
    anual = 1 - 0.12 * np.exp(-((fechas.dayofyear - 220) / 25.0) ** 2)
    picos = np.ones(len(t))
    for d in RNG.choice(len(t), 14, replace=False):
        picos[d:d + 3] *= [2.4, 1.6, 1.2][: len(picos[d:d + 3])]
    visitas = tendencia * semana * anual * picos * np.exp(RNG.normal(0, 0.05, len(t)))
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"), "visitas": visitas.round().astype(int)}).to_csv(OUT / "visitas_diario.csv", index=False)


def paro():
    """Paro registrado mensual ficticio en una provincia (estacional: verano y Navidad)."""
    fechas = pd.date_range("2016-01-01", "2025-12-01", freq="MS")
    t = np.arange(len(fechas))
    tendencia = 190000 - 650 * t + 9000 * np.sin(t / 30)
    tendencia[(fechas >= "2020-04-01") & (fechas <= "2021-03-01")] += 30000
    estac = {1: 6000, 2: 5000, 3: 2500, 4: -500, 5: -4500, 6: -8000, 7: -9500, 8: -6000,
             9: 1500, 10: 4000, 11: 5000, 12: -1500}
    serie = tendencia + np.array([estac[m] for m in fechas.month]) + RNG.normal(0, 1500, len(t))
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m"), "parados": serie.round().astype(int)}).to_csv(OUT / "paro_mensual.csv", index=False)


def municipios(n=140):
    """Indicadores ficticios de 140 municipios."""
    pob = np.round(np.exp(RNG.normal(8.6, 1.4, n))).astype(int) + 300
    renta = np.round(RNG.normal(11500, 1800, n) + 900 * np.log10(pob)).astype(int)
    internet = np.clip(62 + 0.0016 * (renta - 9000) + 3 * np.log10(pob) + RNG.normal(0, 4, n), 40, 99).round(1)
    edad_media = np.clip(RNG.normal(44, 3.5, n) - 1.2 * np.log10(pob) + 4, 36, 56).round(1)
    paro = np.clip(22 - 0.0011 * (renta - 9000) + RNG.normal(0, 2.5, n), 4, 30).round(1)
    prensa = np.clip(8 + 0.9 * (edad_media - 40) + 0.0006 * (renta - 9000) + RNG.normal(0, 2.5, n), 2, 35).round(1)
    comarca = RNG.choice(["Litoral", "Interior", "Área metropolitana"], n, p=[0.4, 0.4, 0.2])
    pd.DataFrame({"municipio": [f"Municipio {i:03d}" for i in range(1, n + 1)], "comarca": comarca,
                  "poblacion": pob, "renta_media_persona": renta, "tasa_paro": paro,
                  "edad_media": edad_media, "hogares_internet_pct": internet,
                  "lectores_prensa_pct": prensa}).to_csv(OUT / "municipios.csv", index=False)


def encuestas_electorales(k=36):
    """Sondeos ficticios de intención de voto para dos candidaturas (A y B)."""
    fechas = pd.date_range("2025-01-10", periods=k, freq="7D")
    verdad_a = np.linspace(0.33, 0.36, k)
    verdad_b = np.linspace(0.35, 0.34, k)
    filas = []
    for f, va, vb in zip(fechas, verdad_a, verdad_b):
        empresa = RNG.choice(["Demoscopia Sur", "Instituto Levante", "Opina Datos", "Sondea"])
        n = int(RNG.choice([600, 800, 1000, 1200, 1500, 2000]))
        a = RNG.binomial(n, va) / n
        b = RNG.binomial(n, vb) / n
        filas.append({"fecha": f.strftime("%Y-%m-%d"), "empresa": empresa, "tamano_muestra": n,
                      "pct_A": round(100 * a, 1), "pct_B": round(100 * b, 1)})
    pd.DataFrame(filas).to_csv(OUT / "sondeos.csv", index=False)


def verificaciones(n=900):
    """Contenidos revisados por una agencia de verificación ficticia."""
    plataforma = RNG.choice(["WhatsApp", "X", "Facebook", "TikTok", "Web"], n, p=[0.30, 0.22, 0.18, 0.18, 0.12])
    tema = RNG.choice(["Salud", "Política", "Inmigración", "Clima", "Economía", "Sucesos"], n,
                      p=[0.20, 0.25, 0.15, 0.12, 0.13, 0.15])
    formato = RNG.choice(["Texto", "Imagen", "Vídeo", "Audio"], n, p=[0.35, 0.30, 0.25, 0.10])
    p_falso = 0.55 + 0.15 * (plataforma == "WhatsApp") + 0.10 * (formato == "Audio") - 0.15 * (plataforma == "Web")
    u = RNG.random(n)
    veredicto = np.where(u < p_falso, "Falso", np.where(u < p_falso + 0.25, "Engañoso", "Verdadero"))
    compart = np.round(np.exp(RNG.normal(6.5, 1.6, n) + 0.6 * (veredicto != "Verdadero"))).astype(int)
    pd.DataFrame({"id": np.arange(1, n + 1), "plataforma": plataforma, "tema": tema, "formato": formato,
                  "veredicto": veredicto, "veces_compartido": compart}).to_csv(OUT / "verificaciones.csv", index=False)


if __name__ == "__main__":
    for f in [encuesta_medios, salarios_redaccion, audiencias, ipc, cesta, salario_nominal,
              visitas_web, paro, municipios, encuestas_electorales, verificaciones]:
        f()
    print("Datos generados en", OUT)
