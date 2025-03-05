import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql123",
  database="mydatabase"
)

mycursor = mydb.cursor()
sql = "UPDATE login SET password = 'NewPassword12' WHERE username = 'Tanvi12'"

mycursor.execute(sql)
mydb.commit()

#Check if the table get updated in mysql
#select * from mydatabase.login;

#mycursor.executemany(sql,values)
#mydb.commit()
mycursor.execute("SELECT * FROM login")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)
