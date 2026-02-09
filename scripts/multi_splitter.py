import os
import shutil
import random
from tqdm import tqdm

# ========== CONFIG ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This is where your scraped images live
CRAWLER_ROOT = os.path.join(BASE_DIR, "crawler", "screenshots")
# This is where the model will look for training
DATA_ROOT = os.path.join(BASE_DIR, "data")

SPLIT_RATIO = 0.8


def prepare_and_split():
    # Identify all classes based on folders in crawler/screenshots (e.g., 'gun', 'not_gun')
    categories = [d for d in os.listdir(CRAWLER_ROOT) if os.path.isdir(os.path.join(CRAWLER_ROOT, d))]

    if not categories:
        print("[x] No category folders found in crawler/screenshots!")
        return

    print(f"[*] Found categories: {categories}")

    for category in categories:
        source_dir = os.path.join(CRAWLER_ROOT, category)
        train_dest = os.path.join(DATA_ROOT, "train", category)
        val_dest = os.path.join(DATA_ROOT, "val", category)

        # 1. CLEANUP: Delete existing train/val folders for this category to ensure a fresh start
        for folder in [train_dest, val_dest]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)

        # 2. COLLECT: Get all images from the specific crawler folder
        all_images = [f for f in os.listdir(source_dir) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]

        if not all_images:
            print(f"[!] No images found for category: {category}. Skipping...")
            continue

        random.shuffle(all_images)

        # 3. SPLIT: Calculate indices
        split_idx = int(len(all_images) * SPLIT_RATIO)
        train_files = all_images[:split_idx]
        val_files = all_images[split_idx:]

        print(f"\n[*] Processing [{category}]: {len(train_files)} to Train, {len(val_files)} to Val")

        # 4. MOVE: Transfer files to data/train/category and data/val/category
        for f in tqdm(train_files, desc=f" {category} (Train)"):
            shutil.move(os.path.join(source_dir, f), os.path.join(train_dest, f))

        for f in tqdm(val_files, desc=f" {category} (Val)"):
            shutil.move(os.path.join(source_dir, f), os.path.join(val_dest, f))

    print(f"\n[✓] Fresh split complete for all categories in {DATA_ROOT}")


if __name__ == "__main__":
    prepare_and_split()