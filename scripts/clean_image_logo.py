import os
from PIL.Image import Image


FOLDER = "screenshots/gun"
removed = 0
MIN_WIDTH = 100
MIN_HEIGHT = 100

for img in os.listdir(FOLDER):
    path = os.path.join(FOLDER, img)
    try:
        im = Image.open(path)
        w, h = im.size
        if w < MIN_WIDTH or h < MIN_HEIGHT:
            os.remove(path)
            removed += 1
    except:
        pass