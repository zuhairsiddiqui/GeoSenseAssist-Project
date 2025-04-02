import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
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


#test string input.
def TestUserString():
    userString = input("Enter a question for the AI: ")
    response = chat_session.send_message(userString)
    print(response.text)


#test image input
def get_image_from_user(image_path):
    """Get an image from the user and prepare it for the API"""
    #image_path = input("Enter the path to your image file: ")  # Prompt the user for the image path, image_path will store it.
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def analyze_image_geometry(image_path, command):
    """Get an image from the user and analyze its geometry"""
    img = get_image_from_user(image_path)
    input = command
    if img:
        # Send the image with a prompt to the chat session
        response = chat_session.send_message(
            #[img, "Analyze the geometry of the image."]
            #[img, "Provide only the name this shape."]
            [img, input]
        )
        #print(response.text)
        return response.text
    else:
        print("No valid image provided.")

# Example usage
if __name__ == "__main__":
    print("Gemini Image Analysis Tool")
    print("--------------------------")
    TestUserString()
    analyze_image_geometry()