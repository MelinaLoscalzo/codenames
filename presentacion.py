from juego import Codenames
import gamelib
import repositorio
import random
import tda


#Constantes 

#Dimensiones del tablero
ANCHO_TABLERO = 5
ALTO_TABLERO = 5
ANCHO_CELDA = 200
ALTO_CELDA = 126


def dibujar_tablero(juego):
    """
    Recibe: Un objeto Juego de la Clase Codenames.

    Dibuja el estado actual del tablero del juego.
    """
    gamelib.draw_image("img/fondo.gif", 1, 1) 

    for y in range(ALTO_TABLERO):
        for x in range(ANCHO_TABLERO):
            
            palabra, revelar, tarjeta = juego.tablero[x][y]

            if revelar:
                if (x,y) in juego.llave.keys():
                    _, tarjeta = juego.llave[(x,y)]
                    gamelib.draw_image(f"img/{tarjeta}.gif", x*150 + 100, y*100 + 10) 
                else:
                    gamelib.draw_image(f"img/{tarjeta}.gif", x*150 + 100, y*100 + 10)  
            else:
                gamelib.draw_image(f"img/tarjeta.gif", x*150 + 100, y*100 + 10)            
            
            gamelib.draw_text(palabra, x*150 + 140, y*100 + 70,size=10,fill="black",anchor="nw")


def dibujar_llave(juego,spymaster): 
    """
    Recibe: Un objeto Juego de la Clase Codenames y Spymaster que va a ver la llave.

    Dibuja la llave mostran las ubicaciones donde se encuentran los agentes de cada equipo y el asesino. 
    """

    info = juego.llave
    tablero_llave = [["N/N" for x in range(5)] for y in range(5)]  
        
    if spymaster in juego.equipo_Azul[0]:
        gamelib.draw_image(f"img/fondo_llaveA.gif",10 + 900, 10+50)
    else:
        gamelib.draw_image(f"img/fondo_llaveR.gif",10 + 900, 10+50)   
      
  
    for y in range(5):
        for x in range(5):
            
            color, _ = info.get((x,y), ("inocente", None))
            tablero_llave[x][y] = color            
            
            if tablero_llave[x][y] == "rojo":
                gamelib.draw_image("img/llaveR.gif",x*40 + 935 , y*40 + 80)     
            elif tablero_llave[x][y] == "azul":
                gamelib.draw_image("img/llaveA.gif",x*40 + 935 , y*40 + 80)
            elif tablero_llave[x][y] == "asesino":
                gamelib.draw_image("img/llaveAsesino.gif",x*40 + 935, y*40 + 80)
            else:
                gamelib.draw_image("img/llaveB.gif",x*40 + 935, y*40 + 80)     

def dibujar_clue(juego):
    """
    Recibe: Un objeto de la Clase Codenames.
    
    Escribe hasta las 10 ultimas clues, una de bajo de la otra, que se encuentran en las lista de clues usadas del juego. Escribe la ultima clue ingresada de cada equipo con el color del mismo.    
    """
    gamelib.draw_image('img/clueA.gif', 10 + 880, 10 + 50)
    lista_azul = juego.lista_blue_clues_usadas[-1:-10:-1]
    
    if juego.lista_blue_clues_usadas:
        gamelib.draw_text(f"{lista_azul[0]}", 990, 140, size = 10, fill = "blue")
        if len(lista_azul) > 1:
            for i in range(1, len(lista_azul)):
                gamelib.draw_text(f"{lista_azul[i]}", 990, 140 + i * 10, size = 10, fill = "white")

    gamelib.draw_image('img/clueR.gif',10 + 1100, 10 + 50)
    lista_rojo = juego.lista_red_clues_usadas[-1:-10:-1]
    
    if juego.lista_red_clues_usadas:
        gamelib.draw_text(f"{lista_rojo[0]}", 1210, 140, size = 10, fill = "red")
        if len(lista_rojo) > 1:
            for i in range(1, len(lista_rojo)):
                gamelib.draw_text(f"{lista_rojo[i]}", 990, 140 + i * 10, size = 10, fill = "white")

def mostrar_ganador(juego):
    """
    Recibe: Un objeto juego de la clase Codenames. 

    Compara los puntajes de cada equipo e informa quien fue es el ganador o si hubo un empate.
    """
    _, _, puntos_A = juego.equipo_Azul
    _, _, puntos_R = juego.equipo_Rojo

    if puntos_A == puntos_R:
        gamelib.draw_text("¡Es un empate!", 500 ,450 , size=6)
    elif puntos_R > puntos_A:
        gamelib.draw_text("¡El ganador es el Equipo Rojo!", 500, 450 ,size=6)
    elif puntos_R < puntos_A:
        gamelib.draw_text("¡El ganador es el Equipo Azul!", 500, 450 , size=6)

  

    
 
    



        







  