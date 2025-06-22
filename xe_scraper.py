import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

class XEScraper:
    def __init__(self):
        self.base_url = "https://www.xe.gr"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'el-GR,el;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
        }

    def get_page(self, url):
        try:
            print(f"Attempting to fetch: {url}")
            response = requests.get(url, headers=self.headers)
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def extract_json_data(self, html_content):
        """Extract property data from the JSON embedded in the page"""
        if not html_content:
            return []

        # Look for the data-json-data attribute in the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the div with data-json-data attribute
        container = soup.find('div', {'data-json-data': True})
        if container:
            json_data = container.get('data-json-data')
            if json_data:
                try:
                    # Parse the JSON data
                    data = json.loads(json_data)
                    if 'results' in data:
                        print(f"Found {len(data['results'])} properties in JSON data")
                        return data['results']
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON data: {e}")
        
        # Alternative: Look for JSON data in script tags
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'results' in script.string:
                # Try to extract JSON from script content
                json_match = re.search(r'"results":\s*(\[.*?\])', script.string)
                if json_match:
                    try:
                        results_json = json.loads(json_match.group(1))
                        print(f"Found {len(results_json)} properties in script tag")
                        return results_json
                    except json.JSONDecodeError:
                        continue
        
        print("No JSON property data found")
        return []

    def find_pagination_info(self, html_content):
        """Extract pagination information from the page"""
        if not html_content:
            return None, None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for pagination elements
        pagination_links = []
        
        # Common pagination selectors
        pagination_selectors = [
            'a[href*="page="]',
            '.pagination a',
            '.pager a',
            'a[href*="&p="]',
            'nav a[href*="page"]'
        ]
        
        for selector in pagination_selectors:
            links = soup.select(selector)
            if links:
                pagination_links.extend(links)
                break
        
        if not pagination_links:
            # Look for any links that might contain page numbers
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                if 'page=' in href or '&p=' in href:
                    pagination_links.append(link)
        
        # Extract page numbers and find the maximum
        max_page = 1
        next_page_url = None
        
        for link in pagination_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Try to extract page number from URL
            if 'page=' in href:
                try:
                    page_match = re.search(r'page=(\d+)', href)
                    if page_match:
                        page_num = int(page_match.group(1))
                        max_page = max(max_page, page_num)
                except ValueError:
                    pass
            
            # Look for "next" or ">" links
            if text.lower() in ['next', 'επόμενη', '>', '»', 'επόμενο'] or 'next' in text.lower():
                next_page_url = urljoin(self.base_url, href)
        
        print(f"Pagination info - Max page found: {max_page}, Next page URL: {next_page_url}")
        return max_page, next_page_url

    def generate_page_urls(self, base_url, max_pages=None):
        """Generate URLs for all pages"""
        urls = [base_url]  # Start with the first page
        
        if max_pages and max_pages > 1:
            for page in range(2, max_pages + 1):
                # Try different pagination URL formats
                if '?' in base_url:
                    page_url = f"{base_url}&page={page}"
                else:
                    page_url = f"{base_url}?page={page}"
                urls.append(page_url)
        
        return urls

    def parse_property_data(self, properties_json):
        """Parse the extracted JSON property data"""
        properties = []
        
        for prop in properties_json:
            try:
                property_data = {
                    'id': prop.get('id', 'N/A'),
                    'title': prop.get('title', 'N/A'),
                    'price': prop.get('price', 'N/A'),
                    'price_per_square_meter': prop.get('price_per_square_meter', 'N/A'),
                    'size': prop.get('size_with_square_meter', 'N/A'),
                    'address': prop.get('address', 'N/A'),
                    'bedrooms': prop.get('bedrooms', 'N/A'),
                    'bathrooms': prop.get('bathrooms', 'N/A'),
                    'construction_year': prop.get('construction_year', 'N/A'),
                    'levels': prop.get('levels', []),
                    'transaction_type': prop.get('transaction_type', 'N/A'),
                    'item_type': prop.get('item_type', 'N/A'),
                    'geo_lat': prop.get('geo_lat', 'N/A'),
                    'geo_lng': prop.get('geo_lng', 'N/A'),
                    'url': prop.get('url', 'N/A'),
                    'company_title': prop.get('company_title', 'N/A'),
                    'is_commercial': prop.get('is_commercial', False),
                    'date_scraped': datetime.now().isoformat()
                }
                properties.append(property_data)
            except Exception as e:
                print(f"Error parsing property: {e}")
                continue
        
        return properties

    def scrape_all_pages(self, base_url, max_pages_to_scrape=None):
        """Scrape all pages of property listings"""
        all_properties = []
        page_count = 0
        
        print(f"Starting to scrape all pages from: {base_url}")
        
        # First, get the first page to determine pagination
        html_content = self.get_page(base_url)
        if not html_content:
            print("Failed to fetch the first page")
            return []
        
        # Extract properties from first page
        properties_json = self.extract_json_data(html_content)
        if properties_json:
            properties = self.parse_property_data(properties_json)
            all_properties.extend(properties)
            page_count += 1
            print(f"Page {page_count}: Found {len(properties)} properties")
        
        # Find pagination info
        max_page, next_page_url = self.find_pagination_info(html_content)
        
        # Determine how many pages to scrape
        if max_pages_to_scrape:
            pages_to_scrape = min(max_page, max_pages_to_scrape)
        else:
            pages_to_scrape = max_page
        
        print(f"Will attempt to scrape {pages_to_scrape} pages total")
        
        # Generate URLs for all pages
        page_urls = self.generate_page_urls(base_url, pages_to_scrape)
        
        # Scrape remaining pages (skip first page as we already scraped it)
        for page_url in page_urls[1:]:
            if max_pages_to_scrape and page_count >= max_pages_to_scrape:
                break
                
            print(f"\nScraping page {page_count + 1}...")
            time.sleep(2)  # Be respectful with delays
            
            html_content = self.get_page(page_url)
            if html_content:
                properties_json = self.extract_json_data(html_content)
                if properties_json:
                    properties = self.parse_property_data(properties_json)
                    all_properties.extend(properties)
                    page_count += 1
                    print(f"Page {page_count}: Found {len(properties)} properties")
                else:
                    print(f"No properties found on page {page_count + 1}")
                    break
            else:
                print(f"Failed to fetch page {page_count + 1}")
                break
        
        print(f"\nCompleted scraping {page_count} pages")
        print(f"Total properties found: {len(all_properties)}")
        return all_properties

    def save_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    scraper = XEScraper()
    
    # Working Athens rental properties URL
    base_url = "https://www.xe.gr/property/r/enoikiaseis-katoikion/ChIJ8UNwBh-9oRQR3Y1mdkU1Nic_athhna"
    
    # Ask user how many pages to scrape
    try:
        max_pages = input("How many pages would you like to scrape? (Enter number or 'all' for all pages): ").strip()
        if max_pages.lower() == 'all':
            max_pages_to_scrape = None
        else:
            max_pages_to_scrape = int(max_pages)
    except ValueError:
        print("Invalid input. Defaulting to scraping first 5 pages.")
        max_pages_to_scrape = 5
    
    # Scrape all pages
    all_properties = scraper.scrape_all_pages(base_url, max_pages_to_scrape)
    
    if all_properties:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"athens_properties_all_pages_{timestamp}.json"
        scraper.save_to_json(all_properties, filename)
        print(f"\nSuccessfully scraped {len(all_properties)} properties from all pages.")
        print(f"Data saved to {filename}")
        
        # Print sample data
        print("\nSample properties:")
        for i, prop in enumerate(all_properties[:5]):
            print(f"{i+1}. {prop['title']} - {prop['price']} - {prop['address']}")
        
        # Print summary statistics
        print(f"\nSummary:")
        print(f"Total properties: {len(all_properties)}")
        
        # Count unique neighborhoods
        neighborhoods = set()
        for prop in all_properties:
            if prop['address'] != 'N/A':
                neighborhoods.add(prop['address'])
        print(f"Unique neighborhoods: {len(neighborhoods)}")
        
        # Price range
        prices = []
        for prop in all_properties:
            price_str = prop['price']
            if price_str != 'N/A' and '€' in price_str:
                try:
                    # Extract numeric price
                    price_num = re.sub(r'[^\d.]', '', price_str.replace('.', '').replace(',', '.'))
                    if price_num:
                        prices.append(float(price_num))
                except:
                    pass
        
        if prices:
            print(f"Price range: €{min(prices):.0f} - €{max(prices):.0f}")
            print(f"Average price: €{sum(prices)/len(prices):.0f}")
    else:
        print("No properties were scraped.")

if __name__ == "__main__":
    main() 