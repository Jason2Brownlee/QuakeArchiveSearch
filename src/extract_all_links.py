# script to extract all links from old gaming websites

import requests
from bs4 import BeautifulSoup
import re

# TARGET_URL = 'http://www.keeg.com/links.html'
# TARGET_URL = 'http://www.erinyes.com/celabs/links.html'
# TARGET_URL = 'http://dd.networx.net.au/aus_link.html'
# TARGET_URL = 'http://www.vision.net.au/~chuck/quake/qlinks.htm'
# TARGET_URL = 'http://ro.com/~rgoodwin/quake/links.html'
# TARGET_URL = 'http://www.sonic.net/gtaylor/quake.shtml'
# TARGET_URL = 'http://www.powerup.com.au/~gbaker/quake/links.htm'
# TARGET_URL = 'http://www.cybernet.dk/users/jensh/quake/main.html'
# TARGET_URL = 'http://redwood.gatsbyhouse.com/quake/qlinks.html'
# TARGET_URL = 'http://www.grayphics.com/3dmacgames/macquake/links.html'
# TARGET_URL = 'http://www.impulse1.com/links.html'
# TARGET_URL = 'http://quake.perfect.co.uk/tfs/links.html'
# TARGET_URL = 'http://www.idsoftware.com/dlquake.html'
# TARGET_URL = 'http://ss-club.holm.ru/quake/links.html'
# TARGET_URL = 'http://www.quake.convey.ru/links.html'
# TARGET_URL = 'http://quake.df.ru/q_links.html'
# TARGET_URL = 'http://www.sign-comsys.com/quake/links.html'
# TARGET_URL = 'http://www.dataforce.net/~crazer/quake/q_links.html'
# TARGET_URL = 'http://quake.spb.ru/linx.news.htm'
# TARGET_URL = 'http://www.quake.spb.ru/skib/klan/klan.htm'
# TARGET_URL = 'http://www.quake.spb.ru/linx.clubs.htm'
# TARGET_URL = 'http://www.quake.ru/links.html'
# TARGET_URL = 'http://quakemaster.warzone.com:80/quakelinks.htm'
# TARGET_URL = 'http://www.msen.com/~psteele/quake'
TARGET_URL = 'https://kod.org.uk/old/files.htm'



import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def fetch_earliest_wayback_snapshot(url):
    """
    Fetches the earliest snapshot of a webpage from the Wayback Machine.
    """
    cdx_api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp,original&filter=statuscode:200&limit=1&sort=asc"

    try:
        response = requests.get(cdx_api_url)
        response.raise_for_status()

        data = response.json()
        if len(data) > 1:
            # The first entry is a header, so we take the second one
            timestamp, original_url = data[1]
            snapshot_url = f"http://web.archive.org/web/{timestamp}/{original_url}"
            print(f"Found earliest snapshot: {snapshot_url}")
            return snapshot_url
        else:
            print("No snapshots available for this URL.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching data from Wayback Machine: {e}")
        return None

def clean_wayback_url(url):
    """
    Cleans the Wayback Machine wrapper from the URL, removes leading protocols and 'www.',
    removes file parts like index.html, and trims trailing slashes.
    """
    # Remove Wayback Machine wrapper
    match = re.match(r'http://web\.archive\.org/web/\d+/(.*)', url)
    if match:
        url = match.group(1)

    # Remove leading protocols (http://, https://)
    url = re.sub(r'^https?://', '', url)

    # Remove leading protocols (ftp://)
    url = re.sub(r'^ftp://', '', url)

    # Remove leading www.
    url = re.sub(r'^www\.', '', url)

    # Parse URL and remove the file part if it's a common file like index.html or main.htm
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Regular expression to match and remove any file ending with .htm or .html
    path = re.sub(r'/[^/]+\.(html?|htm)$', '', path)

    # Remove trailing slash from the path, if present
    path = path.rstrip('/')

    # Reconstruct the cleaned URL without the protocol, www, and file part
    cleaned_url = f"{parsed_url.netloc}{path}"

    return cleaned_url

def extract_urls_from_page(page_url):
    """
    Extracts all unique, cleaned URLs from the webpage.
    """
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all anchor tags
        urls = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Clean the Wayback Machine wrapper, protocol, www, and file part
            original_url = clean_wayback_url(href)

            # Normalize URLs (e.g., fix relative URLs, etc.)
            # if not original_url.startswith('http') :
            #     original_url = re.sub(r'^//', 'http://', original_url)

            # Add cleaned URL to the set (ensures uniqueness)
            urls.add(original_url)

        return sorted(urls)

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

def main():
    # Hardcode the URL you want to scrape here
    url_to_fetch = TARGET_URL

    print(f"Fetching earliest version of: {url_to_fetch}")

    # Step 1: Get the earliest Wayback Machine snapshot
    earliest_snapshot_url = fetch_earliest_wayback_snapshot(url_to_fetch)

    if not earliest_snapshot_url:
        print("Failed to fetch the earliest snapshot.")
        return

    # Step 2: Extract URLs from that page
    print(f"Extracting URLs from: {earliest_snapshot_url}")
    urls = extract_urls_from_page(earliest_snapshot_url)

    if urls:
        print("Unique URLs found:")
        for url in urls:
            print(url)
    else:
        print("No URLs found on the page.")

if __name__ == "__main__":
    main()

