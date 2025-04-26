from flask import Flask, json, Blueprint, render_template, request, send_from_directory, session, redirect, url_for
import mysql.connector
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
import sys
import importlib.util
from flask import session
from . import buttonsFunctionality
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import generateQuiz


from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=os.getenv("MYSQLPORT")
        )
        return conn
    except mysql.connector.Error as err:
        print("MySQL connection error:", err)
        return None

module_name = "ImageDetection"
#module_path = "GeoSenseAssist-Project/ImageDetection.py"  # Adjust as needed
module_path = os.path.join(os.path.dirname(__file__), "..", "ImageDetection.py")

spec = importlib.util.spec_from_file_location(module_name, module_path)
ImageDetection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ImageDetection)
# https://www.youtube.com/watch?v=GQLRVhXnZkE

app = Flask(__name__)

app.config['UPLOAD_DIRECTORY'] = 'uploads/'
parentFolder = 'GeoSenseAssist-Project/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB
upload_dir = os.path.join(parentFolder,app.config['UPLOAD_DIRECTORY'])
os.makedirs(upload_dir, exist_ok=True)
views = Blueprint('views', __name__)

@views.route('/') # will run for main page
def home():
  return render_template("website.html"), 200

@views.route('/login')
def login():
  return render_template("login.html")

@views.route('/uploads/<filename>')
def uploaded_file(filename):
    uploads_path = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    return send_from_directory(uploads_path, filename)


# value = request.form.get(key, default=None), key being educationLevel which we get, and the elementary level being the default.

@views.route('/upload_shapes', methods=['POST'])
def upload_shapes():
    education_level = request.form.get("educationLevel", "elementarylevel")
    shape, analysis = buttonsFunctionality.upload_shapes(education_level)
    return render_template('shapes.html', filename=shape, result=analysis)

@views.route('/upload_graphs', methods=['POST'])
def upload_graphs():
  education_level = request.form.get("educationLevel", "elementarylevel")  
  graph, analysis = buttonsFunctionality.upload_graph(education_level)
  return render_template('graphs.html', filename=graph, result=analysis)

@views.route('/upload_equations', methods=['POST'])
def upload_equation():
  education_level = request.form.get("educationLevel", "elementarylevel")
  equation, analysis = buttonsFunctionality.upload_equation(education_level)
  return render_template('equations.html', filename=equation, result=analysis)

@views.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    if request.method == 'POST':
        selected_image_url = request.form.get('selected_history_image')

        if selected_image_url:
            if 'user_email' not in session: # IF USER IS NOT LGOGED IN
                return redirect(url_for('auth.login')) # if user thats not logged in tries to access history, redirect them to login handled by auth.py
            
            try:
                import requests
                from PIL import Image
                from io import BytesIO
                import tempfile

                response = requests.get(selected_image_url)
                if response.status_code != 200:
                    return "Failed to download selected image.", 400
                
                # Save to a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp_file.write(response.content)
                temp_file.close()

                # Now pass temp_file.name to the generate_quiz_from_image
                quiz_data = generateQuiz.generate_quiz_from_image(temp_file.name)
            except Exception as e:
                print("Error downloading image:", str(e))
                return "Failed to process selected image.", 500

        else:
            # If no history image selected, fallback to uploaded file
            file = request.files.get('fileUpload')
            if file:
                filename = secure_filename(file.filename)
                full_path = os.path.join(upload_dir, filename)
                file.save(full_path)

                quiz_data = generateQuiz.generate_quiz_from_image(full_path)
            else:
                return "No file uploaded or selected.", 400

         # Store the quiz data in the session
        session['quiz_data'] = quiz_data

        user_images = fetch_user_images() if 'user_email' in session else []
        print("RAW QUIZ DATA:", quiz_data['raw_text'])
        quiz_lines = clean_quiz_text(quiz_data['raw_text'])
        print("CLEANED QUIZ LINES:", quiz_lines)
        return render_template("quiz.html", quiz_text=quiz_data['raw_text'], quiz_lines=quiz_lines, user_images=user_images)

    
    else:
        user_images = fetch_user_images() if 'user_email' in session else []
        return render_template("quiz.html", user_images=user_images)

@views.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        submitted_answers = request.form.to_dict()
        quiz_data = session.get('quiz_data', {})
        
        # Calculate score
        score = 0
        results = []
        
        for i, question in enumerate(quiz_data.get('questions', [])):
            user_answer = submitted_answers.get(f'q{i}', '').upper()
            is_correct = user_answer == question['correct_answer']
            if is_correct:
                score += 1
                
            results.append({
                'question': question['text'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct
            })
        
        total_questions = len(quiz_data.get('questions', []))
        percentage = (score / total_questions * 100) if total_questions else 0
        
        return render_template("submit-quiz.html", answers=submitted_answers,results=results,score=score,total_questions=total_questions,percentage=percentage)

    return redirect(url_for("views.quiz_page"))


@views.route('/')
def getHistoryData():
    conn = get_mysql_connection()
    if conn is None:
        return "Database connection failed", 500

    cursor = conn.cursor()
    cursor.execute("SELECT email, created_at, analysis_type, analysis FROM history_table")
    rows = cursor.fetchall()
    print(rows)
    return render_template('history.html', entries=rows)

@views.route('/history')
def submissionHistory():
    try:
        primary_key = session.get("user_email")
        if primary_key is None:
            return redirect(url_for('auth.login'))

        conn = get_mysql_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor()

        buttonsFunctionality.setPrimaryKey(primary_key)

        cursor.execute("SELECT created_at, analysis_type, analysis, image_url FROM history_table WHERE email = %s ORDER BY created_at DESC LIMIT 5", (primary_key,))
        rows = cursor.fetchall()
        rows = [(r[0], r[1], r[2], r[3].strip() if r[3] else None) for r in rows]

        cursor.close()
        conn.close()

        return render_template("history.html", entries=rows)

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return "Internal server error", 500

    except Exception as e:
        print("General error:", e)
        return "Something went wrong", 500
    
def fetch_user_images():
    if 'user_email' not in session:
        return []

    user_email = session['user_email']
    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT image_url FROM history_table WHERE email = %s ORDER BY created_at DESC LIMIT 5",
            (user_email,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [row[0] for row in rows if row[0]]
    return []

def clean_quiz_text(quiz_text):
    # Split smartly so each Question and each Option are separate (this way the quiz doesn't break)
    lines = []
    for raw_line in quiz_text.split('\n'):
        raw_line = raw_line.strip()
        if raw_line.startswith(('A.', 'B.', 'C.', 'D.')):
            # Options are sometimes clumped, this will split if its needed
            parts = raw_line.split(' ')
            buffer = ''
            for part in parts:
                if part in ['A.', 'B.', 'C.', 'D.']:
                    if buffer:
                        lines.append(buffer.strip())
                    buffer = part
                else:
                    buffer += ' ' + part
            if buffer:
                lines.append(buffer.strip())
        else:
            if raw_line:
                lines.append(raw_line)
    return lines

