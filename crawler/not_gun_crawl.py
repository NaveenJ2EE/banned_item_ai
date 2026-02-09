import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIG ==========
# Keywords specifically chosen to fix the "Phone/Remote" confusion
KEYWORDS = ["mobile phone", "tv remote control", "hand tools", "smartphone in hand", "wallet", "electric drill"]
SAVE_DIR_NAME = "not_gun"
MAX_PER_KEYWORD = 250 # Total will be 1000 images

# Base directory for your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL_SAVE_PATH = os.path.join(BASE_DIR, "crawler", "screenshots", SAVE_DIR_NAME)

os.makedirs(FINAL_SAVE_PATH, exist_ok=True)

# ========== SETUP DRIVER ==========
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

total_saved = 0

# ========== LOOP THROUGH KEYWORDS ==========
for keyword in KEYWORDS:
    print(f"\n[*] Starting Scrape for: {keyword}")
    SEARCH_URL = f"https://www.google.com/search?q={keyword}&tbm=isch"
    driver.get(SEARCH_URL)
    time.sleep(5)

    # SCROLL (Same as your working logic)
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # CAPTURE (Using 'img' tag as per your working script)
    images = driver.find_elements(By.TAG_NAME, "img")
    count = 0

    for img in images:
        if count >= MAX_PER_KEYWORD:
            break

        try:
            src = img.get_attribute("src")

            if src and src.startswith("http"):
                img_data = requests.get(src, timeout=5).content
                # Unique filename per image and keyword
                filename = f"{keyword.replace(' ', '_')}_{total_saved}.jpg"
                with open(os.path.join(FINAL_SAVE_PATH, filename), "wb") as f:
                    f.write(img_data)
                count += 1
                total_saved += 1
                if total_saved % 50 == 0:
                    print(f"[✓] Total Progress: {total_saved} images saved")
        except Exception as e:
            continue

print(f"\n[FINISH] Total 'Not Gun' images saved: {total_saved}")
driver.quit()