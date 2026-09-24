#!/usr/bin/env python3
"""Diferenciación numérica con diferencias finitas -- punto de partida.

Ver notas.md para la teoría (cada método se deriva de la serie de
Taylor de f alrededor de x0, con un orden de error distinto) y
practica.md para el enunciado completo de lo que falta completar
aquí.

Ya está implementada diff_forward (diferencia hacia adelante), junto
con las funciones de prueba y un ejemplo de uso. El resto -- las
diferencias hacia atrás y central, y el barrido de h que compara el
error de truncamiento contra el de redondeo -- es la práctica.
"""

import math
from pathlib import Path
import sys

# Para importar fiscomp
raiz_del_repo = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(raiz_del_repo))

from fiscomp.funciones_especiales import seno, coseno
from fiscomp.precision_numerica import error_relativo, EPS


###############################################
# Diferencias finitas
###############################################

def diff_forward(f, x0, h):
    """Diferencia hacia adelante: (f(x0+h) - f(x0)) / h."""
    return (f(x0 + h) - f(x0)) / h


def diff_backward(f, x0, h):
    """Diferencia hacia atrás: (f(x0) - f(x0-h)) / h."""
    return (f(x0) - f(x0 - h)) / h


def diff_central(f, x0, h):
    """Diferencia central: (f(x0+h/2) - f(x0-h/2)) / h."""
    return (f(x0 + h/2) - f(x0 - h/2)) / h


###############################################
# Funciones de prueba
###############################################

def const_5(x):
    return 5.0


def ident(x):
    return x


def sqr(x):
    return x**2


def sin_x2(x):
    return seno(x**2)


###############################################
# Derivadas exactas (Ejercicio 2)
###############################################

def const_5_prima(x):
    return 0.0


def ident_prima(x):
    return 1.0


def sqr_prima(x):
    return 2.0 * x


def sin_x2_prima(x):
    return 2.0 * x * coseno(x**2)


###############################################
# Ejercicio 2: tabla comparativa
###############################################

print("=" * 70)
print("EJERCICIO 2 — Comparación de los tres métodos")
print("=" * 70)

x0 = 6.0
h = 0.1

funciones = [
    ("const_5", const_5, const_5_prima),
    ("ident",   ident,   ident_prima),
    ("sqr",     sqr,     sqr_prima),
    ("sin_x2",  sin_x2,  sin_x2_prima),
]

print(f"\n{'Función':<10} {'Método':<12} {'Aprox':<18} {'Exacta':<18} {'Error rel':<12}")
print("-" * 70)

for nombre, f, f_prima in funciones:
    exacta = f_prima(x0)
    for metodo, aprox in [
        ("forward",  diff_forward(f, x0, h)),
        ("backward", diff_backward(f, x0, h)),
        ("central",  diff_central(f, x0, h)),
    ]:
        try:
            err = error_relativo(aprox, exacta) if exacta != 0 else abs(aprox - exacta)
        except ZeroDivisionError:
            err = 0.0
        print(f"{nombre:<10} {metodo:<12} {aprox:<18.10f} {exacta:<18.10f} {err:<12.3e}")
    print()


###############################################
# Ejercicio 3: barrido de h
###############################################

print("=" * 70)
print("EJERCICIO 3 — Barrido de h para sin(x^2) en x0=1.0")
print("=" * 70)

x0 = 1.0
h = 1.0

# Crear carpeta datos/
carpeta_datos = Path(__file__).resolve().parent / "datos"
carpeta_datos.mkdir(exist_ok=True)

ruta_dat = carpeta_datos / "derivada_sin_x2.dat"

with open(ruta_dat, "w") as archivo:
    archivo.write("# h  diff_forward  error_forward  diff_central  error_central\n")

    for _ in range(50):
        exacta = sin_x2_prima(x0)
        fw = diff_forward(sin_x2, x0, h)
        ct = diff_central(sin_x2, x0, h)
        err_fw = error_relativo(fw, exacta)
        err_ct = error_relativo(ct, exacta)

        archivo.write(f"{h:.6e} {fw:.10e} {err_fw:.10e} {ct:.10e} {err_ct:.10e}\n")

        h = h / 2.0

print(f"Datos guardados en: {ruta_dat}")


###############################################
# Ejercicio 4: h óptima
###############################################

print("\n" + "=" * 70)
print("EJERCICIO 4 — h óptima")
print("=" * 70)

# Leer los datos del .dat
datos = []
with open(ruta_dat) as archivo:
    for linea in archivo:
        if linea.startswith("#"):
            continue
        partes = linea.split()
        if len(partes) == 5:
            datos.append([float(x) for x in partes])

# Encontrar h que minimiza cada error
mejor_fw = min(datos, key=lambda fila: fila[2])
mejor_ct = min(datos, key=lambda fila: fila[4])

h_opt_fw_medida = mejor_fw[0]
h_opt_ct_medida = mejor_ct[0]

# Fórmulas teóricas
h_opt_fw_teorica = math.sqrt(4 * EPS)
h_opt_ct_teorica = (24 * EPS) ** (1/3)

print(f"\nForward:")
print(f"  h óptima medida:  {h_opt_fw_medida:.6e}")
print(f"  h óptima teórica: {h_opt_fw_teorica:.6e}")

print(f"\nCentral:")
print(f"  h óptima medida:  {h_opt_ct_medida:.6e}")
print(f"  h óptima teórica: {h_opt_ct_teorica:.6e}")

# Comentario de respuesta (Ejercicio 4):
# ¿Coinciden exactamente? NO.
# ¿Por qué no tendrían que coincidir?
#   1. La fórmula asume que f y sus derivadas son de orden 1 (es decir,
#      del mismo orden de magnitud). Para sin(x^2) en x0=1, la derivada
#      segunda es 2*cos(x^2) - 4*x^2*sen(x^2), que en x=1 vale
#      2*cos(1) - 4*sen(1) ≈ -2.29. No es de orden 1, es más grande.
#   2. El barrido solo prueba potencias de 1/2 (h = 1, 0.5, 0.25, ...),
#      así que la "h óptima medida" es la más cercana de esas potencias,
#      no la h exacta que minimiza el error.
#   3. El error también incluye redondeo, no solo truncamiento.
