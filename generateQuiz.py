import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import io

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

chat_session = model.start_chat(history=[])


def generate_quiz_from_image(image_path):
    img = PIL.Image.open(image_path)
    prompt = """
    Based on this image, generate a 5-question multiple-choice quiz.
    Include 4 answer options (A–D)
    """
    response = model.generate_content([prompt, img])
    return response.text

