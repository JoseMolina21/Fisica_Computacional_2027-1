# Grafica, en escala log-log, el error relativo de diff_forward y
# diff_central contra h, para ver las dos fuentes de error de
# notas.md compitiendo: el error de truncamiento baja con h
# (pendiente O(h) o O(h^2)) hasta que el error de redondeo lo detiene
# y lo hace volver a subir.
#
# Uso (después de completar la práctica en diferencias_finitas.py --
# ver practica.md -- y correrlo, para que genere el .dat que se lee
# aquí):
#
#   gnuplot graficar_derivada.gp

archivo = "datos/derivada_sin_x2.dat"

# Epsilon de la maquina en doble precision IEEE 754, escrito a mano
# (es un valor fijo del estandar, no depende de la corrida): la misma
# constante que fiscomp.precision_numerica.EPS.
EPS = 2.220446049250313e-16

# h_opt "de juguete" de notas.md (asumiendo f y sus derivadas de orden
# 1): el minimo teorico de cada curva de error, donde el error de
# truncamiento y el de redondeo quedan balanceados.
h_opt_adelante = sqrt(4.0 * EPS)
h_opt_central  = (24.0 * EPS)**(1.0 / 3.0)

set title "Error de diferencias finitas vs. tamano de paso h"
set xlabel "h"
set ylabel "error relativo"

# h y el error recorren varios ordenes de magnitud: log-log es la
# escala natural para ver las pendientes O(h) y O(h^2) como lineas
# rectas.
set logscale xy
set format x "10^{%L}"
set format y "10^{%L}"
set grid

set key top left

# Lineas verticales punteadas en cada h_opt teorico, con etiqueta,
# para comparar contra donde cada curva realmente da vuelta.
set arrow from h_opt_adelante, graph 0 to h_opt_adelante, graph 1 \
    nohead lc rgb "red" dt 2 lw 1.5
set arrow from h_opt_central, graph 0 to h_opt_central, graph 1 \
    nohead lc rgb "blue" dt 2 lw 1.5
set label "h_{opt} adelante" at h_opt_adelante, graph 0.05 \
    rotate by 90 offset 1,0 tc rgb "red"
set label "h_{opt} central" at h_opt_central, graph 0.05 \
    rotate by 90 offset 1,0 tc rgb "blue"

# Columnas del .dat: h  diff_forward  error_forward  diff_central  error_central
plot archivo using 1:3 with linespoints lc rgb "red"  pt 7 ps 0.5 title "adelante, O(h)", \
     archivo using 1:5 with linespoints lc rgb "blue" pt 7 ps 0.5 title "central, O(h^2)"

pause -1 "Presiona Enter para cerrar..."
