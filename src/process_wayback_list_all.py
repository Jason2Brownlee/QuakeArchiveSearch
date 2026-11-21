# read urls to process from temp table then download the full captured url list from wayback for each and store all urls in db
# assumes urls were added via process_wayback_add_all.py
# if there is a url that just won't download, delete it via process_wayback_delete_all.py and remove from the ingested text file

from db import get_db_connection
import requests
from urllib.parse import urlparse, urlunparse, unquote, quote
import time

SLEEP_TIME = 10
REQUEST_TIMEOUT = 30  # how long to wait for a response

def standardize_url(url):
    """
    Standardizes a URL by:
    - Ensuring the protocol is included.
    - Removing default ports (80 for HTTP, 443 for HTTPS).
    - Normalizing trailing slashes.
    - Decoding and re-encoding URL-encoded characters.
    """
    parsed_url = urlparse(url)

    # Ensure the protocol is included, defaulting to http
    scheme = parsed_url.scheme or 'http'
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip('/')  # Normalize trailing slash

    # Remove default ports
    if netloc.endswith(':80'):
        netloc = netloc[:-3]
    elif netloc.endswith(':443'):
        netloc = netloc[:-4]

    # Decode URL-encoded characters and re-encode properly
    path = unquote(path)
    path = quote(path, safe='/')

    # Rebuild the URL with the scheme and the normalized path
    standardized_url = urlunparse((scheme, netloc, path, '', '', ''))

    return standardized_url

def fetch_wayback_urls(url):
    # Force a wait between API requests to avoid spamming
    time.sleep(SLEEP_TIME)

    # CDX API endpoint for querying archived URLs
    cdx_url = f"http://web.archive.org/cdx/search/cdx?url={url}*&output=json&fl=original&collapse=urlkey"

    response = requests.get(cdx_url, timeout=(REQUEST_TIMEOUT,REQUEST_TIMEOUT))
    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()

    # The first element is the header, skip it and process the URLs
    urls = [item[0] for item in data[1:]]

    return urls

def insert_file_url(cursor, quake_website_id, file_url):
    """
    Attempts to insert the file URL into the database.
    Returns True if inserted, False if skipped (e.g., already exists).
    """
    if not file_url or '\x00' in file_url:
        return False

    cursor.execute('''
        INSERT INTO file_url (file_url) VALUES (%s)
        ON CONFLICT DO NOTHING
        RETURNING id
    ''', (file_url,))
    return cursor.fetchone() is not None

def process_url_with_wayback(cursor, url, quake_website_id, processing_method_id):
    # Fetch all unique archived URLs from the Wayback Machine
    urls = fetch_wayback_urls(url)

    # Initialize counters for reporting
    inserted_count = 0
    skipped_count = 0

    # Process and insert each URL
    for original_url in urls:
        standardized_url = standardize_url(original_url)
        if insert_file_url(cursor, quake_website_id, standardized_url):
            inserted_count += 1
        else:
            skipped_count += 1

    # Mark the website as processed for this method
    cursor.execute('''
        INSERT INTO website_processing_status
        (quake_website_id, processing_method_id, status, last_processed)
        VALUES (%s, %s, 'completed', CURRENT_TIMESTAMP)
        ON CONFLICT (quake_website_id, processing_method_id)
        DO UPDATE SET status = EXCLUDED.status,
                      last_processed = EXCLUDED.last_processed
    ''', (quake_website_id, processing_method_id))

    # Return processing results for reporting
    return len(urls), inserted_count

def main():
    # Connect using the shared PostgreSQL helper
    conn = get_db_connection()
    cursor = conn.cursor()

    processing_method_name = "archive.org wayback machine list"

    # Fetch or insert the processing method into the Processing_Method table
    cursor.execute('SELECT id FROM processing_method WHERE method_name = %s', (processing_method_name,))
    method = cursor.fetchone()
    if method is None:
        cursor.execute('INSERT INTO processing_method (method_name, description) VALUES (%s, %s) RETURNING id',
                       (processing_method_name, 'Retrieve archived URLs from the Wayback Machine'))
        processing_method_id = cursor.fetchone()['id']
        conn.commit()
    else:
        processing_method_id = method['id']

    # Retrieve all unprocessed quake websites
    cursor.execute('''
        SELECT qw.id, qw.base_url FROM Quake_Website qw
        LEFT JOIN Website_Processing_Status wps
        ON qw.id = wps.quake_website_id AND wps.processing_method_id = %s
        WHERE wps.status IS NULL OR wps.status != 'completed'
    ''', (processing_method_id,))
    unprocessed_websites = cursor.fetchall()

    print(f'Found {len(unprocessed_websites)} unprocessed urls')

    # Process each unprocessed website
    for website in unprocessed_websites:
        quake_website_id, base_url = website['id'], website['base_url']
        # print(base_url)
        # continue

        try:
            total_found, inserted_count = process_url_with_wayback(cursor, base_url, quake_website_id, processing_method_id)
            # Commit the results for the current website
            conn.commit()
            # Print progress report
            print(f"Processed {base_url}: Found {total_found} URLs, Inserted {inserted_count}")
        except Exception as e:
            print(f"Error processing {base_url}: {e}")
            # Rollback in case of an error, though any commits before this will persist
            conn.rollback()

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
