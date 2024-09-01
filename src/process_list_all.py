import sqlite3

DATABASE = '../data/quake_website.db'



def list_processed_websites():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query to list all processed websites
    cursor.execute('''
        SELECT qw.base_url, wps.last_processed
        FROM Quake_Website qw
        JOIN Website_Processing_Status wps
        ON qw.id = wps.quake_website_id
        JOIN Processing_Method pm
        ON wps.processing_method_id = pm.id
        WHERE pm.method_name = 'archive.org wayback machine list' AND wps.status = 'completed'
        ORDER BY qw.base_url ASC
    ''')

    processed_websites = cursor.fetchall()

    # Print the results
    print("Processed Quake Websites (via Wayback Machine):")
    for base_url, last_processed in processed_websites:
        print(f"{base_url} - Last Processed: {last_processed}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    list_processed_websites()
