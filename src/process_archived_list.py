import sqlite3
import requests
from urllib.parse import urlparse, urlunparse, unquote, quote
import time

DATABASE = '../data/quake_website.db'
SLEEP_TIME = 10
REQUEST_TIMEOUT = 30  # 30 seconds

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
    try:
        cursor.execute('INSERT INTO File_URL (file_url) VALUES (?)', (file_url,))
        return True
    except sqlite3.IntegrityError:
        # This occurs when the URL is already in the database due to the UNIQUE constraint
        return False

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
        INSERT OR REPLACE INTO Website_Processing_Status
        (quake_website_id, processing_method_id, status, last_processed)
        VALUES (?, ?, 'completed', CURRENT_TIMESTAMP)
    ''', (quake_website_id, processing_method_id))

    # Return processing results for reporting
    return len(urls), inserted_count

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    processing_method_name = "archive.org wayback machine list"

    # Fetch or insert the processing method into the Processing_Method table
    cursor.execute('SELECT id FROM Processing_Method WHERE method_name = ?', (processing_method_name,))
    method = cursor.fetchone()
    if method is None:
        cursor.execute('INSERT INTO Processing_Method (method_name, description) VALUES (?, ?)',
                       (processing_method_name, 'Retrieve archived URLs from the Wayback Machine'))
        processing_method_id = cursor.lastrowid
    else:
        processing_method_id = method[0]

    # Retrieve all unprocessed quake websites
    cursor.execute('''
        SELECT qw.id, qw.base_url FROM Quake_Website qw
        LEFT JOIN Website_Processing_Status wps
        ON qw.id = wps.quake_website_id AND wps.processing_method_id = ?
        WHERE wps.status IS NULL OR wps.status != 'completed'
    ''', (processing_method_id,))
    unprocessed_websites = cursor.fetchall()

    print(f'Found {len(unprocessed_websites)} unprocessed urls')

    # Process each unprocessed website
    for quake_website_id, base_url in unprocessed_websites:
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
