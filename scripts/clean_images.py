import os
import cv2
import numpy as np
from PIL import Image
import imagehash
from tqdm import tqdm

# ========== CONFIG ==========
# DATASET_DIR = "crawler/screenshots/gun"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Now we join the root with the actual path to the images
DATASET_DIR = os.path.join(BASE_DIR, "crawler", "screenshots", "gun")

MIN_RESOLUTION = (224, 224)  # Standard for AI training
BLUR_THRESHOLD = 100.0  # Higher = stricter (removes more blur)
HASH_THRESHOLD = 4  # Sensitivity for duplicates (0-6 is standard)


class DatasetCleaner:
    def __init__(self, directory):
        self.directory = directory
        self.files = [f for f in os.listdir(directory) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
        self.hashes = {}
        self.stats = {"corrupted": 0, "too_small": 0, "blurry": 0, "duplicates": 0}

    def get_blur_score(self, image):
        """Calculates blur score from a PIL image object."""
        # Convert PIL to OpenCV format (numpy array)
        open_cv_image = np.array(image.convert('RGB'))
        # Convert RGB to BGR for OpenCV
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def run_cleaning_pipeline(self):
        print(f"[*] Starting deep clean on {len(self.files)} images...")

        for filename in tqdm(self.files):
            path = os.path.join(self.directory, filename)

            try:
                # Use 'with' to ensure the file handle is closed properly
                with Image.open(path) as img:
                    # Fix the 'Palette images with Transparency' warning
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    # 1. Check Integrity & Size
                    width, height = img.size
                    if width < MIN_RESOLUTION[0] or height < MIN_RESOLUTION[1]:
                        os.remove(path)
                        self.stats["too_small"] += 1
                        continue

                    # 2. Check Quality (Blur)
                    score = self.get_blur_score(img)
                    if score < BLUR_THRESHOLD:
                        os.remove(path)
                        self.stats["blurry"] += 1
                        continue

                    # 3. Check Uniqueness (pHash)
                    current_hash = imagehash.phash(img)

                # Separate check for duplicates to avoid file-in-use errors
                is_duplicate = False
                for h in self.hashes:
                    if current_hash - h <= HASH_THRESHOLD:
                        is_duplicate = True
                        break

                if is_duplicate:
                    os.remove(path)
                    self.stats["duplicates"] += 1
                else:
                    self.hashes[current_hash] = filename

            except Exception as e:
                # If we hit an error here, the file is likely truly unreadable
                if os.path.exists(path):
                    os.remove(path)
                self.stats["corrupted"] += 1
                continue

        self.print_summary()

    def print_summary(self):
        print("\n" + "=" * 30)
        print("CLEANING SUMMARY")
        print("=" * 30)
        for key, val in self.stats.items():
            print(f"[-] {key.replace('_', ' ').title()}: {val}")
        print(f"[✓] Remaining Unique Images: {len(self.hashes)}")


if __name__ == "__main__":
    cleaner = DatasetCleaner(DATASET_DIR)
    cleaner.run_cleaning_pipeline()