import assistant
import time
from unidecode import unidecode
from partido import Partido
from estadisticasgenerales import Estadisticas

# Almacenar el tiempo de inicio del partido
tiempo_inicio = time.time()

estadisticas = Estadisticas()

def calcular_minuto():
    tiempo_actual = time.time()
    diferencia_segundos = tiempo_actual - tiempo_inicio
    minuto = int(diferencia_segundos // 60)
    return minuto

def preguntar_estadisticas():
    while True:
        assistant.speak("¿Desea saber alguna estadística adicional?")
        respuesta = assistant.listen().lower()

        if respuesta in ["sí", "si", "¡sí!", ""]:
            assistant.speak("¿Qué desea saber? Opciones: máximo goleador, máximo asistente, equipo con más victorias, tabla de puntos")
            estadistica = assistant.listen().lower()

            if estadistica == "máximo goleador":
                estadisticas.mostrar_maximo_goleador()
            elif estadistica == "máximo asistente":
                estadisticas.mostrar_maximo_asistente()
            elif estadistica == "equipo con más victorias":
                estadisticas.mostrar_equipo_mas_victorias()
            elif estadistica == "tabla de puntos":
                estadisticas.mostrar_puntos()
            else:
                assistant.speak("Opción no reconocida.")

        else:
            assistant.speak("Entendido, seguimos.")
            break



def jugar_otro_partido():
    assistant.speak("¿Quiere jugar otro partido?")
    respuesta = assistant.listen().lower()

    if respuesta in ["sí", "si", "¡sí!", ""]:
        return True
    else:
        assistant.speak("Gracias, hasta luego.")
        return False

def main():
    while True:
        preguntar_estadisticas();
        
        assistant.speak("¿Cuál es el club local?")
        club_local = unidecode(assistant.listen().lower())
        assistant.speak("¿Cuál es el club visitante?")
        club_visitante = unidecode(assistant.listen().lower())
        
        partido = Partido(club_local, club_visitante)
        
        while not partido.partido_terminado:
            minuto_actual = partido.calcular_minuto()
            if minuto_actual >= 90 and partido.tiempo_extra == 0:
                assistant.speak("Hemos llegado al minuto 90. ¿Se va a reponer tiempo?")
                respuesta = assistant.listen()
                if respuesta.lower() in ["sí", "si"]:
                    assistant.speak("¿Cuántos minutos se van a reponer?")
                    tiempo_extra = int(assistant.listen())
                    partido.tiempo_extra = tiempo_extra
                else:
                    partido.terminar_partido()
                    break

            if minuto_actual >= 90 + partido.tiempo_extra:
                assistant.speak("El tiempo de reposición ha terminado. El partido ha terminado.")
                partido.terminar_partido()
                break
            
            assistant.speak("¿Ha sucedido algo en el partido de fútbol?")
            respuesta = assistant.listen()
            print({respuesta})

            if respuesta.lower() in ["sí", "si", "¡sí!", ""]:
                assistant.speak("¿Qué ha sucedido?")
                event = assistant.listen()

                if event.lower() == "marcaron":
                    assistant.speak("¿De quién fue el gol?")
                    autor_gol = assistant.listen().lower()
                    assistant.speak("¿Quién hizo la asistencia?")
                    asistente = assistant.listen().lower()
                    partido.marcar_gol(autor_gol, asistente)

                elif event.lower() == "falta":
                    assistant.speak("¿De quién fue la falta?")
                    autor_falta = assistant.listen().lower()
                    assistant.speak("¿Sobre quién fue la falta?")
                    victima_falta = assistant.listen().lower()
                    assistant.speak("¿Qué tarjeta se mostró?")
                    tarjeta = assistant.listen().lower()
                    partido.cometer_falta(autor_falta, victima_falta, tarjeta)

                elif event.lower() == "partido terminado":
                    assistant.speak("Gracias por la información. El partido ha terminado.")
                    assistant.speak(f'El resultado del partido es, {club_local} {partido.goles_local} {club_visitante} {partido.goles_visitante}')
                    partido.terminar_partido()

                else:
                    assistant.speak("Evento no reconocido.")
            else:
                assistant.speak("Entendido, seguimos.")
            
            time.sleep(10)

        assistant.speak(f'El resultado final del partido es, {club_local} {partido.goles_local} - {club_visitante} {partido.goles_visitante}')
        
        
        
        if not jugar_otro_partido():
            break
if __name__ == '__main__':
    main()