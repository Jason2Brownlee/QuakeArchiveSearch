import sqlite3

def summarize_schema(database_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Iterate over each table and summarize its schema
    schema_summary = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Extract column details
        schema_details = []
        for column in columns:
            column_id, name, col_type, not_null, default_value, primary_key = column
            schema_details.append({
                'Column ID': column_id,
                'Column Name': name,
                'Type': col_type,
                'Not Null': bool(not_null),
                'Default Value': default_value,
                'Primary Key': bool(primary_key)
            })

        schema_summary[table_name] = schema_details

    # Close the connection
    conn.close()

    # Print the summary
    for table_name, columns in schema_summary.items():
        print(f"Table: {table_name}")
        for column in columns:
            print(f"  - {column['Column Name']} ({column['Type']}), "
                  f"Not Null: {column['Not Null']}, "
                  f"Default: {column['Default Value']}, "
                  f"Primary Key: {column['Primary Key']}")
        print()

def files(database_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Fetch all table names
    cursor.execute("SELECT filename FROM files_filename_fts;")

    # 9959
    # cursor.execute("SELECT count(filename) FROM files_filename_fts;")
    results = cursor.fetchall()

    # print(results)

    for name in results:
        print(name)


    # Close the connection
    conn.close()



# Specify the database file name
database_file = "../data/fileplanet.sqlite"

# Summarize the schema
# summarize_schema(database_file)
files(database_file)
