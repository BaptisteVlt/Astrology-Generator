# Scrapping until 2nd december 2022

# Url : https://chaninicholas.com/[sign]-free-daily-horoscope-[month]-[day]-[year]

# Text in div class = "entry-content" second <p>

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import time
import swisseph as swe
import pandas as pd
import pytz

# Configure settings
DELAY = 0.1  # Seconds between requests to avoid overwhelming server
START_DATE = datetime.today()
END_DATE = datetime(2022, 12, 2)
ZODIAC_SIGNS = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
]

def generate_dates():
    current_date = START_DATE
    while current_date >= END_DATE:
        yield current_date
        current_date -= timedelta(days=1)

def format_url(sign, date):
    return f"https://chaninicholas.com/{sign}-free-daily-horoscope-{date.strftime('%B-%#d-%Y').lower()}/"

def scrape_horoscopes():
    with open('horoscopes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Zodiac Sign', 'Horoscope Text'])
        
        for date in generate_dates():
            for sign in ZODIAC_SIGNS:
                url = format_url(sign, date)
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    entry_content = soup.find('div', class_='entry-content')
                    
                    if entry_content:
                        paragraphs = entry_content.find_all('p')
                        if len(paragraphs) >= 2:
                            # Extract text from second paragraph (index 1)
                            horoscope_text = paragraphs[1].get_text(strip=True)
                            writer.writerow([date.date(), sign.capitalize(), horoscope_text])
                            print(f"Scraped {sign} - {date.date()}")
                    
                    time.sleep(DELAY)
                
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 404:
                        continue  # Skip non-existent pages
                    else:
                        print(f"Error {e.response.status_code} for {url}")
                except Exception as e:
                    print(f"Error processing {url}: {str(e)}")

# Add astrological data columns

if __name__ == "__main__":
    scrape_horoscopes()
    print("Scraping complete! Data saved to horoscopes.csv")
