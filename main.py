import assistant
import schedule
import time

def preguntar_evento():
    assistant.speak("¿Ha sucedido algo en el partido de fútbol?")
    respuesta = assistant.listen()
    
    if respuesta.lower() == "sí" or respuesta.lower() == "si":
        assistant.speak("¿Qué ha sucedido?")
        evento = assistant.listen()
        
        if evento.lower() == "gol":
            assistant.speak("¿De quién fue el gol?")
            autor_gol = assistant.listen()
            assistant.speak("¿Quién hizo la asistencia?")
            asistente = assistant.listen()
            print(f"Gol de {autor_gol} con asistencia de {asistente}.")
        
        elif evento.lower() == "falta":
            assistant.speak("¿De quién fue la falta?")
            autor_falta = assistant.listen()
            assistant.speak("¿Sobre quién fue la falta?")
            victima_falta = assistant.listen()
            print(f"Falta de {autor_falta} sobre {victima_falta}.")
        else:
            assistant.speak("Evento no reconocido.")
    else:
        assistant.speak("Entendido, seguimos.")

def main():
    # Programar la pregunta sobre el partido cada minuto
    schedule.every(1).minutes.do(preguntar_evento)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
