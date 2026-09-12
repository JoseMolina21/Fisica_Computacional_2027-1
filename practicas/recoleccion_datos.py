#!/usr/bin/env python3
"""
Práctica 1 — Ejercicio 1: Carga del electrón (experimento de Millikan)
Recolección de datos y estimación de la carga del electrón.
"""

import math
from pathlib import Path
import sys

raiz = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(raiz))

from fiscomp.precision_numerica import error_relativo

# ============================================================
# PARTE A — RECOLECCIÓN DE DATOS
# ============================================================

experimento = input("Nombre del experimento: ")
responsable = input("Nombre del responsable: ")

resumen = {
    "Experimento": experimento,
    "Responsable": responsable,
}

# Valor de la carga del electrón
E_REAL = 1.602176634e-19

# --- Condiciones fijas del experimento (tupla) ---
print("\n--- Condiciones fijas del experimento ---")
voltaje = float(input("Voltaje entre placas (V): "))
distancia = float(input("Distancia entre placas (m): "))
viscosidad = float(input("Viscosidad del aceite (Pa·s): "))

condiciones_fijas = (voltaje, distancia, viscosidad)
resumen["Voltaje (V)"] = voltaje
resumen["Distancia (m)"] = distancia
resumen["Viscosidad (Pa·s)"] = viscosidad

# --- Mediciones de carga (lista) ---
print("\n--- Mediciones de carga de cada gota ---")
cargas_medidas = []
NUM_GOTAS = 4

for i in range(NUM_GOTAS):
    while True:
        try:
            carga = float(input(f"Carga de la gota {i+1} (C): "))
        except ValueError:
            print("  Debe ser un número. Intenta de nuevo.")
        else:
            break

    # bool: ¿la gota es válida?
    # Válida si la carga es positiva y de orden de magnitud razonable
    gota_valida = carga > 0

    if gota_valida:
        cargas_medidas.append(carga)
    else:
        print("  Gota descartada (carga no razonable).")

valores_unicos = set(cargas_medidas)
resumen["Valores únicos"] = valores_unicos



# ============================================================
# PARTE B — ESTIMAR LA CARGA DEL ELECTRÓN
# ============================================================

def desviacion_estandar(promedio, valores):
    """Calcula la desviación estándar de una lista de valores."""
    suma = 0.0
    for v in valores:
        suma += (v - promedio) ** 2
    return math.sqrt(suma / len(valores))


def estimar_carga_electron(cargas_medidas):
    """
    Estima la carga del electrón con el método de Millikan.

    Pasos:
    1. e_aproximada = min(cargas_medidas)
    2. Para cada gota: n = round(carga / e_aproximada)
    3. Estimación por gota: e_individual = carga / n
    4. e_final = promedio de las estimaciones individuales
    5. Desviación estándar de esas estimaciones

    Regresa: (e_final, desviacion, estimaciones_individuales, n_individuales)
    """
    e_aproximada = min(cargas_medidas)

    estimaciones = []
    n_individuales = []

    for carga in cargas_medidas:
        n = round(carga / e_aproximada)
        if n == 0:
            n = 1
        e_individual = carga / n
        estimaciones.append(e_individual)
        n_individuales.append(n)

    e_final = sum(estimaciones) / len(estimaciones)
    desviacion = desviacion_estandar(e_final, estimaciones)

    return e_final, desviacion, estimaciones, n_individuales


# --- Ejecutar la estimación ---
e_estimada, desviacion, e_individuales, n_individuales = estimar_carga_electron(cargas_medidas)
error = error_relativo(e_estimada, E_REAL)

# Agregar al resumen
resumen["Carga estimada (C)"] = e_estimada
resumen["Desviación estándar (C)"] = desviacion
resumen["Error relativo"] = error
resumen["Número de gotas válidas"] = len(cargas_medidas)


# ============================================================
# REPORTE
# ============================================================

ruta_reporte = Path(__file__).parent / "reporte_recoleccion.txt"

with open(ruta_reporte, "w") as f:
    f.write("REPORTE DEL EXPERIMENTO DE MILLIKAN\n")
    f.write("=" * 55 + "\n\n")

    f.write("RESUMEN\n")
    f.write("-" * 55 + "\n")
    for clave, valor in resumen.items():
        f.write(f"{clave}: {valor}\n")

    f.write("\n\nDETALLE POR GOTA\n")
    f.write("-" * 55 + "\n")
    for i, (carga, n, e_ind) in enumerate(zip(cargas_medidas, n_individuales, e_individuales), 1):
        f.write(f"Gota {i}:\n")
        f.write(f"  Carga medida:          {carga:.6e} C\n")
        f.write(f"  n (cargas elementales): {n}\n")
        f.write(f"  Estimación individual:  {e_ind:.6e} C\n\n")

    f.write("\nCOMPARACIÓN CON EL VALOR ACEPTADO\n")
    f.write("-" * 55 + "\n")
    f.write(f"Valor aceptado:  {E_REAL:.6e} C\n")
    f.write(f"Nuestra estimación: {e_estimada:.6e} C\n")
    f.write(f"Error relativo:  {error:.6e}\n")

print(f"\n¡Listo! Reporte generado en: {ruta_reporte}")
print(f"Carga estimada del electrón: {e_estimada:.6e} C")
print(f"Error relativo: {error:.6e}")