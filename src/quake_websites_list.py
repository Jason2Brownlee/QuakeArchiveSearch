import sqlite3

DATABASE = '../data/quake_website.db'

def get_sorted_quake_websites():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Execute a query to get all quake websites sorted by base_url
    cursor.execute('SELECT base_url FROM Quake_Website ORDER BY base_url ASC')
    
    # Fetch all results
    websites = cursor.fetchall()
    
    # Close the database connection
    conn.close()

    # Print the sorted list of URLs
    if websites:
        print("Sorted list of quake websites:")
        for site in websites:
            print(site[0])  # site[0] because fetchall returns a list of tuples
    else:
        print("No quake websites found in the database.")

# Run the function to get and print the sorted list
if __name__ == "__main__":
    get_sorted_quake_websites()
