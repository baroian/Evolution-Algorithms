# scrapers/pararius_scraper.py

import requests
from bs4 import BeautifulSoup
import time
import random
from utilities.user_agents import get_random_user_agent
from utilities.helpers import parse_price, parse_size, get_full_url

def scrape_pararius(criteria):
    """Scrape Pararius for accommodations matching the criteria."""
    listings = []
    headers = {'User-Agent': get_random_user_agent()}
    base_url = "https://www.pararius.com/apartments/{city}"

    for city in criteria['cities']:
        url = base_url.format(city=city.lower().replace(' ', '-'))
        response = requests.get(url, headers=headers)
        time.sleep(random.uniform(1, 3))  # Random delay

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            properties = soup.find_all('section', class_='listing-search-item')

            for prop in properties:
                title_elem = prop.find('a', class_='listing-search-item__link--title')
                price_elem = prop.find('div', class_='listing-search-item__price')
                size_elem = prop.find('li', class_='illustrated-features__item--surface-area')

                if not (title_elem and price_elem and size_elem):
                    continue  # Skip if essential elements are missing

                title = title_elem.get_text(strip=True)
                link = get_full_url(title_elem['href'], base_url)
                price_text = price_elem.get_text(strip=True)
                size_text = size_elem.get_text(strip=True)

                price = parse_price(price_text)
                size = parse_size(size_text)

                if price <= criteria['max_price'] and size >= criteria['min_size']:
                    listing = {
                        'id': link,
                        'title': title,
                        'price': price,
                        'size': size,
                        'city': city,
                        'link': link
                    }
                    listings.append(listing)
        else:
            print(f"Failed to retrieve Pararius listings for {city}: {response.status_code}")

    return listings
