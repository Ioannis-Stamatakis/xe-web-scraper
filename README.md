# Athens Property Web Scraper 

 **A web scraper of xe.gr for obtaining Athens rental property data**

## Project Overview

This project contains a Python web scraper that extracts rental property data from xe.gr, specifically focused on Athens properties. 

- Web scraping with Python (BeautifulSoup)
- JSON data extraction and parsing

##  Features

- **Multi-page scraping**: Automatically detects and scrapes available pages
- **Rich property data** including:
  -  Property ID, title, price, and price per square meter
  -  Size, address, bedrooms, and bathrooms
  -  Construction year and floor level
  -  Geographic coordinates (latitude/longitude)
  -  Property URLs and company information
  -  Transaction and item types
- **Interactive mode**: Choose how many pages to scrape
- **Summary statistics**: Get insights on price ranges, neighborhoods, and averages
- **Respectful scraping**: Built-in delays and error handling

##  Project Structure

- `xe_scraper.py` - Main scraper script with pagination support
- `requirements.txt` - Python dependencies
- `.gitignore` - Files to exclude from version control

##  Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Scraper
```bash
python xe_scraper.py
```

### 3. Choose number of pages
When prompted, you can:
- Enter a number (e.g., `5` for first 5 pages)
- Enter `all` to scrape all available pages

### 4. If you get a 403 error
- Enter xe.gr manually and pass the check that you are human.

The scraper will automatically:
-  Fetch property listings from xe.gr
-  Extract JSON data embedded in each page
-  Parse and clean property information
-  Save results to a timestamped JSON file
-  Provide summary statistics

##  What You'll Get

### Recent Scraping Results
Our latest scraping session collected:
- **612 properties** across 18 pages
- **97 unique neighborhoods** in Athens
- **Price range**: €250 - €175,000 per month
- **Average price**: €1,244 per month
- **Diverse property types**: Apartments, houses, buildings, and more

### Sample Properties 
- 42 τ.μ. apartment in Γκύζη for €800/month
- 74 τ.μ. apartment in Κυψέλη for €1,050/month  
- 26 τ.μ. apartment in Πεδίον Άρεως for €430/month
- 150 τ.μ. apartment in Κολωνάκι for €5,500/month

##  Data Structure

Each property record contains comprehensive information perfect for analysis:

```json
{
    "id": "850419044",
    "title": "Διαμέρισμα 42 τ.μ.",
    "price": "800 €",
    "price_per_square_meter": "19 €/τ.μ.",
    "size": "42 τ.μ.",
    "address": "Αθήνα (Γκύζη)",
    "bedrooms": "1",
    "bathrooms": "1",
    "construction_year": "2021",
    "levels": ["7ος"],
    "transaction_type": "LET.NORMAL",
    "item_type": "re_residence",
    "geo_lat": 37.9915075,
    "geo_lng": 23.7513675,
    "url": "https://www.xe.gr/property/d/enoikiaseis-katoikion/850419044/athhna-gkyzh-800-42",
    "company_title": "Dimitrios Moraitis",
    "is_commercial": true,
    "date_scraped": "2025-06-14T11:02:13.930754"
}
```

##  Technical Implementation

### Smart Data Extraction
- **JSON extraction**: Finds data embedded in the page's `data-json-data` attribute
- **Pagination handling**: Automatically detects and navigates through pages
- **Rate limiting**: 2-second delays between requests
- **Error handling**: Gracefully handles failed requests and missing data

### Performance & Ethics
- **~34 properties per page** (typical)
- **Automatic stopping** when encountering rate limits
- **Respectful delays** between requests
- **Complete logging** for transparency

##  Dataset usage

The scraped dataset is ideal for:
-  **Machine Learning**: Price prediction models
-  **Data Analysis**: Market trends and patterns
-  **Geospatial Analysis**: Location-based insights
-  **Educational Projects**: Learning web scraping and data science
-  **Real Estate Research**: Understanding Athens rental market

## ⚠️ Important Disclaimers

**This project is for educational purposes only.**

- Built to learn Python and web scraping techniques
- NOT intended for commercial use or data resale
- Respects xe.gr's servers with 2-second delays between requests
- Users should review xe.gr's terms of service and robots.txt before use

**Please use responsibly and ethically!**

##  Contributing to Learning

This project welcomes contributions for educational purposes:
-  Bug fixes and improvements
-  Data analysis examples
-  Documentation enhancements
-  Code optimization

##  Questions or Concerns?

If xe.gr or any stakeholders have concerns about this educational project, please reach out. I am committed to:
- Respecting intellectual property rights
- Following ethical web scraping practices
- Supporting educational use of technology
- Being responsive to legitimate concerns

**Remember**: This tool is for learning and education. Always respect website terms of service