import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql123",
  database="mydatabase"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")

#mycursor.execute("CREATE TABLE login (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100), password VARCHAR(100))")

#Check if the table got created in mysql
#select * from mydatabase.login;

#sql = "INSERT INTO login (username, password) VALUES (%s,%s)"
#values = [
#    ('Tanvi12', 'Winter12'),
#    ('Bob1$', 'Schhol1$'),
#    ('mk10', 'Birthdaycake41')
#]

#Check if the table get updated in mysql
#select * from mydatabase.login;

#mycursor.executemany(sql,values)
#mydb.commit()
mycursor.execute("SELECT * FROM login")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)
