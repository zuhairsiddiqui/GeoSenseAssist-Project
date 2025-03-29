from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
import importlib.util
from . import buttonsFunctionality
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

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
  return render_template("website.html")

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

@views.route('/upload_shapes', methods=['POST'])
def upload_shapes():
    shape, analysis = buttonsFunctionality.upload_shapes("of a 9th - 12th grader")
    return render_template('Shapes.html', filename=shape, result=analysis)

@views.route('/upload_graphs', methods=['POST'])
def upload_graphs():
  graph, analysis = buttonsFunctionality.upload_graph("of a 9th - 12th grader")
  return render_template('graphs.html', filename=graph, result=analysis)

@views.route('/upload_equations', methods=['POST'])
def upload_equation():
  equation, analysis = buttonsFunctionality.upload_equation("of a 9th - 12th grader")
  return render_template('equations.html', filename=equation, result=analysis)

