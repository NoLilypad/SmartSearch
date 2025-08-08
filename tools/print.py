import sqlite3
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pages.db')

def print_titles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute('SELECT title FROM pages'):
        print(row[0])
    conn.close()

if __name__ == "__main__":
    print_titles()
