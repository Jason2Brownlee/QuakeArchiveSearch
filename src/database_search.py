import sqlite3

DATABASE = '../data/quake_website.db'

def connect_read_only(db_path):
    """Connect to the SQLite database in read-only mode."""
    uri = f'file:{db_path}?mode=ro'
    return sqlite3.connect(uri, uri=True)

def search_urls_endswith(cursor, search_term):
    """Search for file URLs that end with the given search term."""
    cursor.execute('SELECT file_url FROM File_URL WHERE file_url LIKE ?', (f'%{search_term}',))
    results = cursor.fetchall()
    return [result[0] for result in results]

def search_urls_contains(cursor, search_term):
    """Search for file URLs that contain the given search term."""
    cursor.execute('SELECT file_url FROM File_URL WHERE file_url LIKE ?', (f'%{search_term}%',))
    results = cursor.fetchall()
    return [result[0] for result in results]

def search_for_file(search_term_endswith):
    # Connect to the SQLite database in read-only mode
    conn = connect_read_only(DATABASE)
    cursor = conn.cursor()

    # Search URLs that end with the search term
    results_endswith = search_urls_endswith(cursor, search_term_endswith)
    print(f"\nURLs ending with '{search_term_endswith}':")
    for url in results_endswith:
        print(url)

    # Close the database connection
    conn.close()

def search_in_url(search_term_contains):
    # Connect to the SQLite database in read-only mode
    conn = connect_read_only(DATABASE)
    cursor = conn.cursor()

    # Search URLs that contain the search term
    results_contains = search_urls_contains(cursor, search_term_contains)
    print(f"\nURLs containing '{search_term_contains}':")
    for url in results_contains:
        print(url)

    # Close the database connection
    conn.close()

def main():


    # search_for_file('bg')

    search_in_url('frogbot')




if __name__ == "__main__":
    main()
