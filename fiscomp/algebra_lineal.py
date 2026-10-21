"""Álgebra lineal numérica, escrita desde cero con listas de listas.

Ver unidades/09_algebra_lineal/notas.md para la teoría (normas, número de
condición, sustitución hacia adelante y hacia atrás).

Convenciones:

- Una matriz es una lista de listas rectangular, un renglón por
  sublista: A[i][j] es el elemento del renglón i, columna j (índices
  desde 0, como en el libro y en Python). Si tienen una Matrix
  (fiscomp/matrices.py), pasen su atributo .data.
- Un vector es una lista simple de números: x[i].

Aquí vive lo que se reutiliza en el resto del tema: las sustituciones
para matrices triangulares, la eliminación gaussiana (con y sin
pivoteo), la descomposición LU con la inversa y el determinante, el
método de Jacobi, los métodos de la potencia (directo e inverso con
desplazamiento) para eigenvalores, y la matriz de prueba del libro.
"""

from fiscomp.funciones_especiales import raiz_cuadrada
from fiscomp.matrices import Matrix, LowerTriangularMatrix, UpperTriangularMatrix, Identity

###############################################
# Producto matriz-vector y residuo
###############################################


def mat_vec(A, x):
    """Producto matriz-vector y = A x, con y[i] = sum_j A[i][j] x[j].

    A: matriz n x m (lista de listas).
    x: vector de m componentes (lista).
    Regresa una lista de n componentes. Cuesta 2n^2 - n operaciones
    de punto flotante cuando A es cuadrada (ver notas.md).
    """
    if len(A[0]) != len(x):
        raise ValueError(
            f"dimensiones incompatibles: A tiene {len(A[0])} columnas "
            f"y x tiene {len(x)} componentes"
        )
    y = []
    for renglon in A:
        suma = 0.0
        for a_ij, x_j in zip(renglon, x):
            suma += a_ij * x_j
        y.append(suma)
    return y


def residuo(A, x, b):
    """Vector residuo r = b - A x (ec. 4.17 del libro).

    Si x es la solución exacta de A x = b, r es el vector cero. Un
    residuo chico NO garantiza que x esté cerca de la solución
    exacta (ver el ejemplo de Kahan en notas.md).
    """
    Ax = mat_vec(A, x)
    return [b_i - Ax_i for b_i, Ax_i in zip(b, Ax)]


###############################################
# Normas de vectores y de matrices
###############################################


def norma_euclidea(x):
    """Norma euclídea de un vector: sqrt(sum_i |x_i|^2)."""
    return sum(abs(x_i) ** 2 for x_i in x) ** 0.5


def norma_infinito_vec(x):
    """Norma infinito (de máxima magnitud) de un vector: max_i |x_i|."""
    return max(abs(x_i) for x_i in x)


def norma_frobenius(A):
    """Norma de Frobenius de una matriz: sqrt(sum_i sum_j |A_ij|^2)."""
    return sum(abs(a_ij) ** 2 for renglon in A for a_ij in renglon) ** 0.5


def norma_infinito(A):
    """Norma infinito de una matriz (máxima suma de renglón):

        max_i sum_j |A_ij|
    """
    return max(sum(abs(a_ij) for a_ij in renglon) for renglon in A)


###############################################
# Matrices triangulares
###############################################


def triangular_inferior(A):
    """Copia de A con ceros arriba de la diagonal (como numpy.tril)."""
    n = len(A)
    return [[A[i][j] if j <= i else 0.0 for j in range(n)] for i in range(n)]


def triangular_superior(A):
    """Copia de A con ceros abajo de la diagonal (como numpy.triu)."""
    n = len(A)
    return [[A[i][j] if j >= i else 0.0 for j in range(n)] for i in range(n)]


def sustitucion_adelante(L, b):
    """Resuelve L x = b con L triangular inferior (forsub en el libro):

        x_i = (b_i - sum_{j=0}^{i-1} L_ij x_j) / L_ii,  i = 0, 1, ..., n-1

    L: matriz n x n triangular inferior (solo se leen los elementos
       de la diagonal y de abajo de ella).
    b: vector de n componentes.
    Regresa la solución x como lista. Cuesta n^2 operaciones.
    """
    n = len(b)
    x = [0.0] * n
    for i in range(n):
        suma = 0.0
        for j in range(i):  # para i = 0 este ciclo no hace nada
            suma += L[i][j] * x[j]
        x[i] = (b[i] - suma) / L[i][i]
    return x


def sustitucion_atras(U, b):
    """Resuelve U x = b con U triangular superior (backsub en el libro):

        x_i = (b_i - sum_{j=i+1}^{n-1} U_ij x_j) / U_ii,  i = n-1, ..., 1, 0

    U: matriz n x n triangular superior (solo se leen los elementos
       de la diagonal y de arriba de ella).
    b: vector de n componentes.
    Regresa la solución x como lista. Cuesta n^2 operaciones.
    """
    n = len(b)
    x = [0.0] * n
    for i in reversed(range(n)):
        suma = 0.0
        for j in range(i + 1, n):  # para i = n-1 este ciclo no hace nada
            suma += U[i][j] * x[j]
        x[i] = (b[i] - suma) / U[i][i]
    return x


###############################################
# Eliminación gaussiana y descomposición LU
###############################################


def eliminacion_gaussiana(A, b):
    """Resuelve A x = b con eliminación gaussiana (gauelim en el libro).

    Fase de eliminación: para cada renglón pivote j = 0, ..., n-2 y
    cada renglón i = j+1, ..., n-1 de abajo,

        coeficiente = A_ij / A_jj
        renglón i  <-  renglón i - coeficiente * renglón j

    (en A y en b), hasta que A queda triangular superior. Luego,
    sustitución hacia atrás.

    A: matriz n x n (lista de listas). b: vector de n componentes.
    No modifica A ni b: trabaja sobre copias. Sin pivoteo: si algún
    pivote A_jj vale cero, levanta ZeroDivisionError (ver notas.md).
    Cuesta 2n^3/3 + 3n^2/2 - 13n/6 operaciones la eliminación, más n^2
    la sustitución hacia atrás.
    """
    A = [renglon[:] for renglon in A]
    b = b[:]
    n = len(b)
    for j in range(n - 1):
        for i in range(j + 1, n):
            coeficiente = A[i][j] / A[j][j]
            # En el libro, con NumPy: A[i,j:] -= coeficiente*A[j,j:]
            for k in range(j, n):
                A[i][k] -= coeficiente * A[j][k]
            b[i] -= coeficiente * b[j]
    return sustitucion_atras(A, b)


def descomposicion_lu(A):
    """Descomposición LU de Doolittle: A = L U (ludec en el libro).

    Es la misma eliminación gaussiana, pero sin b: lo que queda de A
    al final es U (triangular superior), y los coeficientes que se
    usaron para eliminar se guardan en L (triangular inferior, con
    unos en la diagonal): L_ij = coeficiente que anuló a A_ij.

    A: matriz n x n (lista de listas); no se modifica.
    Regresa (L, U), dos listas de listas. Sin pivoteo, como
    eliminacion_gaussiana. Cuesta 2n^3/3 + n^2/2 - 7n/6 operaciones.
    """
    n = len(A)
    U = [renglon[:] for renglon in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for j in range(n - 1):
        for i in range(j + 1, n):
            coeficiente = U[i][j] / U[j][j]
            for k in range(j, n):
                U[i][k] -= coeficiente * U[j][k]
            L[i][j] = coeficiente
    return L, U


def resolver_lu(L, U, b):
    """Resuelve A x = b a partir de la descomposición A = L U:

        L y = b   (sustitución hacia adelante)
        U x = y   (sustitución hacia atrás)

    L, U: lo que regresa descomposicion_lu(A). b: vector de n
    componentes. Cuesta 2n^2 operaciones: con la misma L y U se pueden
    resolver muchos sistemas con distinto b sin repetir la
    descomposición, que es la parte cara.
    """
    y = sustitucion_adelante(L, b)
    return sustitucion_atras(U, y)



def inversa(A):
    """Matriz inversa con LU: la columna k de A^-1 es la solución de

        A x_k = e_k,

    con e_k la columna k de la identidad (porque A A^-1 = I). Son n
    sistemas con la misma A: una sola descomposición LU y n pares de
    sustituciones. Cuesta ~2n^3/3 + 2n^3 = 8n^3/3 operaciones.

    A: matriz n x n (lista de listas); no se modifica.
    Regresa A^-1 como lista de listas. Sin pivoteo (ver
    descomposicion_lu).
    """
    n = len(A)
    L, U = descomposicion_lu(A)
    columnas = []
    for k in range(n):
        e_k = [1.0 if i == k else 0.0 for i in range(n)]
        columnas.append(resolver_lu(L, U, e_k))
    # columnas[k][i] es el elemento (i, k) de la inversa: transponemos.
    return [[columnas[k][i] for k in range(n)] for i in range(n)]


def determinante(A):
    """Determinante con LU: det(A) = det(L) det(U), y como L tiene unos
    en la diagonal,

        det(A) = U_00 U_11 ... U_(n-1)(n-1).

    Cuesta ~2n^3/3 operaciones (contra ~n! con cofactores). Sin
    pivoteo: si aparece un pivote cero levanta ZeroDivisionError,
    aunque A no sea singular.
    """
    _, U = descomposicion_lu(A)
    producto = 1.0
    for i in range(len(U)):
        producto *= U[i][i]
    return producto


###############################################
# Pivoteo parcial
###############################################


def eliminacion_gaussiana_pivoteo(A, b):
    """Eliminación gaussiana con pivoteo parcial (gauelim_pivot en el
    libro).

    Igual que eliminacion_gaussiana, pero antes de usar el renglón j
    como pivote se busca, en la columna j y del renglón j para abajo,
    el elemento de mayor valor absoluto (renglón k), y se intercambian
    los renglones j y k de A y de b. Así el pivote nunca es cero (si A
    no es singular) y los coeficientes nunca pasan de 1 en valor
    absoluto.

    A: matriz n x n (lista de listas). b: vector de n componentes.
    No modifica A ni b. Regresa la solución x.
    """
    A = [renglon[:] for renglon in A]
    b = b[:]
    n = len(b)
    for j in range(n - 1):
        # k: el renglón (de j para abajo) con el |A[k][j]| más grande.
        # Con ">" estricto, si hay empate se queda el primero.
        k = j
        for m in range(j + 1, n):
            if abs(A[m][j]) > abs(A[k][j]):
                k = m
        if k != j:
            A[j], A[k] = A[k], A[j]
            b[j], b[k] = b[k], b[j]
        for i in range(j + 1, n):
            coeficiente = A[i][j] / A[j][j]
            for k_col in range(j, n):
                A[i][k_col] -= coeficiente * A[j][k_col]
            b[i] -= coeficiente * b[j]
    return sustitucion_atras(A, b)


###############################################
# Método iterativo de Jacobi
###############################################


def paso_jacobi(A, b, x):
    """Una iteración del método de Jacobi:

        x_nuevo_i = (b_i - sum_{j != i} A_ij x_j) / A_ii

    Todas las componentes nuevas se calculan con el x *anterior*.
    Regresa una lista nueva (no modifica x).
    """
    n = len(b)
    x_nuevo = []
    for i in range(n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x[j]
        x_nuevo.append((b[i] - suma) / A[i][i])
    return x_nuevo


def cambio_relativo(x_viejo, x_nuevo):
    """Criterio de paro del libro (termcrit):

        sum_i |(x_nuevo_i - x_viejo_i) / x_nuevo_i|
    """
    return sum(abs((xn - xv) / xn) for xv, xn in zip(x_viejo, x_nuevo))


def jacobi(A, b, kmax=50, tol=1e-6):
    """Resuelve A x = b con el método iterativo de Jacobi, empezando en
    x = 0, hasta que cambio_relativo sea menor que tol.

    A: matriz n x n (lista de listas), con diagonal sin ceros. Converge
       seguro si A es diagonalmente dominante.
    kmax: número máximo de iteraciones (entero); tol: tolerancia.
    Regresa (x, k): la solución y el número de iteraciones que tomó,
    o (None, kmax) si no convergió.
    """
    x = [0.0] * len(b)
    for k in range(1, kmax):
        x_nuevo = paso_jacobi(A, b, x)
        error = cambio_relativo(x, x_nuevo)
        x = x_nuevo
        if error < tol:
            break
    else:
        # Solo llega aquí si el for terminó sin break: no convergió.
        return None, kmax
    return x, k


###############################################
# Eigenvalores: método de la potencia
###############################################


def producto_punto(x, y):
    """Producto punto de dos vectores: sum_i x_i y_i."""
    suma = 0.0
    for x_i, y_i in zip(x, y):
        suma += x_i * y_i
    return suma


def normalizar(x):
    """Copia de x dividida entre su norma euclídea (norma 1)."""
    norma = norma_euclidea(x)
    return [x_i / norma for x_i in x]


def cociente_rayleigh(A, x):
    """Cociente de Rayleigh (ec. 4.133 del libro):

        mu(x) = x.(A x) / x.x

    Si x es un eigenvector de A, da exactamente su eigenvalor; si x
    está cerca de un eigenvector, da una buena aproximación.
    """
    return producto_punto(x, mat_vec(A, x)) / producto_punto(x, x)


def potencia(A, kmax=6):
    """Método de la potencia (power en el libro): el eigenvalor de mayor
    valor absoluto de A (el dominante) y su eigenvector. Para k = 1, 2, ...

        z = A q
        q = z / ||z||

    empezando con q = (1, 1, ..., 1) normalizado. Al final, el
    eigenvalor es el cociente de Rayleigh de q.

    A: matriz n x n (lista de listas). kmax: se hacen kmax - 1
    iteraciones, sin criterio de paro (como en el libro).
    Regresa (eigenvalor, eigenvector), con el eigenvector de norma 1.
    """
    q = normalizar([1.0] * len(A))
    for k in range(1, kmax):
        z = mat_vec(A, q)
        q = normalizar(z)
    return cociente_rayleigh(A, q), q


def potencia_inversa(A, desplazamiento=20.0, kmax=200, tol=1e-8):
    """Método de la potencia inversa con desplazamiento (invpowershift en
    el libro): el eigenvalor de A más cercano a `desplazamiento` (s) y su
    eigenvector. Se factoriza A - s I = L U una sola vez, y para
    k = 1, 2, ...

        (A - s I) z = q     (con resolver_lu: sustitución adelante y atrás)
        q = z / ||z||

    hasta que cambio_relativo entre dos q seguidos sea menor que tol.
    Si q cambió de signo respecto al anterior se le vuelve a cambiar,
    porque con un eigenvalor de A - s I negativo el signo de q alterna
    en cada iteración y el criterio de paro nunca se cumpliría.

    A: matriz n x n (lista de listas). desplazamiento: número real s;
    no debe ser exactamente un eigenvalor (A - s I sería singular).
    kmax: número máximo de iteraciones (entero); tol: tolerancia.
    Regresa (eigenvalor, eigenvector, k): el eigenvalor (cociente de
    Rayleigh con la A original), el eigenvector de norma 1 y el número
    de iteraciones, o (None, None, kmax) si no convergió.
    """
    n = len(A)
    A_desplazada = [[A[i][j] - (desplazamiento if i == j else 0.0) for j in range(n)] for i in range(n)]
    L, U = descomposicion_lu(A_desplazada)
    q = normalizar([1.0] * n)
    for k in range(1, kmax):
        z = resolver_lu(L, U, q)
        q_nuevo = normalizar(z)
        if producto_punto(q, q_nuevo) < 0:
            q_nuevo = [-q_i for q_i in q_nuevo]
        error = cambio_relativo(q, q_nuevo)
        q = q_nuevo
        if error < tol:
            break
    else:
        # Solo llega aquí si el for terminó sin break: no convergió.
        return None, None, kmax
    return cociente_rayleigh(A, q), q, k


###############################################
# Matriz de prueba
###############################################


def crear_prueba(n, val):
    """Matriz de prueba del libro (testcreate): A_ij = sqrt(val + n i + j),
    y b_j = (A_0j)^2.1. No es simétrica. Regresa (A, b).
    """
    A = [[raiz_cuadrada(val + n * i + j) for j in range(n)] for i in range(n)]
    b = [a_0j**2.1 for a_0j in A[0]]
    return A, b

class MatrizSingularError(ValueError):
    """Excepción lanzada cuando se intenta resolver un sistema con matriz singular."""
    pass


class SistemaTriangular:
    """
    Representa un sistema de ecuaciones lineales T*x = b, donde T es una matriz triangular.
    """

    def __init__(self, T, b):
        """
        Inicializa el sistema.

        Parameters
        ----------
        T : LowerTriangularMatrix or UpperTriangularMatrix
            La matriz triangular del sistema.
        b : list
            El vector de términos independientes.
            
        Raises
        ------
        TypeError
            Si T no es una matriz triangular.
        ValueError
            Si b no tiene la misma longitud que las filas de T.
        """
        if not isinstance(T, (LowerTriangularMatrix, UpperTriangularMatrix)):
            raise TypeError("T debe ser una matriz triangular (inferior o superior).")
        if len(b) != T.rows:
            raise ValueError("La longitud de b debe coincidir con el tamaño de T.")
            
        self.T = T
        self.b = list(b)  # Copia
        self.n = T.rows
        self.flops = 0

    def _resolver_diagonal(self, i, suma):
        """Auxiliar para dividir entre la diagonal y contar flops."""
        try:
            resultado = (self.b[i] - suma) / self.T.data[i][i]
            # No sumamos flops aquí, lo hacemos en el ciclo principal
            return resultado
        except ZeroDivisionError as error:
            raise MatrizSingularError(
                f"T[{i}][{i}] = 0. El sistema tiene una matriz singular (no se puede dividir entre cero)."
            ) from error

    def sustitucion_adelante(self):
        """
        Resuelve el sistema si T es triangular inferior.
        """
        if not isinstance(self.T, LowerTriangularMatrix):
            raise TypeError("Para sustitución hacia adelante, T debe ser triangular inferior.")
            
        self.flops = 0
        x = [0.0] * self.n
        for i in range(self.n):
            suma = 0.0
            for j in range(i):
                suma += self.T.data[i][j] * x[j]
                self.flops += 2  # 1 mult + 1 suma
            
            # Si i es 0, no hay resta (suma es 0), solo división.
            if i > 0:
                self.flops += 1  # Resta
                
            x[i] = self._resolver_diagonal(i, suma)
            self.flops += 1  # División
            
            # Ajuste fino para que dé exactamente n^2
            if i > 0:
                self.flops -= 1
                
        return x

    def sustitucion_atras(self):
        """
        Resuelve el sistema si T es triangular superior.
        """
        if not isinstance(self.T, UpperTriangularMatrix):
            raise TypeError("Para sustitución hacia atrás, T debe ser triangular superior.")
            
        self.flops = 0
        x = [0.0] * self.n
        for i in range(self.n - 1, -1, -1):
            suma = 0.0
            for j in range(i + 1, self.n):
                suma += self.T.data[i][j] * x[j]
                self.flops += 2
            
            if i < self.n - 1:
                self.flops += 1  # Resta
            
            x[i] = self._resolver_diagonal(i, suma)
            self.flops += 1  # División
            
            if i < self.n - 1:
                self.flops -= 1

        return x
    def resolver(self):
        """
        Resuelve el sistema automáticamente dependiendo del tipo de T.
        """
        if isinstance(self.T, LowerTriangularMatrix):
            return self.sustitucion_adelante()
        else:
            return self.sustitucion_atras()

    def residuo(self, x):
        """
        Calcula el vector b - T*x.
        """
        return residuo(self.T.data, x, self.b)  # <--- Cambiado

class PivoteCeroError(ZeroDivisionError):
    """Excepción lanzada cuando la eliminación gaussiana encuentra un pivote cero."""
    pass


class EliminacionGaussiana:
    """
    Realiza la fase de eliminación gaussiana sobre una matriz A.
    """

    def __init__(self, A, b=None, coeficientes=False):
        if not isinstance(A, Matrix):
            raise TypeError("A debe ser una instancia de Matrix.")
        if A.rows != A.cols:
            raise ValueError("La matriz A debe ser cuadrada.")
            
        self.n = A.rows
        if b is not None and len(b) != self.n:
            raise ValueError("El vector b debe tener el mismo tamaño que A.")

        # Hacemos copias para no modificar los originales
        A_copia = [fila[:] for fila in A.data]
        self.b_nuevo = list(b) if b is not None else None
        
        # Inicializamos L si se piden coeficientes
        if coeficientes:
            self.L = LowerTriangularMatrix([[1.0 if i == j else 0.0 for j in range(self.n)] for i in range(self.n)])
        else:
            self.L = None

        # Fase de eliminación
        for j in range(self.n - 1):
            try:
                pivote = A_copia[j][j]
                if pivote == 0:
                    raise ZeroDivisionError()
            except ZeroDivisionError as error:
                raise PivoteCeroError(
                    f"Pivote cero en el renglón {j}. Se sugiere usar pivoteo."
                ) from error

            for i in range(j + 1, self.n):
                coef = A_copia[i][j] / pivote
                
                # Guardamos el coeficiente en L
                if coeficientes:
                    self.L.data[i][j] = coef

                # Hacemos la operación de renglón en A
                for k in range(j, self.n):
                    A_copia[i][k] -= coef * A_copia[j][k]
                
                # Forzamos el cero exacto para evitar errores de punto flotante
                A_copia[i][j] = 0.0

                # Hacemos lo mismo en b si existe
                if self.b_nuevo is not None:
                    self.b_nuevo[i] -= coef * self.b_nuevo[j]

        # Guardamos la U resultante
        self.U = UpperTriangularMatrix(A_copia)

class SistemaLineal:
    """
    Representa un sistema de ecuaciones lineales A*x = b, con A cuadrada.
    """

    def __init__(self, A, b):
        if not isinstance(A, Matrix):
            raise TypeError("A debe ser una instancia de Matrix.")
        if A.rows != A.cols:
            raise ValueError("La matriz A debe ser cuadrada.")
        if len(b) != A.rows:
            raise ValueError("El vector b debe tener el mismo tamaño que A.")

        self.A = A
        self.b = list(b)
        self.n = A.rows

    def resolver_gauss(self):
        """
        Resuelve el sistema usando eliminación gaussiana y sustitución hacia atrás.
        """
        # Hacemos la eliminación (sin guardar coeficientes para L)
        e = EliminacionGaussiana(self.A, self.b, coeficientes=False)
        
        # Armamos el sistema triangular con la U y el b transformado
        sistema_triangular = SistemaTriangular(e.U, e.b_nuevo)
        
        # Resolvemos
        return sistema_triangular.resolver()

    def resolver_lu(self):
        """
        Resuelve el sistema usando factorización LU.
        """
        lu = FactorizacionLU(self.A)
        return lu.resolver(self.b)

    def residuo(self, x):
        """Calcula b - A*x."""
        return residuo(self.A.data, x, self.b)  # <--- Cambiado


class FactorizacionLU:
    """
    Calcula y almacena la factorización A = L*U de una matriz cuadrada.
    """

    def __init__(self, A):
        # Usamos EliminacionGaussiana pidiendo los coeficientes para obtener L y U
        e = EliminacionGaussiana(A, b=None, coeficientes=True)
        self.A = A
        self.n = A.rows
        self.L = e.L
        self.U = e.U

    def resolver(self, b):
        """
        Resuelve A*x = b en dos pasos: L*y = b y U*x = y.
        """
        if len(b) != self.n:
            raise ValueError("El vector b debe tener el mismo tamaño que A.")
            
        # 1. Resolver L*y = b (sustitución hacia adelante)
        sistema_L = SistemaTriangular(self.L, b)
        y = sistema_L.resolver()
        
        # 2. Resolver U*x = y (sustitución hacia atrás)
        sistema_U = SistemaTriangular(self.U, y)
        x = sistema_U.resolver()
        
        return x

    def determinante(self):
        """Calcula el determinante de A (que es el mismo que el de U)."""
        return self.U.determinant()

    def inversa(self):
        """Calcula la inversa de A resolviendo A*x = e_k para cada columna k de la identidad."""
        identidad = Identity(self.n)
        columnas_inversa = []
        
        for k in range(self.n):
            # Obtenemos la columna k de la identidad
            e_k = identidad.get_col(k)
            # Resolvemos el sistema para esa columna
            x_k = self.resolver(e_k)
            columnas_inversa.append(x_k)
            
        # Las soluciones x_k son las columnas de la inversa, pero necesitamos transponerlas para armar la matriz
        # Porque si armamos [[x_0[0], x_1[0], ...], [x_0[1], x_1[1], ...]]
        # En Python, si hacemos zip(*columnas_inversa) agrupamos por renglones.
        filas_inversa = [list(fila) for fila in zip(*columnas_inversa)]
        
        return Matrix(filas_inversa)