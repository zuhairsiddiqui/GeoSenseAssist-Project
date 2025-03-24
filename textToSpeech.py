import pyttsx3

engine = pyttsx3.init()

def textToSpeech(text):
    engine.say(text)
    engine.runAndWait()

#Example
textToSpeech("Hello, how are you?")
textToSpeech("This is a text-to-speech example.")

# Set the speech rate (speed)
#Slow speeds (50-100 ):
#Moderate speeds (150-200 ):
#Fast speeds (250-300 ): 
#Very fast speeds (400+ )
engine.setProperty('rate', 200)
# Set the volume (0.0 to 1.0)
engine.setProperty('volume', 0.5) 

# Change the voice: 0 = male and 1 = female
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)  
