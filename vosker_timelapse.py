import os
import sys
import time
import subprocess
from pathlib import Path

# =========================
# AUTO-INSTALL DEPENDENCIES
# =========================
def ensure(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure("PIL")
ensure("selenium")
ensure("webdriver_manager")

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# CONFIG (NO HARDCODED SECRETS)
# =========================
EMAIL = os.environ["VOSKER_EMAIL"]
PASSWORD = os.environ["VOSKER_PASSWORD"]

CAMERA_URL = "https://webapp.vosker.com/camera/65d3eca2f63c43f5f0684d8f"

MAX_IMAGES = 100
GIF_LENGTH_SECONDS = 7

BASE_DIR = Path("vosker")
IMAGE_DIR = BASE_DIR / "images"
GIF_PATH = BASE_DIR / "vosker_timelapse.gif"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# SELENIUM SETUP
# =========================
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# =========================
# LOGIN
# =========================
driver.get("https://webapp.vosker.com/login")
time.sleep(4)

driver.find_element(By.ID, "email").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD + Keys.RETURN)
time.sleep(8)

# =========================
# OPEN CAMERA PAGE
# =========================
driver.get(CAMERA_URL)
time.sleep(6)

# =========================
# LOAD IMAGE HISTORY
# =========================
for _ in range(15):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# =========================
# COLLECT IMAGE ELEMENTS
# =========================
imgs = driver.find_elements(By.XPATH, "//img[contains(@src, '.jpg')]")

srcs = []
for img in imgs:
    src = img.get_attribute("src")
    if src and "vosker" in src:
        srcs.append(src)

# newest → oldest → reverse to chronological
srcs = list(dict.fromkeys(srcs))[:MAX_IMAGES]
srcs.reverse()

print(f"Found {len(srcs)} authenticated Vosker images")

# =========================
# DOWNLOAD VIA BROWSER SESSION
# =========================
downloaded = []

for i, url in enumerate(srcs):
    driver.execute_script(f"""
        var img = document.createElement('img');
        img.src = "{url}";
        img.onload = function() {{
            var canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            canvas.getContext('2d').drawImage(img, 0, 0);
            var data = canvas.toDataURL('image/jpeg').split(',')[1];
            window.saveImage = data;
        }};
    """)
    time.sleep(1)

    data = driver.execute_script("return window.saveImage;")
    if not data:
        continue

    path = IMAGE_DIR / f"{i:03d}.jpg"
    with open(path, "wb") as f:
        f.write(bytes.fromhex(data.encode("utf-8").hex()))

    downloaded.append(path)
    print(f"Saved {path}")

driver.quit()

# =========================
# CREATE GIF
# =========================
if len(downloaded) < 2:
    print("ERROR: Not enough valid images")
    sys.exit(1)

frames = [Image.open(p).convert("RGB") for p in downloaded]

duration_ms = int((GIF_LENGTH_SECONDS / len(frames)) * 1000)

frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=duration_ms,
    loop=0,
    optimize=True
)

print(f"✅ GIF CREATED: {GIF_PATH}")
