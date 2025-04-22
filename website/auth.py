from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash # for hashing passwords: https://werkzeug.palletsprojects.com/en/stable/utils/
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Grab DB credentials from .env
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = os.getenv("MYSQLPORT")

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login Page</p>"

@auth.route('/logout')
def logout():
    return "<p>Logout Page</p>"

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data when user presses submit
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')


        # simple check for same password
        if password != confirm_password:
            return redirect(url_for('auth.signup'))
        
        # hash the password once those 2 match
        hashed_password = generate_password_hash(password)

        # Connect to MySQL
        conn = mysql.connector.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQLPORT
        )
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users_table WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return redirect(url_for('auth.signup'))

        # Insert new user
        cursor.execute(
            "INSERT INTO users_table (email, password) VALUES (%s, %s)",
            (email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('views.home'))

    return render_template("signup.html")
