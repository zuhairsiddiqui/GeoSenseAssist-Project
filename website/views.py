from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for
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
import googleTTS


from dotenv import load_dotenv
import pygame

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HOST_NAME = os.getenv("HOST_NAME")
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
conn = mysql.connector.connect(
        host=HOST_NAME,
        user = USER_NAME,
        password = USER_PASSWORD,
        database=DATABASE_NAME
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

@views.route('/sign-up')
def signup():
    return render_template("signup.html")

@views.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

# value = request.form.get(key, default=None), key being educationLevel which we get, and the elementary level being the default.

@views.route('/upload_shapes', methods=['POST'])
def upload_shapes():
    education_level = request.form.get("educationLevel", "elementarylevel")
    shape, analysis = buttonsFunctionality.upload_shapes(education_level)
    return render_template('Shapes.html', filename=shape, result=analysis)

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
   result = request.form.get("result")
   filename = request.form.get("file")
   shape = request.form.get("shape")
   audio = googleTTS.textToSpeech(result,filename)
   pygame.mixer.init()
   pygame.mixer.music.load(audio)
   pygame.mixer.music.play()
   return render_template('Shapes.html', filename=shape, result=result)
