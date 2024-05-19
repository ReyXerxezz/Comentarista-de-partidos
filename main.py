import assistant
# import menu

def main():
    assistant.speak("Marco")
    lectura = assistant.listen()
    print(lectura)
    if(lectura == "Polo"):
        assistant.speak("Correcto")
    else:
        assistant.speak("Te has equivocado")
    

if __name__ == '__main__':
    main()