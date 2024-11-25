import os
import re
import sqlite3
from urllib.parse import urlparse

DATABASE = '../data/quake_website.db'

TESTING = False

if TESTING:
    DATABASE = '../data/quake_website_testing.db'


def is_valid_url(url):
    """
    Check if the given string is a valid URL with a scheme and network location.
    """
    parsed_url = urlparse(url)
    # Check if the URL has a scheme (e.g., 'http', 'https') and a netloc (domain or IP address)
    return all([parsed_url.scheme, parsed_url.netloc])

def load_log_files_and_extract_urls(log_directory):
    """
    Load all .log files from the specified directory, extract URLs using simple string processing,
    and add them to a set. Report URLs as they are added.
    """
    url_set = set()  # To store unique URLs

    # Iterate over all files in the directory
    for file_name in os.listdir(log_directory):
        if file_name.endswith('.log'):  # Only process .log files
            log_file_path = os.path.join(log_directory, file_name)
            print(f"Processing {log_file_path}...")

            try:
                # Read the log file
                with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        # Split the line by whitespace to extract columns
                        columns = line.split()

                        if len(columns) > 2 and columns[2].startswith('URL:'):
                            # Extract the URL (assuming it's the 2nd column after 'URL:')
                            url = columns[2][4:]  # Strip the 'URL:' part

                            if not url:
                                continue

                            # confirm url
                            if not is_valid_url(url):
                                print(f'skipping {url}')

                            if url not in url_set:
                                # print(f"Adding URL: {url}")
                                # print(url)
                                url_set.add(url)
            except Exception as e:
                print(f' > error: {e}')

    return url_set

def count_zip_files(url_set):
    """
    Count the number of URLs in the set that point to .zip files.
    """
    zip_count = 0
    for url in url_set:
        # Check if the URL ends with '.zip' (case insensitive)
        if url.lower().endswith('.zip'):
            zip_count += 1
    return zip_count


def insert_urls_into_db(db_path, url_set):
    """
    Insert URLs into the SQLite database, ensuring no duplicates.
    The table is named 'File_URL' with a column 'file_url'.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if TESTING:
        # Create table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS File_URL (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_url TEXT UNIQUE
            )
        ''')


    # Insert each URL into the table
    for url in url_set:
        try:
            cursor.execute('INSERT OR IGNORE INTO File_URL (file_url) VALUES (?)', (url,))
        except sqlite3.Error as e:
            print(f"Error inserting URL {url}: {e}")

    # Commit changes and close the database connection
    conn.commit()
    conn.close()
    print(f"Inserted {len(url_set)} URLs into the database.")

if __name__ == "__main__":
    # Example usage
    log_directory = '../data/logs/'  # Directory containing the downloaded log files

    # Step 1: Load log files and extract URLs
    url_set = load_log_files_and_extract_urls(log_directory)

    print(f'Loaded {len(url_set)} urls')
    print(f'Found {count_zip_files(url_set)} zip files')

    # Step 2: Insert the URLs into the SQLite database
    insert_urls_into_db(DATABASE, url_set)
