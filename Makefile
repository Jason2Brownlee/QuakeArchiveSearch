# Makefile

WEB=$(CURDIR)/web
DATA=$(CURDIR)/data
SRC=$(CURDIR)/src
BACKUP=$(CURDIR)/data/backup

PYTHON=/usr/local/bin/python3

.PHONY: server check_db check_files wayback_crawl web_crawl wayback_add \
	wayback_list import_filelists cd_crawl extract_links db_health \
	db-backup

# web server
server:
	@cd ${WEB} && ${PYTHON} app.py

# wishlist checkers
# =================

# check db for missing files
check_db:
	@clear
	@cd ${SRC} && ${PYTHON} process_wishlist_url_checker_db.py

# check manual indexes text files
check_files:
	@clear
	@cd ${SRC} && ${PYTHON} process_wishlist_url_checker_files.py

# crawlers
# =================

# crawl wayback for a list of URLs in a file
wayback_crawl:
	@cd ${SRC} && ${PYTHON} process_crawl_wayback.py

# crawl open web for a list of URLs in a file
web_crawl:
	@cd ${SRC} && ${PYTHON} process_crawl_web.py

# crawl directories for urls and report to file
dir_crawl:
	@cd ${SRC} && ${PYTHON} process_crawl_directory.py

# crawl all cds uploaded for user on internet archive
cd_crawl:
	@cd ${SRC} && ${PYTHON} process_index_internet_archive_cds.py

# extract all links from a page
extract_links:
	@cd ${SRC} && ${PYTHON} process_extract_all_links.py

# wayback index
# =================

# add URLs to the database to crawl from a text file
wayback_add:
	@cd ${SRC} && ${PYTHON} process_wayback_add_all.py

# crawl a list of URLs in the database (not yet processed)
wayback_list:
	@cd ${SRC} && ${PYTHON} process_wayback_list_all.py

# delete all urls in the temp table, use when wayback_list get's stuck
wayback_delete:
	@cd ${SRC} && ${PYTHON} process_wayback_delete_all.py

# url imports
# =================

# import urls in text files into db
import_filelists:
	@cd ${SRC} && ${PYTHON} process_import_file_lists_db.py


# database
# =================

# after a large import
db_health:
	@echo "Updating PostgreSQL statistics..."
	@psql -d quake_archive -c "ANALYZE file_url;"
	@echo "\nDatabase health:"
	@psql -d quake_archive -c "SELECT relname AS table_name, n_live_tup AS estimated_rows, n_dead_tup AS dead_rows, last_autovacuum, last_autoanalyze FROM pg_stat_user_tables ORDER BY relname;"
	@echo "\nDatabase sizes:"
	@psql -d quake_archive -c "SELECT relname AS table_name, pg_size_pretty(pg_relation_size(relid)) AS table_size, pg_size_pretty(pg_indexes_size(relid)) AS index_size, pg_size_pretty(pg_total_relation_size(relid)) AS total_size FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC;"

.PHONY: db-backup db-backup-fast

# Compressed backup (one file, good compression)
BACKUP_DATE := $(shell date +%Y%m%d_%H%M%S)
db-backup:
	@mkdir -p $(BACKUP)
	@echo "Backing up PostgreSQL database..."
	@pg_dump -d quake_archive -Fc -Z zstd:3 \
		-f $(BACKUP)/quake_archive_$(BACKUP_DATE).dump
	@echo "Backup complete:"
	@ls -lh $(BACKUP)/quake_archive_$(BACKUP_DATE).dump


