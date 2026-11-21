# read a list of urls from text file and add to a temp db table for processing against the wayback machine
# after this we use process_wayback_list_all.py

from db import get_db_connection
from urllib.parse import urlparse, urlunparse, unquote, quote
import sys

URL_FILE = '../data/quake_websites.txt'


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
    # Initialize counters
    total_urls = 0
    inserted_count = 0
    skipped_count = 0
    error_count = 0
    error_urls = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    with conn.transaction():
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
                                if not standardized_url or '\x00' in standardized_url or '\x00' in original_url:
                                    error_count += 1
                                    error_urls.append(original_url)
                                    continue

                                # A savepoint lets a bad URL fail without aborting other inserts.
                                with conn.transaction():
                                    cursor.execute(
                                        """INSERT INTO quake_website (base_url, original_url)
                                           VALUES (%s, %s)
                                           ON CONFLICT (base_url) DO NOTHING
                                           RETURNING id""",
                                        (standardized_url, original_url)
                                    )
                                    if cursor.fetchone() is not None:
                                        inserted_count += 1
                                    else:
                                        skipped_count += 1
                            except Exception as e:
                                error_count += 1
                                error_urls.append(original_url)
                                print(f"Error processing URL '{original_url}': {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        return

    # Report the results
    print(f"Processing complete.")
    print(f"Total URLs processed: {total_urls} in {filename}")
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


