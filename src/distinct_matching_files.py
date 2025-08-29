DATABASE_FILE = '../data/quake_website.db'


import sqlite3
import sys
from urllib.parse import urlparse, unquote
import os

# Database file constant


def filter_filename(filename):
    """
    Filter and clean filenames to remove unwanted file types and URL encoding.

    Args:
        filename (str): The filename to filter

    Returns:
        str: Cleaned filename, or empty string if should be filtered out
    """
    if not filename:
        return ""

    # URL decode the filename (handles %20, %2F, etc.)
    decoded_filename = unquote(filename)

    # Remove common unwanted extensions
    unwanted_extensions = {
        '.html', '.htm', '.shtml', '.asp', '.aspx', '.php', '.jsp',
        '.cgi', '.pl', '.py', '.rb', '.do', '.action', '.shtm', '.php3'
    }

    # Get file extension (convert to lowercase for comparison)
    file_ext = os.path.splitext(decoded_filename)[1].lower()

    # Filter out unwanted extensions
    if file_ext in unwanted_extensions:
        return ""

    # Filter out files that look like directories or have no extension
    if not file_ext and not decoded_filename.strip():
        return ""

    # Additional cleanup - remove query parameters if they somehow got through
    if '?' in decoded_filename:
        decoded_filename = decoded_filename.split('?')[0]

    # Remove fragment identifiers
    if '#' in decoded_filename:
        decoded_filename = decoded_filename.split('#')[0]

    # Trim whitespace
    cleaned_filename = decoded_filename.strip()

    return cleaned_filename
def extract_filename_from_url(url):
    """
    Extract the filename from a URL.

    Args:
        url (str): The URL to parse

    Returns:
        str: The filename part of the URL, or empty string if no filename
    """
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path

        # Extract filename from path
        filename = os.path.basename(path)

        # Return filename, or empty string if path ends with /
        return filename if filename else ""

    except Exception:
        return ""

def query_files_with_prefix(prefix_pattern):
    """
    Query the File_URL table for URLs matching a prefix pattern and extract filenames.

    Args:
        prefix_pattern (str): Pattern with * wildcards (converted to % for SQL)

    Returns:
        list: Sorted list of distinct filenames from matching URLs
    """
    try:
        # Convert * wildcards to % for SQL LIKE operator
        sql_pattern = prefix_pattern.replace('*', '%')

        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Query for URLs matching the pattern
        query = """
        SELECT file_url
        FROM File_URL
        WHERE file_url LIKE ?
        """

        cursor.execute(query, (sql_pattern,))
        results = cursor.fetchall()

        # Extract and filter filenames from URLs
        filenames = set()  # Use set to automatically handle duplicates
        for row in results:
            url = row[0]
            filename = extract_filename_from_url(url)
            if filename:
                # Apply filtering and cleaning
                cleaned_filename = filter_filename(filename)
                if cleaned_filename:  # Only add if it passes the filter
                    filenames.add(cleaned_filename)

        conn.close()

        # Convert to sorted list
        return sorted(list(filenames))

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def main(search_pattern):
    """
    Main function to search and display filenames from URLs matching the given pattern.

    Args:
        search_pattern (str): Pattern with * wildcards to search for
    """
    print(f"Searching for files in URLs matching pattern: {search_pattern}")
    print("-" * 50)

    # Query the database and extract filenames
    matching_files = query_files_with_prefix(search_pattern)

    if matching_files:
        print(f"Found {len(matching_files)} distinct files:")
        for filename in matching_files:
            print(filename)
    else:
        print("No matching files found.")

if __name__ == "__main__":
    # Hard-coded search patterns - modify these as needed
    search_patterns = [
        "*/idstuff/quake/*"
        # "*/idstuff/quake2/*"
        # "*/idstuff/quake3/*"
    ]

    # Run queries for each pattern
    for pattern in search_patterns:
        main(pattern)
        print()  # Add blank line between results

