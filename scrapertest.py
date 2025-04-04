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

# Function to get Revelstoke snow report
def get_revelstoke_snow_report():
    URL = "https://www.revelstokemountainresort.com/mountain/conditions/snow-report/"
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to fetch data from {URL}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    snow_report = {}

    # Extract relevant data
    try:
        snow_report['new_snow'] = soup.find('div', class_='snow-report__new').find('span', class_='value').get_text(strip=True)
        snow_report['last_hour'] = soup.find('div', class_='amount2').find('span', class_='value').get_text(strip=True)
        snow_report['24_hours'] = soup.find_all('div', class_='amount2')[1].find('span', class_='value').get_text(strip=True)
        snow_report['48_hours'] = soup.find('div', class_='amount3').find('span', class_='value').get_text(strip=True)
        snow_report['7_days'] = soup.find('div', class_='amount4').find('span', class_='value').get_text(strip=True)
        snow_report['base_depth'] = soup.find('div', class_='amount5').find('span', class_='value').get_text(strip=True)
        snow_report['season_total'] = soup.find('div', class_='amount6').find('span', class_='value').get_text(strip=True)
    except Exception as e:
        print(f"Error while parsing snow report: {e}")
        return None

    return snow_report

# Load existing data
with open('scraped_data.json', 'r') as json_file:
    data = json.load(json_file)

# Fetch snow reports
kimberley_snow_report = get_kimberley_snow_report()
kicking_horse_snow_report = get_kicking_horse_snow_report()
fernie_snow_report = get_fernie_snow_report()
revelstoke_snow_report = get_revelstoke_snow_report()

# Generate the HTML file with updated dark mode styles, blue accents, and improved visuals
with open('index.html', 'w') as html_file:
    html_file.write('<html><head><style>\n')

    # Dark mode styles with modern touches
    html_file.write('body { font-family: "Segoe UI", sans-serif; background-color: #121212; color: #E0E0E0; margin: 0; padding: 0; line-height: 1.6; }\n')
    html_file.write('.container { width: 90%; max-width: 1200px; margin: 0 auto; padding: 30px; }\n')

    # Change to grid with 4 columns, centered images
    html_file.write('.row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; justify-items: center; max-width: 100%; margin: 0 auto; }\n')

    # Image container with flex centering
    html_file.write('.image-container { display: flex; justify-content: center; align-items: center; width: 100%; max-width: 315px; height: auto; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }\n')

    # Image styles to ensure it is centered inside the container
    html_file.write('img { width: 100%; height: auto; transition: transform 0.3s ease-in-out; border-radius: 8px; }\n')
    html_file.write('img:hover { transform: scale(1.05); }\n')

    html_file.write('a { color: #1E90FF; text-decoration: none; font-weight: bold; transition: color 0.3s ease; }\n')
    html_file.write('a:hover { color: #4682B4; }\n')

    # Updated table styles to remove grey lines on the sides
    html_file.write('.snow-report-table { width: 100%; border: none; border-radius: 10px; margin: 30px 0; padding: 20px; background-color: #2C2C2C; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); }\n')
    html_file.write('.snow-report-table td, .snow-report-table th { padding: 15px 20px; text-align: center; color: #E0E0E0; }\n')
    html_file.write('.snow-report-table th { background-color: #222; font-weight: bold; border-top-left-radius: 10px; border-top-right-radius: 10px; }\n')
    html_file.write('.snow-report-table tr:nth-child(even) { background-color: #444; }\n')

    # Added bottom corners rounded as well
    html_file.write('.snow-report-table tr:last-child td:first-child { border-bottom-left-radius: 11px; }\n')
    html_file.write('.snow-report-table tr:last-child td:last-child { border-bottom-right-radius: 11px; }\n')

    # Resort header (h2) stylization
    html_file.write('h2 { text-align: center; font-size: 3em; margin: 20px 0; font-weight: bold; color: #1E90FF; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 10px; }\n')

    # Snow forecast link styles
    html_file.write('.snow-forecast-link { background-color: #1E90FF; color: white; padding: 12px 25px; border-radius: 8px; display: inline-block; margin-top: 20px; text-align: center; font-weight: bold; transition: background-color 0.3s ease; }\n')
    html_file.write('.snow-forecast-link:hover { background-color: #4682B4; }\n')

    # Added padding to each resort section with a slightly lighter background color
    html_file.write('.section { padding: 20px; background-color: #333; margin-bottom: 20px; border-radius: 10px; }\n')

    html_file.write('</style></head><body>\n')

    html_file.write('<div class="container">\n')

    resorts_order = ['Kimberley', 'Fernie', 'Revelstoke', 'Kicking Horse', 'Whitewater']

    for resort_name in resorts_order:
        html_file.write('<div class="section">\n')

        for item in data:
            if item['resort_name'] == resort_name:
                # Resort Header with hyperlink
                resort_url = ""
                if resort_name == 'Kimberley':
                    resort_url = "https://skikimberley.com/conditions/snow-report/"
                elif resort_name == 'Kicking Horse':
                    resort_url = "https://kickinghorseresort.com/conditions/snow-report/"
                elif resort_name == 'Fernie':
                    resort_url = "https://skifernie.com/conditions/snow-report/"
                elif resort_name == 'Revelstoke':
                    resort_url = "https://www.revelstokemountainresort.com/mountain/conditions/snow-report/"
                elif resort_name == 'Whitewater':
                    resort_url = "https://skiwhitewater.com/conditions/"

                html_file.write(f'<h2><a href="{resort_url}" target="_blank">{resort_name}</a></h2>\n')

                # Snow report table
                snow_report = None
                if resort_name == 'Kimberley' and kimberley_snow_report:
                    snow_report = kimberley_snow_report
                elif resort_name == 'Kicking Horse' and kicking_horse_snow_report:
                    snow_report = kicking_horse_snow_report
                elif resort_name == 'Fernie' and fernie_snow_report:
                    snow_report = fernie_snow_report
                elif resort_name == 'Revelstoke' and revelstoke_snow_report:
                    snow_report = revelstoke_snow_report

                if snow_report is None:
                    print(f"Warning: No snow report found for {resort_name}")
                else:
                    html_file.write('<table class="snow-report-table">\n')
                    html_file.write('<tr>\n')
                    for key, value in snow_report.items():
                        value_with_cm = f'{value} <sup style="font-size: 35%;">cm</sup>'
                        html_file.write(f'<td style="font-size: 200%">{value_with_cm}</td>\n')
                    html_file.write('</tr>\n')
                    html_file.write('<tr>\n')
                    for key, value in snow_report.items():
                        label = key.replace("_", " ").title()
                        html_file.write(f'<td>{label}</td>\n')
                    html_file.write('</tr>\n')
                    html_file.write('</table>\n')

                # Snow forecast link and Weather link for Kimberley
                resort_name_hyphenated = resort_name.replace(" ", "-")
                snow_forecast_url = f'https://www.snow-forecast.com/resorts/{resort_name_hyphenated}/6day/mid'
                html_file.write(f'<p><span style="display: flex; justify-content: space-between; align-items: center; width: 100%;">')
                html_file.write(f'<a class="snow-forecast-link" href="{snow_forecast_url}" target="_blank">Snow forecast for {resort_name}</a>\n')

                if resort_name == "Kimberley":
                    html_file.write(f'<a class="snow-forecast-link" href="https://weather.gc.ca/?layers=,radar&center=49.44729681,-115.70753362&zoom=-1" target="_blank">Weather Radar</a>\n')

                if resort_name == "Fernie":
                    html_file.write(f'<a class="snow-forecast-link" href="https://skifernie.com/conditions/alpine-weather/" target="_blank">Mountain Weather</a>\n')


                html_file.write(f'</span></p>\n')

                # Add images
                html_file.write('<div class="row">\n')
                image_count = 0
                for img in item['images']:
                    if resort_name == 'Kimberley' and image_count < 2:
                        image_count += 1
                        continue
                    if resort_name == 'Kicking Horse' and image_count == 0:
                        image_count += 1
                        continue
                    if resort_name == 'Fernie' and image_count == 0:
                        image_count += 1
                        continue
                    if resort_name == 'Revelstoke' and image_count == len(item['images']) - 1:
                        continue
                    html_file.write(f'<div class="image-container">{img}</div>\n')
                    image_count += 1
                html_file.write('</div>\n')

                if resort_name == 'Kimberley':
                    html_file.write('''
        <div style="text-align: center;">
            <a href="current.jpg" target="_blank">
                <img src="current.jpg" alt="Kimberley Current Image" 
                     style="width: 85%; max-width: 315px; height: auto; 
                            border-radius: 8px; display: block; margin: 15px auto 0;">
            </a>
        </div>
    ''')

        html_file.write('</div>\n')  # Close section div

print("done")

