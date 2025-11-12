# $ wget https://yaqwsx.github.io/jlcparts/data/cache.zip
# $ wget https://yaqwsx.github.io/jlcparts/data/cache.z01
# $ wget https://yaqwsx.github.io/jlcparts/data/cache.z02

import urllib.request
import os
import zipfile
import glob

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
    # Combine multi-part zip files and extract
    print("Extracting multi-part zip archive...")

    # Check if split parts exist (cache.z01, cache.z02, etc.)
    split_parts = sorted(glob.glob(os.path.join(CACHE_DIR, "cache.z[0-9][0-9]")))
    zip_file = os.path.join(CACHE_DIR, "cache.zip")

    if split_parts:
        # Multi-part zip: combine parts into a single file
        print(f"Found {len(split_parts)} split parts, combining...")
        combined_zip = os.path.join(CACHE_DIR, "cache_combined.zip")
        with open(combined_zip, "wb") as combined:
            # Write all split parts first
            for part in split_parts:
                print(f"  Adding {os.path.basename(part)}...")
                with open(part, "rb") as f:
                    combined.write(f.read())
            # Write the final .zip part
            print("  Adding cache.zip...")
            with open(zip_file, "rb") as f:
                combined.write(f.read())

        # Extract the combined zip to current directory
        print("Extracting combined archive...")
        with zipfile.ZipFile(combined_zip, 'r') as zip_ref:
            zip_ref.extractall(".")

        # Clean up combined file
        os.remove(combined_zip)
        print("Extraction complete!")
    else:
        # Single zip file
        print("Extracting single zip file...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("Extraction complete!")


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
