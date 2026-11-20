# import all urls from text file into db


import sqlite3
from pathlib import Path

# Configuration
DB_PATH = '../data/quake_website.db'

TXT_FILES = [
    # # custom internet archive
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/ia_cd_index/all_files.txt",
    # # tastyspleen
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_badbrent_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_barton_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_cheaters_r_scum_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_deathstalker_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_gator_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_gouki_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_huwahumph_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_inhuman_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_jdolan_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_realistic_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_reflex_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_sofiene_tastyspleen_net.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_tastyspleen_net_quake_downloads.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_towlie_tastyspleen_net.txt",
    # # # archives
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_maddes_net_temp_jason_brownlee.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_aq2world_s3_amazonaws_com_index_html_files.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_clan_rum_org_files.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_quaketastic_com.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_shub_hub_com.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_dukeworld_com.txt",

    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_ftpmirror_infania_net_pub.txt",
    "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_gamers_org.txt",
    # retro
    ##"/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_cd_textfiles_com.txt",
]

BATCH_SIZE = 10000


def import_urls(conn, txt_path):
    """Import URLs from a text file, skipping duplicates."""

    txt_path = Path(txt_path)
    print(f"Processing: {txt_path}")

    before = conn.total_changes
    processed = 0
    batch = []

    with txt_path.open("r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()

            if not url:
                continue

            batch.append((url,))
            processed += 1

            if len(batch) >= BATCH_SIZE:
                conn.executemany(
                    "INSERT OR IGNORE INTO File_URL (file_url) VALUES (?)",
                    batch
                )
                batch.clear()

        if batch:
            conn.executemany(
                "INSERT OR IGNORE INTO File_URL (file_url) VALUES (?)",
                batch
            )

    conn.commit()

    added = conn.total_changes - before
    print(f"  Processed: {processed:,}")
    print(f"  Added:     {added:,}")
    print(f"  Skipped:   {processed - added:,}")

    return added


def main():
    total_added = 0

    with sqlite3.connect(DB_PATH) as conn:
        for txt_file in TXT_FILES:
            total_added += import_urls(conn, txt_file)

    print(f"\nDone. Total new URLs added: {total_added:,}")


if __name__ == "__main__":
    main()
