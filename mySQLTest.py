import mysql.connector

def connect_to_mysql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="5L%0me0)s5",
            database="mydatabase"
        )
        if mydb.is_connected():
            print("Connected to MySQL Database")
            return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
        

#mycursor = mydb.cursor()

#mycursor.execute("SHOW DATABASES")

#mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

#mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

#mycursor.execute("SHOW TABLES")

#for x in mycursor:
#    print(x)

#sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"

#val = [
#    ("John", "Highway 21"),
#    ("Peter", "Apple st 652"),
#    ("Hannah", "Sky st 98"),
#]

#mycursor.executemany(sql, val)

#mydb.commit()

#print(mycursor.rowcount, "were inserted.")

#mycursor.execute("SELECT * FROM customers")

#mycursor.execute("SELECT name, address FROM customers")

#myresult = mycursor.fetchall()

#for x in myresult:
#    print(x)

