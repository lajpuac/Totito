import random
import math
import os

class Totito:
    #seleccionar x/o del jugador
    def __init__(ref):
        ref.tablero = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            ref.JugadorHumano = 'X'
            ref.JugadorIA = "O"
        else:
            ref.JugadorHumano = "O"
            ref.JugadorIA = "X"

    #Muestra el tablero
    def mostrarTablero(tablero):
        print("")
        for i in range(3):
            print("  ",tablero.tablero[0+(i*3)]," | ",tablero.tablero[1+(i*3)]," | ",tablero.tablero[2+(i*3)])
            print("")
            
    def tablero_lleno(ref,estado):
        return not "-" in estado

    def jugador_ha_ganado(ref,estado,jugador):
        if estado[0]==estado[1]==estado[2] == jugador: return True
        if estado[3]==estado[4]==estado[5] == jugador: return True
        if estado[6]==estado[7]==estado[8] == jugador: return True
        if estado[0]==estado[3]==estado[6] == jugador: return True
        if estado[1]==estado[4]==estado[7] == jugador: return True
        if estado[2]==estado[5]==estado[8] == jugador: return True
        if estado[0]==estado[4]==estado[8] == jugador: return True
        if estado[2]==estado[4]==estado[6] == jugador: return True

        return False

    def RevisarGanador(ref):
        if ref.jugador_ha_ganado(ref.tablero,ref.JugadorHumano):
            os.system("cls")
            print(f"   Jugador {ref.JugadorHumano} ha ganado el juego!")
            return True
            
        if ref.jugador_ha_ganado(ref.tablero,ref.JugadorIA):
            os.system("cls")
            print(f"   Jugador {ref.JugadorIA} ha ganado el juego!")
            return True

        # Empate?
        if ref. tablero_lleno(ref.tablero):
            os.system("cls")
            print("Es un empate!")
            return True
        return False

    def inicio(ref):
        inA = JugadoIA(ref.JugadorIA)
        humano = JugadorHumano(ref.JugadorHumano)
        while True:
            os.system("cls")
            print(f"   turno {ref.JugadorHumano} jugador")
            ref.mostrarTablero()
            
            #Humano
            casilla = humano.TurnoHumano(ref.tablero)
            ref.tablero[casilla] = ref.JugadorHumano
            if ref.RevisarGanador():
                break
            
            #IA
            casilla = inA.moviemientoIA(ref.tablero)
            ref.tablero[casilla] = ref.JugadorIA
            if ref.RevisarGanador():
                break

        # Mostrar Tablero final
        print()

        ref.mostrarTablero()

class JugadorHumano:
    def __init__(ref,letra):
        ref.letra = letra
    
    def TurnoHumano(ref,estado):
        # pedir la letra
        while True:
            casilla =  int(input("Ingrese la casilla del (1-9): "))
            print()
            if estado[casilla-1] == "-":
                break
        return casilla-1

class JugadoIA(Totito):
    def __init__(ref,letra):
        ref.JugadorIA = letra
        ref.JugadorHumano = "X" if letra == "O" else "O"

    def jugadores(ref,estado):
        n = len(estado)
        x = 0
        o = 0
        for i in range(9):
            if(estado[i] == "X"):
                x = x+1
            if(estado[i] == "O"):
                o = o+1
        
        if(ref.JugadorHumano == "X"):
            return "X" if x==o else "O"
        if(ref.JugadorHumano == "O"):
            return "O" if x==o else "X"
    
    def acciones(ref,estado):
        return [i for i, x in enumerate(estado) if x == "-"]
    
    def resultado(ref,estado,accion):
        nuevoEstado = estado.copy()
        jugador = ref.jugadores(estado)
        nuevoEstado[accion] = jugador
        return nuevoEstado
    
    def terminal(ref,estado):
        if(ref.jugador_ha_ganado(estado,"X")):
            return True
        if(ref.jugador_ha_ganado(estado,"O")):
            return True
        return False

    def minmax(ref, estado, jugador):
        max_jugador = ref.JugadorHumano  
        otro_jugador = 'O' if jugador == 'X' else 'X'

        #comprobar si el movimiento anterior es el ganador
        if ref.terminal(estado):
            return {'posicion': None, 'puntuacion': 1 * (len(ref.acciones(estado)) + 1) if otro_jugador == max_jugador else -1 * (
                        len(ref.acciones(estado)) + 1)}
        elif ref. tablero_lleno(estado):
            return {'posicion': None, 'puntuacion': 0}

        if jugador == max_jugador:
            mejor = {'posicion': None, 'puntuacion': -math.inf}  # maximo
        else:
            mejor = {'posicion': None, 'puntuacion': math.inf}  # minimo
        for posible_mov in ref.acciones(estado):
            nuevoEstado = ref.resultado(estado,posible_mov)
            sim_puntuacion = ref.minmax(nuevoEstado, otro_jugador)  # simular movimiento

            sim_puntuacion['posicion'] = posible_mov  # movimiento proximo

            if jugador == max_jugador:  #X jugador maximo
                if sim_puntuacion['puntuacion'] > mejor['puntuacion']:
                    mejor = sim_puntuacion
            else:
                if sim_puntuacion['puntuacion'] < mejor['puntuacion']:
                    mejor = sim_puntuacion
        return mejor

    def moviemientoIA(ref,estado):
        casilla = ref.minmax(estado,ref.JugadorIA)['posicion']
        return casilla

# Empezar el juego
totit = Totito()
totit.inicio()