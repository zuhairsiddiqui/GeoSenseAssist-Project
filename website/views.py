from flask import Flask, json, Blueprint, render_template, request, send_from_directory, session, redirect, url_for
import mysql.connector
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
import sys
import importlib.util
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
        file = request.files['fileUpload']
        if file:
            filename = secure_filename(file.filename)
            full_path = os.path.join(upload_dir, filename)
            file.save(full_path)

            quiz_text = generateQuiz.generate_quiz_from_image(full_path)
            return render_template("quiz.html", quiz_text=quiz_text)

    return render_template("quiz.html")

@views.route('/submit')
def submit():
    return render_template("submit-quiz.html")


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

        cursor.execute("""
                SELECT created_at, analysis_type, analysis, image_url
                FROM history_table
                WHERE email = %s
                ORDER BY created_at DESC
                LIMIT 5
                """, (primary_key,))
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
