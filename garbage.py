import os
import requests
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("::notice::[DEBUG] Starting script execution...")

# Set up the Chrome WebDriver (headless for GitHub Actions)
options = webdriver.ChromeOptions()
options.headless = True  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("::notice::[DEBUG] WebDriver initialized. Logging into Vosker...")

# Open the Vosker login page
driver.get("https://webapp.vosker.com/")

# Locate the login elements and log in
email_elem = driver.find_element(By.ID, "email")
password_elem = driver.find_element(By.ID, "password")
email_elem.send_keys("sentoblake@gmail.com")  # Replace with your email
password_elem.send_keys("1Keepitreal!")  # Replace with your password
password_elem.send_keys(Keys.RETURN)

# Wait for the page to load after login
time.sleep(5)

print("::notice::[DEBUG] Login complete. Searching for images...")

# Find the first .jpg image on the page
images = driver.find_elements(By.XPATH, "//img[contains(@src, '.jpg')]")

if images:
    image_url = images[0].get_attribute("src")
    print(f"::notice::[DEBUG] Found image URL: {image_url}")

    # Download the image
    image_response = requests.get(image_url)

    if image_response.status_code == 200:
        # Save image in the root folder
        save_path = os.path.join(os.getcwd(), "current.jpg")
        with open(save_path, "wb") as file:
            file.write(image_response.content)

        print(f"::notice::[DEBUG] Image saved to {save_path}")

        # Configure Git for GitHub Actions
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
        subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"])

        # Add and commit the image
        subprocess.run(["git", "add", save_path])
        subprocess.run(["git", "commit", "-m", "Updated Vosker image"], check=True)

        # Push changes using GitHub Token
        repo_url = f"https://x-access-token:{os.getenv('GITHUB_TOKEN')}@github.com/TheHowToDad/Old-Bald-Skier-Snow-Reports.git"
        subprocess.run(["git", "push", repo_url, "main"], check=True)

        print("::notice::[DEBUG] Image committed and pushed successfully.")
    else:
        print("::error::Failed to download the image. HTTP Status:", image_response.status_code)
else:
    print("::error::No .jpg images found!")

# Close the browser
driver.quit()
