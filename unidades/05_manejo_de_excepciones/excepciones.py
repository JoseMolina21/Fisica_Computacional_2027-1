#!/usr/bin/env python3

###############################################
# Errores de sintaxis vs. excepciones
###############################################

# Un error de sintaxis (SyntaxError) es un programa mal escrito: ni
# siquiera llega a ejecutarse (por ejemplo, un "if" sin ":" al final).
# Una excepción, en cambio, ocurre en tiempo de ejecución: el
# programa está bien escrito, pero algo sale mal al correrlo (dividir
# entre cero, abrir un archivo que no existe, convertir "abc" a
# float). De eso trata esta unidad: cómo anticipar y manejar esas
# condiciones, en vez de dejar que el programa termine abruptamente.

###############################################
# Manejo de excepciones: try / except
###############################################

# Calculamos la rapidez media de una partícula (distancia / tiempo).
# Si el tiempo es 0, la división lanza ZeroDivisionError.
mediciones_tiempo = [2.0, 0.0, 4.0]
distancia = 10.0

for tiempo in mediciones_tiempo:
    try:
        rapidez = distancia / tiempo
    except ZeroDivisionError:
        print(f"tiempo={tiempo}: medición inválida (tiempo=0), se descarta")
    else:
        # else corre solo si el try NO lanzó ninguna excepción -- aquí
        # es el lugar correcto para el código que depende de que
        # `rapidez` sí se haya podido calcular.
        print(f"tiempo={tiempo}: rapidez = {rapidez} m/s")

# Capturar varios tipos de excepción a la vez: convertir texto a
# float puede fallar con ValueError (texto que no es un número), y
# aquí de paso con TypeError si alguien pasa None en vez de texto.
mediciones_crudas = ["9.81", "9.79", "nueve punto ocho", None, "9.80"]

for medicion in mediciones_crudas:
    try:
        valor = float(medicion)
    except (ValueError, TypeError) as error:
        print(f"medición {medicion!r} descartada: {type(error).__name__}: {error}")
    else:
        print(f"medición {medicion!r} -> {valor} m/s^2")

###############################################
# Lanzar excepciones: raise
###############################################

# Python no sabe, por sí solo, qué valores tienen sentido físico. Si
# una función recibe un dato físicamente imposible, conviene lanzar
# la excepción explícitamente, en vez de dejar que el error aparezca
# más adelante (y más difícil de rastrear) en otro cálculo.


def energia_cinetica(masa, velocidad):
    """Calcula la energía cinética (J). Lanza ValueError si masa < 0
    (una masa negativa no tiene sentido físico)."""
    if masa < 0:
        raise ValueError(f"la masa no puede ser negativa: {masa}")
    return 0.5 * masa * velocidad**2


try:
    energia_cinetica(-2.0, 3.0)
except ValueError as error:
    print(f"energia_cinetica rechazó la entrada: {error}")

print(f"energia_cinetica(2.0, 3.0) = {energia_cinetica(2.0, 3.0)} J")

###############################################
# Encadenamiento de excepciones: raise ... from ...
###############################################

# Cuando una excepción de "bajo nivel" (aquí, ValueError de float())
# se traduce a una excepción más significativa para quien llama a la
# función, `from` conserva el error original en el traceback (como
# "causa"), en vez de esconderlo.


def leer_temperatura(texto):
    """Convierte texto a un float que representa una temperatura en
    Celsius. Lanza ValueError con un mensaje más claro que el de
    float() si el texto no se puede convertir."""
    try:
        return float(texto)
    except ValueError as error:
        raise ValueError(f"'{texto}' no es una temperatura válida") from error


try:
    leer_temperatura("mucho frío")
except ValueError as error:
    print(f"leer_temperatura falló: {error}")
    print(f"causa original: {error.__cause__!r}")

###############################################
# Excepciones definidas por el usuario
###############################################

# Heredar de Exception (no de BaseException) permite crear categorías
# de error propias del dominio del problema, que quien llama a la
# función puede capturar específicamente (en vez de un ValueError
# genérico que podría venir de cualquier otro lado).


class TemperaturaImposibleError(Exception):
    """Se lanza cuando una temperatura está por debajo del cero
    absoluto (-273.15 °C), algo físicamente imposible."""


CERO_ABSOLUTO_CELSIUS = -273.15


def validar_temperatura(temperatura_celsius):
    if temperatura_celsius < CERO_ABSOLUTO_CELSIUS:
        raise TemperaturaImposibleError(
            f"{temperatura_celsius} °C está por debajo del cero "
            f"absoluto ({CERO_ABSOLUTO_CELSIUS} °C)"
        )
    return temperatura_celsius


try:
    validar_temperatura(-300.0)
except TemperaturaImposibleError as error:
    print(f"validar_temperatura rechazó la entrada: {error}")

print(f"validar_temperatura(25.0) = {validar_temperatura(25.0)} °C")

###############################################
# finally: acciones de limpieza
###############################################

# El bloque finally se ejecuta siempre -- haya habido excepción o no,
# y aunque el except la vuelva a lanzar. Sirve para garantizar que
# algo pase pase lo que pase (aquí, nada más registrar que se intentó
# procesar la medición; en código real, algo como cerrar una conexión
# o liberar un recurso).

for temperatura in (25.0, -300.0):
    try:
        validar_temperatura(temperatura)
    except TemperaturaImposibleError as error:
        print(f"rechazada: {error}")
    finally:
        print(f"-- fin del procesamiento de la medición {temperatura} °C --")

###############################################
# with: acciones de limpieza predefinidas (y manejo de errores de E/S)
###############################################

# El bloque with (unidad 04) ya se encarga de cerrar el archivo pase
# lo que pase adentro -- es la versión "predefinida" de un
# try/finally. Aquí además capturamos el error si el archivo no
# existe, un caso muy común al leer datos de un experimento.
try:
    with open("datos/no_existe.txt") as archivo:
        contenido = archivo.read()
except FileNotFoundError as error:
    print(f"no se pudo leer el archivo: {error}")

###############################################
# Ejercicio: procesar una bitácora de mediciones con errores
###############################################

# Una bitácora de temperaturas capturada a mano, con errores típicos:
# texto que no es un número, y una medición físicamente imposible.
# El objetivo es procesar todo lo que sí se pueda, reportar cada
# problema (sin tronar el programa), y al final dar un resumen.

bitacora_cruda = ["22.5", "23.1", "veintitrés", "-300.0", "21.8", ""]

temperaturas_validas = []
errores = []

for renglon in bitacora_cruda:
    try:
        temperatura = leer_temperatura(renglon)
        validar_temperatura(temperatura)
    except ValueError as error:
        errores.append(str(error))
    except TemperaturaImposibleError as error:
        errores.append(str(error))
    else:
        temperaturas_validas.append(temperatura)

print(f"\nTemperaturas válidas: {temperaturas_validas}")
print(f"Errores encontrados ({len(errores)}):")
for error in errores:
    print(f"  - {error}")

if temperaturas_validas:
    promedio = sum(temperaturas_validas) / len(temperaturas_validas)
    print(f"Promedio: {promedio:.2f} °C")

# Para extender en clase:
#
# 1. leer_temperatura() y validar_temperatura() lanzan ValueError y
#    TemperaturaImposibleError por separado -- ¿conviene que
#    TemperaturaImposibleError herede de ValueError en vez de
#    Exception? (Así un solo `except ValueError` capturaría ambas.)
#    Pruébalo y simplifica los except del ejercicio de arriba.
# 2. ¿Qué pasa si accidentalmente pones `except Exception` como
#    primer except (antes de los específicos)? Pruébalo y explica por
#    qué el orden de los except sí importa.
