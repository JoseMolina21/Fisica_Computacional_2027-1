#!/usr/bin/env python3
"""Grafica, con matplotlib, el error relativo de diff_forward y
diff_central contra h.

Versión en Python de graficar_derivada.gp (gnuplot); hace lo mismo:
error relativo contra h en escala log-log, con una línea vertical en
la h_opt teórica de cada método (ver notas.md).

matplotlib no es parte del entorno base del curso (README.md solo
instala fiscomp). Para instalarlo, con el entorno virtual activado
(desde la raíz del repositorio):

    source .venv/bin/activate
    pip install matplotlib

Uso (después de completar la práctica en diferencias_finitas.py --
ver practica.md -- y correrlo, para que genere el .dat que se lee
aquí):

    python3 graficar_derivada.py
"""

from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError as error:
    raise SystemExit(
        "Este script necesita matplotlib, que no está instalado en este "
        "entorno virtual. Actívenlo (source .venv/bin/activate, desde la "
        "raíz del repositorio) e instálenlo con: pip install matplotlib"
    ) from error

CARPETA_DATOS = Path(__file__).resolve().parent / "datos"
RUTA_DATOS = CARPETA_DATOS / "derivada_sin_x2.dat"

# Epsilon de la máquina en doble precisión IEEE 754, escrito a mano
# (es un valor fijo del estándar, no depende de la corrida): la misma
# constante que fiscomp.precision_numerica.EPS.
EPS = 2.220446049250313e-16

# h_opt "de juguete" de notas.md (asumiendo f y sus derivadas de orden
# 1): el mínimo teórico de cada curva de error, donde el error de
# truncamiento y el de redondeo quedan balanceados.
H_OPT_ADELANTE = (4.0 * EPS) ** 0.5
H_OPT_CENTRAL = (24.0 * EPS) ** (1.0 / 3.0)


def leer_datos(ruta):
    """Lee el .dat generado por la práctica (Ejercicio 3).

    Columnas esperadas: h  diff_forward  error_forward  diff_central
    error_central, separadas por espacios; las líneas que empiezan
    con '#' se ignoran.
    """
    h_vals, error_adelante, error_central = [], [], []
    with open(ruta) as archivo:
        for linea in archivo:
            if linea.startswith("#") or not linea.strip():
                continue
            columnas = linea.split()
            h_vals.append(float(columnas[0]))
            error_adelante.append(float(columnas[2]))
            error_central.append(float(columnas[4]))
    return h_vals, error_adelante, error_central


def main():
    if not RUTA_DATOS.exists():
        raise SystemExit(
            f"No encontré {RUTA_DATOS}. Completen la práctica en "
            "diferencias_finitas.py primero (debe generar ese archivo; "
            "ver practica.md)."
        )

    h_vals, error_adelante, error_central = leer_datos(RUTA_DATOS)

    fig, ax = plt.subplots()
    ax.plot(h_vals, error_adelante, "o-", color="red", markersize=3, label="adelante, O(h)")
    ax.plot(h_vals, error_central, "o-", color="blue", markersize=3, label="central, O(h^2)")

    ax.axvline(H_OPT_ADELANTE, color="red", linestyle="--", label="h_opt adelante")
    ax.axvline(H_OPT_CENTRAL, color="blue", linestyle="--", label="h_opt central")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("h")
    ax.set_ylabel("error relativo")
    ax.set_title("Error de diferencias finitas vs. tamaño de paso h")
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    ax.legend()

    plt.show()


if __name__ == "__main__":
    main()
