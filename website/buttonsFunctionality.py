import mysql.connector
from flask import Flask, Blueprint, request
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
import importlib.util
from dotenv import load_dotenv
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import googleTTS

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


module_name = "ImageDetection"
#module_path = "GeoSenseAssist-Project/ImageDetection.py"  # Adjust as needed
module_path = os.path.join(os.path.dirname(__file__), "..", "ImageDetection.py")

spec = importlib.util.spec_from_file_location(module_name, module_path)
ImageDetection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ImageDetection)

app = Flask(__name__)

app.config['UPLOAD_DIRECTORY'] = 'uploads/'
parentFolder = 'GeoSenseAssist-Project/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB
upload_dir = os.path.join(parentFolder,app.config['UPLOAD_DIRECTORY'])
os.makedirs(upload_dir, exist_ok=True)
views = Blueprint('views', __name__)

def upload_shapes(education_level):

    image, file_path = accessFilePath()

    shape = ImageDetection.analyze_image_geometry(file_path, "Provide only the name this shape")
    numOfSides = ImageDetection.analyze_image_geometry(file_path, "Provide only the number of sides for this shape")
    numOfAngles = ImageDetection.analyze_image_geometry(file_path, "Provide only the number of interior angles for this shape")
    sizeOfAngles = ImageDetection.analyze_image_geometry(file_path, "Provide only the numerical values for the sizes of each of the interior angles")
    sizeOfSides = ImageDetection.analyze_image_geometry(file_path, "Provide only the numerical values for the sizes of each of the side lengths of the shape")
    analysis  = ImageDetection.analyze_image_geometry(file_path, "Analyze the geometry of the shape according to the education level of" + education_level + "within 999 characters.")

    print("acquired variables")

    table = 'shape_table'
    sql = f"INSERT INTO {table} (shape, num_of_Sides, num_of_Angles, size_of_Angles, size_lengths, overall_analysis) VALUES (%s,%s,%s,%s,%s, %s)"
    val = (shape,numOfSides,numOfAngles, sizeOfAngles, sizeOfSides, analysis)
    accessDatabase(sql, val)
    print("successfully added")

    return image, analysis

def upload_graph(education_level):
    
    image, file_path = accessFilePath()
    graph = ImageDetection.analyze_image_geometry(file_path, "Provide only what type of graph it is.")
    xAxis = ImageDetection.analyze_image_geometry(file_path, "Provide what the x-axis category is for the graph. If it isn't provided, simply respond Not Provided")
    yAxis = ImageDetection.analyze_image_geometry(file_path, "Provide what the y-axis category is for the graph. If it isn't provided, simply respond Not Provided")
    analysis  = ImageDetection.analyze_image_geometry(file_path, "Analyze the graph according to the education level of" + education_level + "within 999 characters.")
    print("acquired variables")
    table = 'graph_table'
    sql = f"INSERT INTO {table} (graph_type, x_axis, y_axis, overall_analysis) VALUES (%s,%s,%s,%s)"
    val = (graph, xAxis, yAxis, analysis)
  
    accessDatabase(sql, val)

    return image, analysis

    


def upload_equation(education_level):
    
    image, file_path = accessFilePath()
    equation = ImageDetection.analyze_image_geometry(file_path, "Provide only what kind of equation it is.")
    numOfTerms = ImageDetection.analyze_image_geometry(file_path, "Provide only the numerical value of the number of terms.")
    highest_deg = ImageDetection.analyze_image_geometry(file_path, "Provide only what the highest degree is for the equation.")
    analysis = ImageDetection.analyze_image_geometry(file_path, "Analyze the equation according to the education level of" + education_level + "within 999 characters.")
    print("acquired variables")
    table = 'equation_table'

    sql = f"INSERT INTO {table} (equation_type, num_of_terms, highest_Degree, overall_analysis) VALUES (%s,%s,%s,%s)"
    val = (equation,numOfTerms, highest_deg, analysis)
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