import yaml
import urllib.parse
import pandas as pd
from time import sleep
from tqdm.auto import tqdm
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

runid = dt.now().strftime("%Y-%m-%d %H:%M:%S")

# Load parameters from YAML files
with open("params/root.yml", "r") as stream:
    params = yaml.safe_load(stream)

with open(params["config"]["user_params"], "r") as stream:
    scrape_params = yaml.safe_load(stream)

with open(params["config"]["auth_params"], "r") as stream:
    auth_params = yaml.safe_load(stream)

# Print the path to verify it's correct
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)
browser.maximize_window()

# Perform login
browser.get(params["urls"]["login"])
username = browser.find_element(By.ID, "email")
password = browser.find_element(By.ID, "pass")
submit = browser.find_element(By.NAME, "login")
username.send_keys(auth_params["username"])
password.send_keys(auth_params["password"])
submit.click()

post_data = []

# Scrape data for each keyword
for keyword in tqdm(sorted(set(scrape_params["keywords"])), desc=f"Run ID : {runid}"):
    # Construct the search URL
    browser.get(
        params["urls"]["search_prefix"]
        + urllib.parse.quote_plus(keyword)
        + params["urls"]["search_filter_postfix"]
    )
    
    # Scroll down to load all posts
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for i in range(60):  # Wait for new content to load
            sleep(1)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height != last_height:
                break
        if new_height == last_height:
            break
        last_height = new_height

    # Extract post data
    for post in tqdm(
        browser.find_elements(By.CLASS_NAME, "story_body_container"), desc=keyword
    ):
        try:
            header_elem = post.find_element(By.TAG_NAME, "header")
            meta_elem = header_elem.find_element(
                By.XPATH, './/div[@data-sigil="m-feed-voice-subtitle"]'
            ).find_element(By.TAG_NAME, "a")
            post_data.append(
                {
                    "search_term": keyword,
                    "post_link": meta_elem.get_attribute("href"),
                    "post_time": meta_elem.get_attribute("textContent"),
                    "body_text": post.get_attribute("textContent").replace(
                        header_elem.get_attribute("textContent"), ""
                    ),
                }
            )
        except Exception:
            post_data.append(
                {
                    "search_term": keyword,
                    "body_text": post.get_attribute("textContent"),
                }
            )

    # Save raw data to CSV
    pd.DataFrame(post_data).to_csv(f"outputs/raw/{runid}.csv", index=False)

# Close the browser
browser.close()
browser.quit()

# Load the raw data
raw_df = pd.read_csv(f"outputs/raw/{runid}.csv")

# Filter and save the data based on specific conditions
raw_df[
    (raw_df["post_time"].str.len() < 12)
    | (raw_df["post_time"].str.lower().str.contains("september"))
    | (raw_df["post_time"].str.lower().str.contains("october"))
    | (raw_df["body_text"].str.lower().str.contains("oct"))
].groupby("body_text")[["search_term", "post_time", "post_link"]].apply(
    lambda g: list(map(tuple, g.values.tolist()))
).reset_index().to_csv(
    f"outputs/filtered/{runid}.csv", index=False
)

raw_df[(raw_df["post_time"].str.len() < 12)].groupby("body_text")[
    ["search_term", "post_time", "post_link"]
].apply(lambda g: list(map(tuple, g.values.tolist()))).reset_index().to_csv(
    f"outputs/filtered/{runid}-recent.csv", index=False
)
