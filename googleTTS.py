from gtts import gTTS

#textToSpeech function will be called to generate an mp3 file containing TTS of a given string.
#the created mp3 file will then be sent to the website and played to help user interpret text 
def textToSpeech(userText):
    obj = gTTS(text=userText, lang='en', slow=False)
    obj.save("audio.mp3")
