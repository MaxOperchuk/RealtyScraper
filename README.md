# RealtyScraper
### A web scraper that scrapes real estate data from the web and stores it in a json file.

### Description
The scraper fetches real estate data from the specified data source, realtylink.org, and stores this data in a local json file. The user can then request the latest real estate information about last 60 property's via the scraper.

### Technologies Used
- Python
- Beautiful Soup
- Scrapy
- Selenium

### Quick Start

Python3 must be installed
1. Clone the repository to your local machine:
```bash
git clone the-link-from-your-forked-repo
```
2. Create venv and install requirements in it:
```bash
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

3. Create a .env file in the root directory of the project and indicate the number of properties you want to scrape:
- For example "APARTMENT_SCRAPE_LIMIT=60"

4. Run the scraper:
```bash
scrapy crawl apartments -O apartments.json
```

That's it! You have successfully scraped the real estate data from the web and stored it in a json file.
