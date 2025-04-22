import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
#dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv()

# Get database credentials from environment variables
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = os.getenv("MYSQLPORT")


try:
    # First connection to create database if it doesn't exist
    conn = mysql.connector.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQLPORT
    )

    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
    print(f"Database '{MYSQL_DATABASE}' created or already exists.")
    
    # Close initial connection
    cursor.close()
    conn.close()
    
    # Connect to the specific database
    conn = mysql.connector.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQLPORT
    )

    cursor = conn.cursor()
    
    # Begin transaction
    cursor.execute("START TRANSACTION")


    # Create users_table if it doesn't exist
    users_tb = "users_table"
    cursor.execute(f"SHOW TABLES LIKE '{users_tb}'")
    result = cursor.fetchone()


    if not result:
        create_table_query = f"""
        CREATE TABLE {users_tb} (
            email VARCHAR(255)  PRIMARY KEY, 
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        print(f"Table '{users_tb}' was created successfully.")
    else:
        print(f"Table '{users_tb}' already exists.")


    # Create shape_table if it doesn't exist
    history_tb = "history_table"
    cursor.execute(f"SHOW TABLES LIKE '{history_tb}'") 
    result = cursor.fetchone()

    # Need users table to be created before this one, as this one tries to link to users_table(email), and when thats not there it breaks.
    # https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html 
    if not result:
        create_table_query = f"""
            CREATE TABLE {history_tb} (

            email VARCHAR(255), -- email of user, will be used to link with users table so each persons history is different
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- when was the analysis made? so we can delete oldest after we have 5
            analysis_type VARCHAR(255), -- type: graph, shape, or equation
            analysis VARCHAR(1000), -- the general description of the image
            image_url VARCHAR(1000), -- the url of the image, storing it with imgur so we dont have to waste DB storage
            -- links it to the other table, delete the history of the user if that user is deleted from the table as well
            FOREIGN KEY (email) REFERENCES users_table(email) ON DELETE CASCADE 
            );
        """
        cursor.execute(create_table_query)
        print(f"Table '{history_tb}' was created successfully.")
    else:
        print(f"Table '{history_tb}' already exists.")
    
    
    
    # Commit all changes
    cursor.execute("COMMIT")
    print("Database and tables created successfully!")


except mysql.connector.Error as e:
    if conn.is_connected():
        cursor.execute("ROLLBACK")  # Undo all queries if any fail
    print(f"MySQL Error: {e}")

except Exception as e:
    if 'conn' in locals() and conn.is_connected():
        cursor.execute("ROLLBACK")
    print(f"General Error: {e}")

finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn and conn.is_connected():
        conn.close()
        print("MySQL connection closed.")


