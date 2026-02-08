import os, hashlib

FOLDER = "screenshots/gun"
hashes = {}
removed = 0

for img in os.listdir(FOLDER):
    path = os.path.join(FOLDER, img)
    with open(path, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
    if h in hashes:
        os.remove(path)
        removed += 1
    else:
        hashes[h] = img

print(f"✅ Removed {removed} duplicate images")