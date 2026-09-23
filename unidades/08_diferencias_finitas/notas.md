# Unidad 08 — Diferencias finitas

## Temas
- **Física computacional:** diferenciación numérica — diferencia hacia
  adelante (*forward difference*), diferencia hacia atrás (*backward
  difference*) y diferencia central (*central difference*); derivación
  de cada una a partir de la serie de Taylor; el error de truncamiento
  (*approximation error*) compitiendo contra el error de redondeo
  (*roundoff error*, ver unidad 06) al elegir el tamaño de paso
  $h$.

## Diferenciación analítica

La derivada de $f$ en un punto $\tilde{x}$ se define, como siempre, por
el límite

$$
\left.\frac{df(x)}{dx}\right|_{\tilde{x}} = \lim_{h \to 0} \frac{f(\tilde{x}+h) - f(\tilde{x})}{h}.
$$

En la práctica casi nunca evaluamos este límite directamente: usamos
las reglas de diferenciación (potencias, cociente, producto, regla de
la cadena, derivadas de funciones especiales) que ya conocemos, por
ejemplo

$$
\frac{d}{dx}e^{\sin(2x)} = 2\cos(2x)\,e^{\sin(2x)}.
$$

Estas reglas dan la derivada exacta, como una expresión simbólica.
Cuando la evaluación numérica de esa expresión oscurece más de lo que
ayuda, o cuando el cálculo a mano es tedioso, se recurre a un paquete
de álgebra computacional (*computer algebra system*) como SymPy o Sage,
que manipula expresiones simbólicamente en vez de solo con números.

Pero en cómputo científico casi siempre queremos, en cambio, evaluar
derivadas *numéricamente*, a partir de la función evaluada en unos
cuantos puntos (por ejemplo, cuando la función viene de datos
experimentales, o cuando ni siquiera tenemos una expresión cerrada
para ella). Para eso sirven las **diferencias finitas**.

## Diferencias finitas

La idea ingenua es tomar la definición de la derivada y, en vez de
tomar el límite $h \to 0$, simplemente usar una $h$ "chica":

$$
f'(\tilde{x}) \approx \frac{f(\tilde{x}+h) - f(\tilde{x})}{h}.
$$

Esta receta ad hoc deja varias preguntas sin responder: ¿qué tan
precisa es? ¿qué tan "chica" debe ser $h$? Nótese además que, al hacer
$h$ más chica, el numerador $f(\tilde{x}+h) - f(\tilde{x})$ *también*
se hace más chico (estamos evaluando $f$ en dos puntos cada vez más
próximos entre sí): cualquier error al evaluar ese numerador se
amplifica al dividirlo entre una $h$ cada vez más chica. Para responder
estas preguntas de forma sistemática, en vez de partir de la
definición del límite, derivamos cada fórmula de diferencias finitas a
partir de la **serie de Taylor** de $f$, lo que nos da control expreso
sobre el error cometido.

### Diferencia hacia adelante (Forward difference)

Partimos de la expansión de Taylor de $f(x+h)$ alrededor de $x$:

$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2}f''(x) + \frac{h^3}{6}f'''(x) + \cdots
$$

Despejando $f'(x)$:

$$
f'(x) = \frac{f(x+h) - f(x)}{h} - \frac{h}{2}f''(x) - \cdots
$$

y quedándonos solo con el primer término del lado derecho obtenemos la
**aproximación de diferencia hacia adelante**:

$$
f'(x) = \frac{f(x+h) - f(x)}{h} + O(h).
$$

Se llama "hacia adelante" porque arranca en $x$ y se mueve en la
dirección positiva hasta $x+h$: geométricamente, es la pendiente de la
recta que une $f(x)$ con $f(x+h)$. El error que se comete al truncar la
serie de Taylor es $O(h)$: es decir, el error decrece linealmente con
$h$ (a grandes rasgos, si $h$ no es demasiado chica, reducir $h$ a la
mitad reduce el error aproximadamente a la mitad).

### Diferencia hacia atrás (Backward difference)

De forma análoga, partiendo de la expansión de Taylor de $f(x-h)$:

$$
f(x-h) = f(x) - h f'(x) + \frac{h^2}{2}f''(x) - \frac{h^3}{6}f'''(x) + \cdots
$$

se despeja

$$
f'(x) = \frac{f(x) - f(x-h)}{h} + O(h),
$$

la **aproximación de diferencia hacia atrás**, que se mueve desde $x$
en dirección negativa hasta $x-h$. Forward y backward son ambas
**diferencias no centradas** (*non-central differences*): usan dos
evaluaciones de $f$ que no están distribuidas simétricamente alrededor
de $x$.

### Análisis de error de la diferencia hacia adelante

Queremos $h$ chica, pero no demasiado chica, porque hay dos fuentes de
error compitiendo:

- **Error de truncamiento** $E_{\text{app}}$, por cortar la serie de
  Taylor:
  $$
  E_{\text{app}} = \frac{h}{2}|f''(x)|.
  $$
  Este error *decrece* con $h$.
- **Error de redondeo** $E_{\text{ro}}$: el numerador
  $f(x+h) - f(x)$ resta dos números muy cercanos entre sí (ver
  cancelación catastrófica, unidad 06); el error absoluto de esa
  resta es aproximadamente $2|f(x)|\epsilon_{\text{mach}}$, y al
  dividir entre $h$:
  $$
  E_{\text{ro}} = \frac{2|f(x)|\epsilon_{\text{mach}}}{h}.
  $$
  Este error *crece* al achicar $h$.

El error total es $E = E_{\text{app}} + E_{\text{ro}}$. Minimizando
respecto a $h$ (derivando e igualando a cero) se obtiene el paso
óptimo y el error mínimo correspondiente:

$$
h_{\text{opt}} = \sqrt{\frac{4\epsilon_{\text{mach}}\,f(x)}{f''(x)}},
\qquad
E_{\text{opt}} = \sqrt{4\epsilon_{\text{mach}}\,f(x)\,f''(x)}.
$$

Si $f(x)$ y $f''(x)$ son de orden 1, con $\epsilon_{\text{mach}}
\approx 2^{-52} \approx 2\times10^{-16}$ (doble precisión) esto da
$h_{\text{opt}} \approx \sqrt[]{4\epsilon_{\text{mach}}} \approx
3\times10^{-8}$ y un error mínimo $E_{\text{opt}} \approx
3\times10^{-8}$ también. Ese error no es nada impresionante: la
diferenciación analítica (sección anterior) no tiene error de
truncamiento en absoluto, solo el error de evaluar $f$.

Ojo: afirmaciones como "el error de truncamiento es $O(h)$" solo valen
para funciones razonablemente bien portadas; si la derivada de orden
correspondiente no existe o diverge, esta escala no aplica.

### Diferencia central (Central difference)

Para mejorar sobre forward/backward, partimos de la expansión de
Taylor centrada en $x$, pero con pasos de tamaño $h/2$ hacia cada lado:

$$
f\!\left(x+\tfrac{h}{2}\right) = f(x) + \frac{h}{2}f'(x) + \frac{h^2}{8}f''(x) + \frac{h^3}{48}f'''(x) + \cdots
$$

$$
f\!\left(x-\tfrac{h}{2}\right) = f(x) - \frac{h}{2}f'(x) + \frac{h^2}{8}f''(x) - \frac{h^3}{48}f'''(x) + \cdots
$$

**Restando** la segunda de la primera, se cancelan $f(x)$ y todas las
derivadas de orden par; despejando $f'(x)$:

$$
f'(x) = \frac{f\!\left(x+\tfrac{h}{2}\right) - f\!\left(x-\tfrac{h}{2}\right)}{h} - \frac{h^2}{24}f'''(x) - \cdots
$$

lo que da la **aproximación de diferencia central**:

$$
f'(x) = \frac{f\!\left(x+\tfrac{h}{2}\right) - f\!\left(x-\tfrac{h}{2}\right)}{h} + O(h^2).
$$

Se llama "central" porque las dos evaluaciones, en $x - h/2$ y
$x + h/2$, están centradas alrededor de $x$ (y siguen separadas entre
sí por una distancia $h$, igual que forward/backward). También usa
solo dos evaluaciones de $f$, igual que forward, pero el error de
truncamiento es $O(h^2)$ en vez de $O(h)$: como $h$ es chica, $h^2$ es
todavía más chica, así que para la misma $h$ la diferencia central es
más precisa (a grandes rasgos, reducir $h$ a la mitad *cuadruplica* la
calidad de la aproximación, en vez de solo duplicarla).

Cuando solo se cuenta con una tabla de datos discretos
$(x_i, f(x_i))$, $i=0,\dots,n-1$, la diferencia central no se puede
usar en los extremos $x_0$ ni $x_{n-1}$ (no hay punto "del otro lado");
ahí es necesario usar forward o backward. En los puntos intermedios sí
se puede usar central, evaluando en $x_i \pm h/2$ (o, de forma
equivalente y más común en la práctica con datos en rejilla, usando
los vecinos $x_{i-1}$ y $x_{i+1}$).

### Análisis de error de la diferencia central

Con el mismo tipo de cuentas que en la sección anterior (ver problema
en el material del curso), el error total resulta

$$
E = E_{\text{app}} + E_{\text{ro}} = \frac{h^2}{24}|f'''(x)| + \frac{2|f(x)|\epsilon_{\text{mach}}}{h},
$$

y minimizando respecto a $h$:

$$
h_{\text{opt}} = \left(\frac{24\,\epsilon_{\text{mach}}\,f(x)}{f'''(x)}\right)^{1/3},
\qquad
E_{\text{opt}} = \left(\frac{9}{8}\epsilon_{\text{mach}}^2\,[f(x)]^2\,|f'''(x)|\right)^{1/3}.
$$

Con $f(x)$ y $f'''(x)$ de orden 1, esto da $h_{\text{opt}} \approx
(24\epsilon_{\text{mach}})^{1/3} \approx 2\times10^{-5}$ y
$E_{\text{opt}} \approx (9\epsilon_{\text{mach}}/8)^{1/3} \approx
4\times10^{-11}$: mucho mejor que el $10^{-8}$ de la diferencia hacia
adelante, aunque todavía peor que la diferenciación analítica.

Un resultado llamativo: el paso óptimo de la diferencia central
($10^{-5}$) es *mucho más grande* que el de la diferencia hacia
adelante ($10^{-8}$), a pesar de que el error final es mucho menor. El
mejor algoritmo permite usar una $h$ más grande y aun así obtener un
mejor resultado.

### Comparación

| Método    | Evaluaciones de $f$          | Error de truncamiento | $h_{\text{opt}}$ (orden) | $E_{\text{opt}}$ (orden) |
|:----------|:------------------------------|:----------------------:|:-------------------------:|:--------------------------:|
| Adelante  | $f(x)$, $f(x+h)$               | $O(h)$                  | $10^{-8}$                  | $10^{-8}$                    |
| Atrás     | $f(x-h)$, $f(x)$               | $O(h)$                  | $10^{-8}$                  | $10^{-8}$                    |
| Central   | $f(x-h/2)$, $f(x+h/2)$          | $O(h^2)$                | $10^{-5}$                  | $10^{-11}$                   |

(órdenes de magnitud para $\epsilon_{\text{mach}}$ de doble precisión y
$f$, sus derivadas, de orden 1)

## Contenido
- [`diferencias_finitas.py`](diferencias_finitas.py): punto de
  partida, con `diff_forward` ya implementada, las funciones de
  prueba ($f(x)=5$, $f(x)=x$, $f(x)=x^2$, $f(x)=\sin(x^2)$) y un
  ejemplo de uso. `diff_backward`, `diff_central`, la comparación
  contra la derivada exacta, el barrido de $h$ (potencias de $1/2$)
  que muestra en números la competencia entre el error de
  truncamiento y el error de redondeo descrita arriba, y guardar ese
  barrido en `datos/derivada_sin_x2.dat` son la **práctica** (ver
  [`practica.md`](practica.md)).
- [`graficar_derivada.gp`](graficar_derivada.gp) y
  [`graficar_derivada.py`](graficar_derivada.py) (gnuplot y
  matplotlib, respectivamente — este último con instrucciones de
  instalación en el `.venv` del curso al inicio del archivo): ya
  están completos, listos para usarse una vez terminada la práctica.
  Grafican, en escala log-log, el error relativo de las diferencias
  hacia adelante y central contra $h$ (leyendo
  `datos/derivada_sin_x2.dat`, con el formato de columnas descrito en
  `practica.md`); se ven las pendientes $O(h)$ y $O(h^2)$ del error de
  truncamiento, y cómo cada curva da vuelta y empieza a subir cuando
  el error de redondeo toma el control. Marcan con una línea vertical
  punteada el $h_{\text{opt}}$ "de juguete" de cada método (las
  fórmulas de la sección de análisis de error arriba), justo donde
  cada curva da vuelta. Se corren con `gnuplot graficar_derivada.gp` o
  `python3 graficar_derivada.py`, después de haber completado la
  práctica en `diferencias_finitas.py` (que es quien genera el
  `.dat`).
