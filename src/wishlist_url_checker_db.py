# find all file urls in the database for files in the wishlist that are not in the url wishlist

import sqlite3

# DATABASE = '../data/quake_website.db'
DATABASE = '../data/quake_website2.db'

EXCLUSIONS = '../data/exclusions.txt'

def read_text_file(file_path):
    """
    Read lines from a text file and return them as a set.
    """
    data = set()
    with open(file_path, 'r') as file:
        for line in file:
            # strip whitespace
            line = line.strip()
            # skip empty lines
            if not line:
                continue
            # skip comments
            if line.startswith('#'):
                continue
            # store in set
            data.add(line)
    return data

def main(pairs):
    # Connect to the SQLite database
    uri = f'file:{DATABASE}?mode=ro'
    conn = sqlite3.connect(uri, uri=True)
    cursor = conn.cursor()

    for name, url_wishlist_path,filename_wishlist_path in pairs:
        # report name
        print(f'\n{name}')

        # Read URLs and filenames from the text files into sets
        url_wishlist = read_text_file(url_wishlist_path)
        filename_wishlist = read_text_file(filename_wishlist_path)
        # read exclusions file
        exclusions = read_text_file(EXCLUSIONS)

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
                if file_url not in url_wishlist and file_url not in exclusions:
                    matching_urls.add(file_url)

            # always print filename
            # print(filename)

            # Display the results
            if matching_urls:
                print(filename)
                for url in sorted(matching_urls):
                    print(f'\t{url}')

    # Close the connection
    conn.close()

if __name__ == '__main__':

    pairs = [
            ['Navy Seals',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/marco_wishlist_urls.txt',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/marco_navy_seals_wishlist.txt'],
            ['Fantasy Quake',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/marco_wishlist_urls.txt',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/marco_fantasy_wishlist.txt'],
            ['Quake Matrix',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/marco_wishlist_urls.txt',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/marco_matrix_wishlist.txt'],
            ['Quaddicted',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/quaddicted_wishlist_urls.txt',
              '/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/quaddicted_wishlist.txt'],
            ['ThreeWaveCTF',
              '/Users/jasonb/Development/Quake/ThreeWaveCTF/research/wishlist_urls.txt',
              '/Users/jasonb/Development/Quake/ThreeWaveCTF/research/wishlist.txt'],
            ['TeamFortressQuakeArchive',
              '/Users/jasonb/Development/Quake/TeamFortressQuakeArchive/research/wishlist_urls.txt',
              '/Users/jasonb/Development/Quake/TeamFortressQuakeArchive/research/wishlist.txt'],
            ['QuakeOfficialArchive',
             '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist_urls.txt',
             '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist.txt'],
            ['QuakeBotArchive',
             '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist_urls.txt',
             '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt']
             ]

    main(pairs)
