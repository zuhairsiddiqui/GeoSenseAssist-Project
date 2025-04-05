import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

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

# Fetch data from table
cursor.execute("SELECT * FROM equation_table")

# Get all rows
rows = cursor.fetchall()

# Display data
for row in rows:
    print(row)

print("--------------------------------------------------------------------------")

# Fetch data from table
cursor.execute("SELECT * FROM shape_table")

# Get all rows
rows = cursor.fetchall()

# Display data
for row in rows:
    print(row)

print("----------------------------------------------------------------------------")

# Fetch data from table
cursor.execute("SELECT * FROM graph_table")

# Get all rows
rows = cursor.fetchall()

# Display data
for row in rows:
    print(row)


# Close connection
cursor.close()
