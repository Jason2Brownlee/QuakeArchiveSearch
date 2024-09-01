# Quake Archive Search

This project provides a searchable index of all known Quake file URLs.

* Discover the existence of quake releases (mods, maps, patches, etc.)
* Discover historical URLs where files were hosted and could be downloaded.

## Problem

The Quake community has produced a vast amount of content over the years, including mods, maps, texture packs, and other files. However, as time passes, many of these files become difficult to locate due to broken links, defunct websites, and scattered hosting locations. This situation makes it challenging for Quake enthusiasts to discover, access, and preserve this valuable content.

## Solution

The Quake Archive Search project addresses this issue by providing a comprehensive database and search tool for Quake 1 file URLs. Key features include:

- A centralized index of known Quake file URLs
- Powerful search capabilities, including wildcard support
- Integration with the Internet Archive's Wayback Machine for accessing archived versions of files
- Tools for creating and updating the file archive from various sources
- A user-friendly web interface built with Flask
- Python scripts for programmatic access to the database

This project aims to serve as a vital resource for the Quake community, enabling easier discovery and preservation of Quake-related content.

## Why Not Just Use the Wayback Machine?

While the Internet Archive's Wayback Machine is an invaluable resource for accessing archived web content, it has limitations when it comes to discovering and accessing Quake-related files across multiple websites:

1. Limited Cross-Site Search: The Wayback Machine only allows searching within one website at a time. Our Quake Archive Search enables users to **search across all archived websites simultaneously**, greatly expanding the scope of discoverable content.

2. No Archive Crawling: The Wayback Machine doesn't crawl the content of archived webpages. This means that files and URLs listed within archived pages remain hidden unless manually inspected. Our tool **actively crawls and indexes the content of archived webpages**, uncovering a wealth of previously inaccessible Quake file URLs.

3. Quake-Specific Focus: Unlike the general-purpose Wayback Machine, our tool is **tailored specifically for the archived Quake webpages**. It understands the context of Quake file types, hosting patterns, and community-specific resources.

4. Aggregation and Standardization: We collect URLs from various sources, standardize their format, and remove duplicates, providing a clean, unified database of Quake file locations.

By addressing these specific issues, the Quake Archive Search project complements the Wayback Machine, offering a more powerful and targeted solution for preserving and accessing the rich history of Quake content.