import sqlite3

DATABASE_FILE = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/quake_cds.db"

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()



# Create File_URL table
cursor.execute('''
CREATE TABLE IF NOT EXISTS File_URL (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_url TEXT NOT NULL UNIQUE
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database schema created and processing methods inserted successfully.")
