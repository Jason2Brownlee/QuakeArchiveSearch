import sqlite3
import re
from urllib.parse import urlparse
from collections import defaultdict
from tqdm import tqdm

DATABASE = '../data/quake_website.db'

def connect_read_only(db_path):
    """Connect to the SQLite database in read-only mode."""
    uri = f'file:{db_path}?mode=ro'
    return sqlite3.connect(uri, uri=True)

# Define the number of top domains to display
TOP_N = 100  # Change this to set the number of top domains to display

# Connect to the SQLite database
conn = connect_read_only(DATABASE)
cursor = conn.cursor()

# SQL query to extract all URLs
query = "SELECT file_url FROM File_URL"
cursor.execute(query)

# Fetch all URLs from the database
urls = cursor.fetchall()

# Use a dictionary to count the number of .zip files for each domain
domain_zip_count = defaultdict(int)

# Function to extract domain from URL
def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except Exception as e:
        return None

# Process each URL and count .zip files per domain
print("Processing URLs...")
for (url,) in tqdm(urls, desc="Processing URLs"):
    domain = extract_domain(url)
    if domain:
        # Check if the URL ends with .zip (case insensitive)
        if re.search(r'\.zip$', url, re.IGNORECASE):
            domain_zip_count[domain] += 1

# Sort the domains by the number of .zip files in descending order
sorted_domains = sorted(domain_zip_count.items(), key=lambda x: x[1], reverse=True)

# Display the top N domains with the most .zip files
print(f"\nTop {TOP_N} Domains with the Most .zip Files:")
print(f"{'Domain':<50} {'# of .zip Files'}")
print("-" * 60)
for domain, count in sorted_domains[:TOP_N]:
    print(f"{domain:<50} {count}")

# Close the database connection
conn.close()


# Top 10 Domains with the Most .zip Files:
# Domain                                             # of .zip Files
# ------------------------------------------------------------
# www.quaddicted.com                                 153167
# www.gamers.org                                     117122
# cd.textfiles.com                                   81098
# ftp.jussieu.fr                                     64471
# src.doc.ic.ac.uk                                   63112
# ftp.sunet.se                                       59213
# ftp.tu-clausthal.de                                43797
# www.fortunecity.com                                42633
# sunsite.doc.ic.ac.uk                               32729
# sunsite.org.uk                                     26345


# Top 100 Domains with the Most .zip Files:
# Domain                                             # of .zip Files
# ------------------------------------------------------------
# www.quaddicted.com                                 153167
# www.gamers.org                                     117122
# cd.textfiles.com                                   81098
# ftp.jussieu.fr                                     64471
# src.doc.ic.ac.uk                                   63112
# ftp.sunet.se                                       59213
# ftp.tu-clausthal.de                                43797
# www.fortunecity.com                                42633
# sunsite.doc.ic.ac.uk                               32729
# sunsite.org.uk                                     26345
# ftp.epix.net                                       25983
# ftpmirror1.infania.net                             25679
# www.cdrom.com                                      24060
# crydee.sai.msu.ru                                  22128
# ftp.fu-berlin.de                                   21240
# mirrors.syringanetworks.net                        21181
# youfailit.net                                      21001
# gamers.org                                         19419
# www.retroarchive.org                               18110
# dukeworld.duke4.net                                17056
# ftp.telepac.pt                                     15130
# members.nbci.com                                   13369
# geocities.com                                      12767
# www.mmnt.net                                       12104
# www.3ddownloads.com                                10542
# annex.retroarchive.org                             10229
# www.dreamlandbbs.com                               8444
# www.geocities.com                                  8427
# ftp.sun.ac.za                                      8105
# www.btinternet.com                                 8101
# mirror.its.dal.ca                                  7531
# wcarchive.cdrom.com                                7173
# home.sol.no                                        7097
# www.xs4all.nl                                      6717
# mirrors.telepac.pt                                 5276
# mirror.aarnet.edu.au                               4994
# public.planetmirror.com                            4819
# www.algonet.se                                     4607
# www.time2quake.com                                 4355
# dukeworld.com                                      3873
# ftp.cdrom.com                                      3732
# web.ukonline.co.uk                                 3720
# ftp.infomagic.com                                  3640
# ftp.gamers.org                                     3620
# 3ddownloads.com                                    2910
# www.gamesmania.com                                 2878
# ftp.mancubus.net                                   2628
# www.quaketastic.com                                2336
# www.planetquake.com                                2281
# ftp.zx.net.nz                                      2105
# aminet.net                                         1849
# www.inlink.com                                     1691
# ftp.volftp.vol.it                                  1619
# www.botepidemic.com                                1572
# ftp.3dgamers.com                                   1392
# webpages.charter.net                               1363
# www.dragonfire.net                                 1315
# luna.gui.uva.es                                    1186
# planetmirror.com                                   1110
# web.inter.nl.net                                   1055
# www.aminet.net                                     1040
# www.acc.umu.se                                     977
# ftp.stomped.com                                    975
# classicdosgames.com                                964
# pages.infinit.net                                  948
# www.bluesnews.com                                  947
# ftp.chg.ru                                         941
# doomgate.gamers.org                                938
# ftp.freesoftware.com                               815
# www.dra.nl                                         803
# www.snowcrest.net                                  780
# people.wiesbaden.netsurf.de                        776
# public.ftp.planetmirror.com                        761
# ftp.saix.net                                       738
# www.scitechsoft.com                                705
# www2.passagen.se                                   694
# apogee1.com                                        679
# www.fileplanet.com                                 678
# www.gamesdomain.co.uk                              671
# www.whiterock.com                                  636
# www.intercity.dk                                   611
# quaketastic.com                                    547
# download.gamespot.com                              524
# ftp.task.gda.pl                                    523
# asp.planetquake.com                                518
# www.classicdosgames.com                            497
# www.gibbed.com                                     478
# sunsite.unc.edu                                    463
# mrelusive.com                                      460
# quakemecca.simplenet.com                           454
# reality.sgi.com                                    449
# dd.networx.net.au                                  432
# archive.uwp.edu                                    431
# www.quake2.com                                     425
# www.powerup.com.au                                 421
# www.hover.net                                      419
# quake.errorabove.com                               410
# www.richwhitehouse.com                             407
# www.happypuppy.com                                 404
# www.meccaworld.com                                 404