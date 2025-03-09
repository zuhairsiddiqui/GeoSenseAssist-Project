import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "zuhair",
    password = "siddiqui"
)


cursor = conn.cursor()
# Create database if it doesn't exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS GeoSensedb")
print("Database created successfully.")

cursor.close()

conn = mysql.connector.connect(
    host="localhost",
    user="zuhair",
    password="siddiqui",
    database="GeoSensedb"
)
cursor = conn.cursor()

# Create a users table
# cursor.execute("""
#     CREATE TABLE entry (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         date VARCHAR(100),
#         shape VARCHAR(100)
#     )
# """)

print("Database and table created successfully!")


# Close connection
cursor.close()
conn.close()


# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="zuhair",
    password="siddiqui",
    database="GeoSensedb"
)

cursor = conn.cursor()

# Table and column details
table_name = "entry"
column_name = "date"

# Check if the column exists
cursor.execute(f"""
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}' 
    AND COLUMN_NAME = '{column_name}' 
    AND TABLE_SCHEMA = DATABASE()
""")

column_exists = cursor.fetchone()[0]

if column_exists == 0:
    # If column does not exist, add it
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(255)")
    conn.commit()
    print(f"Column '{column_name}' added successfully!")
else:
    print(f"Column '{column_name}' already exists.")

# Close connection
cursor.close()
conn.close()

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="zuhair",
    password="siddiqui",
    database="GeoSensedb"
)

cursor = conn.cursor()

sql = "ALTER TABLE entry MODIFY COLUMN shape VARCHAR(255)"
try:
    cursor.execute(sql)
    conn.commit()  # Save changes
    print("Column 'shape' size increased successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()