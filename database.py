import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "app_user",
    password = "P@ssw0rd$124!"
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
    
    conn = mysql.connector.connect(
        host = "localhost",
        user = "app_user",
        password = "P@ssw0rd$124!",
        database ="GeoSensedb"
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



# Create a users table
# cursor.execute("""
#     CREATE TABLE entry (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         date VARCHAR(100),
#         shape VARCHAR(100)
#     )
# """)






# cursor = conn.cursor()

# # Table and column details
# table_name = "entry"
# column_name = "date"

# # Check if the column exists
# cursor.execute(f"""
#     SELECT COUNT(*) 
#     FROM INFORMATION_SCHEMA.COLUMNS 
#     WHERE TABLE_NAME = '{table_name}' 
#     AND COLUMN_NAME = '{column_name}' 
#     AND TABLE_SCHEMA = DATABASE()
# """)

# column_exists = cursor.fetchone()[0]

# if column_exists == 0:
#     # If column does not exist, add it
#     cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(255)")
#     conn.commit()
#     print(f"Column '{column_name}' added successfully!")
# else:
#     print(f"Column '{column_name}' already exists.")

# cursor = conn.cursor()

# sql = "ALTER TABLE entry MODIFY COLUMN shape VARCHAR(255)"
# try:
#     cursor.execute(sql)
#     conn.commit()  # Save changes
#     print("Column 'shape' size increased successfully!")
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
# finally:
#     cursor.close()
#     conn.close()