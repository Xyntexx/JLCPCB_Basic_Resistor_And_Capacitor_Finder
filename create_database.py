# $ wget https://yaqwsx.github.io/jlcparts/data/cache.zip
# $ wget https://yaqwsx.github.io/jlcparts/data/cache.z01
# $ wget https://yaqwsx.github.io/jlcparts/data/cache.z02

import urllib.request
import os
import zipfile
import glob
import subprocess
import sys
import shutil

CACHE_DIR = "cache_downloads"


def download_file(url):
    # Download file from internet
    os.makedirs(CACHE_DIR, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(CACHE_DIR, filename)
    print("Downloading " + filename + "...")
    urllib.request.urlretrieve(url, filepath)


def download_files():
    #     = # Download file from internet
    url = "https://yaqwsx.github.io/jlcparts/data/cache.zip"

    download_file(url)
    i = 1
    while True:
        try:
            url = "https://yaqwsx.github.io/jlcparts/data/cache.z" + f"{i:02d}"
            download_file(url)
            i += 1
        except:
            print("File does not exist")
            break


def create_database():
    # Extract database from downloaded files
    print("Extracting database archive...")

    # Check if split parts exist (cache.z01, cache.z02, etc.)
    split_parts = sorted(glob.glob(os.path.join(CACHE_DIR, "cache.z[0-9][0-9]")))
    zip_file = os.path.join(CACHE_DIR, "cache.zip")

    if split_parts:
        # Multi-volume ZIP archive detected
        print(f"Found {len(split_parts)} split archive parts")

        try:
            # Try using patoolib which can handle split archives via 7-Zip
            import patoolib
            print("Extracting using patoolib...")
            patoolib.extract_archive(zip_file, outdir=".")
            print("Extraction complete!")

            # patoolib may extract to cache_1.sqlite3, rename if needed
            if os.path.exists("cache_1.sqlite3") and not os.path.exists("cache.sqlite3"):
                print("Renaming extracted database file...")
                shutil.move("cache_1.sqlite3", "cache.sqlite3")
            elif os.path.exists("cache_1.sqlite3") and os.path.exists("cache.sqlite3"):
                # Replace old with new
                os.remove("cache.sqlite3")
                shutil.move("cache_1.sqlite3", "cache.sqlite3")

        except ImportError:
            print("ERROR: patoolib not installed.")
            print("Please install it: pip install patool")
            print("")
            print("Or manually extract the archive using one of these methods:")
            print(f"  1. Windows Explorer: Right-click '{zip_file}' -> Extract All")
            print(f"  2. Install WinRAR or 7-Zip and extract '{zip_file}'")
            raise
        except Exception as e:
            print(f"ERROR during extraction: {e}")
            print("")
            print("Please manually extract the archive using one of these methods:")
            print(f"  1. Windows Explorer: Right-click '{zip_file}' -> Extract All")
            print(f"  2. Install WinRAR or 7-Zip and extract '{zip_file}'")
            raise

    else:
        # Single ZIP file
        print("Extracting single ZIP file...")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(".")
            print("Extraction complete!")
        except zipfile.BadZipFile as e:
            if "span multiple disks" in str(e):
                print("")
                print("ERROR: This is a multi-volume ZIP archive.")
                print("Please extract it manually using Windows Explorer, WinRAR, or 7-Zip.")
                print(f"Right-click on '{zip_file}' and select 'Extract All' or 'Extract Here'.")
            raise


if __name__ == "__main__":
    # check if file exists
    zip_path = os.path.join(CACHE_DIR, "cache.zip")
    if os.path.isfile(zip_path):
        print("File exists")
    else:
        print("File does not exist")
        download_files()
    create_database()

    # Open sql lite database .sqlite3 file
