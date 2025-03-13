from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
import subprocess

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.headless = False  # Set to True if you don't need the browser UI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the Vosker login page
driver.get("https://webapp.vosker.com/")

# Locate the login elements and log in
email_elem = driver.find_element(By.ID, "email")
password_elem = driver.find_element(By.ID, "password")
email_elem.send_keys("sendtoblake@gmail.com")  # Replace with your email
password_elem.send_keys("1Keepitreal!")        # Replace with your password
password_elem.send_keys(Keys.RETURN)

# Wait for the page to load after login
time.sleep(5)

# Find the image file that ends with '.jpg'
images = driver.find_elements(By.XPATH, "//img[contains(@src, '.jpg')]")

# Check if we have found any .jpg images
if images:
    image_url = images[0].get_attribute("src")
    print(f"Found image URL: {image_url}")
    
    # Download the image using requests
    image_response = requests.get(image_url)
    
    if image_response.status_code == 200:
        # Save the image to GitHub workspace
        save_path = "/home/runner/work/TheHowToDad/Old-Bald-Skier-Snow-Reports/Old-Bald-Skier-Snow-Reports/current.jpg"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, "wb") as file:
            file.write(image_response.content)
        print(f"Image saved to {save_path}")

        # Commit and push the image to GitHub
        subprocess.run(["git", "add", save_path])
        subprocess.run(["git", "commit", "-m", "Updated Vosker image"])
        subprocess.run(["git", "push", "origin", "main"])  # Change 'main' if using another branch
        
    else:
        print("Failed to download the image")
else:
    print("No .jpg image found.")

# Close the browser
driver.quit()
