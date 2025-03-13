import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import requests

# Function to get Kimberley snow report
def get_kimberley_snow_report():
    options = Options()
    options.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://skikimberley.com/conditions/snow-report/")

        # Wait for the key elements to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "snowReportNewSnow24"))
        )

        # Parse the page source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract snow report data
        snow_report = {
            "overnight": soup.find("div", {"id": "snowReportNewSnowFallOvernight"}).get_text(strip=True),
            "last_24_hours": soup.find("div", {"id": "snowReportNewSnowFall24"}).get_text(strip=True),
            "last_48_hours": soup.find("div", {"id": "snowReportNewSnowFall48"}).get_text(strip=True),
            "last_7_days": soup.find("div", {"id": "snowReportNewSnowFall7days"}).get_text(strip=True),
            "base": soup.find("div", {"id": "snowReportNewSnowFallPack"}).get_text(strip=True),
            "season_total": soup.find("div", {"id": "snowReportNewSnowFallYTD"}).get_text(strip=True),
        }

        return snow_report

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

# Function to get Kicking Horse snow report
def get_kicking_horse_snow_report():
    options = Options()
    options.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://kickinghorseresort.com/conditions/snow-report/")

        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rcr-snow-subheader"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        snow_report = {
            "overnight": soup.find("div", {"id": "snowReportNewSnowFallOvernight"}).get_text(strip=True),
            "last_24_hours": soup.find("div", {"id": "snowReportNewSnowFall24"}).get_text(strip=True),
            "last_48_hours": soup.find("div", {"id": "snowReportNewSnowFall48"}).get_text(strip=True),
            "last_7_days": soup.find("div", {"id": "snowReportNewSnowFall7days"}).get_text(strip=True),
            "base": soup.find("div", {"id": "snowReportNewSnowFallPack"}).get_text(strip=True),
            "season_total": soup.find("div", {"id": "snowReportNewSnowFallYTD"}).get_text(strip=True),
        }

        return snow_report

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

# Function to get Fernie snow report
def get_fernie_snow_report():
    options = Options()
    options.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://skifernie.com/conditions/snow-report/")

        # Wait for the key elements to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "snowReportNewSnow24"))
        )

        # Parse the page source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract snow report data
        snow_report = {
            "overnight": soup.find("div", {"id": "snowReportNewSnowFallOvernight"}).get_text(strip=True),
            "last_24_hours": soup.find("div", {"id": "snowReportNewSnowFall24"}).get_text(strip=True),
            "last_48_hours": soup.find("div", {"id": "snowReportNewSnowFall48"}).get_text(strip=True),
            "last_7_days": soup.find("div", {"id": "snowReportNewSnowFall7days"}).get_text(strip=True),
            "base": soup.find("div", {"id": "snowReportNewSnowFallPack"}).get_text(strip=True),
            "season_total": soup.find("div", {"id": "snowReportNewSnowFallYTD"}).get_text(strip=True),
        }

        return snow_report

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()
