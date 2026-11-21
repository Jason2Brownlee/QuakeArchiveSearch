"""Shared PostgreSQL connection helper for Quake archive scripts."""

import psycopg
from psycopg.rows import dict_row

DATABASE = "dbname=quake_archive"


def get_db_connection():
    """Return a PostgreSQL connection with dictionary-style query results."""
    return psycopg.connect(DATABASE, row_factory=dict_row)
