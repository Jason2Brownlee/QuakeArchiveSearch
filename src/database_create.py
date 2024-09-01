import sqlite3

DATABASE = '../data/quake_website.db'

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create Quake_Website table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Quake_Website (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_url TEXT NOT NULL UNIQUE,
    original_url TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create Processing_Method table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Processing_Method (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_name TEXT NOT NULL,
    description TEXT
)
''')

# Create Website_Processing_Status table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Website_Processing_Status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quake_website_id INTEGER NOT NULL,
    processing_method_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    last_processed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(quake_website_id, processing_method_id),
    FOREIGN KEY(quake_website_id) REFERENCES Quake_Website(id),
    FOREIGN KEY(processing_method_id) REFERENCES Processing_Method(id)
)
''')

# Create File_URL table
cursor.execute('''
CREATE TABLE IF NOT EXISTS File_URL (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_url TEXT NOT NULL UNIQUE
)
''')

# Create File_Source table (optional)
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS File_Source (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     file_url_id INTEGER NOT NULL,
#     processing_method_id INTEGER NOT NULL,
#     FOREIGN KEY(file_url_id) REFERENCES File_URL(id),
#     FOREIGN KEY(processing_method_id) REFERENCES Processing_Method(id)
# )
# ''')

# Insert some processing methods into Processing_Method table
cursor.execute('''
INSERT INTO Processing_Method (method_name, description) 
VALUES 
('archive.org wayback machine list', 'Query archive.org to get a list of unique URLs that were archived'),
('archive.org wayback machine crawl', 'Download archived files and crawl them for file links'),
('live site crawl', 'Download the current version of the site and crawl all links')
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database schema created and processing methods inserted successfully.")
