# Scraping Google Maps using Scrapy-playwright

I am using Python 3.12.3 and WSL 2 Ubuntu to run this project.

## Installation

### Prerequisites
- Python 3.10+ 
- pip
- playwright

### Steps
1. Clone the repository
   	```bash
   	git clone https://github.com/girisuryamawandi/Scraping-Google-MAp-Using-Scrapy-Playwright.git

2. Go to the folder
3. Install the dependencies
   ```
   pip install -r requirements.txt
4. Run the script and save the result in CSV
   ```
   scrapy crawl googlemaps -o result.csv
