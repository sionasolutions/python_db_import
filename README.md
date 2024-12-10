
# MySQL Database Automation Script

This Python script automates the process of managing MySQL databases. It performs the following tasks:

1. **Checks if a specific database exists.**  
2. **Drops the database if it exists.**  
3. **Creates a new database with the desired collation.**  
4. **Imports a `.sql` file to the newly created database.**

The script is specifically configured to work with the **Laragon** MySQL setup on Windows but can be adjusted for other platforms such as Ubuntu.

---

## Prerequisites

1. **Python**: Ensure Python is installed on your system.
2. **MySQL Connector for Python**: Install it using:
   ```bash
   pip install mysql-connector-python
   ```
3. **MySQL**: Ensure MySQL is installed and properly configured.
4. **Laragon (Optional)**: If you're using Laragon, update the path to the MySQL executable in the script.

---

## Configuration

### 1. Update the MySQL Executable Path
Update the `mysql_command` variable with the correct path to your MySQL executable. For Laragon on Windows, it should look like this:
```python
mysql_command = r'C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe'
```

### 2. Define the Database Name
Set the desired database name in the script:
```python
db_name = 'your_database_name'
```

### 3. Place the `.sql` File
Ensure the `.sql` file (with the same name as the database) is in the same directory as the script:
```plaintext
|-- main.py
|-- your_database_name.sql
```

### 4. Set MySQL Connection Credentials
Update the `host`, `user`, and `password` variables with your MySQL credentials:
```python
host = 'localhost'
user = 'root'
password = 'your_password'
```

---

## Usage

### For Windows
Run the script using:
```bash
python.exe .\main.py
```

### For Ubuntu
Run the script using:
```bash
python main.py
```

---

## How It Works

1. **Database Check**  
   The script connects to the MySQL server and checks if the specified database already exists:
   ```sql
   SHOW DATABASES LIKE 'db_name';
   ```

2. **Drop Database**  
   If the database exists, it is dropped:
   ```sql
   DROP DATABASE db_name;
   ```

3. **Create Database**  
   A new database is created with `utf8_general_ci` collation:
   ```sql
   CREATE DATABASE db_name CHARACTER SET utf8 COLLATE utf8_general_ci;
   ```

4. **Import SQL File**  
   The `.sql` file is imported into the newly created database using a `subprocess` call to the MySQL command-line utility:
   ```bash
   mysql -h localhost -u root -p{password} db_name < db_name.sql
   ```

---

## Error Handling

The script handles common errors gracefully:
1. **MySQL Connection Errors**  
   If the script cannot connect to MySQL, it displays the error message.
   
2. **SQL Import Errors**  
   If the `.sql` file is missing or the import fails, the error is printed.

---

## Notes

- **Security**: Avoid hardcoding the password in production. Use environment variables or MySQL option files (`.my.cnf`) for better security.
- **Compatibility**: Tested on Windows with Laragon. Minor adjustments may be needed for other platforms.

---

## Example Output

```plaintext
Database 'db_name' already existed and was deleted.
Database 'db_name' created successfully with utf8_general_ci collation.
SQL file 'db_name.sql' imported into 'db_name' successfully.
```

---

## License

This script is open-source and available for use under the MIT License. Contributions are welcome! 😊

---
