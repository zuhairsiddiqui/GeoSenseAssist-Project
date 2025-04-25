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
    Carefully analyze the uploaded image.

    If the image is math-related,
    generate a 5-question multiple-choice quiz based solely on the math content in the image.

    Each question must have:
    - A clear math-related question
    - 4 answer options labeled A–D
    - The correct answer indicated like this:
    Answer: A

    Format exactly like this:

    1. Question text?
    A. Option A
    B. Option B
    C. Option C
    D. Option D
    Answer: A

    (repeat for all questions)

    If the image is not math-related, respond with: "This image is not math-related."
    """
    response = model.generate_content([prompt, img])
    
    # Parse the response to extract questions and correct answers
    questions = []
    current_question = None
    
    for line in response.text.split('\n'):
        line = line.strip()
        # Fixed the tuple construction for question numbers
        if any(line.startswith(f"{i}.") for i in range(1, 6)):  # Question line
            if current_question:
                questions.append(current_question)
            current_question = {
                'text': line,
                'options': [],
                'correct_answer': None
            }
        elif line.startswith(('A.', 'B.', 'C.', 'D.')):  # Option line
            current_question['options'].append(line)
        elif line.startswith('Answer:'):  # Answer line
            current_question['correct_answer'] = line.split(':')[1].strip()
    
    if current_question:  # Add the last question
        questions.append(current_question)
    
    return {
        'raw_text': response.text,
        'questions': questions
    }
