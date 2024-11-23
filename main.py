# main.py

import time
import schedule
from scrapers.pararius_scraper import scrape_pararius
from scrapers.funda_scraper import scrape_funda
from scrapers.kamernet_scraper import scrape_kamernet
from utilities.database import load_seen_listings, save_new_listings
from utilities.logger import log_listing
from utilities.helpers import print_listing

# Define search criteria
SEARCH_CRITERIA = {
    'cities': ['Leiden', 'Den Haag'],
    'max_price': 1300,
    'min_size': 29
}

def run_scrapers():
    """Run all scraper functions and handle new listings."""
    seen_listings = load_seen_listings()
    new_listings = []

    for scrape_function in [scrape_pararius, scrape_funda, scrape_kamernet]:
        try:
            listings = scrape_function(SEARCH_CRITERIA)
            for listing in listings:
                if listing['id'] not in seen_listings:
                    print_listing(listing)
                    log_listing(listing)
                    new_listings.append(listing['id'])
        except Exception as e:
            print(f"Error scraping {scrape_function.__name__}: {e}")

    # Update the list of seen listings
    save_new_listings(new_listings)

if __name__ == "__main__":
    # Schedule the bot to run every 10 minutes
    schedule.every(10).minutes.do(run_scrapers)
    run_scrapers()  # Initial run

    while True:
        schedule.run_pending()
        time.sleep(1)
