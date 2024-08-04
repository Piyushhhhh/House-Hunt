# Facebook Rental House Scraper

This project automates the search for rental house listings on Facebook using a Python script. It leverages Selenium for web scraping and allows users to filter and save search results based on specific keywords.

## Installation
 **Clone the Repository**:
   ```bash
   git clone https://github.com/Piyushhhhh/facebook-rental-scraper.git
   cd facebook-rental-scraper
```

## Setup

### 1. Install Chrome and ChromeDriver:

- Please make sure that you have Google Chrome installed.
- Download the appropriate version of ChromeDriver for your system from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
- Place the ChromeDriver executable in the specified path or ensure it's in your system's PATH.

### 2. Configuration Files:

- **root.yml**: This is the main configuration file that points to other required configuration files.
- **auth.yml**: Contains Facebook login credentials.
- **user.yml**: Contains keywords for search.
  
**Example root.yml**:
```root.yml
auth_params: params/auth.yml
user_params: params/user.yml

chromedriver: /path/to/chromedriver # replace with your chrome driver path

urls:
  login: "https://www.facebook.com"
  search_prefix: "https://m.facebook.com/search/posts?q="
  search_filter_postfix: "&filters=eyJycF9jcmVhdGlvbl90aW1lOjAiOiJ7XCJuYW1lXCI6XCJjcmVhdGlvbl90aW1lXCIsXCJhcmdzXCI6XCJ7XFxcInN0YXJ0X3llYXJcXFwiOlxcXCIyMDIzXFxcIixcXFwic3RhcnRfbW9udGhcXFwiOlxcXCIyMDIzLTFcXFwiLFxcXCJlbmRfeWVhclxcXCI6XFxcIjIwMjNcXFwiLFxcXCJlbmRfbW9udGhcXFwiOlxcXCIyMDIzLTEyXFxcIixcXFwic3RhcnRfZGF5XFxcIjpcXFwiMjAyMy0xLTFcXFwiLFxcXCJlbmRfZGF5XFxcIjpcXFwiMjAyMy0xMi0zMVxcXCJ9XCJ9IiwicmVjZW50X3Bvc3RzOjAiOiJ7XCJuYW1lXCI6XCJyZWNlbnRfcG9zdHNcIixcImFyZ3NcIjpcIlwifSJ9" #replace with your search filter
```
**Example auth.yml: Contains your Facebook login credentials**:
```yml
username: your_facebook_username
password: your_facebook_password
```
**Example user.yml: Contains the keywords for the search.**:
```yml
keywords:
  - "apartment"
  - "house for rent"
```
### 3. Running the Script:
After setting up the configuration files, you can run the script using:
```bash
python main.py
```
### 4. Output:

- The script will save raw data to ''outputs/raw/directory'' in CSV format.
- Filtered results will be saved in ''outputs/filtered/directory'', including a recent posts CSV.

### Script Overview
The script performs the following actions:-
- Login: Automates login to Facebook.
- Search: Performs searches based on the keywords from user.yml.
- Scroll & Scrape: Scrolls through the search results to load all posts and extracts the required data.
- Save Data: Saves raw and filtered data to CSV files.

### You can install the required Python packages with:
 ```bash
pip install selenium pandas tqdm pyyaml
```
### Troubleshooting
- Ensure ChromeDriver and Chrome versions are compatible.
- Verify paths in root.yml and other configuration files.
- Check if you have a stable internet connection and correct Facebook credentials.
