import assistant

def main():
    assistant.speak("hola")
    listened = assistant.listen()
    print(f">> {listened}")

if __name__ == "__main__":
    main()