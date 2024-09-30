#!/bin/sh

PYTHON=/usr/local/bin/python3
DATA=../data

# clear the screen
clear

# just once
# make a copy of the sqlite database file
cp ${DATA}/quake_website.db ${DATA}/quake_website2.db
# check the database for new urls
${PYTHON} ./wishlist_url_checker_db.py

# # Infinite loop
# while true
# do
# 	# make a copy of the sqlite database file
# 	cp ${DATA}/quake_website.db ${DATA}/quake_website2.db
# 	# check the database for new urls
# 	${PYTHON} ./wishlist_url_checker_db.py
# 	# wait a moment before trying again
# 	sleep 60
# done