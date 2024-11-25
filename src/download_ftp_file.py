# download a file from ftp

import ftplib
import os
import time
import urllib.parse

# number of times to retry the download
RETRIES = 3
# how long o wait for a connection in seconds
TIMEOUT = 60
# how long to wait between retries in seconds
WAIT = 20

def download_ftp_file(ftp_url, retries, timeout):
    """Download a ZIP file from an FTP server with retries and timeout.

    Args:
        ftp_url (str): The FTP URL of the file (e.g., ftp://server/path/to/file.zip).
        retries (int): Number of times to retry on timeout. Default is 3.
        timeout (int): Timeout in seconds for the connection. Default is 60.
    """
    # Parse the FTP URL
    parsed_url = urllib.parse.urlparse(ftp_url)
    ftp_host = parsed_url.hostname
    ftp_path = parsed_url.path
    filename = os.path.basename(ftp_path)

    # Establish FTP connection with retry logic
    attempt = 0
    while attempt < retries:
        try:
            print(f"Connecting to {ftp_host} (Attempt {attempt + 1}/{retries})...")
            with ftplib.FTP() as ftp:
                ftp.connect(ftp_host, timeout=timeout)
                ftp.login()  # Adjust with user/password if needed

                # Callback to report messages from the server
                ftp.set_debuglevel(1)

                # Navigate to the directory containing the file
                ftp.cwd(os.path.dirname(ftp_path))

                # Download the file
                with open(filename, 'wb') as local_file:
                    ftp.retrbinary(f"RETR {filename}", local_file.write)

                print(f"Successfully downloaded: {filename}")
                break  # Exit loop on success

        except ftplib.all_errors as e:
            print(f"Error: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {WAIT} seconds...")
                time.sleep(WAIT)
            else:
                print("Max retries reached. Download failed.")

if __name__ == "__main__":
    # file to download
    ftp_url = "ftp://l37-193-142-252.novotelecom.ru/distrib/DOS/fromDiman/msdos/games/quake/quakegam.zip"
    # download file
    download_ftp_file(ftp_url, RETRIES, TIMEOUT)
