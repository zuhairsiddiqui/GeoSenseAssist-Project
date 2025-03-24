import pyttsx3

engine = pyttsx3.init()

def textToSpeech(text):
    engine.say(text)
    engine.runAndWait()
