# report all urls on a website downloaded from the wayback machine
# assumes already crawled and added to db, this is just for a visual review of extracted urls
# scroll down and type in the bottom and add the url

import os
import time
import re
import requests
from urllib.parse import urljoin, urlparse, urlunparse, unquote, quote
from bs4 import BeautifulSoup
import hashlib
import json
import sqlite3

# config
temp_dir = "../data/wayback_downloads"
DATABASE = '../data/quake_website.db'
year_cutoff = 2010
delay_seconds = 15

# api locations
WAYBACK_API_URL = "http://web.archive.org/cdx/search/cdx"
WAYBACK_BASE_URL = "http://web.archive.org/web/"

# global vars
last_download_time = 0



# Create the temporary directory if it doesn't exist
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def fetch_wayback_urls(base_url, year_cutoff, website_temp_dir):
    # Construct the cache filename based on the base URL and year cutoff
    cache_filename = os.path.join(website_temp_dir, f"wayback_urls_{year_cutoff}_{hashlib.md5(base_url.encode('utf-8')).hexdigest()}.json")

    # Check if the cache file exists
    # if os.path.exists(cache_filename):
    #     print(f"Loading cached Wayback URLs from {cache_filename}")
    #     with open(cache_filename, 'r', encoding='utf-8') as cache_file:
    #         return json.load(cache_file)

    # If cache does not exist, perform the API query
    params = {
        'url': f"{base_url}/*",  # Adding /* to match all URLs that start with the base URL
        'output': 'json',
        'fl': 'timestamp,original,mimetype,statuscode',
        'filter': 'statuscode:200',
        'from': '1996',
        'to': str(year_cutoff),
        'collapse': 'digest'  # This helps avoid duplicates
    }
    response = requests.get(WAYBACK_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    print(data)

    # Cache the result to a file
    with open(cache_filename, 'w', encoding='utf-8') as cache_file:
        json.dump(data, cache_file)


    print(f"Cached Wayback URLs to {cache_filename}")

    return data[1:]  # Skip the header row


def is_text_content(mimetype):
    return 'text/html' in mimetype or 'text/plain' in mimetype

def standardize_url(url):
    """
    Standardizes a URL by:
    - Ensuring the protocol is included.
    - Removing default ports (80 for HTTP, 443 for HTTPS).
    - Normalizing trailing slashes.
    - Decoding and re-encoding URL-encoded characters.
    - Removing unwanted special characters.
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

def remove_archive_prefix(url):
    if not url:
        return url

    # typical case
    if 'web.archive.org/web/' in url:
        return re.sub(r'https?://web\.archive\.org/web/[0-9]+/', '', url)

    # unusual case
    if url.startswith('/web/'):
        return re.sub('^/web/[0-9]+/', '', url)

    return url

def clean_url(url):
    # skip bad urls
    if url in ['#', '/']:
        return None
    if url in ['http', 'https', 'ftp']:
        return None
    if url.startswith('mailto'):
        return None
    if url.startswith('news:'):
        return None

    # standardize the result for insertion into the database
    try:
        url = standardize_url(url)
    except:
        return None

    return url

def rate_limited():
    global last_download_time
    current_time = time.time()
    time_since_last_call = current_time - last_download_time

    if time_since_last_call < delay_seconds:
        sleep_time = delay_seconds - time_since_last_call
        time.sleep(sleep_time)

    # Update the last_time after potentially sleeping
    last_download_time = time.time()

def download_and_parse_url(filename, original_url):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # Parse the content to extract URLs
    extracted_urls = extract_urls_from_content(content, original_url)
    return extracted_urls

# check all tokens for urls
def get_urls_from_txt(content):
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

def extract_urls_from_content(content, base_url):
    urls = set()

    # Parse HTML and extract href links
    try:
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            # remove archive.org prefix if present
            href = remove_archive_prefix(href)

            # check for email address
            if href.startswith('mailto'):
                continue
            if '@' in href:
                continue

            full_url = urljoin(base_url, href)
            cleaned_url = clean_url(full_url)
            if cleaned_url:
                urls.add(cleaned_url)
    except Exception as e:
        print(f"HTML parsing failed for {base_url}, but continuing with regex URL extraction: {e}")

    # Search the entire content for URLs
    links = get_urls_from_txt(content)
    for link in links:
        cleaned_url = clean_url(link)
        if cleaned_url:
            urls.add(cleaned_url)

    return urls

def sanitize_url_for_dirname(url):
    """
    Sanitize the website URL to create a safe directory name.
    Replace characters that are not alphanumeric or underscore with an underscore.
    """
    return re.sub(r'[^\w\-]', '_', url)




def process_quake_website():

    quake_websites = ['cdrom.com/pub/planetquake']

    for quake_website_url in quake_websites:
        print(f"Processing website: {quake_website_url}")

        orig_url = f'http://{quake_website_url}'

        all_extracted_urls = set()

        # Sanitize the website URL to create a directory name
        sanitized_url = sanitize_url_for_dirname(quake_website_url)

        # Create a unique temp directory for this website
        url_hash = hashlib.md5(quake_website_url.encode('utf-8')).hexdigest()
        website_temp_dir = os.path.join(temp_dir, f"{sanitized_url}_{url_hash}")

        for root, _, files in os.walk(website_temp_dir):
            for filename in files:
                # construct the path
                filepath = os.path.join(root, filename)
                # get urls
                extracted_urls = download_and_parse_url(filepath, orig_url)
                # update set
                all_extracted_urls.update(extracted_urls)
        # report all urls
        for item in sorted(all_extracted_urls):
            print(f'> {item}')


# entry point
if __name__ == "__main__":
    process_quake_website()
