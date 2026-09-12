import math

def pi_leibniz(n_terminos):
    suma = 0.0
    signo = 1.0
    for i in range(n_terminos):
        suma += signo / (2 * i + 1)
        signo *= -1
    return suma * 4

N = 1_000_000  
pi_aprox = pi_leibniz(N)
error = abs(pi_aprox - math.pi)

print(f"PI aproximado con {N} términos: {pi_aprox}")
print(f"math.pi: {math.pi}")
print(f"Error absoluto: {error}")
print(f"Error relativo: {error / math.pi}")