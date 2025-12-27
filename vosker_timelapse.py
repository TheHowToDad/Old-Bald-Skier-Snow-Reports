import os
import sys
import requests
from PIL import Image
from io import BytesIO

# =========================
# DEFINITIVE REPO ROOT
# =========================
ROOT = os.path.dirname(os.path.abspath(__file__))

VOSKER_DIR = os.path.join(ROOT, "vosker")
IMAGE_DIR = os.path.join(VOSKER_DIR, "images")
GIF_PATH = os.path.join(VOSKER_DIR, "vosker_timelapse.gif")

# =========================
# FORCE DIRECTORY CREATION
# =========================
os.makedirs(IMAGE_DIR, exist_ok=True)

print("Repo root:", ROOT)
print("Vosker dir:", VOSKER_DIR)
print("Image dir:", IMAGE_DIR)

# =========================
# TEST IMAGE URLS
# (Replace later with Vosker URLs)
# =========================
IMAGE_URLS = [
    "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png",
]

valid_images = []

# =========================
# DOWNLOAD + VALIDATE
# =========================
for i, url in enumerate(IMAGE_URLS):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()

        img = Image.open(BytesIO(r.content))
        img.verify()

        img = Image.open(BytesIO(r.content)).convert("RGB")

        path = os.path.join(IMAGE_DIR, f"{i:03}.jpg")
        img.save(path, "JPEG")

        valid_images.append(path)
        print("Saved:", path)

    except Exception as e:
        print(f"Skipping invalid image {url}: {e}")

if len(valid_images) < 2:
    sys.exit("ERROR: Not enough valid images to create GIF")

# =========================
# CREATE GIF
# =========================
frames = [Image.open(p) for p in valid_images]

frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=700,
    loop=0
)

print("GIF CREATED:", GIF_PATH)
