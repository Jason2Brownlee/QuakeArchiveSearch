# Quake Archive Search

This project provides a searchable index of all known Quake file URLs.

* Discover the existence of quake releases (mods, maps, patches, etc.)
* Discover historical URLs where files were hosted and could be downloaded.

## Problem

Quake archiving involves locating and hosting all released files.

This might be focused on a theme (e.g. all releases of all quake bots in the [quake bot archive](https://github.com/Jason2Brownlee/QuakeBotArchive)).

This might be focused on a single mod (e.g. all releases of 3wavectf in the [three wave ctf archive](https://github.com/Jason2Brownlee/ThreeWaveCTF))

Quake file archiving involves two activities:

1. Discovering what files were released.
	a. Searching URL lists in the wayback machine for individual quake websites.
	b. Google searches
	c. Searches of USENET archives.
	d. Searches of file lists for individual quake CDs (magazines, complications, etc.)
	e. Manually reading news posts on historical quake webpages.
	f. Manually reading download pages for quake mod webpages.
	g. Manually reading USENET posts.
	h. etc.
2. Acquiring a copy of all known files
	a. Download from archive.org
	b. Downloading from the internet.
	c. Downloading from another archive.


Discovering what files exist is time consuming.

It typically involves manually reading and manually searching old quake news posts for mention of the quake mod under study and discovering mention and URL links to the mod.

Once a filename release convention for the mod is established, we can search on google, usenet, and url archives in the wayback machine for specific websites.

## Solution

What is needed is an index of all known Quake file URLs.

This will help in two ways:

1. Help to locate all versions of a mod using wildcards.
2. List all location where the file was known to have been hosted.

For example, if we know that frogbot releases were released like `frogbot007.zip`, then we can search all known URLs with a wildcard search like `frogbot00*.zip`. This will expose releases like `frogbot005.zip` and `frogbot003.zip` but perhaps less widly known releases like `frogbot011a.zip` and `frogbot012b.zip`.

Once we know what files to acquire, we need to know real URLs for where these files were hosted historically. This is so we can check if they were archived in the wayback machine and acquire them.

Other places to look for the preservation of the URLs includes:

* Game magazine CDs and distinct FTP archives, both already searchable by [discmaster](http://discmaster.textfiles.com/search).
* BBS CD archives, already searchable by [textfiles](https://textfiles.com/)
* Google is less reliable as a file search engine, but sometimes will discover a result.


