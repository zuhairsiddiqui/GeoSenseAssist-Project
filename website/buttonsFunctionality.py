import mysql.connector
from flask import Flask, Blueprint, request
import requests
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
import importlib.util
from dotenv import load_dotenv
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


cloudinary.config( 
    cloud_name = os.getenv("CLOUD_NAME"), 
    api_key = os.getenv("IMAGE_API"), 
    api_secret = os.getenv("IMAGE_SECRET")
)




 ##Get the username from applying the code from chatgpt onto one of the html files
 ##go through each function and change it to hold the values for the new table
 ##Whenever a user makes a new entry, use sql commands to count how many entries there are, if there are more than 10, delete them
module_name = "ImageDetection"
#module_path = "GeoSenseAssist-Project/ImageDetection.py"  # Adjust as needed
module_path = os.path.join(os.path.dirname(__file__), "..", "ImageDetection.py")

spec = importlib.util.spec_from_file_location(module_name, module_path)
ImageDetection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ImageDetection)

app = Flask(__name__)

app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB
upload_dir = os.path.join('uploads')
os.makedirs(upload_dir, exist_ok=True)
views = Blueprint('views', __name__)


primKey = None
def setPrimaryKey(pKey):
    global primKey 
    primKey = pKey

def getPrimaryKey():
    return primKey

def upload_shapes(education_level):
    primary_key = getPrimaryKey()
    print(primary_key)
    image, file_path = accessFilePath()
    URL = upload_image_to_cloudinary(file_path)
    analysis_type = ImageDetection.analyze_image_geometry(file_path, "Provide what type of analysis it is (Shape, Graph, or Equation) (One Word)")
    analysis  = ImageDetection.analyze_image_geometry(file_path, "Analyze the geometry of the shape according to the education level of" + education_level + "within 999 characters. Keep in mind the user is blind, keep responses to a minimal, only facts.")

    print("acquired variables")

    table = 'history_table'
    sql = f"INSERT INTO {table} (email, analysis_type, analysis,image_url) VALUES (%s, %s, %s, %s)"
    val = (primary_key, analysis_type, analysis, URL)
    accessDatabase(sql, val)
    print("successfully added")

    return image, analysis

def upload_graph(education_level):
    primary_key = getPrimaryKey()
    print(primary_key)
    image, file_path = accessFilePath()
    URL = upload_image_to_cloudinary(file_path)
    graph = ImageDetection.analyze_image_geometry(file_path, "Provide what type of analysis it is (Shape, Graph, or Equation) (One Word)")
    analysis  = ImageDetection.analyze_image_geometry(file_path, "Analyze the graph according to the education level of" + education_level + "within 999 characters. Keep in mind the user is blind, keep responses to a minimal, only facts.")
    print("acquired variables")
    table = 'history_table'
    sql = f"INSERT INTO {table} (email, analysis_type, analysis,image_url) VALUES (%s, %s,%s, %s)"
    val = (primary_key, graph, analysis, URL)
  
    accessDatabase(sql, val)

    return image, analysis

    


def upload_equation(education_level):
    primary_key = getPrimaryKey()
    print(primary_key)
    image, file_path = accessFilePath()
    URL = upload_image_to_cloudinary(file_path)
    analysis_type = ImageDetection.analyze_image_geometry(file_path, "Provide what type of analysis it is (Shape, Graph, or Equation) (One Word)")
    analysis = ImageDetection.analyze_image_geometry(file_path, "Analyze the equation according to the education level of" + education_level + "within 999 characters. Keep in mind the user is blind, keep responses to a minimal, only facts.")
    print("acquired variables")
    table = 'history_table'

    sql = f"INSERT INTO {table} (email, analysis_type, analysis,image_url) VALUES (%s, %s,%s, %s)"
    val = (primary_key, analysis_type, analysis, URL)
    accessDatabase(sql, val)

    print("successfully added")
    
    return image, analysis


def accessFilePath():
    print("before acquiring")
    try:
        file = request.files['fileUpload']
        print(upload_dir)
        if file:
            full_path = os.path.join(upload_dir, secure_filename(file.filename))
            file.save(full_path)
            
    except RequestEntityTooLarge:
        return "File is larger than the 16 MB Limit"

    image = file.filename
    print("image:", image)
    print("full_path:", full_path)
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get current script directory
    file_path = os.path.abspath(full_path)
    print("file_path", file_path)

    return image, file_path

def accessDatabase(sql,val):
    
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
    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    print("successfully added")

def upload_image_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(image_path)
        print(response['secure_url'])
        return response['secure_url']  # This is the image URL you can use in HTML
    except Exception as e:
        print("Upload failed:", e)
        return None
