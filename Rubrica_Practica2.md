# Rúbrica — Práctica 2 (Programación orientada a objetos: `VectorND` y `Matrix`)

- **Alumno:** José María Molina López
- **Repositorio:** Fisica_Computacional_2027-1
- **Fecha de revisión:** 30 de septiembre de 2026

Revisión de la Práctica 2

## Resultado de las pruebas automáticas

Resultado: `OK`, `FALLÓ`, `ERROR` (el código lanzó una excepción, por ejemplo porque el archivo no se puede importar) u `OMITIDA` (no encontré tu clase `Matrix`).

| Prueba | Parte | Resultado | Detalle |
| --- | --- | --- | --- |
| `test_shape_y_datos` | Base | OK |  |
| `test_sin_renglones` | Base | OK |  |
| `test_renglones_de_distinta_longitud` | Base | OK |  |
| `test_str_muestra_las_entradas` | Base | OK |  |
| `test_transpose` | Base | OK |  |
| `test_copy_es_independiente` | Base | OK |  |
| `test_suma` | Ej. 1 | OK |  |
| `test_resta` | Ej. 1 | OK |  |
| `test_dimensiones_distintas` | Ej. 1 | OK |  |
| `test_escalar_por_derecha_e_izquierda` | Ej. 2 | OK |  |
| `test_tipo_no_soportado` | Ej. 2 | OK |  |
| `test_matrices_cuadradas` | Ej. 2 | OK |  |
| `test_matrices_no_cuadradas` | Ej. 2 | OK |  |
| `test_dimensiones_internas_incompatibles` | Ej. 2 | OK |  |

## Parte 1 — `VectorND` (versión hecha en clase) — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Subiste tu propia versión de `VectorND` hecha en clase (no solo la copia del repositorio del curso) | 5 | 0 |
| Se puede construir un vector de N componentes y se imprime bien (`__repr__`) | 3 | 0 |
| Suma y resta componente a componente correctas | 4 | 0 |
| Negativo, multiplicación por escalar y acceso por índice (lo que se vio en clase) | 3 | 0 |
| **Subtotal Parte 1** | **15** | **0** |

**Observaciones**
- El único `VectorND` de tu repositorio es `fiscomp/vectores.py`, que es el archivo del repositorio del curso (llegó al clonar el repositorio del profesor). La Parte 1 pedía tu propia versión hecha en clase, así que esta parte queda sin puntos.

## Parte 2 — `Matrix` — 75 pts

### Ejercicio 1 — Suma y resta — 30 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| `__add__` suma elemento a elemento | 10 | 10 |
| `__add__` levanta `ValueError` si las dimensiones no coinciden | 5 | 5 |
| `__sub__` da el resultado correcto | 8 | 8 |
| `__sub__` levanta `ValueError` si las dimensiones no coinciden | 4 | 4 |
| `__sub__` reutiliza `__add__` y `__mul__` (`A + B * -1`) en lugar de repetir el recorrido | 3 | 3 |
| **Subtotal Ejercicio 1** | **30** | **30** |

### Ejercicio 2 — Multiplicación — 45 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Matriz por escalar (`matriz * escalar`) | 8 | 8 |
| Escalar por matriz (`escalar * matriz`, con `__rmul__`) | 5 | 5 |
| `TypeError` si se multiplica por algo que no es número ni `Matrix` | 5 | 5 |
| Multiplicación de matrices cuadradas | 12 | 12 |
| Multiplicación de matrices no cuadradas | 8 | 8 |
| `ValueError` si las dimensiones internas no coinciden (`self.cols != other.rows`) | 7 | 7 |
| **Subtotal Ejercicio 2** | **45** | **45** |

**Observaciones de la Parte 2**
- Corrí las pruebas del curso sobre tu `Matrix` y pasa las 14, incluidos los casos de error.
- Tu resta reutiliza la suma y el producto por escalar, que era la idea.
- Además validas que `other` sea una `Matrix` en `__add__` y `__sub__`. Bien pensado.

## Calidad y entrega — 10 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Lo que ya venía hecho sigue funcionando: construcción y validación, `print`, `shape`, `get_row`/`get_col`, `transpose`, `copy` | 4 | 4 |
| Tu `Matrix` está en un archivo que se puede importar y corre sin errores | 3 | 3 |
| Código claro: docstrings o comentarios en los métodos que completaste, sin restos de los `TODO` | 3 | 3 |
| **Subtotal Calidad** | **10** | **10** |

**Observaciones**
- Documentaste tus métodos y el código es fácil de seguir.

## Penalizaciones (criterios transversales)

| Concepto | Rango | Aplicado |
| --- | --- | ---: |
| Usar `numpy` u otra librería para hacer las operaciones: la idea es implementarlas | −5 a −10 | 0 |
| Entrega difícil de seguir: hay varias versiones de `Matrix` o `VectorND` y no se distingue cuál es la final | −1 a −2 | 0 |

No descuento por los nombres de tus archivos ni por las carpetas que elegiste, mientras se entienda dónde está cada cosa y funcione.

**Observaciones**
- No hubo penalizaciones.

## Calificación final

| Concepto | Máx | Obtenido |
| --- | ---: | ---: |
| Parte 1 — `VectorND` | 15 | 0 |
| Parte 2 — `Matrix` | 75 | 75 |
| Calidad y entrega | 10 | 10 |
| Penalizaciones | | 0 |
| **Total** | **100** | **85** |

## Comentarios generales y sugerencias

- Tu `Matrix` está completa y bien documentada.
- Perdiste los puntos de la Parte 1 porque no subiste tu `VectorND`.

## Nota

La suma base es 100 pts. Cuando una prueba automática falla por algo ajeno a tu código (por ejemplo, el nombre de un archivo), lo reviso a mano y te doy el crédito si funciona. Si algo de esta revisión no te queda claro, coméntamelo.
