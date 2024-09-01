import sqlite3

DATABASE = '../data/quake_website.db'

def connect_read_only(db_path):
    """Connect to the SQLite database in read-only mode."""
    uri = f'file:{db_path}?mode=ro'
    return sqlite3.connect(uri, uri=True)

def list_all_file_urls():
    # Connect to the SQLite database
    conn = connect_read_only(DATABASE)
    cursor = conn.cursor()

    # Query to list all file URLs
    cursor.execute('SELECT file_url FROM File_URL ORDER BY file_url ASC')

    file_urls = cursor.fetchall()

    # Print the results
    print("All File URLs:")
    for file_url in file_urls:
        print(file_url[0])

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    list_all_file_urls()
