import sqlite3

DATABASE_FILE = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/quake_cds.db"

QUAKE_CD_FILES = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/quake_addon_cds_files.txt"


def load_urls_to_db(txt_file, db_name):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print(f'Connected to {db_name}')
    
    # Read URLs from the text file
    with open(txt_file, 'r') as file:
        urls = file.readlines()
    print(f'Read {len(urls)} lines from {txt_file}')
    
    # Insert URLs into the database, handling duplicates
    for url in urls:
        url = url.strip()  # Remove any extra whitespace/newlines
        if url:  # Avoid inserting empty lines
            try:
                cursor.execute("INSERT OR IGNORE INTO File_URL (file_url) VALUES (?)", (url,))
            except sqlite3.Error as e:
                print(f"Error inserting {url}: {e}")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Done.")

# entry
if __name__ == '__main__':
    # Example usage:
    load_urls_to_db(QUAKE_CD_FILES, DATABASE_FILE)
