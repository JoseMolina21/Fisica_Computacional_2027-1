#!/usr/bin/env python3
"""
Ejercicio 3 de la Práctica 4 — Complejidad.

3a. Flops de producto punto y producto de matrices:
    - Producto punto de n componentes: n multiplicaciones y (n-1) sumas = 2n - 1 flops.
      Orden: O(n)
    - Producto de dos matrices n x n: n^2 productos punto de n componentes.
      Total: n^2 * (2n - 1) = 2n^3 - n^2 flops.
      Orden: O(n^3)
"""

import math
import time
from pathlib import Path
import sys

# Importar fiscomp
raiz_del_repo = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(raiz_del_repo))

from fiscomp.matrices import Matrix, LowerTriangularMatrix
from fiscomp.algebra_lineal import SistemaTriangular

# 3b. Contar con código

def producto_punto_contando(x, y):
    """Calcula el producto punto y cuenta sus flops."""
    if len(x) != len(y):
        raise ValueError("Los vectores deben tener el mismo tamaño.")
    
    suma = 0.0
    flops = 0
    for i in range(len(x)):
        suma += x[i] * y[i]
        flops += 2  # 1 multiplicación + 1 suma
        
    if len(x) > 0:
        flops -= 1  # La primera suma no cuenta (sumar k números cuesta k-1 sumas)
        
    return suma, flops

def mat_vec_contando(A, x):
    """Calcula A*x y cuenta sus flops."""
    if A.cols != len(x):
        raise ValueError("Dimensiones incompatibles.")
        
    resultado = []
    flops_totales = 0
    for i in range(A.rows):
        fila = A.data[i]
        val, f = producto_punto_contando(fila, x)
        resultado.append(val)
        flops_totales += f
        
    return resultado, flops_totales

def mat_mat_contando(A, B):
    """Calcula A*B y cuenta sus flops."""
    if A.cols != B.rows:
        raise ValueError("Dimensiones incompatibles.")
        
    resultado = []
    flops_totales = 0
    for i in range(A.rows):
        fila_res = []
        for j in range(B.cols):
            col_B = [B.data[k][j] for k in range(B.rows)]
            val, f = producto_punto_contando(A.data[i], col_B)
            fila_res.append(val)
            flops_totales += f
        resultado.append(fila_res)
        
    return Matrix(resultado), flops_totales


# 3b. Tabla de conteos

carpeta_datos = Path(__file__).resolve().parent / "datos"
carpeta_datos.mkdir(exist_ok=True)

ruta_conteo = carpeta_datos / "conteo_flops.dat"

with open(ruta_conteo, "w") as archivo:
    archivo.write("# n  producto_punto  mat_vec  mat_mat  sustitucion\n")
    
    print("=" * 70)
    print("3b. Tabla de conteo de flops (código vs fórmulas)")
    print("=" * 70)
    print(f"{'n':<5} {'Prod Punto':<12} {'Mat-Vec':<12} {'Mat-Mat':<12} {'Sustitucion':<12}")
    print("-" * 70)
    
    for n in [1, 2, 4, 8, 16, 32, 64]:
        # Generar datos de prueba
        v1 = [1.0] * n
        v2 = [2.0] * n
        
        A = Matrix([[1.0] * n for _ in range(n)])
        B = Matrix([[2.0] * n for _ in range(n)])
        
        # Matriz triangular inferior de n x n (unos en la diagonal y abajo)
        T_data = []
        for i in range(n):
            fila = [0.0] * n
            for j in range(i + 1):
                fila[j] = 1.0
            T_data.append(fila)
        T = LowerTriangularMatrix(T_data)
        
        # Contar
        _, f_pp = producto_punto_contando(v1, v2)
        _, f_mv = mat_vec_contando(A, v1)
        _, f_mm = mat_mat_contando(A, B)
        
        sistema = SistemaTriangular(T, v1)
        sistema.resolver()
        f_sus = sistema.flops
        
        print(f"{n:<5} {f_pp:<12} {f_mv:<12} {f_mm:<12} {f_sus:<12}")
        archivo.write(f"{n} {f_pp} {f_mv} {f_mm} {f_sus}\n")


# 3c. Medir el tiempo

print("\n" + "=" * 70)
print("3c. Medición de tiempos")
print("=" * 70)

ruta_tiempos = carpeta_datos / "tiempos.dat"

def medir_tiempo(func, repeticiones=3):
    """Mide el tiempo más rápido de ejecutar func() varias veces."""
    mejor_tiempo = float('inf')
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        func()
        fin = time.perf_counter()
        mejor_tiempo = min(mejor_tiempo, fin - inicio)
    return mejor_tiempo

with open(ruta_tiempos, "w") as archivo:
    archivo.write("# n  t_sustitucion  t_mat_mat\n")
    
    valores_n = [25, 50, 100, 200]
    
    for n in valores_n:
        # Preparar datos para sustitución
        T_data = [[1.0 if j <= i else 0.0 for j in range(n)] for i in range(n)]
        T = LowerTriangularMatrix(T_data)
        b = [1.0] * n
        
        # Preparar datos para multiplicación de matrices
        A = Matrix([[1.0] * n for _ in range(n)])
        B = Matrix([[2.0] * n for _ in range(n)])
        
        # Medir tiempos
        t_sus = medir_tiempo(lambda: SistemaTriangular(T, b).resolver())
        t_mm = medir_tiempo(lambda: A * B)
        
        print(f"n = {n}: t_sus = {t_sus:.6f}s, t_mat_mat = {t_mm:.6f}s")
        archivo.write(f"{n} {t_sus:.6e} {t_mm:.6e}\n")


# Calcular el exponente p
print("\n" + "=" * 70)
print("Estimación del exponente p (t(2n)/t(n) ~ 2^p)")
print("=" * 70)

def calcular_p(t1, t2):
    """Calcula p aproximado entre dos tiempos t1 y t2 (donde t2 es de n duplicada)."""
    if t1 > 0 and t2 > 0:
        return math.log2(t2 / t1)
    return 0.0

for i in range(len(valores_n) - 1):
    n1 = valores_n[i]
    n2 = valores_n[i+1]
    
    # Volver a calcular los tiempos para la impresión
    T_data = [[1.0 if j <= i else 0.0 for j in range(n1)] for i in range(n1)]
    T1 = LowerTriangularMatrix(T_data)
    t1_sus = medir_tiempo(lambda: SistemaTriangular(T1, [1.0]*n1).resolver())
    
    T_data = [[1.0 if j <= i else 0.0 for j in range(n2)] for i in range(n2)]
    T2 = LowerTriangularMatrix(T_data)
    t2_sus = medir_tiempo(lambda: SistemaTriangular(T2, [1.0]*n2).resolver())
    
    A1 = Matrix([[1.0] * n1 for _ in range(n1)])
    B1 = Matrix([[2.0] * n1 for _ in range(n1)])
    t1_mm = medir_tiempo(lambda: A1 * B1)
    
    A2 = Matrix([[1.0] * n2 for _ in range(n2)])
    B2 = Matrix([[2.0] * n2 for _ in range(n2)])
    t2_mm = medir_tiempo(lambda: A2 * B2)
    
    p_sus = calcular_p(t1_sus, t2_sus)
    p_mm = calcular_p(t1_mm, t2_mm)
    
    print(f"Entre n={n1} y n={n2}: p_sustitucion ~ {p_sus:.2f}, p_mat_mat ~ {p_mm:.2f}")


# 3d. Preguntas
print("\n" + "=" * 70)
print("3d. Respuestas a las preguntas")
print("=" * 70)
print("""
1. ¿Qué valores de p obtuvieron? ¿Se acercan más a 2 y 3 para n chica o grande?
   Los valores de p se acercan más a los teóricos (2 y 3) para n grande.
   Para n chica, el tiempo no sigue bien la fórmula porque Python hace mucho
   más que solo operaciones de punto flotante: crear listas, llamar funciones,
   recorrer ciclos, manejar memoria. Todo ese "overhead" pesa más cuando n es chica.

2. La sustitución y el producto matriz-vector son ambos O(n^2), pero con prefactores distintos.
   La sustitución (n^2 flops) debería ser más rápida que el producto matriz-vector
   (2n^2 - n flops). Aproximadamente el doble de rápida para n grande, ya que
   2n^2 - n es casi el doble de n^2.

3. Si resolver un sistema triangular con n=1000 tarda t, ¿cuánto tardaría con n=10,000?
   Como es O(n^2), al multiplicar n por 10, el tiempo se multiplica por 10^2 = 100.
   Tardaría 100t aproximadamente.
   ¿Y un producto de matrices si con n=1000 tarda t'? Como es O(n^3), al multiplicar
   n por 10, el tiempo se multiplica por 10^3 = 1000. Tardaría 1000t' aproximadamente.
   En álgebra lineal importa mucho si un método es O(n^2) u O(n^3) porque para
   matrices grandes (como n=10,000), la diferencia es de 10 veces más rápido (o más),
   lo cual es la diferencia entre que el programa termine en segundos o en horas.
""")