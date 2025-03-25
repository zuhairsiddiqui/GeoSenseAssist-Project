import mysql.connector


# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="aap0259",
    password="Ap4699992142",
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
