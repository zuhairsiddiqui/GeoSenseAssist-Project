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
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Your local IP: {local_ip}")



# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Get API key safely
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is missing. Ensure you have a .env file and it's correctly loaded.")


genai.configure(api_key=api_key)




app = create_app()
if __name__ == '__main__':
    import socket
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"Access the app at: http://{local_ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)




app.config['UPLOAD_DIRECTORY'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

os.makedirs(app.config['UPLOAD_DIRECTORY'], exist_ok=True)

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

if __name__ == '__main__':
    app.run(debug=True)


