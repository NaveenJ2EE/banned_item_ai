import os
import time
import hashlib
import requests
from ddgs import DDGS
from PIL import Image
from io import BytesIO

SAVE_DIR = "screenshots/gun"
os.makedirs(SAVE_DIR, exist_ok=True)

QUERIES = [
    "gun",
    "handgun",
    "pistol",
    "revolver",
    "rifle",
    "shotgun",
    "firearm",
    "weapon gun",
    "black handgun",
    "metal pistol"
]

IMAGES_PER_QUERY = 300
SLEEP_BETWEEN_DOWNLOADS = 1.2
SLEEP_BETWEEN_QUERIES = 8

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def download_image(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return False

        img = Image.open(BytesIO(r.content)).convert("RGB")
        name = hashlib.md5(url.encode()).hexdigest()
        img.save(os.path.join(SAVE_DIR, f"{name}.jpg"), "JPEG")
        return True
    except:
        return False


total = 0

with DDGS() as ddgs:
    for q in QUERIES:
        print(f"\n🔍 Searching: {q}")

        try:
            results = ddgs.images(
                keywords=q,
                max_results=IMAGES_PER_QUERY,
                safesearch="off"
            )

            count = 0
            for r in results:
                if download_image(r.get("image")):
                    total += 1
                    count += 1
                    time.sleep(SLEEP_BETWEEN_DOWNLOADS)

            print(f"Downloaded {count} images for '{q}'")

        except Exception as e:
            print(f"⚠️ Skipping '{q}' due to rate limit")

        time.sleep(SLEEP_BETWEEN_QUERIES)

print(f"\n✅ TOTAL IMAGES DOWNLOADED: {total}")