"""Constantes numéricas calculadas en la práctica."""

# PI calculado con la serie de Leibniz:
# pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
# Se sumaron 1,000,000 de términos.
#
# Valor real de math.pi: 3.141592653589793
# Error absoluto: 1.0000000187915248e-06
# Error relativo: 3.183098921653188e-07
#
# No se puede llegar a EPS porque la serie de Leibniz converge
# muy lento (como 1/n): reducir el error a la mitad requiere el
# doble de términos. Llegar a 1e-16 tomaría ~1e16 términos,
# inviable en un tiempo razonable.
PI = 3.1415916535897743