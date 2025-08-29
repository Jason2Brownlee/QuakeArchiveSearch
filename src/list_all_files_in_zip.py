# List all files in a zip, recursively

import zipfile
import os
import tempfile
import shutil
from typing import List, Set
from pathlib import Path

def explore_zip_recursive(zip_path: str, prefix: str = "", visited: Set[str] = None, temp_dir: str = None, output_file = None) -> List[str]:
    """
    Recursively explore a zip file and return a list of all files found,
    including files within nested zip files and exe files treated as zip archives.
    Uses temporary files for large nested archives instead of loading into memory.

    Args:
        zip_path: Path to the zip file
        prefix: Path prefix to prepend to file paths
        visited: Set of already visited zip files to prevent infinite recursion
        temp_dir: Temporary directory for extracting nested archives
        output_file: Open file handle to write found files to as we find them

    Returns:
        List of file paths with zip prefixes
    """
    if visited is None:
        visited = set()

    if temp_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="zip_explorer_")

    file_list = []

    try:
        if zip_path in visited:
            return file_list  # Prevent infinite recursion
        visited.add(zip_path)

        current_prefix = f"{prefix}{os.path.basename(zip_path)}/"

        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            for file_info in zip_file.filelist:
                file_path = file_info.filename
                full_path = current_prefix + file_path

                # Add current file to list
                file_list.append(full_path)

                # Report progress and save to file
                print(f">{full_path}")
                if output_file:
                    output_file.write(full_path + '\n')
                    output_file.flush()  # Ensure immediate write to disk

                # Check if file is a zip or exe that we should try to open
                if (file_path.lower().endswith(('.zip', '.exe')) and
                    not file_info.is_dir()):

                    try:
                        # Create a temporary file for the nested archive
                        temp_file_path = os.path.join(temp_dir, f"nested_{len(file_list)}.tmp")

                        print(f"Extracting nested archive: {full_path} (Size: {file_info.file_size:,} bytes)")

                        # Check if the nested file is too large (you can adjust this threshold)
                        MAX_NESTED_SIZE = 2 * 1024 * 1024 * 1024  # 2GB limit for nested files
                        if file_info.file_size > MAX_NESTED_SIZE:
                            print(f"Warning: Skipping {full_path} - too large ({file_info.file_size:,} bytes)")
                            continue

                        # Extract nested archive to temporary file
                        with zip_file.open(file_path) as source:
                            with open(temp_file_path, 'wb') as dest:
                                # Copy in chunks to avoid memory issues
                                chunk_size = 64 * 1024  # 64KB chunks
                                while True:
                                    chunk = source.read(chunk_size)
                                    if not chunk:
                                        break
                                    dest.write(chunk)

                        # Recursively explore the nested archive
                        nested_files = explore_zip_recursive(
                            temp_file_path,
                            full_path + "/",
                            visited.copy(),  # Use a copy to avoid shared state in recursion
                            temp_dir,
                            output_file
                        )
                        file_list.extend(nested_files)

                        # Clean up the temporary file immediately
                        try:
                            os.unlink(temp_file_path)
                        except OSError:
                            pass

                    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError):
                        # Skip if the exe/zip file cannot be opened as a zip
                        print(f"Info: Could not open {full_path} as zip archive (likely not a zip file)")
                    except MemoryError:
                        print(f"Warning: Not enough memory to extract {full_path}")
                    except OSError as e:
                        print(f"Warning: Disk space or I/O error extracting {full_path}: {e}")
                    except Exception as e:
                        # Skip any other errors (corrupted files, etc.)
                        print(f"Warning: Could not process {full_path}: {e}")

    except (zipfile.BadZipFile, zipfile.LargeZipFile, FileNotFoundError, RuntimeError) as e:
        print(f"Error: Could not open zip file {zip_path}: {e}")
    except Exception as e:
        print(f"Unexpected error processing {zip_path}: {e}")

    return file_list

def get_disk_space_gb(path: str) -> float:
    """Get available disk space in GB for the given path."""
    try:
        statvfs = os.statvfs(path)
        return (statvfs.f_bavail * statvfs.f_frsize) / (1024**3)
    except AttributeError:
        # Windows
        import shutil
        total, used, free = shutil.disk_usage(path)
        return free / (1024**3)

def main():
    # Hard-coded paths - CHANGE THESE PATHS
    # ZIP_FILE_PATH = "/Users/jasonb/Games/QuakeFiles/quake-cloud-08-2025.zip"
    # OUTPUT_FILE_PATH = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/cloud-file-list-2025.txt"

    ZIP_FILE_PATH = "/Users/jasonb/Games/QuakeFiles/cheating-20230420T202208Z-001.zip"
    OUTPUT_FILE_PATH = "/Users/jasonb/Development/Quake/QuakeArchiveSearch/data/cheating-list-2025.txt"


    print(f"Exploring zip file: {ZIP_FILE_PATH}")
    print(f"Output will be saved to: {OUTPUT_FILE_PATH}")

    # Check if the zip file exists and get its size
    if not os.path.exists(ZIP_FILE_PATH):
        print(f"Error: Zip file not found: {ZIP_FILE_PATH}")
        return

    zip_size_gb = os.path.getsize(ZIP_FILE_PATH) / (1024**3)
    print(f"Zip file size: {zip_size_gb:.2f} GB")

    # Check available disk space
    temp_dir = tempfile.gettempdir()
    available_space_gb = get_disk_space_gb(temp_dir)
    print(f"Available disk space in temp directory ({temp_dir}): {available_space_gb:.2f} GB")

    if available_space_gb < zip_size_gb * 0.5:  # Want at least 50% of zip size available
        print(f"Warning: Low disk space. You may need at least {zip_size_gb * 0.5:.2f} GB free for safe operation.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return

    print("=" * 50)

    # Create a temporary directory for nested archives
    temp_dir = tempfile.mkdtemp(prefix="zip_explorer_")

    try:
        print(f"Using temporary directory: {temp_dir}")
        print("Starting exploration...")
        print("=" * 50)

        # Open output file for writing
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as output_file:
            # Get all files recursively
            all_files = explore_zip_recursive(ZIP_FILE_PATH, temp_dir=temp_dir, output_file=output_file)

        print("=" * 50)
        print(f"Exploration complete!")
        print(f"Total files found: {len(all_files)}")
        print(f"All file paths saved to: {OUTPUT_FILE_PATH}")

    except IOError as e:
        print(f"Error: Could not write to output file {OUTPUT_FILE_PATH}: {e}")
        return

    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up temporary directory {temp_dir}: {e}")

if __name__ == "__main__":
    main()

