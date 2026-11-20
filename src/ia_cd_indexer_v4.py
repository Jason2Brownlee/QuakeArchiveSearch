#!/usr/bin/env python3
"""Index downloadable files inside Internet Archive CD images without downloading ISOs.

Edit the SETTINGS section, then run: python ia_cd_indexer_v4.py
Dependencies: pip install requests beautifulsoup4
"""

# ========================= SETTINGS =========================
UPLOADER = "kingshadow7"

OUTPUT_DIR = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/ia_cd_index"       # All output, relative to this script (or absolute)
CACHE_DIR = "cache"                  # Cached HTTP response bodies under OUTPUT_DIR
URLS_FILE = "all_files.txt"          # One fully qualified download URL per line
ITEMS_FILE = "items.txt"
MAX_ITEMS = 0                        # 0 = all; use 5 for a test
REQUEST_DELAY_SECONDS = 2.0          # Delay between network requests
REQUEST_TIMEOUT_SECONDS = 180
MAX_RETRIES = 5

# Refresh settings are independent. False = reuse cached responses when present.
# Missing cache files are ALWAYS downloaded, regardless of these settings.
#
# Typical use: set REFRESH_SEARCH = True to discover newly uploaded items while
# leaving REFRESH_METADATA and REFRESH_LISTINGS False to reuse cached records.
#
# REFRESH_SEARCH:
#   True  = fetch all upload-discovery API pages again (find new/removed uploads).
#   False = reuse cached discovery pages. Newly uploaded items may be missed.
#
# REFRESH_METADATA:
#   True  = fetch each discovered item's metadata JSON again (find newly added
#           or renamed disc images within existing Archive.org items).
#   False = reuse cached metadata JSON when available.
#
# REFRESH_LISTINGS:
#   True  = fetch the View Contents HTML again for every discovered disc image
#           (find files added or changed inside previously indexed images).
#   False = reuse cached View Contents HTML when available.
#
# These settings do NOT delete the cache. Successful refreshes replace the old
# cached response for their category. Every run rebuilds all_files.txt from
# scratch, regardless of refresh settings.
REFRESH_SEARCH = False
REFRESH_METADATA = False
REFRESH_LISTINGS = False
IMAGE_EXTENSIONS = (".iso", ".img", ".bin", ".nrg", ".mdf", ".isz")
USER_AGENT = "ResearchCDIndexer/2.0 (personal archival indexing)"
# ============================================================

import hashlib
import json
import sys
import time
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

BASE = "https://archive.org"
ROOT = Path(OUTPUT_DIR)
if not ROOT.is_absolute():
    ROOT = Path(__file__).resolve().parent / ROOT
CACHE = ROOT / CACHE_DIR


def fetch(session, url, category):
    """Cache raw JSON/HTML responses, including final redirected page URL."""
    directory = CACHE / category
    directory.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    body_path = directory / (key + (".json" if category != "listings" else ".html"))
    info_path = directory / (key + ".url.json")
    refresh = {
        "search": REFRESH_SEARCH,
        "metadata": REFRESH_METADATA,
        "listings": REFRESH_LISTINGS,
    }[category]
    if body_path.exists() and info_path.exists() and not refresh:
        info = json.loads(info_path.read_text(encoding="utf-8"))
        return body_path.read_text(encoding="utf-8"), info["final_url"]
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=(15, REQUEST_TIMEOUT_SECONDS))
            response.raise_for_status()
            if not response.text.strip():
                raise ValueError("Empty response")
            # Save only successful responses. Atomic replace prevents truncated cache.
            tmp = body_path.with_suffix(body_path.suffix + ".tmp")
            tmp.write_text(response.text, encoding="utf-8")
            tmp.replace(body_path)
            info_path.write_text(json.dumps({"requested_url": url, "final_url": response.url}, indent=2), encoding="utf-8")
            time.sleep(REQUEST_DELAY_SECONDS)
            return response.text, response.url
        except (requests.RequestException, ValueError) as exc:
            if attempt == MAX_RETRIES - 1:
                raise RuntimeError(f"Failed fetching {url}: {exc}") from exc
            time.sleep(min(60, 3 * 2 ** attempt))


def discover(session):
    items = set()
    page = 1
    while True:
        q = quote(f"_uploader_useritem:@{UPLOADER.lstrip('@')}", safe="")
        url = f"{BASE}/advancedsearch.php?q={q}&fl%5B%5D=identifier&rows=500&page={page}&output=json"
        body, _ = fetch(session, url, "search")
        result = json.loads(body)["response"]
        docs = result["docs"]
        items.update(d["identifier"] for d in docs)
        print(f"Discovery page {page}: {len(docs)} records, {len(items)} total", flush=True)
        if not docs or page * 500 >= result["numFound"]:
            break
        page += 1
    if not items:
        raise RuntimeError(
            f"No uploaded items found for @{UPLOADER.lstrip('@')} via "
            "_uploader_useritem search. Check the username or try "
            "REFRESH_SEARCH=True."
        )
    return sorted(items)


def images_from_metadata(metadata):
    return [f["name"] for f in metadata.get("files", [])
            if isinstance(f.get("name"), str)
            and f["name"].lower().endswith(IMAGE_EXTENSIONS)
            and f.get("source") != "derivative"]


def readable_url(url):
    """Decode escaped path characters, especially %2F -> / and %20 -> space.

    Browsers generally accept these human-readable URLs. Preserve encoded ? and #
    because decoding them would change the meaning of the URL.
    """
    parts = urlsplit(url)
    path = unquote(parts.path)
    path = path.replace("?", "%3F").replace("#", "%23")
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def parse_listing(html, listing_url):
    """Extract file URLs from IA's view_archive.php table.

    The actual table has columns: file, as jpg, timestamp, size.
    We rely on file links and numeric sizes rather than exact HTML nesting.
    """
    soup = BeautifulSoup(html, "html.parser")
    results = set()
    for tr in soup.select("tr"):
        cells = tr.find_all("td")
        if len(cells) < 2:
            continue
        link = cells[0].find("a", href=True)
        if link is None:
            continue
        # File rows have a numeric byte size. Directory rows have no size.
        size = cells[-1].get_text(" ", strip=True).replace(",", "")
        if not size.isdigit():
            continue
        url = urljoin(listing_url, link["href"])
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https"):
            continue
        if not (parsed.hostname == "archive.org" or
                (parsed.hostname or "").endswith(".archive.org")):
            continue
        # View Contents file links point to /download/<item>/<iso>/<path>
        # Use the link itself, rather than constructing a URL from filename text.
        if "/download/" not in parsed.path:
            continue
        results.add(readable_url(url))
    if not results:
        title = soup.title.get_text(" ", strip=True) if soup.title else "(no title)"
        raise ValueError(f"No file links found (page title: {title}; {len(html)} bytes). "
                         "Check the cached listing HTML.")
    return sorted(results)


def is_archive_listing(html):
    """Don't cache a generic error page as a successful archive listing."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    return "listing of " in text and ("timestamp" in text or "size" in text)


def fetch_listing(session, url):
    """Use the actual View Contents endpoint, with automatic repair of old caches."""
    html, final_url = fetch(session, url, "listings")
    try:
        return parse_listing(html, final_url)
    except ValueError:
        # Older versions may have cached a non-listing or temporary IA page.
        # Delete only this URL's listing cache and retry once.
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        for suffix in (".html", ".url.json"):
            (CACHE / "listings" / (key + suffix)).unlink(missing_ok=True)
        html, final_url = fetch(session, url, "listings")
        return parse_listing(html, final_url)

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/json"})
    items = discover(session)
    print(f"Found {len(items)} uploaded items", flush=True)
    if MAX_ITEMS > 0:
        items = items[:MAX_ITEMS]
    (ROOT / ITEMS_FILE).write_text("\n".join(items) + "\n", encoding="utf-8")

    # Rebuild the text index from scratch every run. Cached HTTP responses
    # mean this normally needs no network traffic after initial discovery.
    # Flush after each CD image so interrupted runs leave useful results.
    destination = ROOT / URLS_FILE
    seen = set()
    count = 0
    with destination.open("w", encoding="utf-8") as output:
        for i, item in enumerate(items, 1):
            print(f"[{i}/{len(items)}] {item}", flush=True)
            try:
                metadata_url = f"{BASE}/metadata/{quote(item, safe='')}"
                body, _ = fetch(session, metadata_url, "metadata")
                images = images_from_metadata(json.loads(body))
            except Exception as exc:
                print(f"  Metadata error: {exc}", file=sys.stderr)
                continue
            if not images:
                print("  No disc images in metadata", flush=True)
            for image_name in images:
                listing_url = f"{BASE}/download/{quote(item, safe='')}/{quote(image_name, safe='/')}/"
                try:
                    urls = fetch_listing(session, listing_url)
                    new_urls = [url for url in urls if url not in seen]
                    for url in new_urls:
                        output.write(url + "\n")
                    output.flush()
                    seen.update(new_urls)
                    count += len(new_urls)
                    print(f"  OK {image_name}: {len(urls)} files ({len(new_urls)} new)", flush=True)
                except Exception as exc:
                    print(f"  ERROR {image_name}: {exc}", file=sys.stderr)
    print(f"Done: {count} file URLs in {destination}")
    if count == 0:
        print("WARNING: No URLs indexed. Check the per-item messages above. "
              "Try REFRESH_SEARCH=True to refresh discovery, or "
              "REFRESH_METADATA=True for stale item metadata.",
              file=sys.stderr)
    print(f"Cached HTML and API responses: {CACHE}")


if __name__ == "__main__":
    main()
