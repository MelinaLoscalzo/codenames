import gamelib
import repositorio 
import random
from difflib import SequenceMatcher

class Codenames:

    def __init__(self, jugadores):
        self.jugadores = dict(jugadores)
        self.ids_jugadores = list(self.jugadores.keys())

        random.shuffle(self.ids_jugadores)
        jugadores_rojos = self.ids_jugadores[:len(self.ids_jugadores) // 2]
        jugadores_azules = self.ids_jugadores[len(self.ids_jugadores) // 2:]
    
        self.equipo_Rojo = [tuple(jugadores_rojos), "rojo", 0]
        self.equipo_Azul = [tuple(jugadores_azules), "azul" , 0]
        self.tablero = [[("N/A", False) for x in range(5)] for y in range(5)]
        self.llave = {}
        self.orden_spymasters = repositorio.cargar_pila_spymasters(jugadores_rojos, jugadores_azules) 
        self.lista_red_clues_usadas = []
        self.lista_blue_clues_usadas = []

    def generar_tablero(self):            
        """
        Asigna una palabra y un agente a cada una de las celdas del tablero.
        """

        self.tablero = repositorio.cargar_palabras_al_tablero(self.tablero)
        self.tablero = repositorio.cargar_agentes_inocentes(self.tablero) 
        return self.tablero
      
    def generar_llave(self):
        """
        Genera la llave que contiene coordenas aleatorias del tablero y por cada una de ellas, la llave contiene los agentes correspondientes de cada equipo y el asesino.
        """

        coordenadas = []    
        for y in range(5):
            for x in range(5):
                coordenadas.append((x, y))
        
        res = {}                
        res[coordenadas.pop(random.randrange(len(coordenadas)))] = "asesino", "asesino"
        
        for _ in range(4):            
            res[coordenadas.pop(random.randrange(len(coordenadas)))] = "azul", "azulF"
            res[coordenadas.pop(random.randrange(len(coordenadas)))] = "rojo", "rojoF"

        for _ in range(4):
            res[coordenadas.pop(random.randrange(len(coordenadas)))] = "azul", "azulM"
            res[coordenadas.pop(random.randrange(len(coordenadas)))] = "rojo", "rojoM"
            
        self.llave = res
        return self.llave 

    def seleccionar_spymaster(self):
        """
        ---> Devuelve el spymaster correspondien a la nueva ronda y toda la informacion del equipo al que pertenece.
        """
        spymaster = self.orden_spymasters.desapilar()
        if spymaster in self.equipo_Azul[0]:
            return spymaster, self.equipo_Azul
        return spymaster, self.equipo_Rojo
      
    def turno(self, nueva_ronda):      
        """
        Recibe un booleano que es True si la ronda es nueva.
        
        Si la ronda es nueva:
        ---> Devuelve una cadena 'spymaster' 
        De lo contrario:
        ---> Devuelve una cadena 'equipo' """
        
        if nueva_ronda:
            return "spymaster"
        return "equipo"

    def pedir_pista(self):
        """
        Este metodo pide al jugador que ingrese una pista y la cantidad de palabras del tablero
        que podrian estar relacionas. 
         
        ---> Devuelve una tupla(pista, cantidad) """
        
        for _ in range(3):
            palabra = str(gamelib.input("Ingrese una palabras de pista para guiar a tu equipo: "))
            nro_pista = str(gamelib.input("Ingrse el numero de tarjetas asociadas: "))

            if not palabra and not nro_pista:
                return "", 0
            elif not palabra.isspace() and (nro_pista.isdigit() and int(nro_pista) > 0):
                return palabra.upper(), int(nro_pista)

            gamelib.say("No se pudo validar tu entrada vuelve a ingresarla.")

        gamelib.say("Has perdido tu turno.")
        return "", 0 

    def pista_es_valida(self, pista):
        """ 
        Recibe: la palabra de la pista que forma la clue.
        
        Verifica si la palabra es una palabra similar a las del tablero o si es una palabra del tablero escrita al reves.

        ---> Devuelve: True si pasa la verificacion, de lo contrario, False 
        """
               
        pista = pista.upper()
        for y in range(5):
            for x in range(5):
                palabra = self.tablero[x][y][0]
                if palabra == pista[::-1]:
                    return False
                if SequenceMatcher(None,palabra,pista).ratio() >= 0.75:
                    return False 
 
        return True
 
    def penalizar(self, spymaster):
        """
        Recibe: El nombre del spymaster que cometio la falta.

        Informa al usurio que se cometio una falta con la clue correctamente ingresada.
        Asigna aleatoriamente un agente del equipo que hizo falta al contrario. 
        
        ---> Devuelve: Valor True para cambiar la ronda del juego.
        """

        rojo, azul = self.equipo_Rojo[1], self.equipo_Azul[1]
        jugadores_azules = self.equipo_Azul[0]

        gamelib.say(f"Se ha detectado una falta del jugador {self.jugadores[spymaster]}. Se le asignara un agente al equipo contrario.")

        if spymaster in jugadores_azules:
            for coord in self.llave.keys(): 
                color , _ = self.llave[coord]                
                if color == azul: 
                    self.llave[coord] = ('rojo','rojoM')
                    break
        else: 
            for coord in self.llave.keys():
                color, _ = self.llave[coord]
                if color == rojo:
                    self.llave[coord] = ('azul','azulM') 
                    break 
        
        return True

    def pedir_agente(self, coordenadas, equipo):
        """
        Recibe una coordenada del tablero y el equipo en juego.

        Segun corresponda altera los puntos del equipo.

        ---> Devuelve True si hay que cambiar la ronda, de lo contrario False. 
        """
        
        x, y = coordenadas
        palabra, _, tarjeta = self.tablero[x][y]
        self.tablero[x][y] = palabra, True, tarjeta 
        
        if coordenadas in self.llave.keys():
            agente, _ = self.llave[coordenadas] 

            if agente == equipo[1]:     
                equipo[2] += 1
                return False
            
            if agente == "asesino":
                equipo[2] -=5
                return True
                
            if agente != equipo[1] and not agente == "asesino":
                if equipo[1] in self.equipo_Azul:                    
                    self.equipo_Rojo[2] += 1 
                else:
                    self.equipo_Azul[2] += 1
                return True          
        
        equipo[2] -= 1
        return True
        
    def agregar_clue_usada(self, clue, spymaster):
        """
        Recibe una clue entera (palabra, numero) y el spymaster que la genero.

        Agrega a la clue la lista de clues usadas del equipo al que pertenece el Spymaster.
        """
        if spymaster in self.equipo_Azul[0]:
            self.lista_blue_clues_usadas.append(clue)
        else:
            self.lista_red_clues_usadas.append(clue)        

    def terminado(self):
        return self.orden_spymasters.esta_vacia()        

