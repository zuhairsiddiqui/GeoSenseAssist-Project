import mysql.connector


# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="zuhair",
    password="siddiqui",
    database="GeoSensedb"
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
