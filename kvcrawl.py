import requests
import re
from bs4 import BeautifulSoup

# Base query URL with a placeholder for the start parameter
base_url = 'https://www.kv.ee/search?orderby=pawl&view=default&deal_type=2&county=1&parish=1061&city%5B0%5D=5701&city%5B1%5D=1003&city%5B2%5D=1004&city%5B3%5D=1008&city%5B4%5D=1010&city%5B5%5D=1011&rooms_min=2&limit=100'

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
                
                matching_listings.append({
                    'title': title,
                    'link': link,
                    'price': price
                })
    
    return matching_listings

def main():
    # Ask for the keyword to search 
    # base_url = input("Enter the base query url : ")
    total_pages = 5
    keyword = input("Enter the keyword to search for: ")
   
    
    all_matching_listings = []
    # total_pages = 6  # Change this to the number of pages you want to crawl
    results_per_page = 100  # Maximum results per page

    for page in range(total_pages):
        start_index = page * results_per_page
        print(f"Fetching page starting at {start_index}...")
        url = f"{base_url}&start={start_index}"  # Append start parameter for pagination
        print(f"Requesting URL: {url}")  # Print the URL being requested
        html_content = fetch_page(url)
        
        if html_content:
            # Parse the listings with the provided keyword
            matching_listings = parse_listings(html_content, keyword)
            all_matching_listings.extend(matching_listings)  # Collect results from all pages
            
            # Print the results found on this page for debugging
            #print(f"Page {page + 1} found {len(matching_listings)} matching listings.")
            
            # Optional: Print the titles of matching listings
            # for listing in matching_listings:
                # print(f" - Found listing: {listing['title']} (Link: {listing['link']}")
        else:
            print("Failed to retrieve the search results.")
            break  # Stop if page fetch fails
    
    if all_matching_listings:
        print(f"Found {len(all_matching_listings)} unique listings with '{keyword}*':")
        for listing in all_matching_listings:
            print(f"Title: {listing['title']}")
            print(f"Link: {listing['link']}")
            print(f"Price: {listing['price']}")
            print("-" * 40)
    else:
        print(f"No listings found with '{keyword}*'.")

# Run the crawler
main()
