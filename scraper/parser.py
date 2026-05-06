from bs4 import BeautifulSoup
import re


def parse_price(price_text):
    """
    Converts a price string like "$154.98" or "$1,204.00" into a float 154.98
    
    We need this because the price comes as text from HTML.
    We can't do math on text — we need an actual number.
    """
    if not price_text:
        return None
    
    # re.sub removes anything that isn't a digit or decimal point
    # "$1,204.98" → "1204.98"
    cleaned = re.sub(r'[^\d.]', '', price_text)
    
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_listings(html):
    """
    Takes raw HTML from eBay and returns a list of listings.
    Each listing is a dictionary with title, price, and url.
    """
    if not html:
        print("No HTML to parse")
        return []
    
    # Create a BeautifulSoup object — this builds the navigable tree
    # "html.parser" is Python's built-in HTML parser, no extra install needed
    soup = BeautifulSoup(html, "html.parser")
    
    # Find ALL listing cards on the page using the class we found in Card 1
    # This returns a list — one element per listing card
    cards = soup.find_all("div", class_="s-card__title")
    
    print(f"Found {len(cards)} listing cards on this page")
    
    listings = []
    
    for card in cards:
        # For each card, we need to go UP to find the parent container
        # that holds title, price, and link together
        # .find_parent() walks up the HTML tree
        container = card.find_parent("div", class_="su-card-container__content")
        
        if not container:
            continue  # skip if we can't find the container
        
        # --- Extract title ---
        title_element = container.find("div", class_="s-card__title")
        title = title_element.get_text(strip=True) if title_element else None
        
        # --- Extract price ---
        price_element = container.find("span", class_="s-card__price")
        price_raw = price_element.get_text(strip=True) if price_element else None
        price = parse_price(price_raw)
        
        # --- Extract URL ---
        link_element = container.find("a", class_="s-card__link")
        url = link_element.get("href") if link_element else None
        
        # Only add this listing if we got all three pieces of data
        if title and price and url:
            if title == "Shop on eBay" or "itm/123456" in url:
                continue
            listings.append({
                "title": title,
                "price_usd": price,
                "url": url
            })
    
    return listings


if __name__ == "__main__":
    # We import our fetch function from Card 2 to test this end to end
    from fetch import fetch_ebay_sold_listings
    
    print("Fetching page...")
    html = fetch_ebay_sold_listings("sony wh1000xm4")
    
    print("Parsing listings...")
    listings = parse_listings(html)
    
    print(f"\nExtracted {len(listings)} listings\n")
    
    # Print first 5 listings to check they look right
    for i, listing in enumerate(listings[:5]):
        print(f"Listing {i+1}:")
        print(f"  Title: {listing['title']}")
        print(f"  Price: ${listing['price_usd']}")
        print(f"  URL:   {listing['url'][:60]}...")
        print()