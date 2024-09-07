# delete useless urls

import sqlite3

# Global constants for configuration
DB_PATH = '../data/quake_website.db'
DEBUG_MODE = False  # Set to False if you don't want to run in debug mode by default

# Function to report URLs that match the deletion criteria
def debug_mode(cursor, delete_criteria):
    # Construct the query for debugging
    query = f"""
    SELECT file_url FROM File_URL
    WHERE {" OR ".join([f"file_url LIKE '{criteria}'" for criteria in delete_criteria])}
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Display examples and total count
    if results:
        print("Examples of URLs to be deleted:")
        for url in results[:50]:
            print(url[0])

        print(f"\nTotal number of URLs to be deleted: {len(results)}")
    else:
        print("No URLs match the criteria for deletion.")

# Function to delete entries that match the criteria
def delete_entries(cursor, delete_criteria):
    # Construct the query for deletion
    delete_query = f"""
    DELETE FROM File_URL
    WHERE {" OR ".join([f"file_url LIKE '{criteria}'" for criteria in delete_criteria])}
    """
    cursor.execute(delete_query)
    print("Deletion complete.")

# Main function to execute the script
def main(delete_patterns):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if DEBUG_MODE:
        debug_mode(cursor, delete_patterns)
    else:
        delete_entries(cursor, delete_patterns)
        conn.commit()

    conn.close()

# Entry point for the script
if __name__ == "__main__":
    # Define the deletion patterns you want to use
    # Example patterns: ["%/robots.txt", "%.png"]
    DELETE_PATTERNS = [
        "%/robots.txt",
        "%/%.png",
        "%/%.gif",
        "%/%.jpg",
        "%/%.png%22",
        "%/%.gif%22",
        "%/%.jpg%22",
        "%/%.bmp",
        "%/%.svg",
        "%/%.tif",
        "%/%.tiff",
        "%/%.webp",
        "%/%.ico",
        "%/%.css",
        "%/%.js"
        ]

    # Run the main function with the specified patterns
    main(DELETE_PATTERNS)
