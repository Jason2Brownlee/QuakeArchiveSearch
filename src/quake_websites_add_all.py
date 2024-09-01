import sqlite3
from urllib.parse import urlparse, urlunparse, unquote, quote
import sys

DATABASE = '../data/quake_website.db'

# URL_FILE = '../data/quake_websites.txt'
# URL_FILE = '../data/quake_bot_websites.txt'
# URL_FILE = '../data/quake_bot_research_websites2.txt'
URL_FILE = '../data/quake_official_websites.txt'


def standardize_url(url):
    """
    Standardizes the URL by:
    - Removing protocol/scheme.
    - Removing 'www.' prefix if present.
    - Removing default filenames like 'index.html', 'default.htm', etc.
    - Removing trailing slashes.
    - Ensuring consistent URL encoding.
    """
    # Parse the URL
    parsed = urlparse(url.strip())

    # Extract netloc and path
    netloc = parsed.netloc or parsed.path  # Handles URLs without scheme
    path = parsed.path if parsed.netloc else ''

    # Remove 'www.' prefix
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    # Remove default filenames
    default_filenames = ['index.html', 'index.htm', 'default.html', 'default.htm']
    path_parts = path.rstrip('/').split('/')
    if path_parts and path_parts[-1].lower() in default_filenames:
        path_parts = path_parts[:-1]
    path = '/'.join(path_parts)

    # Remove trailing slash unless it's the root '/'
    if path != '/':
        path = path.rstrip('/')

    # Ensure consistent URL encoding
    path = quote(unquote(path))

    # Reconstruct the standardized URL
    standardized_url = f"{netloc}{path}"

    return standardized_url

def load_quake_websites(filename):
    """
    Loads quake websites from a text file into the database,
    after standardizing and checking for uniqueness.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Initialize counters
    total_urls = 0
    inserted_count = 0
    skipped_count = 0
    error_count = 0
    error_urls = []

    try:
        # Open the file and process each URL
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # skip comments
                if line and line.startswith('#'):
                    continue
                total_urls += 1
                original_url = line.strip()
                if not original_url:
                    continue  # Skip empty lines
                try:
                    standardized_url = standardize_url(original_url)
                    if standardized_url:
                        # Check if the URL is already in the database
                        cursor.execute('SELECT id FROM Quake_Website WHERE base_url = ?', (standardized_url,))
                        if cursor.fetchone() is None:
                            # Insert the URL if it doesn't exist
                            cursor.execute('INSERT INTO Quake_Website (base_url, original_url) VALUES (?, ?)', (standardized_url, original_url))
                            inserted_count += 1
                        else:
                            # Skip the URL if it already exists
                            skipped_count += 1
                    else:
                        error_count += 1
                        error_urls.append(original_url)
                except Exception as e:
                    error_count += 1
                    error_urls.append(original_url)
                    print(f"Error processing URL '{original_url}': {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        conn.close()
        return

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Report the results
    print(f"Processing complete.")
    print(f"Total URLs processed: {total_urls}")
    print(f"URLs inserted into database: {inserted_count}")
    print(f"URLs skipped (already present): {skipped_count}")
    print(f"URLs with errors: {error_count}")
    if error_urls:
        print("\nThe following URLs encountered errors during processing:")
        for url in error_urls:
            print(f"- {url}")

# Example usage
if __name__ == '__main__':
    load_quake_websites(URL_FILE)
    # if len(sys.argv) != 2:
    #     print("Usage: python load_quake_websites.py <path_to_url_file>")
    # else:
    #     filename = sys.argv[1]
    #     load_quake_websites(filename)


