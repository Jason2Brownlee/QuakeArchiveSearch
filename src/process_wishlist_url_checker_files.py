# !/usr/bin/env python3
"""
File Path Matcher - Find wanted files in file path lists
"""

# update:
# I prefer to import all of the urls and search the db  directly....


import os
from pathlib import Path

# CONFIGURATION - Edit these paths
WANTED_FILES_LIST = [
    # '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist.txt',
    '/Users/jasonb/Development/Quake/QuakeNavySeals/research/wishlist.txt',
    '/Users/jasonb/Development/Quake/ThreeWaveCTF/research/wishlist.txt',
    '/Users/jasonb/Development/Quake/TeamFortressQuakeArchive/research/wishlist.txt',
    # '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt',
    # '/Users/jasonb/Development/Quake/Quake2OfficialArchive/research/wishlist.txt',
    # '/Users/jasonb/Development/Quake/Quake3OfficialArchive/research/wishlist.txt',
    # '/Users/jasonb/Development/Quake/Quake2BotArchive/research/wishlist.txt',
    '/Users/jasonb/Development/Quake/QuakeRallyArchive/research/wishlist.txt',
    # '/Users/jasonb/Development/Quake/ActionQuake2Archive/research/wishlist.txt',
    # smaller
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/aop_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/fantasy_quake_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/gno_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/humandebris_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/matrix_quake_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/ninja_quake_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/oxymoron5_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/quaddicted_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/stalker_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/super_quake_wishlist.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/wishlists/viktor_wishlist.txt",
    # Add more wanted files txt files here
]

FILE_PATHS_LIST = [
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/list-cheating-zip.txt",
    # ## "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/list-killer-cds.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/list_fileplanet.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/list-cloud-file-crawl-2025.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/list_all_quake_cds.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/list_quaddicted.txt",

    # custom internet archive
    "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/ia_cd_index/all_files.txt",
    # tastyspleen
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
    # # archives
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_maddes_net_temp_jason_brownlee.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_aq2world_s3_amazonaws_com_index_html_files.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_clan_rum_org_files.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_quaketastic_com.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_shub_hub_com.txt",
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_dukeworld_com.txt",
    "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_www_gamers_org.txt",
    "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_ftpmirror_infania_net_pub.txt",
    # # retro
    # "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/crawl_targets/crawl_cd_textfiles_com.txt",

    # add more file lists here....
]

#!/usr/bin/env python3
"""
File Path Matcher - Find wanted files in file path lists
"""

# Set to True for case-insensitive matching
CASE_INSENSITIVE = True

def load_wanted_files(wanted_files_list):
    """Load all wanted files from the specified txt files into a set."""
    wanted_files = set()

    print(f"Loading wanted files from {len(wanted_files_list)} file(s)...")

    for txt_file in wanted_files_list:
        txt_path = Path(txt_file)
        if not txt_path.exists():
            print(f"Warning: File '{txt_file}' does not exist, skipping...")
            continue

        try:
            with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    filename = line.strip()
                    if filename and not filename.startswith('#'):  # Skip empty lines and comments
                        # Extract just the filename from full paths
                        wanted_files.add(os.path.basename(filename))
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")

    print(f"Loaded {len(wanted_files)} unique wanted files")
    return wanted_files

def process_filepath_file(filepath_file, wanted_files):
    """Process a single file containing file paths and report matches."""
    hits_found = 0

    if not Path(filepath_file).exists():
        print(f"Warning: File '{filepath_file}' does not exist, skipping...")
        return 0

    try:
        with open(filepath_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                filepath = line.strip()
                if not filepath or filepath.startswith('#'):  # Skip empty lines and comments
                    continue

                # Check if any wanted file is present anywhere in this line
                for wanted_file in wanted_files:
                    search_line = filepath.lower()
                    search_wanted = wanted_file.lower()

                    if search_wanted in search_line:
                        print(f"\t'{wanted_file}' found in: {filepath}")
                        hits_found += 1
                        break  # Found a match, no need to check other wanted files for this line

    except Exception as e:
        print(f"Error processing {filepath_file}: {e}")
        return 0

    return hits_found

def main():
    # Load all wanted files into memory
    wanted_files = load_wanted_files(WANTED_FILES_LIST)

    if not wanted_files:
        print("No wanted files loaded. Exiting.")
        return

    # Make matching case-insensitive if requested
    if CASE_INSENSITIVE:
        wanted_files = {f.lower() for f in wanted_files}
        print("Using case-insensitive matching")

    print(f"\nProcessing {len(FILE_PATHS_LIST)} file path list(s)...")
    print("=" * 50)

    total_hits = 0

    for filepath_file in FILE_PATHS_LIST:
        filename = os.path.basename(filepath_file)
        print(f"\nProcessing: {filename}")

        hits = process_filepath_file(filepath_file, wanted_files)
        total_hits += hits
        
        # print(f"Found {hits} hit(s) in {filepath_file}")
    
    print("=" * 50)
    print(f"Total hits found: {total_hits}")

if __name__ == "__main__":
    main()