import os
import sys
import time
import subprocess
from pathlib import Path

# =========================
# AUTO-INSTALL
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
# CONFIG
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
# BROWSER
# =========================
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

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
# CAMERA PAGE
# =========================
driver.get(CAMERA_URL)
time.sleep(6)

# =========================
# FORCE LOAD HISTORY
# =========================
for _ in range(18):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# =========================
# FIND IMAGE CONTAINERS
# =========================
tiles = driver.find_elements(
    By.XPATH,
    "//img | //div[contains(@class,'image')]"
)

print(f"Found {len(tiles)} possible image elements")

saved = []

for i, el in enumerate(tiles[:MAX_IMAGES]):
    try:
        path = IMAGE_DIR / f"{i:03d}.png"
        el.screenshot(str(path))
        saved.append(path)
        print(f"Captured {path}")
    except Exception:
        continue

driver.quit()

# =========================
# GIF CREATION
# =========================
if len(saved) < 2:
    print("ERROR: Not enough valid images")
    sys.exit(1)

frames = [Image.open(p).convert("RGB") for p in saved]

duration_ms = int((GIF_LENGTH_SECONDS / len(frames)) * 1000)

frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=duration_ms,
    loop=0,
    optimize=True
)

print(f"✅ Vosker timelapse created: {GIF_PATH}")
