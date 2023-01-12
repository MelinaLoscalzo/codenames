from tda import Pila
import gamelib
import random

def cargar_agentes_inocentes(tablero):
    """ Recibe un tablero con formato de listas de listas. 
        
        Incorpora por cada celda una tajeta de Inocente. 
        
        --> Devuelve el tablero recibido con las tarjetas."""
    
    for x in range(len(tablero[0])):
        for y in range(len(tablero)):
            palabra, revelado = tablero[x][y]
            if x % 2 == 0:
                tablero[x][y] = palabra, revelado, "inocenteF"
            else:
                tablero[x][y] = palabra, revelado, "inocenteM"

    return tablero

def cargar_palabras_al_tablero(tablero): 
    """ Recibe un tablero con el formato de listas de listas Ej: [ [elem], [elem]]. 
    
        Segun sus dimensiones carga las palabras necesarias para el mismo.
        
        --> Devuelve el tablero con palabras nuevas. """
        
    cantidad = len(tablero) * len(tablero[0])
    pila_palabras = _cargar_palabras(cantidad)
    
    for y in range(len(tablero)):
        for x in range(len(tablero[0])):
            _, revelacion = tablero[x][y]
            tablero[x][y] = pila_palabras.pop(), revelacion

    return tablero 

def _cargar_palabras(cantidad_solicitada):
    """ Recibe una cantidad de palabras.

        Carga palabras del archivo palabras.txt. Mezcla las palabras cargadas y las apila asi como tambien verifica si el archivo tiene las palabras sufieintes para jugar.
        
        --> Devuelve una pila de palabras.""" 
    
    palabras_cargadas = []

    try:
        with open("palabras.txt","r") as archivo:
            for linea in archivo:
                palabras_cargadas.append(linea.rstrip())                      
                
    except IOError:
        print("No se pudo abrir el archivo.")
    
    random.shuffle(palabras_cargadas)  
    
    if len(palabras_cargadas[:cantidad_solicitada]) < cantidad_solicitada:
        raise Exception("No hay suficientes palabras en el archivo palabras.txt para jugar.")
    
    return palabras_cargadas[:cantidad_solicitada]                   
      
def cargar_pila_spymasters(id_jugadores_A, id_jugadores_B):
    """ Recibe un arreglo con los equipos que van a jugar. 
        
        Apila intercalando los integrantes de cada equipo. 
        
        --> Devuelve una pila con el orden de los spymasters. """

    res = Pila()
    
    while id_jugadores_A and id_jugadores_B:
    
        id_A = random.choice(id_jugadores_A)
        id_jugadores_A.remove(id_A)
        id_B = random.choice(id_jugadores_B)
        id_jugadores_B.remove(id_B)
        res.apilar(id_A)
        res.apilar(id_B)
 
    return res

def limpiar_coordenada(x, y):
    """
    Recibe: Un valor de X y un valor de Y donde el usuario hizo click en la pantalla.
    
    ---> Devuelve: una tupla(X, Y) cuales valores reflejan una posible coordenada del tablero del juego.
    """
    return ( (x - 100) // 150, (y - 10) // 100 )

def verificar_si_pertenece_tablero(coordenada, juego):
    """
    Recibe: una coordenada = (X, Y) y un objeto de la Clase Codenames.

    ---> Devuelve: True solo si la coordenada recibida pertenece al tablero del juego y esta no fue revelada.
    """
    
    x, y = coordenada 
    
    if 0 <= x < len(juego.tablero) and 0 <= y < len(juego.tablero[0]):
        if not juego.tablero[x][y][1]:
            return True  
    
    return False
 
def ingresar_jugadores():
    """
    Pide al usuario que ingrese los jugadores para armar los equipos para jugar. Se le pedira ingresar jugadores al usuario hasta poder tener equipos con la misma cantidad de jugadores.

    ---> Devuelve: Un lista de dos elementos los cuales, contiene en cada uno, un lista mezclada con los jugadores ingresados.  
    """

    jugadores = {}
    num = 0
    
    while True:
        jugador = gamelib.input("Ingrese el nombre de un jugador: (Si termino de ingresar los jugadores solo toque OK.)")    
           
        if not jugador:
            if len(jugadores) % 2 == 0 and len(jugadores) > 0:
                break
            gamelib.say("Falta ingresar un jugador mas.")
            continue

        if jugador and not jugador.isspace():
            jugadores[num] = jugador
            gamelib.say(f"Se ingreso al jugador: {jugador} con el numero {num}")
            num += 1
        
    return jugadores        
       