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
import time
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

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
    URL = upload_to_imgur(file_path)
    analysis_type = ImageDetection.analyze_image_geometry(file_path, "Provide only the name this shape")
    analysis  = ImageDetection.analyze_image_geometry(file_path, "Analyze the geometry of the shape according to the education level of" + education_level + "within 999 characters.")

    print("acquired variables")

    table = 'history_table'
    sql = f"INSERT INTO {table} (email, analysis_type, analysis,image_url) VALUES (%s, %s,%s, %s)"
    val = (primary_key, analysis_type, analysis, URL)
    accessDatabase(sql, val)
    print("successfully added")

    return image, analysis

def upload_graph(education_level):
    primary_key = getPrimaryKey()
    print(primary_key)
    image, file_path = accessFilePath()
    URL = upload_to_imgur(file_path)
    graph = ImageDetection.analyze_image_geometry(file_path, "Provide only what type of graph it is.")
    analysis  = ImageDetection.analyze_image_geometry(file_path, "Analyze the graph according to the education level of" + education_level + "within 999 characters.")
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
    URL = upload_to_imgur(file_path)
    analysis_type = ImageDetection.analyze_image_geometry(file_path, "Provide only what kind of equation it is.")
    analysis = ImageDetection.analyze_image_geometry(file_path, "Analyze the equation according to the education level of" + education_level + "within 999 characters.")
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


def upload_to_imgur(image_path, max_retries=5):
    CLIENT_ID = os.getenv("CLIENT_ID")
    headers = {'Authorization': f'Client-ID {CLIENT_ID}'}

    for attempt in range(max_retries):
        with open(image_path, 'rb') as file:
            response = requests.post(
                'https://api.imgur.com/3/image',
                headers=headers,
                files={'image': file}
            )

        if response.status_code == 200:
            data = response.json()
            print(data['data']['link'])
            return data['data']['link']

        elif response.status_code == 429:
            print("Rate limited by Imgur (429). Retrying...")

            retry_after = response.headers.get("Retry-After")
            if retry_after:
                sleep_time = int(retry_after)
            else:
                sleep_time = 2 ** attempt  # exponential backoff

            print(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)

        else:
            print(f"Upload failed (status {response.status_code}): {response.text}")
            return None

    print("Max retries exceeded.")
    return None
