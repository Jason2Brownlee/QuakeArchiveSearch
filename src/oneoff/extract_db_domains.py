#!/usr/bin/env python3
"""Extract unique URL hostnames from the Quake Archive PostgreSQL database.

Place this file alongside db.py, then run:
    python extract_db_domains.py

Requires: pip install "psycopg[binary]"

Reads the URLs using a named (server-side) cursor in bounded batches: the
75M rows are never loaded into Python memory together. Only unique hostnames
are held in memory. No extra database tables or indexes are created.
"""

from pathlib import Path
from urllib.parse import urlsplit
import time

from psycopg import sql
from psycopg.rows import tuple_row

# Add parent directory to Python's module search path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from db import get_db_connection

# ========================= SETTINGS =========================
TABLE_NAME = "file_url"  # Change to "File_URL" if your table was created quoted.
COLUMN_NAME = "file_url"
OUTPUT_FILE = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/all_domains.txt"
BATCH_SIZE = 20_000
REPORT_EVERY = 1_000_000  # URLs examined between progress messages
# ============================================================


def hostname_from_url(value):
    """Return a lowercase hostname; retain subdomains, omit ports and paths."""
    if not isinstance(value, str) or not value:
        return None
    try:
        parts = urlsplit(value)
        if parts.scheme.lower() not in ("http", "https"):
            return None
        hostname = parts.hostname  # strips username, password, and port
        if not hostname:
            return None
        return hostname.lower().rstrip(".") or None
    except ValueError:  # malformed IPv6 brackets, etc.
        return None


def main():
    domains = set()
    total = valid = 0
    start = time.monotonic()
    next_report = REPORT_EVERY

    print("Scanning URL hostnames from PostgreSQL...", flush=True)
    # This connection is already configured by your existing db.py.
    with get_db_connection() as conn:
        # Named cursor: PostgreSQL streams rows on demand rather than loading
        # all matching rows into the client.
        with conn.cursor(name="domain_scan", row_factory=tuple_row) as cursor:
            # Use the exact table name as stored in PostgreSQL.
            query = sql.SQL("SELECT {} FROM {}").format(
                sql.Identifier(COLUMN_NAME),
                sql.Identifier(TABLE_NAME),
            )
            cursor.execute(query)
            while rows := cursor.fetchmany(BATCH_SIZE):
                for (url,) in rows:
                    total += 1
                    hostname = hostname_from_url(url)
                    if hostname:
                        valid += 1
                        domains.add(hostname)
                if total >= next_report:
                    elapsed = max(time.monotonic() - start, 0.001)
                    print(
                        f"  {total:,} URLs scanned | {len(domains):,} unique domains "
                        f"| {total / elapsed:,.0f} URLs/sec",
                        flush=True,
                    )
                    next_report = (total // REPORT_EVERY + 1) * REPORT_EVERY

    output_path = Path(OUTPUT_FILE)

    # Write atomically so an existing output file isn't partially overwritten.
    with output_path.open("w", encoding="utf-8") as f:
        for domain in sorted(domains):
            f.write(domain + "\n")

    elapsed = time.monotonic() - start
    print("\nFinished:")
    print(f"  URLs scanned:      {total:,}")
    print(f"  Valid HTTP(S) URLs:{valid:>13,}")
    print(f"  Invalid/other:     {total - valid:,}")
    print(f"  Unique hostnames:  {len(domains):,}")
    print(f"  Elapsed:           {elapsed / 60:.1f} minutes")
    print(f"  Output file:       {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
