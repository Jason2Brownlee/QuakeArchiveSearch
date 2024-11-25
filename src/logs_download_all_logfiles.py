import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def download_log_files(base_url, target_directory):
    # Step 1: Fetch the directory listing page
    response = requests.get(base_url)
    response.raise_for_status()  # Raise an error for bad responses
    html_content = response.text

    # Step 2: Parse the HTML content to extract all relative links
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    # Step 3: Convert relative URLs to absolute URLs and filter for .log files
    log_file_urls = []
    for link in links:
        href = link.get('href')
        if href and href.endswith('.log'):  # Only look for .log files
            log_file_url = urljoin(base_url, href)  # Convert relative to absolute URL
            log_file_urls.append(log_file_url)

    # Step 4: Download each .log file to the target directory
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for log_file_url in log_file_urls:
        # Get the file name from the URL
        file_name = os.path.basename(urlparse(log_file_url).path)
        file_path = os.path.join(target_directory, file_name)

        # Download the log file
        print(f"Downloading {log_file_url}...")
        log_response = requests.get(log_file_url)
        log_response.raise_for_status()  # Ensure the request was successful

        # Save the log file to the target directory
        with open(file_path, 'wb') as log_file:
            log_file.write(log_response.content)

        print(f"Saved to {file_path}")

if __name__ == "__main__":
    # Example usage
    base_url = 'https://www.quaddicted.com/webarchive/'  # Replace with the actual URL
    target_directory = '../data/logs'  # Replace with your target directory

    download_log_files(base_url, target_directory)
