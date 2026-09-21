# Rúbrica — Práctica 1 (Tipos de datos, control de flujo y funciones)

- **Alumno:** José María Molina López
- **Repositorio:** Fisica_Computacional_2027-1
- **Fecha de revisión:** 20 de septiembre de 2026

Revisión de la Práctica 1

## Resultado de las pruebas automáticas

Resultado: `OK`, `FALLÓ`, `OMITIDA` (la prueba no encontró el archivo o la función con el nombre que espera) o `TIEMPO` (no terminó dentro del límite de tiempo).

| Prueba | Ejercicio | Resultado | Detalle |
| --- | --- | --- | --- |
| `test_factorial` | Base (no se califica) | OK |  |
| `test_seno` | Base (no se califica) | OK |  |
| `test_coseno` | 3 | OK |  |
| `test_exponencial` | 3 | OK |  |
| `test_ln` | 3 | OK |  |
| `test_pi_guardado` | 2 | OK |  |
| `test_corre_sin_errores_y_genera_el_reporte` | 1 | OK |  |
| `test_reporte_existe` | 4 | OK |  |

## Ejercicio 1 — Carga del electrón (experimento de Millikan) — 35 pts

### Parte A — Recolección de datos — 12 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| El script de recolección corre de principio a fin y captura los datos con `input()`, convirtiendo a `int`/`float` lo que regresa como `str` | 3 | 3 |
| `str`: nombre del experimento y del responsable | 1 | 1 |
| `float`/`int`: condiciones del experimento y mediciones | 1 | 1 |
| `bool`: alguna condición con criterio razonable (p. ej., si la gota es válida) | 1 | 1 |
| `tuple`: condiciones que no cambian entre gotas (voltaje, distancia entre placas, viscosidad) | 1 | 1 |
| `list`: carga medida de cada gota, en Coulombs (al menos 3 o 4 gotas) | 1 | 1 |
| `set`: valores únicos medidos | 1 | 1 |
| `dict`: resumen final del experimento, completado en la Parte B | 1 | 1 |
| Datos coherentes: unidades en Coulombs, orden de magnitud cercano a 1e-19, experimento (real o inventado) con sentido | 2 | 1 |
| **Subtotal Parte A** | **12** | **11** |

**Observaciones**
- Tu `practicas/recoleccion_datos.py` corre completo (prueba automática OK) y también lo probé a mano con datos válidos. Capturas todo con `input()`, conviertes a `float` y usas `str`, `float`/`int`, `bool` (`gota_valida`), `tuple` (`condiciones_fijas`), `list`, `set` y `dict`. Gracias por la nota sobre haber empezado en Colab; se nota que le agarraste el truco a VS Code.
- Para decidir si una gota es válida solo revisas que la carga sea positiva; el enunciado sugería revisar también el orden de magnitud. Aquí podrías agregar esa condición.
- Validas con `try`/`except` las cargas, pero no el voltaje, la distancia ni la viscosidad: si escribo texto en alguno, el programa se rompe con `ValueError`. Aquí te conviene reutilizar la misma validación.
- Sobre los datos: en el reporte de `practicas/Practica 1/` tus cargas sí son del orden de 1e-19 C, pero las condiciones no tienen mucho sentido físico (23 m entre placas y una viscosidad de 1.6e-19 Pa·s, que se parece más a una carga). Además, el `reporte_recoleccion.txt` que queda junto a tu script tiene los datos de la prueba automática (todo en 1, con error relativo de 6e18). Vuelve a correr el script con datos como 500 V, 0.005 m entre placas y cargas cercanas a múltiplos de 1.6e-19 C, y sube ese reporte.

### Parte B — Estimación de la carga del electrón — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Función que estima la carga del electrón (`estimar_carga_electron` u otro nombre claro) en el mismo script; regresa la estimación de `e` y su desviación estándar | 3 | 3 |
| Primera aproximación con el mínimo de las cargas medidas | 2 | 2 |
| `n = round(carga / e_aproximada)` para cada gota | 2 | 2 |
| Estimación por gota `carga / n`; el promedio de esas estimaciones es la estimación final | 2 | 2 |
| Desviación estándar calculada correctamente sobre las estimaciones por gota (fórmula explícita; población o muestra, pero consistente) | 3 | 3 |
| Error relativo contra `e = 1.602176634e-19 C` (con `error_relativo()` del curso o una versión propia), agregado al `dict` del resumen | 3 | 3 |
| **Subtotal Parte B** | **15** | **15** |

**Observaciones**
- Tu `estimar_carga_electron` está completa y con docstring: `min`, `round` con protección para `n < 1`, estimación por gota, promedio y desviación poblacional (función `desviacion_estandar` con `math.sqrt`) sobre las estimaciones por gota. Regresa `(e_final, desviación, estimaciones, n)`; la comparé contra mi cálculo de referencia y coincide. Excelente.
- Calculas el error relativo con `error_relativo` de `fiscomp.precision_numerica` contra `E_REAL = 1.602176634e-19` y lo agregas al `dict` del resumen.

### Reporte — 8 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Genera un archivo de reporte (por ejemplo `reporte_recoleccion.txt`) con `open()` y `write()` (o `print(file=...)`), en la carpeta del script o en una ruta que funcione en cualquier computadora | 3 | 3 |
| Incluye el resumen del `dict`: carga estimada, desviación estándar y error relativo | 3 | 3 |
| Incluye el detalle de cada gota: carga medida, `n` y estimación individual | 2 | 2 |
| **Subtotal Reporte** | **8** | **8** |

**Observaciones**
- Tu reporte se escribe con `open()`/`write()` junto al script (`Path(__file__)`) e incluye el resumen del dict (carga estimada, desviación, error relativo), el detalle por gota (carga medida, `n`, estimación individual) y la comparación con el valor aceptado. Muy completo.
- Abre el archivo con `encoding="utf-8"`: como no lo indicas, en Windows se guarda en otra codificación y en GitHub se ven caracteres raros en 'Pa·s', 'Desviación', etc.
- Tienes dos `reporte_recoleccion.txt` distintos (`practicas/` y `practicas/Practica 1/`); deja solo uno, el de una corrida con datos reales, para que no se confunda cuál es el definitivo.

## Ejercicio 2 — π con el método de Leibniz — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Suma correctamente la serie de Leibniz (`1 − 1/3 + 1/5 − …`, multiplicada por 4) con muchos términos; no vale copiar `math.pi` ni escribir el valor a mano | 5 | 5 |
| `PI` queda guardado como constante en un archivo que otros programas puedan importar (por ejemplo `fiscomp/constantes.py`), con un valor cercano al real (error relativo menor que 1e-4) y sin volver a correr la suma en cada import | 4 | 4 |
| Comentario que indica qué tan cerca quedaste, comparando contra `math.pi` | 3 | 3 |
| Explicación de por qué no se puede llegar más lejos en un tiempo razonable (convergencia lenta, error del orden de 1/N) | 3 | 3 |
| **Subtotal Ejercicio 2** | **15** | **15** |

**Observaciones**
- Tu `practicas/Practica 1/Ejercicio 2.py` suma 1,000,000 de términos de Leibniz con un ciclo (signo alternante y multiplicas por 4) y `fiscomp/constantes.py` guarda `PI = 3.1415916535897743` sin volver a correr la suma (`test_pi_guardado` OK).
- En `constantes.py` comentas el error absoluto (1e-6) y relativo (3.18e-7) contra `math.pi`, y explicas que la serie converge como 1/N, así que llegar a EPS requeriría ~1e16 términos. Justo lo que se pedía. Excelente.

## Ejercicio 3 — El resto de las funciones especiales — 35 pts

### `coseno(x)` — 10 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Da resultados correctos en los valores de prueba (`test_coseno`; crédito parcial por valor de `x`) | 6 | 6 |
| Serie de Taylor con `EPS` como criterio de corte, siguiendo el patrón de `seno()` | 2 | 2 |
| Reutiliza `factorial()`, no usa `math`, código claro y con docstring o comentarios | 2 | 2 |
| **Subtotal `coseno`** | **10** | **10** |

### `exponencial(x)` — 10 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Da resultados correctos en los valores de prueba (`test_exponencial`; crédito parcial por valor de `x`, incluidos los negativos) | 6 | 6 |
| Serie de Taylor con `EPS` como criterio de corte, siguiendo el patrón de `seno()` | 2 | 2 |
| Reutiliza `factorial()`, no usa `math`, código claro y con docstring o comentarios | 2 | 2 |
| **Subtotal `exponencial`** | **10** | **10** |

### `ln(x)` — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Da resultados correctos en los valores de prueba (`test_ln`; crédito parcial por valor de `x`; 2.0, 5.0 y 10.0 requieren una serie que converja rápido fuera del entorno de `x = 1`) | 8 | 8 |
| Serie con `EPS` como criterio de corte (no un número fijo de términos) y sin `math` | 4 | 4 |
| Funciona para cualquier `x > 0` (serie de `ln((1+y)/(1-y))`, reducción de rango u otra) y lo documentas: qué serie usaste, para qué rango es válida y por qué | 3 | 3 |
| **Subtotal `ln`** | **15** | **15** |

**Observaciones del Ejercicio 3**
- `coseno`, `exponencial` y `ln` pasan todas las pruebas (8/8, 7/7 y 6/6 valores), usan `EPS` como criterio de corte y `factorial()`, no usan `math` y las tres traen docstring. `exponencial` da bien también con `x` negativos.
- Tu `ln` usa la serie de `ln((1+y)/(1-y))` con `y = (x-1)/(x+1)`, funciona para cualquier `x > 0` y lanza `ValueError` si `x <= 0`. Podrías agregar en el docstring por qué esa serie converge para cualquier `x > 0` (`|y| < 1`) y por qué no basta la de Taylor alrededor de 1.
- Escribiste las tres funciones después del bloque `if __name__ == "__main__":`; funciona, pero quedan mejor arriba de ese bloque, junto a `seno`.

## Ejercicio 4 — Error de sus funciones especiales — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Comparas `seno`, `coseno`, `exponencial` y `ln` contra `math.sin`, `math.cos`, `math.exp` y `math.log` con `error_relativo()`, para varios valores de `x` que permitan ver dónde crece el error | 5 | 5 |
| Reporte con los resultados escrito con `open()` en modo escritura (`w`) y `write()` (unidad 04), legible: `x`, valor aproximado, valor real y error | 3 | 3 |
| Identificas al menos un valor de `x` donde el error es sorprendentemente alto | 3 | 2 |
| Explicas por qué: el valor "real" queda muy cerca de cero y el error *relativo* se dispara aunque el error absoluto sea chico | 4 | 4 |
| **Subtotal Ejercicio 4** | **15** | **14** |

**Observaciones**
- Tu `practicas/Practica 1/Ejercicio 4.py` compara las cuatro funciones contra `math` con `error_relativo` en 8 valores de x (de 0.1 a 10) y escribe con `open()`/`write()` un reporte legible con x, tu valor, el de `math` y el error; el resultado está en `practicas/reporte_ejercicio4.txt`.
- Tu explicación de por qué se dispara el error relativo es correcta y clara: divide entre el valor real, y si este es casi 0 el cociente se infla aunque el error absoluto sea del orden de 1e-16. Además nombras casos concretos (`coseno` cerca de pi/2, `seno` cerca de pi, `ln` cerca de 1).
- Aquí deberías incluir esos valores en tu tabla para verlo con tus propios datos: en los 8 valores que probaste todos los errores quedan en ~1e-16 (salvo seno y coseno en x = 10, ~1e-13, por la cancelación al alejarse de 0), así que tu respuesta 'Sí' no se ve respaldada por tu reporte. Prueba `x = pi` y `x = pi/2` y lo vas a ver.

## Reto opcional — crédito adicional (hasta 5 pts)

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Reducción de rango en `seno`/`coseno` (llevar `x` a un intervalo chico con identidades trigonométricas) y evidencia de que mejora la precisión para `x` grande | 5 | 0 |

**Observaciones**
- Este reto era opcional y no lo entregaste.

## Penalizaciones (criterios transversales)

| Concepto | Rango | Aplicado |
| --- | --- | ---: |
| Uso de `math` (u otra librería) dentro de las funciones para calcular `sin`, `cos`, `exp`, `log` o `factorial`: la idea es reimplementarlas | −2 a −5 | 0 |
| Código sin comentarios ni docstrings mínimos, nombres de variables poco claros o funciones monolíticas | −1 a −3 | 0 |
| Entrega difícil de seguir: hay versiones distintas del mismo archivo y no se distingue cuál es la final | −1 a −2 | 0 |

No descuento por los nombres de tus archivos, de tus funciones ni por las carpetas que elegiste, mientras se entienda dónde está cada cosa y funcione.

**Observaciones**
- No te apliqué ninguna penalización.

## Calificación final

| Concepto | Máx | Obtenido |
| --- | ---: | ---: |
| Ejercicio 1 — Carga del electrón | 35 | 34 |
| Ejercicio 2 — π con Leibniz | 15 | 15 |
| Ejercicio 3 — Funciones especiales | 35 | 35 |
| Ejercicio 4 — Error de las funciones | 15 | 14 |
| Penalizaciones | | 0 |
| Crédito adicional | (+5) | 0 |
| **Total** | **100** | **98** |

## Comentarios generales y sugerencias

- Tu trabajo está muy completo: todo corre, las pruebas del curso pasan y el código se entiende bien. Me gustó tu `ln` (funciona para cualquier x > 0) y que documentaste en `constantes.py` qué tan cerca quedó tu PI.
- Para mejorar: (1) corre el Ejercicio 1 con datos con sentido físico y sube ese reporte, en lugar del que quedó con los datos de prueba (todo en 1); (2) abre los reportes con `encoding="utf-8"`; y (3) agrega `pi` y `pi/2` a la tabla del Ejercicio 4 para que se vea el error relativo disparado.

## Nota

La suma base es 100 pts. El reto opcional suma crédito adicional hasta 5 pts y no sustituye ningún criterio obligatorio de los ejercicios 1–4. Cuando tu trabajo muestra verificación numérica sólida aunque falte algún detalle menor, te doy crédito parcial proporcional. Si algo de esta revisión no te queda claro, coméntamelo y lo revisamos.
