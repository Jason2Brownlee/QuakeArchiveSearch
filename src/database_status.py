import sqlite3

DATABASE = '../data/quake_website.db'

import sqlite3

def connect_read_only(db_path):
    """Connect to the SQLite database in read-only mode."""
    uri = f'file:{db_path}?mode=ro'
    return sqlite3.connect(uri, uri=True)

def summarize_database():
    # Connect to the SQLite database in read-only mode
    conn = connect_read_only(DATABASE)
    cursor = conn.cursor()

    # Summary 1: Total number of quake websites
    cursor.execute('SELECT COUNT(*) FROM Quake_Website')
    total_websites = cursor.fetchone()[0]

    # Summary 2: Total number of file URLs
    cursor.execute('SELECT COUNT(*) FROM File_URL')
    total_file_urls = cursor.fetchone()[0]

    # Summary 3: Number of websites processed by each processing method
    cursor.execute('''
        SELECT pm.method_name, COUNT(DISTINCT wps.quake_website_id) AS processed_count
        FROM Website_Processing_Status wps
        JOIN Processing_Method pm ON wps.processing_method_id = pm.id
        WHERE wps.status = 'completed'
        GROUP BY pm.method_name
        ORDER BY processed_count DESC
    ''')
    processed_by_method = cursor.fetchall()

    # Output the summary
    print("\nDatabase Summary Report")
    print("=========================")
    print(f"Total Quake Websites: {total_websites:,}")
    print(f"Total File URLs: {total_file_urls:,}\n")

    print("Websites Processed by Each Method:")
    print("----------------------------------")
    for method_name, processed_count in processed_by_method:
        print(f"{method_name}: {processed_count:,}/{total_websites:,} websites processed")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    summarize_database()
