# Function to get Whitewater snow report
def get_whitewater_snow_report():
    URL = "https://www.skiwhitewater.com/snow-report"
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

# Fetch snow reports
kimberley_snow_report = get_kimberley_snow_report()
kicking_horse_snow_report = get_kicking_horse_snow_report()
fernie_snow_report = get_fernie_snow_report()
revelstoke_snow_report = get_revelstoke_snow_report()
whitewater_snow_report = get_whitewater_snow_report()  # Add Whitewater snow report

# Generate the HTML file
with open('display_images_and_report.html', 'w') as html_file:
    html_file.write('<html><head><style>\n')
    html_file.write('body { font-family: Arial, sans-serif; background-color: black; color: white; }\n')
    html_file.write('.row { display: flex; flex-wrap: wrap; margin-bottom: 20px; }\n')
    html_file.write('.image-container { margin: 10px; }\n')
    html_file.write('img { width: 300px; height: auto; border: 1px solid #ccc; padding: 5px; }\n')
    html_file.write('a { color: #1E90FF; text-decoration: none; }\n')
    html_file.write('a:hover { text-decoration: underline; color: #87CEFA; }\n')
    html_file.write('.snow-report { list-style-type: none; padding-left: 0; }\n')
    html_file.write('.snow-report li { margin-bottom: 10px; }\n')
    html_file.write('</style></head><body>\n')

    for item in data:
        resort_name = item['resort_name']
        
        # Adding the hyperlink to the resort header linking to the snow report page
        if resort_name == 'Kimberley':
            html_file.write(f'<h2><a href="https://skikimberley.com/conditions/snow-report/" target="_blank">{resort_name}</a></h2>\n')
        elif resort_name == 'Kicking Horse':
            html_file.write(f'<h2><a href="https://kickinghorseresort.com/conditions/snow-report/" target="_blank">{resort_name}</a></h2>\n')
        elif resort_name == 'Fernie':
            html_file.write(f'<h2><a href="https://skifernie.com/conditions/snow-report/" target="_blank">{resort_name}</a></h2>\n')
        elif resort_name == 'Revelstoke':
            html_file.write(f'<h2><a href="https://www.revelstokemountainresort.com/mountain/conditions/snow-report/" target="_blank">{resort_name}</a></h2>\n')
        elif resort_name == 'Whitewater':
            html_file.write(f'<h2><a href="https://www.skiwhitewater.com/snow-report" target="_blank">{resort_name}</a></h2>\n')  # Add Whitewater header

        # Add Kimberley Snow Report below its header
        if resort_name == 'Kimberley' and kimberley_snow_report:
            html_file.write('<ul class="snow-report">\n')
            for key, value in kimberley_snow_report.items():
                html_file.write(f'<li><strong>{key.replace("_", " ").title()}:</strong> {value}</li>\n')
            html_file.write('</ul>\n')

        # Add Kicking Horse Snow Report below its header
        if resort_name == 'Kicking Horse' and kicking_horse_snow_report:
            html_file.write('<ul class="snow-report">\n')
            for key, value in kicking_horse_snow_report.items():
                html_file.write(f'<li><strong>{key.replace("_", " ").title()}:</strong> {value}</li>\n')
            html_file.write('</ul>\n')

        # Add Fernie Snow Report below its header
        if resort_name == 'Fernie' and fernie_snow_report:
            html_file.write('<ul class="snow-report">\n')
            for key, value in fernie_snow_report.items():
                html_file.write(f'<li><strong>{key.replace("_", " ").title()}:</strong> {value}</li>\n')
            html_file.write('</ul>\n')

        # Add Revelstoke Snow Report below its header
        if resort_name == 'Revelstoke' and revelstoke_snow_report:
            html_file.write('<ul class="snow-report">\n')
            for key, value in revelstoke_snow_report.items():
                html_file.write(f'<li><strong>{key.replace("_", " ").title()}:</strong> {value}</li>\n')
            html_file.write('</ul>\n')

        # Add Whitewater Snow Report below its header
        if resort_name == 'Whitewater' and whitewater_snow_report:  # Add Whitewater snow report
            html_file.write('<ul class="snow-report">\n')
            for key, value in whitewater_snow_report.items():
                html_file.write(f'<li><strong>{key.replace("_", " ").title()}:</strong> {value}</li>\n')
            html_file.write('</ul>\n')

        # Add snow forecast link
        resort_name_hyphenated = resort_name.replace(" ", "-")
        snow_forecast_url = f'https://www.snow-forecast.com/resorts/{resort_name_hyphenated}/6day/mid'
        html_file.write(f'<p><a href="{snow_forecast_url}" target="_blank">Snow forecast for {resort_name}</a></p>\n')

        # Add images
        html_file.write('<div class="row">\n')
        image_count = 0
        for img in item['images']:
            if resort_name == 'Kimberley' and image_count < 2:
                image_count += 1
                continue  # Skip the first two images
            if resort_name == 'Kicking Horse' and image_count == 0:
                image_count += 1
                continue  # Skip the first image for Kicking Horse
            if resort_name == 'Fernie' and image_count == 0:
                image_count += 1
                continue  # Skip the first image for Fernie
            if resort_name == 'Revelstoke' and image_count == len(item['images']) - 1:
                continue  # Skip the last image for Revelstoke
            html_file.write(f'<div class="image-container">{img}</div>\n')
            image_count += 1
        html_file.write('</div>\n')

        # Add Easter Chair link for Kimberley
        if resort_name == 'Kimberley':
            html_file.write(f'<p><a href="https://webapp.vosker.com/" target="_blank">Easter Chair</a></p>\n')

    html_file.write('</body></html>')

print("HTML file updated with hyperlinks to snow report pages for each resort.")

