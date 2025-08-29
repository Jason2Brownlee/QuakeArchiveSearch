# Makefile

WEB=$(CURDIR)/web
DATA=$(CURDIR)/data
SRC=$(CURDIR)/src

PYTHON=/usr/local/bin/python3

.PHONY: server backup check process_crawl process_list process_add clean

# web server
server:
	@cd ${WEB} && ${PYTHON} app.py

# make a backup of the database file
backup:
	@cp ${DATA}/quake_website.db ${DATA}/quake_website2.db

# check db for missing files
check: backup
	@clear
	@cd ${SRC} && ${PYTHON} wishlist_url_checker_db.py

# crawl a list of URLs in a file
process_crawl:
	@cd ${SRC} && ${PYTHON} process_archived_crawl.py

# crawl a list of URLs in the database (not yet processed)
process_list:
	@cd ${SRC} && ${PYTHON} process_archived_list.py

# add URLs to the database to crawl from a text file
process_add:
	@cd ${SRC} && ${PYTHON} quake_websites_add_all.py

# delete garbage from the database make it smaller
clean:
	@cd ${SRC} && ${PYTHON} database_clean.py
