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

os.makedirs(IMAGE_DIR, exist_ok=True)

print("Repo root:", ROOT)
print("Vosker dir:", VOSKER_DIR)
print("Image dir:", IMAGE_DIR)

# =========================
# HEADERS (FIX 403)
# =========================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VoskerTimelapse/1.0)"
}

# =========================
# TEST IMAGE URLS (403-SAFE)
# =========================
IMAGE_URLS = [
    "https://picsum.photos/640/360",
    "https://picsum.photos/640/361",
    "https://picsum.photos/640/362",
]

valid_images = []

# =========================
# DOWNLOAD + VALIDATE
# =========================
for i, url in enumerate(IMAGE_URLS):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
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

