# .gitignore file to ignore the app.db file which is the SQLite database used in the project

import sqlite3
from pathlib import Path

# database path to deploy the db to the backend folder
DB_PATH = Path(__file__).parent / "app.db"

# funcction to connect to the database 
# creates a connection to the SQLite database using the specified path
# sets the row factory to sqlite3.Row to allow accessing columns by name
def get_connection():
    db_connection = sqlite3.connect(DB_PATH)
    db_connection.row_factory = sqlite3.Row
    return db_connection

# function to create the modules table if it doesn't exist
# calls the get_connection function to connect to the database
# executes the SQL command to create the table with the specified columns and data types
# commits the changes and closes the connection
def create_table():
    table_conn = get_connection()
    cursor = table_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_name TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            term_or_semester TEXT NOT NULL,
            study_type TEXT NOT NULL,
            start_date DATE NOT NULL, 
            end_date DATE NOT NULL,
            chart_colour TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
    ''')
    table_conn.commit()
    table_conn.close()

create_table()

