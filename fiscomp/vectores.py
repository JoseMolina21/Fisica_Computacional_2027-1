#!/usr/bin/env python3
"""Vector de N dimensiones.

Generaliza la idea de la clase Punto (unidad 07) a un
número arbitrario de coordenadas, usando una lista en vez de atributos
x, y fijos. Además de los operadores aritméticos, valida sus entradas
y traduce los errores de bajo nivel a mensajes más claros (unidad 05,
manejo de excepciones): ver __init__, __truediv__ y normalizado().
"""


class VectorND:
    """Vector de N dimensiones, representado por una lista de coordenadas."""

    def __init__(self, coords):
        try:
            self.coords = list(coords)
        except TypeError as error:
            raise TypeError(
                "coords debe ser algo iterable (lista, tupla, ...), no "
                f"{type(coords).__name__}"
            ) from error

        if not self.coords:
            raise ValueError("un VectorND necesita al menos una coordenada")

        for c in self.coords:
            if not isinstance(c, (int, float)):
                raise TypeError(
                    f"coordenada no numérica: {c!r} ({type(c).__name__})"
                )

    def __repr__(self):
        return f"VectorND({self.coords!r})"

    def __len__(self):
        return len(self.coords)

    def __eq__(self, otro):
        if not isinstance(otro, VectorND):
            return NotImplemented
        return self.coords == otro.coords

    def __getitem__(self, indice):
        return self.coords[indice]

    def _checar_dimensiones(self, otro):
        if len(self) != len(otro):
            raise ValueError(
                f"las dimensiones no coinciden: {len(self)} != {len(otro)}"
            )

    def __add__(self, otro):
        self._checar_dimensiones(otro)
        return VectorND([a + b for a, b in zip(self.coords, otro.coords)])

    def __neg__(self):
        return VectorND([-a for a in self.coords])

    def __sub__(self, otro):
        self._checar_dimensiones(otro)
        return VectorND([a - b for a, b in zip(self.coords, otro.coords)])

    def __mul__(self, escalar):
        """Multiplicación por escalar: v * escalar (no muta v)."""
        return VectorND([a * escalar for a in self.coords])

    __rmul__ = __mul__

    def __truediv__(self, escalar):
        """División por escalar: v / escalar (no muta v).

        Si escalar es 0, la división de cada coordenada ya lanza
        ZeroDivisionError por sí sola; aquí solo se deja propagar
        (normalizado() la atrapa más abajo para dar un mensaje más
        claro cuando el vector es el vector cero).
        """
        return VectorND([a / escalar for a in self.coords])

    def dot(self, otro):
        """Producto escalar (dot product): suma de a*b para cada par
        (a, b) tomado de self y otro."""
        self._checar_dimensiones(otro)
        return sum(a * b for a, b in zip(self.coords, otro.coords))

    def norm(self):
        """Norma euclídea: sqrt(v . v)."""
        return self.dot(self) ** 0.5

    def normalizado(self):
        """Regresa el vector unitario (norma 1) en la misma dirección.

        Lanza ZeroDivisionError con un mensaje más claro que el de
        __truediv__ si el vector es el vector cero, que no tiene
        dirección definida (mismo patrón que leer_temperatura en la
        unidad 05: traducir un error de bajo nivel a uno más
        significativo, conservando la causa original con `from`).
        """
        try:
            return self / self.norm()
        except ZeroDivisionError as error:
            raise ZeroDivisionError(
                "no se puede normalizar el vector cero (no tiene dirección "
                "definida)"
            ) from error

    def distancia_a(self, otro):
        """Distancia euclídea entre self y otro: norma de (self - otro)."""
        return (self - otro).norm()


if __name__ == "__main__":
    v1 = VectorND([1, 2, 3])
    v2 = VectorND([4, 5, 6])

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"-v1 = {-v1}")
    print(f"2 * v1 = {2 * v1}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"v1 / 2 = {v1 / 2}")
    print(f"v1 (sin mutar tras las operaciones de arriba) = {v1}")
    print(f"v1[0] = {v1[0]}, len(v1) = {len(v1)}")
    print(f"v1 . v2 = {v1.dot(v2)}")  # 1*4 + 2*5 + 3*6 = 32
    print(f"norm(v1) = {v1.norm()}")  # sqrt(1+4+9) = sqrt(14)
    print(f"distancia_a(v1, v2) = {v1.distancia_a(v2)}")
    print(f"normalizado(v1) = {v1.normalizado()}")
    print(f"norm(normalizado(v1)) = {v1.normalizado().norm()}")  # ~1.0
    print(f"v1 == VectorND([1, 2, 3]) -> {v1 == VectorND([1, 2, 3])}")

    print(30 * "=")

    # Manejo de excepciones: entradas inválidas y vector cero
    entradas_invalidas = [5, [], [1, "dos", 3]]
    for entrada in entradas_invalidas:
        try:
            VectorND(entrada)
        except (TypeError, ValueError) as error:
            print(f"VectorND({entrada!r}) rechazado: {type(error).__name__}: {error}")

    cero = VectorND([0, 0, 0])
    try:
        cero.normalizado()
    except ZeroDivisionError as error:
        print(f"normalizado() del vector cero: {error}")
        print(f"causa original: {error.__cause__!r}")
