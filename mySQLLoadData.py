import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5L%0me0)s5",
    database="mydatabase"
)

data = []

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM customers")

for x in mycursor:
    data.append(x)

for x in data:
    print(x)
