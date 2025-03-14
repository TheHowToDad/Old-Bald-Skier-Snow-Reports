import os
import requests
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
        # Debugging: Print the current working directory
        print(f"Current working directory: {os.getcwd()}")

        # Set the save path relative to the GitHub folder
        # Assuming you're saving to a folder called 'images' within your repo
        save_path = os.path.join(os.getcwd(), "images", "current.jpg")
        print(f"Saving image to: {save_path}")

        # Create directories if necessary
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the image
        with open(save_path, "wb") as file:
            file.write(image_response.content)
        print(f"Image saved to {save_path}")

        # Check if the file exists before committing
        if os.path.exists(save_path):
            print(f"File {save_path} exists, ready to commit.")

            # Git commit and push
            subprocess.run(["git", "add", save_path])
            subprocess.run(["git", "commit", "-m", "Updated Vosker image"])
            subprocess.run(["git", "push", "origin", "main"])  # Change 'main' if using another branch
        else:
            print(f"File {save_path} not found after saving.")
    else:
        print("Failed to download the image.")
else:
    print("No .jpg image found.")

# Close the browser
driver.quit()
