# $ wget https://yaqwsx.github.io/jlcparts/data/cache.zip
# $ wget https://yaqwsx.github.io/jlcparts/data/cache.z01
# $ wget https://yaqwsx.github.io/jlcparts/data/cache.z02
# $ 7z x cache.zip


import urllib.request
import os


def download_file(url):
    # Download file from internet
    filename = os.path.basename(url)
    print("Downloading " + filename + "...")
    urllib.request.urlretrieve(url, filename)


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
    # Unzip file
    print("Unzipping file...")
    os.system(r'"C:\Program Files\7-Zip\7z.exe" e cache.zip -y')


if __name__ == "__main__":
    # check if file exists
    if os.path.isfile("cache.zip"):
        print("File exists")
    else:
        print("File does not exist")
        download_files()
    create_database()

    # Open sql lite database .sqlite3 file
