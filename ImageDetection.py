import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#connect API KEY
genai.configure(api_key=os.environ["API_KEY"])


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

#to do: add image to the chat session
#response = chat_session.send_message(input_file,"Analyze the geometry of the image.")

response = chat_session.send_message("Analyze the geometry of the image.")

print(response.text)