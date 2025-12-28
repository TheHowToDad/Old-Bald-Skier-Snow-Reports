import sys
import os
import time
import subprocess
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# CONFIG
# =========================
EMAIL = "sendtoblake@gmail.com"
PASSWORD = "1Keepitreal!"
CAMERA_URL = "https://webapp.vosker.com/camera/65d3eca2f63c43f5f0684d8f"

MAX_IMAGES = 100
GIF_SECONDS = 7

REPO_ROOT = os.getcwd()
VOSKER_DIR = os.path.join(REPO_ROOT, "vosker")
IMAGE_DIR = os.path.join(VOSKER_DIR, "images")
GIF_PATH = os.path.join(VOSKER_DIR, "vosker_timelapse.gif")

# =========================
# FORCE DIRECTORIES
# =========================
os.makedirs(IMAGE_DIR, exist_ok=True)
print("Vosker dir:", VOSKER_DIR)

# =========================
# SELENIUM LOGIN
# =========================
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://webapp.vosker.com/login")
time.sleep(3)

driver.find_element(By.ID, "email").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD + Keys.RETURN)
time.sleep(8)

driver.get(CAMERA_URL)
time.sleep(8)

# =========================
# SCROLL TO LOAD HISTORY
# =========================
for _ in range(15):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)

# =========================
# COLLECT IMAGE URLS
# =========================
imgs = driver.find_elements(By.XPATH, "//img")
image_urls = []

for img in imgs:
    src = img.get_attribute("src")
    if src and "vosker" in src and src.startswith("http"):
        if src not in image_urls:
            image_urls.append(src)

image_urls = image_urls[-MAX_IMAGES:]
print(f"Found {len(image_urls)} Vosker images")

if len(image_urls) < 2:
    print("ERROR: Not enough images")
    driver.quit()
    sys.exit(1)

# =========================
# TRANSFER COOKIES
# =========================
session = requests.Session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

driver.quit()

# =========================
# DOWNLOAD IMAGES (AUTHENTICATED)
# =========================
downloaded = []

for i, url in enumerate(image_urls):
    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()

        path = os.path.join(IMAGE_DIR, f"{i:03d}.jpg")
        with open(path, "wb") as f:
            f.write(r.content)

        Image.open(path).verify()  # HARD VALIDATION
        downloaded.append(path)
        print("Downloaded", path)

    except Exception as e:
        print("Skipped", url, e)

if len(downloaded) < 2:
    print("ERROR: No valid images downloaded")
    sys.exit(1)

# =========================
# CREATE GIF
# =========================
frames = [Image.open(p).convert("RGB") for p in downloaded]
frame_ms = int((GIF_SECONDS / len(frames)) * 1000)

frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=frame_ms,
    loop=0
)

print("✅ GIF CREATED:", GIF_PATH)

