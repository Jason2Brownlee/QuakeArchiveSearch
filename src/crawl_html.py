# Crawls HTML directory listings under base URLs, caches pages by URL hash, and writes all URLs found to text files.

import hashlib
import os
import re
import time
import urllib.request
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET
from urllib.parse import quote

# ---- settings ----
BASE_URLS = [
    # quake clan
    # "http://www.clan-rum.org/files/",

    # quake files
    # "https://www.quaketastic.com/",

    # q2 stuff
    # "https://tastyspleen.net/quake/downloads/",
    # "https://realistic.tastyspleen.net/",
    # "https://badbrent.tastyspleen.net/",
    # "https://barton.tastyspleen.net/",
    # "https://cheaters-r-scum.tastyspleen.net/",
    # "https://deathstalker.tastyspleen.net/",
    # "https://gator.tastyspleen.net/",
    # "https://gouki.tastyspleen.net/",
    # "https://huwahumph.tastyspleen.net/",
    # "https://inhuman.tastyspleen.net/",
    # "https://jdolan.tastyspleen.net/",
    # "https://reflex.tastyspleen.net/",
    # "https://sofiene.tastyspleen.net/",
    # "https://towlie.tastyspleen.net/",

    # quake
    # "https://shub-hub.com/",
    # "https://www.maddes.net/temp/jason.brownlee/",

    # aq2
    # "https://aq2world.s3.amazonaws.com/index.html#files/",

    # ftp
    # "https://dukeworld.com/",
    # "https://ftpmirror.infania.net/pub/",
    "https://www.gamers.org/",
##    "https://www.quaddicted.com/files/",

    # generic retro
    "http://cd.textfiles.com/",

    # need to rework so it can visit http://annex.retroarchive.org/
    # "http://www.retroarchive.org/",

    # general quake
    "https://archives.aq2world.com/",
    "https://www.quaketerminus.com/",
    "https://www.geocities.ws/oldquaker/",
    "https://www.randars.com/bots/",

]

SKIP_PATTERNS = [        # URLs containing any of these are ignored entirely
    # generally
    "/README",
    "/CHANGES",
    "/REJECTS",
    "/00cheats",
    # https://ftpmirror.infania.net/pub/
    "/pub/Hobbes/",
    "/pub/pc/",
    "/pub/simtelnet/",
    "/pub/turnkeylinux/",
    # gamers.org
    "/pub/archives/plans/",
    "/pub/archives/doom/articles/1995/",
    "/pub/archives/quake/articles/",
    "/uwp-uml/romulus/hints/",
    "/pub/archives/idNews/",
]

OUTPUT_DIR = "../data/crawl_downloads"  # cached pages go in OUTPUT_DIR/<domain>/<hash>
TARGETS_DIR = "../data/crawl_targets"   # URL lists go in TARGETS_DIR/crawl_<base>.txt

FORCE_REDOWNLOAD = False                # True = ignore cache and fetch everything again
LIST_OUT_OF_SCOPE = True   # True = list every link found; crawling stays limited to the base

DELAY_SECONDS = 5                      # pause after each network request
TIMEOUT_SECONDS = 10

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
PAGE_EXTENSIONS = {"", ".html", ".htm", ".php", ".asp", ".aspx", ".jsp"}
# --------------------------

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append(value.strip())


def normalize(url):
    p = urlsplit(url)
    d = parse_qs(p.query).get("dir")
    query = urlencode({"dir": d[0]}, safe="/") if d else ""   # keep only ?dir=
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, query, ""))

def skipped(url):
    u = url.lower()
    return any(s.lower() in u for s in SKIP_PATTERNS)

def url_hash(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def looks_like_page(url):
    path = urlsplit(url).path
    return path.endswith("/") or os.path.splitext(path)[1].lower() in PAGE_EXTENSIONS


def in_scope(url, base):
    u, b = urlsplit(url), urlsplit(base)
    ud = parse_qs(u.query).get("dir", [""])[0]
    bd = parse_qs(b.query).get("dir", [""])[0]
    dir_ok = not bd or (ud + "/").startswith(bd.rstrip("/") + "/")
    return u.netloc == b.netloc and u.path.startswith(b.path) and dir_ok


def get_page(url, domain_dir, html_only=True):
    """Return (final_url, html) from cache or the network, or None if not an HTML page / failed."""
    cache_path = os.path.join(domain_dir, url_hash(url))

    if os.path.exists(cache_path) and not FORCE_REDOWNLOAD:
        with open(cache_path, encoding="utf-8") as f:
            final_url = f.readline().rstrip("\n")
            return final_url, f.read()

    print(f"  downloading {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if html_only and "text/html" not in ctype.lower():
                print(f"  skipped (not html: {ctype})")
                return None
            charset = resp.headers.get_content_charset() or "utf-8"
            html = resp.read().decode(charset, errors="replace")
            final_url = resp.geturl()
        # first line of the cache file is the real url (after any redirects), rest is the html
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(final_url + "\n" + html)
        return final_url, html
    except Exception as e:
        print(f"  FAILED {url}: {e}")
        return None
    finally:
        time.sleep(DELAY_SECONDS)


def crawl(base):
    base = normalize(base)
    if not base.endswith("/") and "?" not in base:
        base += "/"
    print(f"\n=== {base}")

    domain_dir = os.path.join(OUTPUT_DIR, urlsplit(base).netloc.replace(":", "_"))
    os.makedirs(domain_dir, exist_ok=True)
    os.makedirs(TARGETS_DIR, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9]+", "_", base.split("://", 1)[-1]).strip("_")
    target_path = os.path.join(TARGETS_DIR, f"crawl_{name}.txt")

    queue = [base]
    seen = {base}
    found = set()

    while queue:
        page_url = queue.pop(0)
        page = get_page(page_url, domain_dir)
        if page is None:
            continue
        final_url, html = page

        parser = LinkParser()
        parser.feed(html)

        for href in parser.links:
            if href.startswith(("mailto:", "javascript:", "#")):
                continue
            full = normalize(urljoin(final_url, href))

            if not LIST_OUT_OF_SCOPE and not in_scope(full, base):
                continue
            if full not in found:
                found.add(full)
                print(full)

            # only crawl in-scope, non-skipped, page-looking links
            if full in seen or skipped(full) or not in_scope(full, base) or not looks_like_page(full):
                continue
            seen.add(full)
            queue.append(full)

        # rewrite after every page so a killed run still leaves a usable file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(found)) + "\n")

    print(f"=== done: {len(found)} urls -> {target_path}")

def is_s3(url):
    return urlsplit(url).netloc.lower().endswith(".s3.amazonaws.com")


def crawl_s3(base):
    p = urlsplit(base)
    prefix = p.fragment                      # "#files/" -> "files/"
    root = f"{p.scheme}://{p.netloc}"
    print(f"\n=== {base} (s3 listing, prefix '{prefix}')")

    domain_dir = os.path.join(OUTPUT_DIR, p.netloc.replace(":", "_"))
    os.makedirs(domain_dir, exist_ok=True)
    os.makedirs(TARGETS_DIR, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9]+", "_", base.split("://", 1)[-1]).strip("_")
    target_path = os.path.join(TARGETS_DIR, f"crawl_{name}.txt")

    found = []
    token = None
    while True:
        api = f"{root}/?list-type=2&prefix={quote(prefix)}"
        if token:
            api += "&continuation-token=" + quote(token, safe="")
        page = get_page(api, domain_dir, html_only=False)
        if page is None:
            break
        token = None
        for el in ET.fromstring(page[1]).iter():
            tag = el.tag.split("}")[-1]      # strip the XML namespace
            if tag == "Key":
                url = f"{root}/{quote(el.text)}"
                found.append(url)
                print(url)
            elif tag == "NextContinuationToken":
                token = el.text
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(found)) + "\n")
        if not token:
            break

    print(f"=== done: {len(found)} urls -> {target_path}")

if __name__ == "__main__":
    for base_url in BASE_URLS:
        crawl_s3(base_url) if is_s3(base_url) else crawl(base_url)
