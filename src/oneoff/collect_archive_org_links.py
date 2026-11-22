#!/usr/bin/env python3
"""Collect archive.org URLs from Markdown bullet links in links.txt files.

Edit TARGET_DIR, then run:
    python collect_archive_org_links.py

Recursively searches TARGET_DIR for files named links.txt. Matches bullets
such as: * [Disc 1](https://archive.org/details/example)
Saves unique URLs and prints a summary at the end.
"""

from pathlib import Path
from urllib.parse import urlsplit
import re

# ======================== SETTINGS ========================
TARGET_DIR = Path("/Users/jasonb/Development/Quake/quakeaddoncds/dev/cds")
OUTPUT_FILE = "/Users/jasonb/Downloads/archive_org_links.txt"  # Written inside TARGET_DIR
# ==========================================================

# Markdown bullet link, allowing *, -, + and optional spaces.
# Captures the URL (including URLs wrapped in <...>).
LINK_RE = re.compile(r"^\s*[-*+]\s+\[[^\]]+\]\(\s*<?(https?://[^\s)>]+)", re.IGNORECASE)


def is_archive_org(url: str) -> bool:
    """Allow archive.org and its subdomains, not lookalike domains."""
    try:
        host = (urlsplit(url).hostname or "").lower()
    except ValueError:
        return False
    return host == "archive.org" or host.endswith(".archive.org")


def main() -> None:
    root = TARGET_DIR.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Target directory does not exist: {root}")

    found = set()
    files_checked = 0
    links_checked = 0
    matching_links = 0
    errors = []

    for path in sorted(p for p in root.rglob("links.txt") if p.is_file()):
        files_checked += 1
        try:
            with path.open("r", encoding="utf-8-sig", errors="replace") as source:
                for line in source:
                    match = LINK_RE.match(line)
                    if not match:
                        continue
                    links_checked += 1
                    url = match.group(1)
                    if is_archive_org(url):
                        matching_links += 1
                        found.add(url)
        except OSError as exc:
            errors.append(f"{path}: {exc}")

    destination = root / OUTPUT_FILE
    sorted_urls = sorted(found)
    with destination.open("w", encoding="utf-8") as output:
        for url in sorted_urls:
            output.write(url + "\n")

    print(f"links.txt files found:  {files_checked}")
    print(f"Markdown links examined: {links_checked}")
    print(f"archive.org links found: {matching_links}")
    print(f"Unique archive.org URLs: {len(sorted_urls)}")
    print(f"Output: {destination}")
    if errors:
        print(f"Files with read errors: {len(errors)}")
        for error in errors:
            print(f"  {error}")
    print("\nURLs:")
    for url in sorted_urls:
        print(url)


if __name__ == "__main__":
    main()
