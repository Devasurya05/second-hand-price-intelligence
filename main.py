# main.py
# Orchestrates the full scrape job: fetch → parse → save
# To change the search query, update SEARCH_QUERY below

from scraper.fetch import fetch_ebay_sold_listings, create_session
from scraper.parser import parse_listings
from scraper.save import save_to_csv

# ── Config ────────────────────────────────────────────────────────────────────
SEARCH_QUERY = "Sony WH-1000XM4"   # ← change this to scrape a different product
TOTAL_PAGES  = 10
# ─────────────────────────────────────────────────────────────────────────────

def run_scrape(query: str, total_pages: int) -> list:
    all_listings = []
    consecutive_empty = 0
    
    session = create_session()  # ← one session for the entire job

    for page in range(1, total_pages + 1):
        print(f"Fetching page {page} of {total_pages}...")

        html = fetch_ebay_sold_listings(session, query, page)  # ← pass session in

        if html is None:
            print(f"  ✗ Page {page} failed — skipping")
            consecutive_empty += 1
        else:
            listings = parse_listings(html)
            print(f"  ✓ {len(listings)} listings found")

            if len(listings) == 0:
                consecutive_empty += 1
                print(f"  ⚠ Empty page ({consecutive_empty} consecutive)")
            else:
                consecutive_empty = 0
                all_listings.extend(listings)

        if consecutive_empty >= 2:
            print(f"\nTwo consecutive empty pages — stopping early at page {page}.")
            break

    return all_listings

if __name__ == "__main__":
    listings = run_scrape(SEARCH_QUERY, TOTAL_PAGES)

    if listings:
        save_to_csv(listings, folder="data")
        print(f"\nDone. {len(listings)} total listings saved.")
    else:
        print("\nNo listings collected. Check fetch errors above.")