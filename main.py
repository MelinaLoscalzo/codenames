import gamelib
import presentacion
from juego import Codenames
import repositorio

ANCHO_VENTANA = 1340
ALTO_VENTANA = 700

def mostrar_estado_juego(juego, spymaster, nro_turno):
    
    jugadores_azules, color_azul, puntos_azules = juego.equipo_Azul
    jugadores_rojos, color_rojos, puntos_rojos = juego.equipo_Rojo
    
    if spymaster in jugadores_azules:
        jugador = juego.jugadores[spymaster]
        color = color_azul
    else:
        jugador = juego.jugadores[spymaster]
        color = color_rojos

    if juego.turno(nro_turno) == "spymaster":
        gamelib.draw_text(f"{jugador.upper()} \t\t\t {color.upper()}", ANCHO_VENTANA // 2, 600, size = 10,fill="black" )
    else:
        gamelib.draw_text(f" -- \t\t {color.upper()} ", ANCHO_VENTANA // 2, 600, size = 10, fill = "black")
 
    gamelib.draw_text(f"{color_azul.upper()} -- {puntos_azules} \t\t {color_rojos.upper()} -- {puntos_rojos}", ANCHO_VENTANA // 2, 650, size  = 10, fill = "black")

def mostrar_ganador(juego):

    _, color_azul, puntos_azules = juego.equipo_Azul
    _, color_rojo, puntos_rojos = juego.equipo_Rojo

    if puntos_azules > puntos_rojos:
        gamelib.draw_image('img/game_overA.gif',400,100)
        gamelib.say(f"¡El ganador es Equipo {color_azul}!")
    elif puntos_azules == puntos_rojos:
        gamelib.draw_image('img/game_overE.gif',400,100)
        gamelib.say(f"Empate...")                
    else:
        gamelib.draw_image('img/game_overR.gif',400,100)
        gamelib.say(f"El ganador es Equipo {color_rojo}!")
    gamelib.play_sound('sound/game_over.wav')
       
def main():

    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    gamelib.play_sound('sound/sound_juego.wav')
    jugadores_ingresados = repositorio.ingresar_jugadores()
    juego = Codenames(jugadores_ingresados) 
    juego.generar_tablero()
    juego.generar_llave() 
        
    while gamelib.loop(fps=30):
        
        if not juego.terminado():
            spymaster, equipo = juego.seleccionar_spymaster()
            nueva_ronda = True
            cambiar_de_ronda = False
            mostrar_estado_juego(juego, spymaster, nueva_ronda)
        else:
            presentacion.dibujar_tablero(juego)
            mostrar_estado_juego(juego, spymaster, nueva_ronda)
            break

        while not cambiar_de_ronda:
            gamelib.draw_begin()
            presentacion.dibujar_tablero(juego)
            
            if juego.turno(nueva_ronda) == "spymaster":
                mostrar_estado_juego(juego, spymaster, nueva_ronda)
                nueva_ronda = False

                presentacion.dibujar_llave(juego,spymaster)
                palabra, nro_pista = juego.pedir_pista() 

                if not palabra:
                    cambiar_de_ronda = True
                elif juego.pista_es_valida(palabra):
                    juego.agregar_clue_usada(f"{palabra} -- {nro_pista}", spymaster)
                else:    
                    cambiar_de_ronda = juego.penalizar(spymaster)
                
                gamelib.draw_end()

            else:
                intentos = 0
                while not cambiar_de_ronda:
                    presentacion.dibujar_tablero(juego)
                    presentacion.dibujar_clue(juego)
                    mostrar_estado_juego(juego, spymaster, nueva_ronda)

                    ev = gamelib.wait()

                    if not ev:
                        break

                    if ev.type == gamelib.EventType.ButtonPress:
                        coordenada = repositorio.limpiar_coordenada(ev.x, ev.y)
                        
                        if repositorio.verificar_si_pertenece_tablero(coordenada, juego):
                            juego.pedir_agente(coordenada, equipo)
                            presentacion.dibujar_tablero(juego)
                            intentos += 1
                
                        if intentos == (nro_pista + 1):
                            cambiar_de_ronda = True
                            gamelib.say("Se acabaron los intentos de tu equipo. Empieza una nueva ronda para el equipo contrario.") 
  
                gamelib.draw_end()
                                        
    gamelib.draw_begin()
    mostrar_ganador(juego)
    gamelib.draw_text("Toca cualquier tecla para cerrar el juego", ANCHO_VENTANA // 2, ALTO_VENTANA - 20, size = 20, fill = "white")    
    gamelib.draw_end()
    gamelib.wait(gamelib.EventType.KeyPress)

gamelib.init(main)