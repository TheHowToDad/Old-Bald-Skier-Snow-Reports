import os
import requests
from PIL import Image

# Paths
ROOT_DIR = os.environ.get("GITHUB_WORKSPACE", ".")
BASE_DIR = os.path.join(ROOT_DIR, "vosker")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
GIF_PATH = os.path.join(BASE_DIR, "vosker_timelapse.gif")

# Make directories
os.makedirs(IMAGE_DIR, exist_ok=True)

# Replace with your actual Vosker image URLs
IMAGE_URLS = [
    "https://webapp.vosker.com/media/...1.jpg",
    "https://webapp.vosker.com/media/...2.jpg",
    "https://webapp.vosker.com/media/...3.jpg",
]

downloaded_files = []

for i, url in enumerate(IMAGE_URLS):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        path = os.path.join(IMAGE_DIR, f"{i:03d}.jpg")
        with open(path, "wb") as f:
            f.write(r.content)
        downloaded_files.append(path)
        print(f"Downloaded {path}")
    except Exception as e:
        print(f"Failed {url}: {e}")

if not downloaded_files:
    print("No images downloaded, GIF cannot be created")
    exit(1)

# Create GIF
frames = [Image.open(f).convert("RGB") for f in downloaded_files]
frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=1000,
    loop=0,
    optimize=True
)

print(f"✅ GIF created at {GIF_PATH}")
