import mysql.connector
from flask import Flask, render_template, request, redirect, Blueprint
import numpy as np
import random
from datetime import datetime
from dotenv import load_dotenv
import ImageDetection 
import google.generativeai as genai
from website import create_app
import os




# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Get API key safely
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is missing. Ensure you have a .env file and it's correctly loaded.")


genai.configure(api_key=api_key)


app = create_app()
app.config['UPLOAD_DIRECTORY'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

os.makedirs(app.config['UPLOAD_DIRECTORY'], exist_ok=True)

conn = mysql.connector.connect(
        host="localhost",
        user="zuhair",
        password="siddiqui",
        database="GeoSenseDB"
    )

# @app.route('/')
# def index():
#  #   data = np.arange(1,11)
# #    random_number = random.randint(1,100)
#     return render_template('website.html')  # Renders the HTML form


# @app.route('/submit', methods=['POST'])
# def submit():

#     # print("before acquiring")
#     # shape = request.form['image']
#     # image = ImageDetection.analyze_image_geometry(shape)
#     # date_time = datetime.now()
#     # print("acquired variables")

#     # cursor = conn.cursor()
#     # sql = "INSERT INTO entry (shape, date) VALUES (%s,%s)"
#     # val = (image,date_time)
#     # cursor.execute(sql, val)
#     # conn.commit()

#     # print("successfully added")
#     pass
#     # return redirect('/')

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
        
#         print("before acquiring")
        
#         if 'fileUpload' not in request.files:
#           return "No file part", 400
    
#         file = request.files['fileUpload']

#         if file.filename == '':
#           return "No selected file", 400

#         if file:
#             file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], secure_filename(file.filename)))          


#         # uploads_folder = Path("uploads")
#         # file_name = "example.txt"  # Change to the file you want
#         file_path = file  # Create the full path
        

#         if file_path.exists():
#           print("File found:", file_path.resolve())
#         else:
#           print("File not found.")


#         shape = file_path
#         image = ImageDetection.analyze_image_geometry(shape)
#         date_time = datetime.now()
#         print("acquired variables")

#         cursor = conn.cursor()
#         sql = "INSERT INTO entry (shape, date) VALUES (%s,%s)"
#         val = (image,date_time)
#         cursor.execute(sql, val)
#         conn.commit()

#         print("successfully added")
          
#     except RequestEntityTooLarge:
#         return "File is larger than the 16 MB Limit"

#     return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)


