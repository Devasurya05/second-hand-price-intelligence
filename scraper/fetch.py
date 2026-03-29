import requests
import time
import random

# This is what tells eBay we're a real browser and not a bot.
# Without this, eBay will block us almost immediately.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def build_ebay_url(search_query, page_number=1):
    """
    Builds the eBay sold listings URL for a given search query and page.
    
    search_query: what you're searching for e.g. "sony wh1000xm4"
    page_number: which page of results (default is page 1)
    """
    # Replace spaces with + for URL formatting
    query = search_query.replace(" ", "+")
    
    base_url = "https://www.ebay.com/sch/i.html"
    
    # These parameters are what we figured out in Card 1
    # LH_Sold=1 and LH_Complete=1 filter to sold listings only
    url = (
        f"{base_url}"
        f"?_nkw={query}"
        f"&LH_Sold=1"
        f"&LH_Complete=1"
        f"&_pgn={page_number}"  # page number parameter
    )
    
    return url


def fetch_page(url):
    """
    Fetches the raw HTML from a given URL.
    Returns the HTML text if successful, None if it failed.
    """
    try:
        # Send the request pretending to be a browser
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Check if eBay returned a success response (status code 200)
        # 200 = OK, 403 = blocked, 404 = not found, 429 = rate limited
        if response.status_code == 200:
            print(f"Successfully fetched: {url[:60]}...")
            return response.text  # this is the raw HTML
        else:
            print(f"Failed with status code: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out — eBay took too long to respond")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error — check your internet")
        return None


def fetch_ebay_sold_listings(search_query, page_number=1):
    """
    Main function — builds the URL and fetches the page.
    Also adds a random delay to be polite to eBay's servers
    and avoid getting blocked.
    """
    url = build_ebay_url(search_query, page_number)
    
    # Random delay between 3 and 6 seconds
    # This mimics human browsing behaviour
    delay = random.uniform(3, 6)
    print(f"Waiting {delay:.1f} seconds before fetching...")
    time.sleep(delay)
    
    html = fetch_page(url)
    return html


# This block only runs if you run this file directly
# It won't run if another file imports from this one
if __name__ == "__main__":
    print("Testing fetch function...")
    
    html = fetch_ebay_sold_listings("sony wh1000xm4")
    
    if html:
        print(f"Got HTML response — length: {len(html)} characters")
        # Print just the first 500 characters so we can sanity check it
        print("\nFirst 500 characters of HTML:")
        print(html[:500])
    else:
        print("Fetch failed")