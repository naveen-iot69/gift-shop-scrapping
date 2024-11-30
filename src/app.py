from flask import Flask, send_file, render_template
import csv
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__, template_folder='templates')



# Scraping function to get gift shop data
def scrape_gift_shops():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    locations = ['Boston, MA', 'New York, NY', 'Providence, RI', 'Hartford, CT', 'Concord, NH', 'Montpelier, VT', 'Augusta, ME']

    data = []

    for location in locations:
        url_location = location.replace(' ', '+').replace(',', '%2C')
        url = f'https://www.yellowpages.com/search?search_terms=gift+shops&geo_location_terms={url_location}'
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            shops = soup.find_all('div', class_='result')

            for shop in shops[:100]:  # Limit to first 100 shops per location
                name = shop.find('a', class_='business-name').get_text() if shop.find('a', class_='business-name') else "N/A"
                phone = shop.find('div', class_='phones phone primary').get_text() if shop.find('div', class_='phones phone primary') else "N/A"
                address = shop.find('div', class_='street-address').get_text() if shop.find('div', class_='street-address') else "N/A"
                city = shop.find('div', class_='locality').get_text() if shop.find('div', class_='locality') else "N/A"
                
                data.append([name, phone, address, city])

    # Save data to CSV
    with open('gift_shops.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Shop Name", "Phone", "Address", "City"])  # CSV header
        writer.writerows(data)

    return 'gift_shops.csv'

# Home page route
@app.route('/')
def index():
    print("Current directory:", os.getcwd())  # Print current working directory
    return render_template('index.html')

# Route to scrape data and download CSV
@app.route('/scrape')
def scrape_and_download():
    csv_file = scrape_gift_shops()  # Scrape and save the file
    return send_file(csv_file, as_attachment=True, download_name="gift_shops.csv")

if __name__ == "__main__":
    app.run(debug=True)
