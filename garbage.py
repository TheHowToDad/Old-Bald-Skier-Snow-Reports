import os
import requests
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

print("::notice::[DEBUG] Starting script execution...")

# Set up Selenium WebDriver for GitHub Actions
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--no-sandbox")  # Required for GitHub Actions
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
chrome_options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(options=chrome_options)

print("::notice::[DEBUG] WebDriver initialized. Logging into Vosker...")

# Open the Vosker login page
driver.get("https://webapp.vosker.com/")

# Locate the login elements and log in
email_elem = driver.find_element(By.ID, "email")
password_elem = driver.find_element(By.ID, "password")
email_elem.send_keys("sendtoblake@gmail.com")  # Replace with your email
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

        # Verify file exists
        if os.path.exists(save_path):
            print("::notice::[DEBUG] Image file exists. Proceeding to commit.")

            # Configure Git
            subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
            subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"])

            # Add, commit, and push the file
            subprocess.run(["git", "add", "current.jpg"])
            subprocess.run(["git", "commit", "-m", "Updated Vosker image"], check=True)

            # Push using GitHub token for authentication
            repo_url = f"https://x-access-token:{os.getenv('GITHUB_TOKEN')}@github.com/TheHowToDad/Old-Bald-Skier-Snow-Reports.git"
            subprocess.run(["git", "push", repo_url, "main"], check=True)

            print("::notice::[DEBUG] Image committed and pushed successfully.")
        else:
            print("::error::Image was not saved correctly.")
    else:
        print("::error::Failed to download the image. HTTP Status:", image_response.status_code)
else:
    print("::error::No .jpg images found!")

# Close the browser
driver.quit()
