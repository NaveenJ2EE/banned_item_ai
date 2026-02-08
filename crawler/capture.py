import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIG ==========
KEYWORD = "gun"
SAVE_DIR = f"screenshots/{KEYWORD}"
MAX_ITEMS = 50
SEARCH_URL = f"https://www.google.com/search?q={KEYWORD}&tbm=isch"

os.makedirs(SAVE_DIR, exist_ok=True)

# ========== SETUP DRIVER ==========
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(SEARCH_URL)
time.sleep(5)

# ========== SCROLL ==========
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# ========== CAPTURE IMAGES ==========
images = driver.find_elements(By.CSS_SELECTOR, "img")
count = 0

for img in images:
    if count >= MAX_ITEMS:
        break

    src = img.get_attribute("src")

    if src and src.startswith("http"):
        try:
            img_data = requests.get(src, timeout=5).content
            with open(f"{SAVE_DIR}/img_{count}.jpg", "wb") as f:
                f.write(img_data)
            print(f"[✓] Saved image {count}")
            count += 1
        except Exception as e:
            print(f"[x] Failed image {count}: {e}")

driver.quit()

print(f"\nDone. Total images saved: {count}")