import mysql.connector
from datetime import datetime
from flask import Flask, Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
import importlib.util



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



conn = mysql.connector.connect(
        host="localhost",
        user = "app_user",
        password = "P@ssw0rd$124!",
        database="GeoSenseDB"
    )



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

@views.route('/upload', methods=['POST'])
def upload():
    print("before acquiring")
    try:
        file = request.files['fileUpload']
        print(upload_dir)
        if file:
            #upload_directory = app.config['UPLOAD_DIRECTORY']
            # filename = secure_filename(file.filename)
            # full_path = os.path.join(upload_directory, filename)
            full_path = os.path.join(upload_dir, secure_filename(file.filename))
            file.save(full_path)
            
    except RequestEntityTooLarge:
        return "File is larger than the 16 MB Limit"

    shape = file.filename
    print("shape:", shape)
    print("full_path:", full_path)
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get current script directory
    file_path = os.path.abspath(full_path)
    print("file_path", file_path)

    command = "Provide only the name this shape"

    image = ImageDetection.analyze_image_geometry(file_path, command)

    command = "Analyze the geometry of the image"
    analysis  = ImageDetection.analyze_image_geometry(file_path, command)
    print("image:", image)
    date_time = datetime.now()
    print("acquired variables")

    cursor = conn.cursor()
    sql = "INSERT INTO entry (shape, date, overall_analysis) VALUES (%s,%s,%s)"
    val = (image,date_time, analysis)
    cursor.execute(sql, val)
    conn.commit()

    print("successfully added")

    return redirect('/')
