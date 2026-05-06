import requests
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


def create_session():
    """
    Creates a requests Session that persists cookies across requests.
    
    A Session object is like a browser tab that stays open.
    It remembers cookies eBay sets on the first visit and sends
    them back on every subsequent request — exactly like a real browser.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # First visit eBay's homepage to get cookies
    # This is what a real browser does before any search
    print("Warming up session — visiting eBay homepage...")
    try:
        response = session.get("https://www.ebay.com", timeout=10)
        print(f"Homepage status: {response.status_code}")
        
        # Small human-like pause after landing on homepage
        time.sleep(random.uniform(2, 4))
        
    except Exception as e:
        print(f"Warning: Could not warm up session: {e}")
    
    return session


def build_ebay_url(search_query, page_number=1):
    """
    Builds the eBay sold listings URL for a given search query and page.
    """
    query = search_query.replace(" ", "+")
    
    url = (
        f"https://www.ebay.com/sch/i.html"
        f"?_nkw={query}"
        f"&LH_Sold=1"
        f"&LH_Complete=1"
        f"&_pgn={page_number}"
    )
    
    return url


def fetch_page(session, url):
    """
    Fetches a page using an existing session (with cookies).
    """
    try:
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"Successfully fetched: {url[:60]}...")
            return response.text
        else:
            print(f"Failed with status code: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error")
        return None


def fetch_ebay_sold_listings(session, search_query, page_number=1):
    """
    Fetches one page of eBay sold listings using an existing session.
    Session is created once externally and reused across pages.
    """
    url = build_ebay_url(search_query, page_number)
    
    delay = random.uniform(5, 10)
    print(f"Waiting {delay:.1f} seconds before fetching search page...")
    time.sleep(delay)
    
    return fetch_page(session, url)


if __name__ == "__main__":
    print("Testing fetch function...")
    
    html = fetch_ebay_sold_listings("sony wh1000xm4")
    
    if html:
        print(f"\nGot HTML — length: {len(html)} characters")
        print("\nFirst 500 characters:")
        print(html[:500])
    else:
        print("Fetch failed")