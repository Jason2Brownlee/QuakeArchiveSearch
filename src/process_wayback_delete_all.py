# use this to delete quake websites we've added that are too slow to download...
# then delete the url from the ingested .txt file so we don't try and process it again

from db import get_db_connection

# use this if you want to see what is deleted before we delete it
DEBUG = False

def select_delete():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            processing_method_name = "archive.org wayback machine list"
            # Fetch the processing method
            cursor.execute('SELECT id FROM Processing_Method WHERE method_name = %s', (processing_method_name,))
            method = cursor.fetchone()
            processing_method_id = method['id']

            # Retrieve all unprocessed quake websites
            cursor.execute('''
                SELECT qw.id, qw.base_url FROM Quake_Website qw
                LEFT JOIN Website_Processing_Status wps
                ON qw.id = wps.quake_website_id AND wps.processing_method_id = %s
                WHERE wps.status IS NULL OR wps.status != 'completed'
            ''', (processing_method_id,))
            unprocessed_websites = cursor.fetchall()

            # Print each unprocessed website
            for row in unprocessed_websites:
                print(row['base_url'])

            if DEBUG:
                return

            ids_to_delete = [row['id'] for row in unprocessed_websites]
            print(len(ids_to_delete))

            # Delete the records with these IDs from Quake_Website table
            if ids_to_delete:
                cursor.execute('''
                    DELETE FROM Quake_Website WHERE id = ANY(%s)
                ''', (ids_to_delete,))
                print(f"{cursor.rowcount} records deleted.")
            # Connection context commits on success, rolls back on error

def main():
    select_delete()

if __name__ == "__main__":
    main()
