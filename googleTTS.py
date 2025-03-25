#functions that read out an input string using tts will be created in this test file, and will then be used in the website 
from gtts import gTTS
import os

def textToSpeech(userText):
    obj = gTTS(text=userText, lang='en', slow=False)
    obj.save("audio.mp3")


