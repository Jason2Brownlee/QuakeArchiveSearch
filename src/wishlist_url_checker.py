# find all file urls in the database for files in the wishlist that are not in the url wishlist

import sqlite3

DATABASE = '../data/quake_website.db'

# Paths to the wishlist files
url_wishlist_path = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist_urls.txt'
filename_wishlist_path = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt'

# url_wishlist_path = '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist_urls.txt'
# filename_wishlist_path = '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist.txt'


def read_text_file(file_path):
    """
    Read lines from a text file and return them as a set.
    """
    data = set()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            data.add(line)
    return data

def main():
    # Read URLs and filenames from the text files into sets
    url_wishlist = read_text_file(url_wishlist_path)
    filename_wishlist = read_text_file(filename_wishlist_path)

    # Connect to the SQLite database
    uri = f'file:{DATABASE}?mode=ro'
    conn = sqlite3.connect(uri, uri=True)
    cursor = conn.cursor()

    # Process each filename in the wishlist
    for filename in sorted(filename_wishlist):
        matching_urls = set()

        # Construct the SQL query to find matching file URLs
        query = """
        SELECT file_url FROM File_URL
        WHERE file_url LIKE ?
        """

        # Execute the query for the current filename
        like_pattern = f'%/{filename}'
        cursor.execute(query, (like_pattern,))

        # Fetch all results for this filename
        results = cursor.fetchall()

        # Check each result if it is not in the URL wishlist
        for row in results:
            file_url = row[0]
            if file_url not in url_wishlist:
                matching_urls.add(file_url)

        # Display the results
        if matching_urls:
            print(filename)
            for url in sorted(matching_urls):
                print(f'\t{url}')

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
