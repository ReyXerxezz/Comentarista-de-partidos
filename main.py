import assistant
import time
import schedule
from partido import Partido

# Almacenar el tiempo de inicio del partido
tiempo_inicio = time.time()

def calcular_minuto():
    tiempo_actual = time.time()
    diferencia_segundos = tiempo_actual - tiempo_inicio
    minuto = int(diferencia_segundos // 60)
    return minuto

def main():
    
    partido = Partido()
    
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

        if respuesta.lower() in ["sí", "si","¡sí!", ""]:
            assistant.speak("¿Qué ha sucedido?")
            event = assistant.listen()

            if event.lower() == "marcaron":
                assistant.speak("¿De quién fue el gol?")
                autor_gol = assistant.listen().lower()
                assistant.speak("¿Quién hizo la asistencia?")
                asistente = assistant.listen().lower()
                partido.marcar_gol(autor_gol, asistente)  # Llamas al método marcar_gol() de la clase Partido

            elif event.lower() == "falta":
                assistant.speak("¿De quién fue la falta?")
                autor_falta = assistant.listen().lower()
                assistant.speak("¿Sobre quién fue la falta?")
                victima_falta = assistant.listen().lower()
                assistant.speak("¿Qué tarjeta se mostró?")
                tarjeta = assistant.listen().lower()
                partido.cometer_falta(autor_falta, victima_falta, tarjeta)  # Llamas al método cometer_falta() de la clase Partido

            elif event.lower() == "partido terminado":
                assistant.speak("Gracias por la información. El partido ha terminado.")
                partido.terminar_partido()  # Llamas al método terminar_partido() de la clase Partido

            else:
                assistant.speak("Evento no reconocido.")
        else:
            assistant.speak("Entendido, seguimos.")
        
        # Esperar un tiempo antes de preguntar nuevamente
        time.sleep(10)  # Espera de 30 segundos

if __name__ == '__main__':
    main()