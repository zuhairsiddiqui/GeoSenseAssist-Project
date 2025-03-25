import mysql.connector
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HOST_NAME = os.getenv("HOST_NAME")
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

mydb = mysql.connector.connect(
        host=HOST_NAME,
        user = USER_NAME,
        password = USER_PASSWORD,
        database=DATABASE_NAME
    )

cursor = mydb.cursor()

# Fetch data from table
cursor.execute("SELECT * FROM entry")

# Get all rows
rows = cursor.fetchall()

# Display data
for row in rows:
    print(row)
# Close connection
cursor.close()
mydb.close()
