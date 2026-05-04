import csv
import os
from datetime import datetime


def save_to_csv(listings, filename=None, folder="../data"):
    """
    Saves a list of listing dictionaries to a CSV file.
    
    listings: the list of dicts from parser.py
    filename: optional custom name, otherwise auto-generates with timestamp
    folder:   where to save it — defaults to the data/ folder
    """
    if not listings:
        print("No listings to save")
        return None
    
    # Auto-generate filename with timestamp if none provided
    # This means each scrape run creates its own file
    # You can always tell when data was collected
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ebay_sold_{timestamp}.csv"
    
    # Make sure the data folder exists
    os.makedirs(folder, exist_ok=True)
    
    filepath = os.path.join(folder, filename)
    
    # Get column names from the first listing's keys
    fieldnames = listings[0].keys()
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()        # writes the column names row
        writer.writerows(listings)  # writes all listing rows
    
    print(f"Saved {len(listings)} listings to {filepath}")
    return filepath


if __name__ == "__main__":
    from fetch import fetch_ebay_sold_listings
    from parser import parse_listings
    
    print("Fetching listings...")
    html = fetch_ebay_sold_listings("sony wh1000xm4")
    
    print("Parsing listings...")
    listings = parse_listings(html)
    
    print("Saving to CSV...")
    filepath = save_to_csv(listings)
    
    if filepath:
        print(f"\nDone. Open {filepath} to see your data.")