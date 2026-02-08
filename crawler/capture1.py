from icrawler.builtin import BingImageCrawler
import os

SAVE_DIR = "screenshots/gun"
os.makedirs(SAVE_DIR, exist_ok=True)

KEYWORDS = [
    "gun",
    "pistol",
    "handgun",
    "revolver",
    "rifle",
    "shotgun",
    "firearm",
    "9mm pistol",
    "glock pistol"
]

IMAGES_PER_KEYWORD = 500   # 9 × 500 = 4500 images

for kw in KEYWORDS:
    print(f"\n🔍 Downloading images for: {kw}")

    crawler = BingImageCrawler(
        storage={"root_dir": SAVE_DIR}
    )

    crawler.crawl(
        keyword=kw,
        filters=None,
        max_num=IMAGES_PER_KEYWORD
    )

print("\n✅ Image collection completed")