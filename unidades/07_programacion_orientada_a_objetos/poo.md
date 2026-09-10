# Programación orientada a objetos (POO)

Notas de teoría sobre POO en general. Para la aritmética de intervalos
como aplicación concreta, ver [`notas.md`](notas.md); el código vive en
[`aritmetica_intervalos.py`](aritmetica_intervalos.py). Los ejemplos
de aquí usan una clase `Punto` más simple, solo para ilustrar cada
concepto por separado antes de verlos combinados en `Intervalo`; la
versión completa y ejecutable de `Punto` está en
[`punto.py`](punto.py).

## ¿Qué es?

Hasta ahora, el código del curso ha sido principalmente
**procedural**: datos por un lado (números, listas, diccionarios,
tuplas) y funciones sueltas por otro que reciben esos datos y los
transforman. La **programación orientada a objetos** (*object-oriented
programming*, OOP) propone empaquetar juntos los datos y las funciones
que operan sobre ellos en una sola unidad: el **objeto**.

No es un reemplazo de lo anterior — dentro de cada método de una clase
se sigue escribiendo código procedural normal (`if`, `for`, funciones
auxiliares, etc.) — sino una forma de organizar el código cuando hay
un concepto con **estado propio** (datos que le pertenecen) y
**comportamiento propio** (operaciones que solo tienen sentido para
ese estado). `Intervalo` es un buen ejemplo: sus datos son `lo` y
`hi`, y su comportamiento (`+`, `-`, `*`, `/`, "¿contiene a x?") solo
tiene sentido en términos de esos dos datos.

## Clases y objetos

Una **clase** (*class*) es una plantilla: describe qué atributos y
métodos va a tener cada ejemplar, pero no es, por sí misma, ningún
ejemplar concreto. Un **objeto** (*object*) o **instancia**
(*instance*) es un ejemplar concreto construido a partir de una clase,
con sus propios valores para esos atributos.

```python
class Punto:
    pass

p1 = Punto()  # p1 es una instancia de Punto
p2 = Punto()  # p2 es otra instancia, distinta de p1

print(type(p1))       # <class '__main__.Punto'>
print(p1 is p2)        # False -- son objetos distintos
print(isinstance(p1, Punto))  # True
```

La relación clase/objeto es la misma que la de tipo/valor que ya
conocen: `int` es un tipo y `3` es un valor de ese tipo; `Punto` es
una clase y `p1` es un objeto de esa clase. De hecho, en Python,
`int`, `list`, `dict`, etc. son clases igual que las que uno define, y
`3`, `[1, 2]`, `{"a": 1}` son instancias de ellas.

## Atributos e `__init__`

Un objeto vacío como `Punto()` no es muy útil todavía. El método
especial `__init__` (el **constructor**, aunque técnicamente
inicializa, no construye) se ejecuta automáticamente al crear un
objeto, y es donde normalmente se asignan sus **atributos de
instancia**:

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punto(3, 4)
print(p.x, p.y)  # 3 4
```

`self` es el primer parámetro de todo método de instancia, y es la
forma en que el método recibe una referencia al objeto sobre el que
fue llamado (`p.__init__(p, 3, 4)` es, conceptualmente, lo que pasa
por debajo cuando se escribe `Punto(3, 4)`). No es una palabra
reservada de Python — es solo una convención universal, casi nadie usa
otro nombre — pero **sí** hay que escribirlo explícitamente como
primer parámetro de cada método.

`self.x = x` crea un atributo `x` en *esa* instancia particular.
Instancias distintas tienen copias independientes:

```python
p1 = Punto(3, 4)
p2 = Punto(0, 0)
p1.x = 100
print(p1.x, p2.x)  # 100 0 -- no se afectan entre sí
```

## Métodos de instancia

Un **método** es una función definida dentro de una clase, que recibe
`self` como primer parámetro y típicamente opera sobre los atributos
de esa instancia:

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia_al_origen(self):
        return (self.x**2 + self.y**2) ** 0.5

p = Punto(3, 4)
print(p.distancia_al_origen())  # 5.0
```

`p.distancia_al_origen()` es azúcar sintáctica por
`Punto.distancia_al_origen(p)`: Python pasa `p` automáticamente como
`self`. Esto es justo lo que ya hacían, sin saberlo, con métodos de
tipos incorporados como `lista.append(x)` (equivalente a
`list.append(lista, x)`) o `"abc".upper()`.

### `@property`: métodos que se usan como atributos

A veces conviene que algo calculado se vea, desde afuera, como un
atributo normal (sin paréntesis) en vez de como un método. El
decorador `@property` hace justo eso — ya lo usa `Intervalo.ancho` y
`Intervalo.centro`:

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def distancia_al_origen(self):
        return (self.x**2 + self.y**2) ** 0.5

p = Punto(3, 4)
print(p.distancia_al_origen)  # 5.0 -- sin paréntesis
```

Es puramente una cuestión de qué tan natural se ve la sintaxis del
lado de quien usa la clase (`intervalo.ancho` se lee mejor que
`intervalo.ancho()`), no cambia nada sobre cómo se escribe el cuerpo
del método.

## Métodos especiales (*dunder methods*)

Los métodos cuyo nombre empieza y termina con doble guion bajo
(*dunder*, de *d*ouble *under*score) son "ganchos" que Python llama
automáticamente en situaciones específicas, en vez de tener que
llamarlos por su nombre. Ya vimos `__init__` (se llama al construir el
objeto); estos son los que más se usan:

| Método | Se llama cuando... |
|---|---|
| `__repr__(self)` | se pide una representación del objeto como texto (`repr(x)`, la consola interactiva, o dentro de un `!r` en un f-string) |
| `__str__(self)` | `str(x)` o `print(x)` (si no está definido, Python usa `__repr__` en su lugar) |
| `__eq__(self, otro)` | se evalúa `x == otro` |
| `__len__(self)` | se evalúa `len(x)` |
| `__contains__(self, item)` | se evalúa `item in x` |
| `__add__(self, otro)` | se evalúa `x + otro` |

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punto({self.x!r}, {self.y!r})"

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

p = Punto(3, 4)
print(p)               # Punto(3, 4) -- usa __repr__
print(p == Punto(3, 4))  # True -- usa __eq__
```

Sin `__repr__`, `print(p)` mostraría algo inútil como
`<__main__.Punto object at 0x7f...>` (la dirección de memoria del
objeto); sin `__eq__`, `p == Punto(3, 4)` daría `False`, porque el
`==` por default compara identidad (¿son el *mismo* objeto?), no
igualdad de contenido.

### Sobrecarga de operadores (*operator overloading*)

`__add__`, `__sub__`, `__mul__`, `__truediv__`, `__neg__`, etc. son la
razón por la que `Intervalo(1, 2) + Intervalo(3, 5)` funciona: `x + y`
en Python **siempre** se traduce, por debajo, a un llamado a método.
Concretamente, para `x + y`:

1. Python intenta `x.__add__(y)`.
2. Si ese método no existe, o regresa la constante especial
   `NotImplemented` (por ejemplo porque `y` es de un tipo que `x` no
   sabe cómo sumar), Python intenta `y.__radd__(x)` (el método
   "reflejado", de *reflected*).
3. Si ninguno de los dos funciona, se lanza `TypeError`.

Siguiendo con `Punto`, basta con definir `__add__` para que el `+`
funcione entre dos puntos (sumándolos como vectores, coordenada a
coordenada):

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punto({self.x!r}, {self.y!r})"

    def __add__(self, otro):
        return Punto(self.x + otro.x, self.y + otro.y)

p1 = Punto(3, 4)
p2 = Punto(1, 1)
print(p1 + p2)  # Punto(4, 5) -- Python traduce esto a p1.__add__(p2)
```

Con solo esto, `p1 + p2` funciona, pero `p1 + 5` no: adentro de
`__add__`, `otro.x` fallaría con `AttributeError` porque un `int` no
tiene atributo `x`. Si quisiéramos que `Punto` también aceptara sumar
un escalar (interpretándolo como sumarlo a ambas coordenadas, digamos)
habría que revisar el tipo de `otro` dentro de `__add__` — exactamente
el papel que cumple `_coaccionar` en `Intervalo` (ver
`aritmetica_intervalos.py`), que convierte cualquier `int`/`float`
suelto en un `Intervalo` de ancho 0 antes de operar.

`__sub__` sigue exactamente el mismo patrón que `__add__` (resta
coordenada a coordenada), y `__mul__` aprovecha que, para un punto
visto como vector, "multiplicar" sí tiene un significado natural con
un escalar suelto (no con otro `Punto`) — escalar cada coordenada:

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punto({self.x!r}, {self.y!r})"

    def __add__(self, otro):
        return Punto(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro):
        return Punto(self.x - otro.x, self.y - otro.y)

    def __mul__(self, escalar):
        return Punto(self.x * escalar, self.y * escalar)

    def __truediv__(self, escalar):
        return Punto(self.x / escalar, self.y / escalar)

    def __neg__(self):
        return Punto(-self.x, -self.y)

p1 = Punto(3, 4)
p2 = Punto(1, 1)
print(p1 - p2)  # Punto(2, 3) -- usa __sub__
print(p1 * 2)   # Punto(6, 8) -- usa __mul__, aquí sí con un int suelto
print(p1 / 2)   # Punto(1.5, 2.0) -- usa __truediv__, mismo patrón que __mul__
print(-p1)      # Punto(-3, -4) -- usa __neg__
```

Nótese la asimetría entre los cuatro: `__add__` y `__sub__` esperan
otro `Punto` del lado derecho (`otro.x`, `otro.y`), `__mul__` y
`__truediv__` esperan un número suelto (`escalar`) — no hay una única
forma "correcta" de definir estos métodos, cada uno recibe el tipo que
tenga sentido para la operación que están modelando. `__neg__` es
distinto de todos los anteriores porque es un **operador unario**: no
recibe ningún segundo operando (`-p1` solo necesita `self`), a
diferencia de `+`, `-`, `*`, `/`, que son binarios y siempre reciben
`otro`.

Y, a diferencia de la suma, `p1 - p2` y `p2 - p1` dan resultados
distintos (la resta no es conmutativa): eso es justo lo que hace que,
más abajo, `Intervalo` necesite un `__rsub__` separado (no un simple
alias a `__sub__`) para que `escalar - Intervalo(...)` reste en el
orden correcto — el mismo razonamiento aplica a `__truediv__` /
`__rtruediv__`, que tampoco es conmutativa.

Esto explica por qué `Intervalo` define tanto `__add__` como
`__radd__` (aliasado al mismo método, porque la suma es conmutativa):
`Intervalo(1,2) + 3` usa `__add__` normalmente, pero `3 + Intervalo(1,2)`
necesita `__radd__`, porque `int.__add__(3, Intervalo(1,2))` no sabe
qué hacer con un `Intervalo` y regresa `NotImplemented`. Para la resta
y la división, que **no** son conmutativas, hace falta escribir
`__rsub__`/`__rtruediv__` por separado (no como simple alias), como en
`aritmetica_intervalos.py`.

## Encapsulación

**Encapsulación** (*encapsulation*) es la idea de que un objeto expone
una interfaz (sus métodos) y oculta los detalles de cómo logra su
comportamiento (sus atributos internos), de forma que quien usa la
clase no necesita saber cómo está implementada por dentro, solo qué
métodos puede llamar y qué hacen.

Python no tiene atributos verdaderamente privados (a diferencia de
otros lenguajes de POO). Las convenciones son:

- `_atributo` (un guion bajo): "privado por convención" — indica "no
  lo uses desde afuera de la clase", pero Python no lo impide.
- `__atributo` (doble guion bajo): activa *name mangling* (Python lo
  renombra internamente a `_NombreDeClase__atributo`), lo que hace más
  difícil (no imposible) acceder desde afuera por accidente.

En este curso, con clases pequeñas como `Intervalo`, no hace falta
tanta ceremonia: sus atributos `lo`/`hi` son públicos a propósito
(leerlos desde afuera es razonable), y la "protección" real está en
que el `__init__` valida `lo <= hi` al crear el objeto.

## Herencia y polimorfismo (mención breve)

Estos son los otros dos pilares clásicos de la POO, que no usamos en
`Intervalo` pero vale la pena conocer:

- **Herencia** (*inheritance*): una clase puede definirse "a partir
  de" otra (`class Hija(Padre):`), heredando sus atributos y métodos y
  pudiendo sobreescribir algunos. Ya la usaron sin llamarla así en la
  [unidad 05](../05_manejo_de_excepciones/): una excepción propia se
  define con `class MiError(Exception): pass`.
- **Polimorfismo** (*polymorphism*): código que llama a un método
  (p. ej. `f(x + y)`) funciona igual sin importar la clase concreta de
  `x`, mientras esa clase implemente `__add__`. Esto es lo que permite
  que `x**2 - 2*x` en `aritmetica_intervalos.py` funcione idéntico ya
  sea que `x` sea un `float` o un `Intervalo` — la función `f` no
  sabe, ni le importa, cuál de los dos es.

## Por qué usar una clase aquí (y no, digamos, una tupla `(lo, hi)`)

Con funciones sueltas, `sumar_intervalos((1,2), (3,5))` también
resolvería el problema numérico. La ventaja de la clase es la sintaxis
y las garantías:

- `X + Y` en vez de `sumar_intervalos(X, Y)` — las expresiones se leen
  como las fórmulas matemáticas que representan.
- `__init__` valida `lo <= hi` **una sola vez**, al crear el objeto —
  con tuplas sueltas, cada función tendría que validar sus argumentos
  por separado (o confiar en que ya vienen bien formados).
- Un `Intervalo(1, 2)` se puede pasar a cualquier función que espere
  un número (gracias a `__add__`, `__pow__`, etc.) sin que esa función
  tenga que enterarse de que está tratando con un intervalo — es el
  polimorfismo de la sección anterior, aplicado directamente al
  ejemplo de acotar el rango de `f(x) = x**2 - 2*x` sobre un intervalo
  en vez de un float.
