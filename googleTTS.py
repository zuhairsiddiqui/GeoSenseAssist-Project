from gtts import gTTS
import os

#textToSpeech function will be called to generate an mp3 file containing TTS of a given string.
#the created mp3 file will then be sent to the website and used appropriately 

current_dir = os.getcwd()

# Define the uploads folder inside the current directory
upload_dir = os.path.join(current_dir, "uploadsAudio")

# Create the directory if it doesn't exist
os.makedirs(upload_dir, exist_ok=True)

def textToSpeech(userText, image):
    obj = gTTS(text=userText, lang='en', slow=False)
    filename = "uploadsAudio/" + image
    obj.save(filename)
    return filename