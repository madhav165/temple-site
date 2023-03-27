import csv
import sqlite3

def insert_data_from_csv_to_sqlite3_table():
    # Connect to SQLite3 database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS states;
    ''')

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS states (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        state TEXT,
                        url TEXT
                    )''')

    # Open CSV file and read data
    with open('states.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            # Insert data into table
            cursor.execute('''INSERT INTO states (
                                state,
                                url
                            )
                            VALUES (?, ?)''', row)

    # Commit changes and close connection
    conn.commit()
    conn.close()

insert_data_from_csv_to_sqlite3_table()