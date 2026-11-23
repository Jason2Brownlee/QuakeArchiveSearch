#!/usr/bin/env python3
"""Index files inside Internet Archive CD images and ZIPs from a list of item URLs.

Does not download disc images or ZIP archives. Requires: pip install requests beautifulsoup4
Edit SETTINGS below and run: python process_index_internet_archive_cds_urls.py

On every run all_files_urls.txt is rebuilt (and flushed after each disc).
Shares the original indexer's cache/metadata and cache/listings directories,
so existing responses are reused unless REFRESH_CACHE is True.
"""

# ========================= SETTINGS =========================


ITEM_URLS = [

# taken from quakediscs.com
"https://archive.org/details/7814-quake",
"https://archive.org/details/AftershockForQuake",
"https://archive.org/details/AftershockForQuakeDeluxe",
"https://archive.org/details/CdZoneIssue48march1997",
"https://archive.org/details/Chartbusters10",
"https://archive.org/details/CompleteGamer6QuakeAdd-ons",
"https://archive.org/details/DEATHMATCH_MANIFESTO",
"https://archive.org/details/Essential_CD_Gamer_Volume_2_PCG55-4-98B_PC-Gamer",
"https://archive.org/details/Juggernaut_for_Quake_2_AddOn",
"https://archive.org/details/Malice23rdCenturyUltraconversionForQuakeUSA",
"https://archive.org/details/MicrobossSUPERDEAD",
"https://archive.org/details/PCGamerOct1997",
"https://archive.org/details/PCZoneCompleteQuakeCD",
"https://archive.org/details/PC_Gamer_Disc_3.7_October_1997",
"https://archive.org/details/QUAKEBIBLE",
"https://archive.org/details/QuakeIINetpackIExtremitiesUSAEurope",
"https://archive.org/details/ShrakForQuakeUSA",
"https://archive.org/details/Triada_Russian_CD_Anthology_Quake_Fenklub/",
"https://archive.org/details/XMenTheRavagesOfApocalypseUSA",
"https://archive.org/details/abyss-of-pandemonium",
"https://archive.org/details/actionware_10",
"https://archive.org/details/aftershock-for-quake-1996-head-games-cd",
"https://archive.org/details/aftershockforquakeusa",
"https://archive.org/details/aftershockforquakeusadeluxeedition",
"https://archive.org/details/aftershocktoolboxtheultimatecommandtoolsforquakeusa",
"https://archive.org/details/aw-10",
"https://archive.org/details/blackstarmultimediaquakestar",
"https://archive.org/details/cd-gamer-august-1997-issue-46",
"https://archive.org/details/cd-gamer-christmas-1999-issue-77-oblivion",
"https://archive.org/details/cd-zone-issue-44-november-1996",
"https://archive.org/details/cd_PC_Zone_64_June_1998/",
"https://archive.org/details/cdrom-aftershock-toolbox",
"https://archive.org/details/cdrom-aktiv-no3-duke-nukem-quake-addons-special",
"https://archive.org/details/cdrom-amigaformatcd33",
"https://archive.org/details/cdrom-eternal-darkness",
"https://archive.org/details/cdrom-q2",
"https://archive.org/details/cdrom-qoole-250",
"https://archive.org/details/cdrom-quake-em",
"https://archive.org/details/cdrom-quake-it",
"https://archive.org/details/cdrom-quake-level-master-5",
"https://archive.org/details/cdrom-quake2-total-destruction",
"https://archive.org/details/cdrom-toolkit-for-quake2",
"https://archive.org/details/cdrom-tremor-for-quake",
"https://archive.org/details/complete-gamer-issue-11/",
"https://archive.org/details/darkhourcanada",
"https://archive.org/details/deathmatchmakerusa",
"https://archive.org/details/fault-line",
"https://archive.org/details/game-mania-for-quake",
"https://archive.org/details/game396",
"https://archive.org/details/hardcore_gamer_quake_2",
"https://archive.org/details/juggernautusa",
"https://archive.org/details/juggernautusadeluxeedition/",
"https://archive.org/details/krogersoftwaregmbhquke",
"https://archive.org/details/levelmastervforquakeusa",
"https://archive.org/details/mega-2-addon",
"https://archive.org/details/mod-programming-in-quake-iiiarena",
"https://archive.org/details/next-level",
"https://archive.org/details/pc-gamer-extended-play-collection-volume-1",
"https://archive.org/details/pc-gamer-extended-play-collection-volume-2",
"https://archive.org/details/pc-gaming-world-issue-40-april-2000",
"https://archive.org/details/pc-powerplay-game-guide",
"https://archive.org/details/pc-powerplay-pc-games-issue-21/",
"https://archive.org/details/pc-powerplay-ultimate-quake-3-companion/",
"https://archive.org/details/pc-zone-issue-88-april-2000",
"https://archive.org/details/pcgamer-coverdisc-extended-play-vol-3",
"https://archive.org/details/pcgamer-coverdisc-extended-play-volume-1/",
"https://archive.org/details/pcgamer-coverdisc-extended-play-volume-2/",
"https://archive.org/details/pcppgg2",
"https://archive.org/details/phenomenon_202502",
"https://archive.org/details/q-2-hard",
"https://archive.org/details/q2-authorized-guide-cdrom",
"https://archive.org/details/qedii-level-creator",
"https://archive.org/details/qediilevelcreatorforquakeiihexeniiquakeusa",
"https://archive.org/details/qedlevelcreatorforquakeusa",
"https://archive.org/details/qooleforquakeusa",
"https://archive.org/details/qu-ake",
"https://archive.org/details/quaaake-1",
"https://archive.org/details/quaaake-2",
"https://archive.org/details/quad-damage",
"https://archive.org/details/quake-2-strategy-master/",
"https://archive.org/details/quake-2000/",
"https://archive.org/details/quake-3/",
"https://archive.org/details/quake-ii-netpack-i-extremities-1998-id-software-activision-cd",
"https://archive.org/details/quake-level",
"https://archive.org/details/quake-plus",
"https://archive.org/details/quake-quake-quake-disc-1",
"https://archive.org/details/quake.-1",
"https://archive.org/details/quake_202502",
"https://archive.org/details/quake_abyss",
"https://archive.org/details/quakers-paradise/",
"https://archive.org/details/quark-3",
"https://archive.org/details/qzone-for-quake-1996-wizardworks-cd",
"https://archive.org/details/resurrection-pack-for-quake",
"https://archive.org/details/shrak-for-quake-v2.0-1996-quantum-axcess-cd",
"https://archive.org/details/sidrial-quake-3-total-conversion",
"https://archive.org/details/superdead-expansion-pack",
"https://archive.org/details/superpower_202204",
"https://archive.org/details/superpower_202306",
"https://archive.org/details/the-extended-play-collection-vol-3",
"https://archive.org/details/the-q-2-files-quake",
"https://archive.org/details/time-of-reckoning",
"https://archive.org/details/toolkit-for-quake-1996-10",
"https://archive.org/details/toolkit-for-quake-ii",
"https://archive.org/details/toolkitforquakeiiusa",
"https://archive.org/details/total-conversions-for-quake",
"https://archive.org/details/total-conversions-for-quake-2",
"https://archive.org/details/total-destruction_202506",
"https://archive.org/details/tremorusa",
"https://archive.org/details/tycultureearthquake",
"https://archive.org/details/ultra-collection-level-add-on-quake-duke",
## "https://archive.org/details/ultra-level-add-on-collection-vol1/",
"https://archive.org/details/x-men-the-ravages-of-apocalypse-a-quake-total-conversion-1997-wizardworks-cd",
"https://archive.org/details/zaero",
"https://archive.org/details/zaero4Q2",
"https://archive.org/download/redump_pc_P",
"https://archive.org/details/prodolzhenie-quake-eec",
# other
"https://archive.org/details/pc-game-pro-quake",
"https://archive.org/details/quake-version-shareware-complete",
"https://archive.org/details/complete-gamer-issue-6-quake-ultimate-add-on-disc",
"https://archive.org/details/computer-gaming-world-december-1997-issue-161",
"https://archive.org/details/spel-4",
"https://archive.org/details/maximum-cd-october-2000",
"https://archive.org/details/IDG_GameStar_DE_Special_2002_04_CD",
"https://archive.org/details/20240524",
"https://archive.org/details/cdrom-cdzone88bonus-200004",
"https://archive.org/details/cd-gamer-august-1997-issue-46",
"https://archive.org/details/cd-rom-software-4",
"https://archive.org/details/online-arena-edition-2000",
"https://archive.org/details/the-best-of-select-games-13",
"https://archive.org/details/cd-zone-issue-109-december-2001-cd-2",


]


OUTPUT_DIR = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/ia_cd_index"  # Same as original script
CACHE_DIR = "cache"                # Same cache directory as original script
URLS_FILE = "cds_all_file_urls.txt"   # Separate output: will not overwrite original index
ITEMS_FILE = "cd_items.txt"      # Separate configured-item list
REFRESH_CACHE = False              # True = re-fetch all metadata and disc listings
REQUEST_DELAY_SECONDS = 2.0       # Only applies to network requests
REQUEST_TIMEOUT_SECONDS = 30
MAX_RETRIES = 2
DISC_EXTENSIONS = (".iso", ".img", ".bin", ".nrg", ".mdf", ".isz")
ZIP_EXTENSIONS = (".zip",)
# Prefer all disc images in an item; consider ZIPs only when there are no disc images.  # Archive.org View Contents
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
    refresh = REFRESH_CACHE
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


def item_identifier(item_url):
    """Accept an IA /details/ URL or a bare Internet Archive identifier."""
    item_url = item_url.strip()
    if not item_url:
        raise ValueError("Empty Internet Archive item URL")
    if "://" not in item_url and "/" not in item_url:
        return item_url
    parts = urlsplit(item_url)
    if parts.hostname not in ("archive.org", "www.archive.org"):
        raise ValueError(f"Expected an archive.org item URL: {item_url}")
    path_parts = parts.path.strip("/").split("/")
    if len(path_parts) < 2 or path_parts[0] not in ("details", "download"):
        raise ValueError(f"Expected an archive.org/details/<identifier> URL: {item_url}")
    return unquote(path_parts[1])


def configured_items():
    """Keep input order and silently deduplicate repeated items."""
    items = []
    seen = set()
    for url in ITEM_URLS:
        item = item_identifier(url)
        if item not in seen:
            items.append(item)
            seen.add(item)
    if not items:
        raise ValueError("ITEM_URLS is empty. Add one or more Archive.org details URLs.")
    return items


def images_from_metadata(metadata):
    """Select disc images, or ZIPs only when no disc image exists in an item.

    Uploads may include both an ISO and an unpacked disc_contents/ tree full
    of ZIPs. Indexing the ISO alone avoids processing those nested ZIPs twice.
    """
    files = [f["name"] for f in metadata.get("files", [])
             if isinstance(f.get("name"), str)
             and f.get("source") != "derivative"]
    discs = [name for name in files if name.lower().endswith(DISC_EXTENSIONS)]
    zips = [name for name in files if name.lower().endswith(ZIP_EXTENSIONS)]
    if discs:
        return discs, "disc", len(zips)
    return zips, "zip", 0


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
    items = configured_items()
    print(f"Configured {len(items)} Internet Archive items", flush=True)
    (ROOT / ITEMS_FILE).write_text("\n".join(items) + "\n", encoding="utf-8")

    # Rebuild the text index from scratch every run. Cached HTTP responses
    # mean this normally needs no network traffic after initial fetching.
    # Flush after each disc image or ZIP so interrupted runs leave useful results.
    destination = ROOT / URLS_FILE
    seen = set()
    count = 0
    with destination.open("w", encoding="utf-8") as output:
        for i, item in enumerate(items, 1):
            print(f"[{i}/{len(items)}] {item}", flush=True)
            try:
                metadata_url = f"{BASE}/metadata/{quote(item, safe='')}"
                body, _ = fetch(session, metadata_url, "metadata")
                images, selection, skipped_zips = images_from_metadata(json.loads(body))
            except Exception as exc:
                print(f"  Metadata error: {exc}", file=sys.stderr)
                continue
            if not images:
                print("  No supported disc images or ZIP archives in metadata", flush=True)
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
              "Try REFRESH_CACHE=True to refresh metadata and disc listings.",
              file=sys.stderr)
    print(f"Cached HTML and API responses: {CACHE}")


if __name__ == "__main__":
    main()
