import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

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
mydb.close()
