# find all file urls in the database for files in the wishlist that are not in the url wishlist


# Paths to the wishlist files
# url_wishlist_path = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist_urls.txt'
# filename_wishlist_path = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt'

url_wishlist_path = '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist_urls.txt'
filename_wishlist_path = '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist.txt'


# local file to check
RAW_FILE = '../data/quake_usenet_raw.txt'


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
    raw_list = read_text_file(RAW_FILE)

    # Process each filename in the wishlist
    for filename in sorted(filename_wishlist):
        matching_urls = set()

        # check each raw url for the file
        for url in raw_list:
            if filename.lower() in url.lower():
                # check if we know about the url already
                if url in url_wishlist:
                    # skip
                    continue
                # report
                print(f'\t{url}')


if __name__ == '__main__':
    main()
