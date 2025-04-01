import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
#dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv()

# Get database credentials from environment variables
HOST_NAME = os.getenv("HOST_NAME")
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

try:
    # First connection to create database if it doesn't exist
    conn = mysql.connector.connect(
        host=HOST_NAME,
        user = USER_NAME,
        password = USER_PASSWORD
    )
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    print(f"Database '{DATABASE_NAME}' created or already exists.")
    
    # Close initial connection
    cursor.close()
    conn.close()
    
    # Connect to the specific database
    conn = mysql.connector.connect(
        host=HOST_NAME,
        user = USER_NAME,
        password = USER_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = conn.cursor()
    
    # Begin transaction
    cursor.execute("START TRANSACTION")
    
    # Create shape_table if it doesn't exist
    shape_tb = "shape_table"
    cursor.execute(f"SHOW TABLES LIKE '{shape_tb}'")
    result = cursor.fetchone()
    
    if not result:
        create_table_query = f"""
        CREATE TABLE {shape_tb} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            shape VARCHAR(255) NOT NULL,
            num_of_Sides VARCHAR(255),
            num_of_Angles VARCHAR(255),
            size_of_Angles VARCHAR(255),
            size_lengths VARCHAR(255),
            overall_Analysis VARCHAR(1000),
            link VARCHAR(1000)
        );
        """
        cursor.execute(create_table_query)
        print(f"Table '{shape_tb}' was created successfully.")
    else:
        print(f"Table '{shape_tb}' already exists.")
    
    # Create equation_table if it doesn't exist
    equation_tb = "equation_table"
    cursor.execute(f"SHOW TABLES LIKE '{equation_tb}'")
    result = cursor.fetchone()
    
    if not result:
        create_table_query = f"""
        CREATE TABLE {equation_tb} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            equation_type VARCHAR(255) NOT NULL,
            num_of_Terms VARCHAR(255),
            highest_Degree VARCHAR(255),
            size_of_Angles VARCHAR(255),
            size_lengths VARCHAR(255),
            overall_Analysis VARCHAR(1000),
            link VARCHAR(1000)
        );
        """
        cursor.execute(create_table_query)
        print(f"Table '{equation_tb}' was created successfully.")
    else:
        print(f"Table '{equation_tb}' already exists.")
    
    # Create graph_table if it doesn't exist
    graph_tb = "graph_table"
    cursor.execute(f"SHOW TABLES LIKE '{graph_tb}'")
    result = cursor.fetchone()
    
    if not result:
        create_table_query = f"""
        CREATE TABLE {graph_tb} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            graph_type VARCHAR(255) NOT NULL,
            x_axis VARCHAR(255),
            y_axis VARCHAR(255),
            overall_Analysis VARCHAR(1000),
            link VARCHAR(1000)
        );
        """
        cursor.execute(create_table_query)
        print(f"Table '{graph_tb}' was created successfully.")
    else:
        print(f"Table '{graph_tb}' already exists.")
    
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