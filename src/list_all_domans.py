import sqlite3
import re
from urllib.parse import urlparse

DATABASE = '../data/quake_website.db'

def connect_read_only(db_path):
    """Connect to the SQLite database in read-only mode."""
    uri = f'file:{db_path}?mode=ro'
    return sqlite3.connect(uri, uri=True)

# Connect to the SQLite database
conn = connect_read_only(DATABASE)
cursor = conn.cursor()

# SQL query to extract all URLs
query = "SELECT file_url FROM File_URL"
cursor.execute(query)

# Fetch all URLs from the database
urls = cursor.fetchall()

# Use a set to store unique domain names
unique_domains = set()

# Function to extract domain from URL
def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain
    except Exception as e:
        return None

# Extract domain names from URLs
for (url,) in urls:
    domain = extract_domain(url)
    if domain:
        unique_domains.add(domain)

# Close the database connection
conn.close()

# Print the result in ascending order
for domain in sorted(unique_domains):
    print(domain)

