import requests
import re
import time
import sys
from bs4 import BeautifulSoup

def fetch_page(url):
    """Fetches the content of a URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}, Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_listings(html_content, keyword):
    """Parses listings from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Select the listings based on the updated structure
    listings = soup.find_all('article', class_='default')
    print(f"Found {len(listings)} listings in total.")

    matching_listings = []
    seen_links = set()  # To keep track of unique links
    
    # Compile a regex pattern to search for the keyword with a wildcard at the end, case-insensitive
    keyword_pattern = re.compile(rf'.*{keyword}.*', re.IGNORECASE)
    
    for i, listing in enumerate(listings):
        # Print progress on the same line
        sys.stdout.write(f"\rParsing advert nr {i + 1} out of {len(listings)}")
        sys.stdout.flush()  # Force the output to be written to the terminal immediately
        
        # Get the listing's description and search for the pattern
        description = listing.get_text().lower()
        
        # Use regex to search for the keyword with wildcards
        if re.search(keyword_pattern, description):
            title_tag = listing.find('div', class_='description').find('h2').find('a')
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            
            link = 'https://www.kv.ee' + (listing['data-object-url'] if 'data-object-url' in listing.attrs else "No link")
            
            # Check if this link has already been seen
            if link not in seen_links:
                seen_links.add(link)  # Add link to seen set
                price_tag = listing.find('div', class_='price')
                price = price_tag.get_text(strip=True) if price_tag else "N/A"
                area_tag = listing.find('div', class_='area')
                area = area_tag.get_text(strip=True) if area_tag else "N/A"
                
                matching_listings.append({
                    'title': title,
                    'link': link,
                    'price': price,
                    'area': area
                })

                # Add a delay between individual adverts to prevent overloading the server
                time.sleep(5)

    print()  # Move to the next line after parsing all listings
    return matching_listings, len(listings)  # Return listings and count of listings

def main():
    # Ask for base url, number of pages to search over, and the keyword to search
    base_url = input("Enter the base url to crawl over: ") 
    total_pages = int(input("Enter the number of pages you want to scrape through: ")) 
    keyword = input("Enter the keyword to search for: ")
    all_matching_listings = []
    results_per_page = None  # Initialize with None until dynamically determined

    for page in range(total_pages):
        # For the first page, fetch results and determine listings count
        if results_per_page is None:
            start_index = 0  # No pagination for the first page
        else:
            start_index = page * results_per_page  # Use dynamically determined results_per_page for pagination
        
        print(f"\rFetching page {page + 1}/{total_pages} starting at {start_index+1}...", end="")
        sys.stdout.flush()
        url = f"{base_url}&start={start_index}"  # Append start parameter for pagination
        html_content = fetch_page(url)
        
        if html_content:
            # Parse the listings and get the number of results per page
            matching_listings, current_results_per_page = parse_listings(html_content, keyword)
            if results_per_page is None:  # Set the dynamic value after parsing the first page
                results_per_page = current_results_per_page

            all_matching_listings.extend(matching_listings)  # Collect results from all pages
        else:
            print("\nFailed to retrieve the search results.")
            break  # Stop if page fetch fails
    print("\nDone fetching pages.")
    
    if all_matching_listings:
        print(f"Found {len(all_matching_listings)} unique listings with '*{keyword}*':")
        for listing in all_matching_listings:
            print(f"Title: {listing['title']}")
            print(f"Link: {listing['link']}")
            print(f"Price: {listing['price']}")
            print(f"Area: {listing['area']}")
            print("-" * 40)
    else:
        print(f"No listings found with '*{keyword}*'.")
# run the crawler
main()
