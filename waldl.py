#!/usr/bin/python3
import os
import sys
import requests
import threading
import random
import pathlib
import string
from PIL import Image

DOWNLOAD_DIR = f"{str(pathlib.Path.home())}/pix/wall"

def generate_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def get_ext(url):
    ext = os.path.splitext(url)[1]
    return ext

def download_wallpaper(url):
    print(f"Downloading {url}")
    res = requests.get(url, allow_redirects=True)
    download_path = f"{DOWNLOAD_DIR}/{generate_id()}{get_ext(url)}"
    open(download_path, 'wb').write(res.content)
    print(f"Downloading done of {url}")
        

def wallpaper_search_api(query):
    query_url = f"https://wallhaven.cc/api/v1/search?q={query}" 
    res = requests.get(query_url)
    response = res.json()
    dl_links = []
    for wallpaper in response["data"]:
        dl_links.append(wallpaper["path"])

    return dl_links


os.makedirs(DOWNLOAD_DIR, exist_ok=True)
if len(sys.argv) < 2:
    print("Usage waldl.py <search_query>")
    quit()

query = sys.argv[1].replace(' ', '+')
wallpapers = wallpaper_search_api(query)
for wallpaper in wallpapers:
    download_wallpaper(wallpaper)

for filename in os.listdir(DOWNLOAD_DIR):
    print(filename)
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    with Image.open(filepath) as img:
        x, y = img.size
        print(x)
        print(y)
        if (x / y) == (16 / 9):
            print("Good!")
        else:
            os.remove(filepath)
