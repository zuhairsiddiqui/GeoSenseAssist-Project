from flask import Flask, json, Blueprint, render_template, request, send_from_directory
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


from dotenv import load_dotenv
import pygame

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = os.getenv("MYSQLPORT")
conn = mysql.connector.connect(
        host=MYSQLHOST,
        user=MYSQLUSER,
        password=MYSQLPASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQLPORT
  )

cursor = conn.cursor()

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

@views.route('/logout')
def logout():
  return render_template("logout.html")

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

@views.route('/audio_analysis', methods=['POST'])
def audio_analysis():
   result = request.form.get("result").replace("*","")
   filename = request.form.get("file")
   shape = request.form.get("shape")
   audio = googleTTS.textToSpeech(result,filename)
   pygame.mixer.init()
   pygame.mixer.music.load(audio)
   pygame.mixer.music.play()
   return render_template('shapes.html', filename=shape, result=result)

@views.route('/quiz')
def quiz():
    return render_template("quiz.html")


