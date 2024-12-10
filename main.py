import mysql.connector
import os
import subprocess

# Define the MySQL command path for Laragon on Windows
mysql_command = r'C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe'  # Update this path if necessary

# Step 1 : Define the database name
db_name = 'db_name'
#Step 2 : Put .sql file in same directory
sql_file = f'{db_name}.sql'  # Assuming the SQL file is named after the database
#Step 3 : (Windows: python.exe .\main.py) (Ubuntu: python main.py)

# MySQL connection parameters
host = 'localhost'
user = 'root'
password = 'root'  # Set this to your actual MySQL password

# Using option 1: .my.cnf option file (create this file with secure permissions in your user directory)
# Uncomment the following line to use the option file:
# mysql_command = f'"{mysql_command}" --defaults-file=~/.my.cnf {db_name} < "{sql_file}"'

# Option 2: Using environment variables for password
# Uncomment and set the environment variable like this:
# os.environ['MYSQL_PWD'] = password

try:
    # Connect to MySQL to manage the database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    database_exists = cursor.fetchone()

    if database_exists:
        # Drop the database if it exists
        cursor.execute(f"DROP DATABASE {db_name}")
        print(f"Database '{db_name}' already existed and was deleted.")

    # Create the database with utf8_general_ci collation
    cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8 COLLATE utf8_general_ci")
    print(f"Database '{db_name}' created successfully with utf8_general_ci collation.")

    # Close the connection to avoid locking issues
    cursor.close()
    conn.close()

    # Import the SQL file into the database
    if os.path.exists(sql_file):
        # If using environment variables, use the command below without password in the command line
        # command = f'"{mysql_command}" -h {host} -u {user} {db_name} < "{sql_file}"'

        # If not using environment variables or option files, use this command format
        command = f'"{mysql_command}" -h {host} -u {user} -p{password} {db_name} < "{sql_file}"'
        
        # Running the command with subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"SQL file '{sql_file}' imported into '{db_name}' successfully.")
        else:
            print(f"Error during SQL import: {result.stderr}")
    else:
        print(f"SQL file '{sql_file}' not found in the current directory.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as err:
    print(f"Unexpected error: {err}")
