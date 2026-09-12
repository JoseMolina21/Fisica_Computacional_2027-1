#!/usr/bin/env python3
"""
Ejercicio 4 — Error de las funciones especiales.

"""

import math
from pathlib import Path
import sys

raiz = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(raiz))

from fiscomp.precision_numerica import error_relativo
from fiscomp import funciones_especiales as fe


VALORES = [0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0]


ruta_reporte = Path(__file__).parent / "reporte_ejercicio4.txt"


with open(ruta_reporte, "w", encoding="utf-8") as f:
    f.write("REPORTE EJERCICIO 4 — Comparación con math\n")
    f.write("=" * 60 + "\n\n")

    for x in VALORES:
        f.write(f"x = {x}\n")
        f.write("-" * 40 + "\n")

        # seno
        aprox = fe.seno(x)
        exacto = math.sin(x)
        err = error_relativo(aprox, exacto)
        f.write(f"  seno:        mío={aprox:.12f}  math={exacto:.12f}  err={err:.3e}\n")

        # coseno
        aprox = fe.coseno(x)
        exacto = math.cos(x)
        err = error_relativo(aprox, exacto)
        f.write(f"  coseno:      mío={aprox:.12f}  math={exacto:.12f}  err={err:.3e}\n")

        # exponencial
        aprox = fe.exponencial(x)
        exacto = math.exp(x)
        err = error_relativo(aprox, exacto)
        f.write(f"  exponencial: mío={aprox:.12f}  math={exacto:.12f}  err={err:.3e}\n")

        # ln
        aprox = fe.ln(x)
        exacto = math.log(x)
        err = error_relativo(aprox, exacto)
        f.write(f"  ln:          mío={aprox:.12f}  math={exacto:.12f}  err={err:.3e}\n")

        f.write("\n")

    f.write("\n" + "=" * 60 + "\n")
    f.write("RESPUESTAS A LAS PREGUNTAS\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        "¿Hay algún valor de x donde el error sea sorprendentemente alto?\n\n"
        "Sí. El error relativo se dispara cuando el valor real está muy cerca\n"
        "de cero, porque la fórmula divide entre el valor exacto:\n\n"
        "    error_relativo = |aprox - exacto| / |exacto|\n\n"
        "Si 'exacto' es casi cero, el denominador se hace minúsculo y el\n"
        "cociente se infla aunque el error absoluto sea chiquito.\n\n"
        "Ejemplos típicos:\n"
        "  - coseno(x) cerca de x = pi/2 ≈ 1.5708, donde cos(x) ≈ 0.\n"
        "  - seno(x) cerca de x = pi ≈ 3.1416, donde sen(x) ≈ 0.\n"
        "  - ln(x) cerca de x = 1, donde ln(1) = 0 exactamente.\n\n"
        "En esos puntos el error relativo puede dar valores grandes o incluso\n"
        "divergir, aunque el error absoluto sea del orden de 1e-16.\n\n"
        "Por eso el profe evitó a propósito valores como pi/2 en las pruebas\n"
        "de coseno: no porque la función esté mal, sino porque el error\n"
        "relativo no es una buena métrica cerca de los ceros de la función.\n"
    )

print(f"Reporte generado en: {ruta_reporte}")
print("Ábrelo para ver los resultados y las respuestas.")