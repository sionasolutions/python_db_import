import sys
import mysql.connector
import os
import subprocess

# MySQL command is typically just 'mysql' if it's in your PATH on macOS
mysql_command = 'mysql'

# Database connection parameters
host = 'localhost'
user = 'root'
# It is recommended to use environment variables for sensitive data like passwords
password = os.getenv('MYSQL_PASSWORD', 'root')  # Default to 'root' if not set

# Get table names from command-line arguments
table_names = sys.argv[1:]  # The script name is excluded

if not table_names:
    print("Error: No table names provided. Please specify at least one table name.")
    sys.exit(1)

# Establish a connection to the MySQL database
try:
    conn = mysql.connector.connect(host=host, user=user, password=password)
    cursor = conn.cursor()

    # Check and drop only the specified tables
    for table_name in table_names:
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if cursor.fetchone():
            cursor.execute(f"DROP TABLE {table_name}")
            print(f"Table '{table_name}' successfully dropped.")
        else:
            print(f"Warning: Table '{table_name}' does not exist.")

    # Reimport the specified tables
    for table_name in table_names:
        sql_file = f"{table_name}.sql"
        if os.path.exists(sql_file):
            # Using subprocess to run MySQL command to import the SQL file
            command = f'{mysql_command} -h {host} -u {user} --password="{password}" < "{sql_file}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"SQL file '{sql_file}' imported successfully for table '{table_name}'.")
            else:
                print(f"Error during SQL import for '{table_name}': {result.stderr}")
        else:
            print(f"Error: SQL file '{sql_file}' not found for table '{table_name}'.")

except mysql.connector.Error as err:
    print(f"MySQL error: {err}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Ensure the MySQL connection is closed properly
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed.")

