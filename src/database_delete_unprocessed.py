# use this to delete quake websites we've added that are too slow to download...

import sqlite3

DATABASE = '../data/quake_website.db'
DEBUG = True

def select_delete():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    processing_method_name = "archive.org wayback machine list"
    # Fetch or insert the processing method into the Processing_Method table
    cursor.execute('SELECT id FROM Processing_Method WHERE method_name = ?', (processing_method_name,))
    method = cursor.fetchone()
    processing_method_id = method[0]

    # Retrieve all unprocessed quake websites
    cursor.execute('''
        SELECT qw.id, qw.base_url FROM Quake_Website qw
        LEFT JOIN Website_Processing_Status wps
        ON qw.id = wps.quake_website_id AND wps.processing_method_id = ?
        WHERE wps.status IS NULL OR wps.status != 'completed'
    ''', (processing_method_id,))
    unprocessed_websites = cursor.fetchall()

    # Process each unprocessed website
    for quake_website_id, base_url in unprocessed_websites:
        print(base_url)

    if DEBUG:
        return

    # Fetch all the IDs
    ids_to_delete = [a for a,_ in unprocessed_websites]
    print(len(ids_to_delete))

    # Delete the records with these IDs from Quake_Website table
    if ids_to_delete:  # Check if there are IDs to delete
        cursor.execute(f'''
            DELETE FROM Quake_Website WHERE id IN ({",".join("?" * len(ids_to_delete))})
        ''', ids_to_delete)

        # Commit the changes
        conn.commit()
        print(f"{cursor.rowcount} records deleted.")

def main():
    select_delete()

if __name__ == "__main__":
    main()