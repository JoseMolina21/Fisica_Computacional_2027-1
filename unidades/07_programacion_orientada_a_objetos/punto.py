#!/usr/bin/env python3
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def distancia_al_origen(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __repr__(self):
        return f"Punto({self.x!r}, {self.y!r})"

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

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


if __name__ == "__main__":
    p1 = Punto(3, 4)
    p2 = Punto(1, 1)

    print("p1 =", p1)                                   # Punto(3, 4)
    print("p2 =", p2)                                   # Punto(1, 1)
    print("p1.distancia_al_origen =", p1.distancia_al_origen)  # 5.0
    print("p1 == Punto(3, 4) ->", p1 == Punto(3, 4))    # True
    print("p1 + p2 =", p1 + p2)                         # Punto(4, 5)
    print("p1 - p2 =", p1 - p2)                         # Punto(2, 3)
    print("p1 * 2 =", p1 * 2)                           # Punto(6, 8)
    print("p1 / 2 =", p1 / 2)                           # Punto(1.5, 2.0)
    print("-p1 =", -p1)                                 # Punto(-3, -4)
