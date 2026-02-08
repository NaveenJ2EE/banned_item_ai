import os
import shutil
import random
from tqdm import tqdm

# ========== CONFIG ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "crawler", "screenshots", "gun")
# Define the root data directories
DATA_ROOT = os.path.join(BASE_DIR, "data")
TRAIN_DIR = os.path.join(DATA_ROOT, "train", "gun")
VAL_DIR = os.path.join(DATA_ROOT, "val", "gun")

SPLIT_RATIO = 0.8


def prepare_and_split():
    # --- PERSPECTIVE: CLEANUP ---
    # Delete existing folders to ensure no stale data remains
    for folder in [TRAIN_DIR, VAL_DIR]:
        if os.path.exists(folder):
            print(f"[*] Removing existing folder: {folder}")
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    # Get images from crawler folder
    all_images = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
    random.shuffle(all_images)

    split_idx = int(len(all_images) * SPLIT_RATIO)
    train_files = all_images[:split_idx]
    val_files = all_images[split_idx:]

    print(f"[*] Moving {len(train_files)} to Train and {len(val_files)} to Val...")

    for f in tqdm(train_files, desc="Training Set"):
        shutil.move(os.path.join(SOURCE_DIR, f), os.path.join(TRAIN_DIR, f))

    for f in tqdm(val_files, desc="Validation Set"):
        shutil.move(os.path.join(SOURCE_DIR, f), os.path.join(VAL_DIR, f))

    print(f"\n[✓] Fresh split complete in {DATA_ROOT}")


if __name__ == "__main__":
    prepare_and_split()