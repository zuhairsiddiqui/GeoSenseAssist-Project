import mysql.connector
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HOST_NAME = os.getenv("HOST_NAME")
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

conn = mysql.connector.connect(
        host=HOST_NAME,
        user = USER_NAME,
        password = USER_PASSWORD,
        database=DATABASE_NAME
    )


cursor = conn.cursor()
# Create database if it doesn't exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS GeoSensedb")
print("Database created successfully.")
if cursor:
    cursor.close()
if conn:
    conn.close()

try:
    
    HOST_NAME = os.getenv("HOST_NAME")
    USER_NAME = os.getenv("USER_NAME")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    conn = mysql.connector.connect(
        host=HOST_NAME,
        user = USER_NAME,
        password = USER_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = conn.cursor()

    cursor.execute("START TRANSACTION;")
    # Table name to check
    print("line 19")
    shape_tb = "shape_table"

    # Query to check if the table exists
    cursor.execute(f"SHOW TABLES LIKE '{shape_tb}'")
    result = cursor.fetchone()

    # If the table doesn't exist, create it
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
########################################################################################
    print("line 47")
    # Table name to check
    equation_tb = "equation_table"

    # Query to check if the table exists
    cursor.execute(f"SHOW TABLES LIKE '{equation_tb}'")
    result = cursor.fetchone()

    # If the table doesn't exist, create it
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
#################################################################################
    print("line 76")
    # Table name to check
    graph_tb = "graph_table"

    # Query to check if the table exists
    cursor.execute(f"SHOW TABLES LIKE '{graph_tb}'")
    result = cursor.fetchone()

    # If the table doesn't exist, create it
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
###################################################################################
    print("line 103")
    # Column check query
    column_name = "overall_analysis"
    table_name = "entry"

    check_column_query = """
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = %s AND COLUMN_NAME = %s AND TABLE_SCHEMA = DATABASE();
    """

    cursor.execute(check_column_query, (table_name, column_name))
    column_exists = cursor.fetchone()[0]  # Fetch the count result

    if column_exists:
        print(f"Column '{column_name}' already exists in table '{table_name}'.")
    else:
        print(f"Column '{column_name}' does not exist. Adding it now...")
        column_data_type = "VARCHAR(1000)"
        # SQL query to add a new column
        alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_data_type};"
        cursor.execute(alter_query)
        print(f"Column '{column_name}' added successfully!")
######################################################################################
    print("line 127")
    # Column check query
    column_name = "link"
    table_name = "entry"

    check_column_query = """
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = %s AND COLUMN_NAME = %s AND TABLE_SCHEMA = DATABASE();
    """

    cursor.execute(check_column_query, (table_name, column_name))
    column_exists = cursor.fetchone()[0]  # Fetch the count result

    if column_exists:
        print(f"Column '{column_name}' already exists in table '{table_name}'.")
    else:
        print(f"Column '{column_name}' does not exist. Adding it now...")
        column_data_type = "VARCHAR(1000)"
        # SQL query to add a new column
        alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_data_type};"
        cursor.execute(alter_query)
        print(f"Column '{column_name}' added successfully!")
#######################################################################################
    cursor.execute("COMMIT;")
    print("Database and tables created successfully!")
except mysql.connector.Error as e:
    cursor.execute("ROLLBACK;")  # Undo all queries if any fail
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()

