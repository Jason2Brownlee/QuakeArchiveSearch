from flask import Flask, request, render_template
import sqlite3
import time
from urllib.parse import quote_plus

DATABASE = '../data/quake_website.db'
# DATABASE = '../data/quake_website2.db'
# DATABASE = '../data/quake_cds.db'

app = Flask(__name__)

# Function to create a connection to the SQLite database
def get_db_connection():
    # connect in a read only manner
    uri = f'file:{DATABASE}?mode=ro'
    conn = sqlite3.connect(uri, uri=True)
    # This allows us to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

# Function to count the total number of file URLs in the database
def get_total_file_url_count():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM File_URL")
    result = cursor.fetchone()
    conn.close()
    return result['total']

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    search_query = ""
    result_count = 0
    search_time = None
    total_file_urls = get_total_file_url_count()

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()

        if search_query:
            # Replace '*' with '%' for SQL LIKE queries
            sql_search_query = search_query.replace('*', '%')

            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Build the SQL query
            sql_query = "SELECT file_url FROM File_URL WHERE file_url LIKE ? ORDER BY file_url ASC LIMIT 1000"
            params = ('%' + sql_search_query + '%',)

            # Execute the query
            start_time = time.time()
            cursor.execute(sql_query, params)
            results = cursor.fetchall()
            search_time = round(time.time() - start_time, 3)
            result_count = len(results)

            # Close the connection
            conn.close()

    return render_template('index.html', results=results, search_query=search_query, total_file_urls=total_file_urls, result_count=result_count, search_time=search_time)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False)