import speech_recognition as sr
from gtts import gTTS
import playsound
import os


def speak(message):
    tts = gTTS(text=message, lang="es", slow=False)
    # filename = os.path.dirname(__file__) + "\\voice.mp3"
    filename = os.path.dirname(__file__) + "/voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        print("Listening ...")
        beep()
    
        audio = r.listen(source)
        said = ""

        try:
            # recognize_bing()
            # recognize_google_cloud()
            # recognize_ibm()
            print("1")
            said = r.recognize_google(audio, language='es-ES')
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said


def beep():
    # filename = os.path.dirname(_file_) + "\\sounds\\beep.mp3"
    filename = os.path.dirname(__file__) + "/sounds/beep.mp3"
    playsound.playsound(filename)