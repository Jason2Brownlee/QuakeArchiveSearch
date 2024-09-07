import os
import re
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, unquote, quote

def is_url_a_file(url):
    # Parse the URL to get the path component
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Get the file extension (if any)
    _, file_extension = os.path.splitext(path)

    # Check if the path ends with a file extension
    return bool(file_extension)

def remove_file_from_url(url):
    # Parse the URL to extract components
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Identify and remove the file portion if present
    root, ext = os.path.splitext(path)
    if ext:  # If there's a file extension, remove the file portion
        path = os.path.dirname(path)  # Get the directory portion of the path

    # Reconstruct the URL without the file portion
    cleaned_url = urlunparse(parsed_url._replace(path=path))

    # Check if the resulting URL is valid
    if not parsed_url.netloc or parsed_url.netloc == '' or parsed_url.path == '' or parsed_url.path == '/':
        # If there's no domain or only a protocol, return None
        return None

    return cleaned_url

def standardize_url(url):
    """
    Standardizes a URL by:
    - Ensuring the protocol is included.
    - Removing default ports (80 for HTTP, 443 for HTTPS).
    - Normalizing trailing slashes.
    - Decoding and re-encoding URL-encoded characters.
    - Removing unwanted special characters.
    """

    # check for bad data
    if url.startswith('#') or url.startswith('javascript'):
        return None
    if url.endswith('.') or url.endswith(',') or url.endswith('*') or url.endswith(')'):
        url = url[:-1]
    if url.endswith("'s"):
        url = url[:-2]

    # skip urls for files
    # if is_url_a_file(url):
    #     return None

    # remove the file portion if present
    url = remove_file_from_url(url)
    if not url:
        return None

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

# HACK
    # remove path
    # path = ''

    # Rebuild the URL with the scheme and the normalized path
    standardized_url = urlunparse((scheme, netloc, path, '', '', ''))

    return standardized_url

# Function to extract URLs from text content
def extract_urls_from_text(content):
    # split into tokens
    tokens = content.split()
    # check each token to see if it is a url
    links = list()
    for token in tokens:
        t = token.lower()
        # check for urls
        if t.startswith('http://'):
            links.append(token)
        if t.startswith('ftp://'):
            links.append(token)
        if t.startswith('ftp.'):
            links.append(f'ftp://{token}')
        if t.startswith('www.'):
            links.append(f'http://{token}')
    return links

# Function to extract URLs from HTML content
def extract_urls_from_html(content, base_url=None):
    urls = set()
    try:
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            full_url = urljoin(base_url, url) if base_url else url
            urls.add(full_url)
    except Exception as e:
        # print(f"Failed to parse HTML content: {e}")
        pass
    return urls

# Function to process a single text file
def process_text_file(filepath):
    urls = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            urls.update(extract_urls_from_text(content))
    except Exception as e:
        # print(f"Failed to read {filepath}: {e}")
        pass
    return urls

# Function to process a single zip file
def process_zip_file(filepath):
    urls = set()
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_file:
            for zip_info in zip_file.infolist():
                if zip_info.filename.endswith(('.txt', '.html', '.htm')):
                    try:
                        with zip_file.open(zip_info) as file:
                            content = file.read().decode('utf-8', errors='ignore')
                            if zip_info.filename.endswith('.txt'):
                                urls.update(extract_urls_from_text(content))
                            else:
                                urls.update(extract_urls_from_html(content))
                    except Exception as e:
                        print(f"Failed to process {zip_info.filename} in {filepath}: {e}")
                elif zip_info.filename.endswith('.zip'):
                    # Recursively process nested zip files
                    nested_zip_path = os.path.join(os.path.dirname(filepath), zip_info.filename)
                    with open(nested_zip_path, 'wb') as nested_zip_file:
                        nested_zip_file.write(zip_file.read(zip_info.filename))
                    urls.update(process_zip_file(nested_zip_path))
                    os.remove(nested_zip_path)  # Clean up extracted nested zip file
    except Exception as e:
        # print(f"Failed to open zip file {filepath}: {e}")
        pass
    return urls

# Function to scan a directory for .txt and .zip files and process them
def scan_directory(dirs):
    all_urls = set()

    for directory in dirs:
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_urls = set()

# HACK, just open everything
                file_urls = process_text_file(filepath)

                # if filename.endswith('.txt'):
                #     # print(f"Processing text file: {filepath}")
                #     file_urls = process_text_file(filepath)

                # elif filename.endswith('.zip'):
                #     # print(f"Processing zip file: {filepath}")
                #     file_urls = process_zip_file(filepath)

                # TODO support .tar.gz and .gz and .rpm

                # clean the urls
                clean_urls = set()
                for url in file_urls:
                    try:
                        clean_url = standardize_url(url)
# HACK, report raw URLs
                        # clean_url = url

                        if clean_url:
                            clean_urls.add(clean_url)
                    except:
                        pass

                # print(f"Found URLs in {filename}:")
                # for url in clean_urls:
                #     print(f" - {url}")

                all_urls.update(clean_urls)

    # Print all unique URLs found
    # print("All unique URLs found:")
    for url in sorted(all_urls):
        print(url)

if __name__ == "__main__":

    # quake bots
    # dirs = ['/Users/jasonb/Development/Quake/QuakeBotArchive/bin/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/eliminator/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/frikbot/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/frogbot/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/mikebot/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/mystery/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/omicron/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/other/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/reaper/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/richmark/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/stoogebot/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/tedbot/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/terminator/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/research/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/research/essays/',
    #         '/Users/jasonb/Development/Quake/QuakeBotArchive/dev/'
    #         ]

    # official
    # dirs = ['/Users/jasonb/Development/Quake/QuakeOfficialArchive/bin/',
    #         '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/',
    #         '/Users/jasonb/Development/Quake/QuakeOfficialArchive/dev/']

    # 3wavectf
    # dirs = ['/Users/jasonb/Development/Quake/ThreeWaveCTF/bin']

    # quakec mailing list
    # dirs = ['/Users/jasonb/Games/QuakeFiles/QuakeCMailingList']

    # newsgroups (to 1997)
    # quakec
    dirs = ['/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake_c/n00/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake_c/n01/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake_c/n02/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake_c/n03/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake_c/n04/',

            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/misc/n00/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/misc/n01/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/misc/n02/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/misc/n03/',

            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/playing/n00/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/playing/n01/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/playing/n02/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/playing/n03/',

            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake/n00/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake/n01/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/quake/n02/',

            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n00/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n01/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n02/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n03/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n04/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n05/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n06/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n07/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n08/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n09/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n10/',
            '/Users/jasonb/Games/QuakeFiles/Qoole/Newsgrps/editing/n11/',
    ]





    scan_directory(dirs)


