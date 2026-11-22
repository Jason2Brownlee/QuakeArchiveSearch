# import all urls from text file into db, comment out as imported


from db import get_db_connection
from pathlib import Path

# Configuration

TXT_FILES = [
    # crawl dirs
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/dir_targets/q2bot_urls.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/dir_targets/tf_urls.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/dir_targets/qr_urls.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/dir_targets/aq2_urls.txt",

    # # custom internet archive
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/ia_cd_index/user_all_file_urls.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/ia_cd_index/cds_all_file_urls.txt",

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

    # quake archives
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_maddes_net_temp_jason_brownlee.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_aq2world_s3_amazonaws_com_index_html_files.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_clan_rum_org_files.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_quaketastic_com.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_shub_hub_com.txt",

    # ftp mirrors
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_dukeworld_com.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_ftpmirror_infania_net_pub.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_gamers_org.txt",

    # retro
# ongoing
    "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_cd_textfiles_com.txt",
]

BATCH_SIZE = 10000


def import_urls(conn, txt_path):
    """Import URLs from a text file, skipping duplicates."""

    txt_path = Path(txt_path)
    print(f"Processing: {txt_path}")

    added = 0
    processed = 0
    batch = []

    with conn.cursor() as cursor, txt_path.open("r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()

            if not url:
                continue

            # PostgreSQL TEXT cannot contain NUL bytes.
            if "\x00" in url:
                print(f"  Skipping URL containing NUL on line {processed + 1}")
                continue

            batch.append((url,))
            processed += 1

            if len(batch) >= BATCH_SIZE:
                cursor.executemany(
                    "INSERT INTO file_url (file_url) VALUES (%s) ON CONFLICT DO NOTHING",
                    batch
                )
                added += cursor.rowcount
                batch.clear()

        if batch:
            cursor.executemany(
                "INSERT INTO file_url (file_url) VALUES (%s) ON CONFLICT DO NOTHING",
                batch
            )
            added += cursor.rowcount

    conn.commit()

    print(f"  Processed: {processed:,}")
    print(f"  Added:     {added:,}")
    print(f"  Skipped:   {processed - added:,}")

    return added


def main():
    total_added = 0

    with get_db_connection() as conn:
        for txt_file in TXT_FILES:
            total_added += import_urls(conn, txt_file)

    print(f"\nDone. Total new URLs added: {total_added:,}")


if __name__ == "__main__":
    main()
