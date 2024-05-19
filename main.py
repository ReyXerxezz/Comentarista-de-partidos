import assistant
import time

# Almacenar el tiempo de inicio del partido
tiempo_inicio = time.time()

def calcular_minuto():
    tiempo_actual = time.time()
    diferencia_segundos = tiempo_actual - tiempo_inicio
    minuto = int(diferencia_segundos // 60)
    return minuto

def main():
    global partido_terminado
    partido_terminado = False
    
    while not partido_terminado:
        assistant.speak("¿Ha sucedido algo en el partido de fútbol?")
        respuesta = assistant.listen()

        if respuesta.lower() in ["sí", "si"]:
            assistant.speak("¿Qué ha sucedido?")
            event = assistant.listen()

            if event.lower() == "marcaron":
                assistant.speak("¿De quién fue el gol?")
                autor_gol = assistant.listen()
                assistant.speak("¿Quién hizo la asistencia?")
                asistente = assistant.listen()
                minuto_gol = calcular_minuto()
                assistant.speak(f"Gol de {autor_gol} con asistencia de {asistente} en el minuto {minuto_gol}.")

            elif event.lower() == "falta":
                assistant.speak("¿De quién fue la falta?")
                autor_falta = assistant.listen()
                assistant.speak("¿Sobre quién fue la falta?")
                victima_falta = assistant.listen()
                minuto_falta = calcular_minuto()
                assistant.speak(f"Falta de {autor_falta} sobre {victima_falta} en el minuto {minuto_falta}.")

            elif event.lower() == "partido terminado":
                assistant.speak("Gracias por la información. El partido ha terminado.")
                assistant.speak("El partido ha terminado.")
                partido_terminado = True

            else:
                assistant.speak("Evento no reconocido.")
        else:
            assistant.speak("Entendido, seguimos.")
        
        # Esperar un tiempo antes de preguntar nuevamente
        time.sleep(30)  # Espera de 30 segundos

if __name__ == '__main__':
    main()