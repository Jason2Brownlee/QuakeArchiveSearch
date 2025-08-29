import sys
import os

def read_filenames(filename_list_path):
    """Read filenames from a text file and return a list with whitespace trimmed."""
    try:
        with open(filename_list_path, 'r') as f:
            filenames = [line.strip() for line in f if line.strip()]
        return filenames
    except FileNotFoundError:
        print(f"Error: Could not find filename list file: {filename_list_path}")
        return []
    except Exception as e:
        print(f"Error reading filename list: {e}")
        return []

def check_files_in_ascii(filenames, ascii_file_path):
    """Check if filenames exist as strings in the ASCII file and report missing ones immediately."""
    try:
        with open(ascii_file_path, 'r') as f:
            ascii_content = f.read().lower()

        not_found_count = 0
        print("\nFiles NOT FOUND in target:")

        for filename in filenames:
            # Case insensitive string-in-string check
            found = filename.lower() in ascii_content
            if not found:
                print(f"  {filename}")
                not_found_count += 1

        if not_found_count == 0:
            print("  None - all files found!")

        return not_found_count

    except FileNotFoundError:
        print(f"Error: Could not find ASCII file: {ascii_file_path}")
        return -1
    except Exception as e:
        print(f"Error reading ASCII file: {e}")
        return -1

def main(filename_list_path, ascii_file_path):
    """Main function to process files and display results."""
    print(f"Reading filenames from: {filename_list_path}")
    print(f"Checking against ASCII file: {ascii_file_path}")
    print("-" * 50)

    # Read the list of filenames
    filenames = read_filenames(filename_list_path)
    if not filenames:
        print("No filenames to process.")
        return

    # Sort filenames (case insensitive)
    filenames.sort(key=str.lower)

    print(f"Found {len(filenames)} filenames to check")

    # Check each filename in the ASCII file and report missing ones immediately
    not_found_count = check_files_in_ascii(filenames, ascii_file_path)
    if not_found_count == -1:
        print("Could not process ASCII file.")
        return

    print(f"\nSummary: {not_found_count}/{len(filenames)} files not found in ASCII file")

if __name__ == "__main__":

    # Quake2
    # FILENAME_LIST_PATH = "../data/quake2_files.txt"
    # ASCII_FILE_PATH = "/Users/jasonb/Development/Quake/Quake2OfficialArchive/README.md"

    # Quake3
    FILENAME_LIST_PATH = "../data/quake3_files.txt"
    ASCII_FILE_PATH = "/Users/jasonb/Development/Quake/Quake3OfficialArchive/README.md"
    
    main(FILENAME_LIST_PATH, ASCII_FILE_PATH)