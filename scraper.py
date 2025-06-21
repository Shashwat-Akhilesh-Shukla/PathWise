from apify_client import ApifyClient
import os

def scrape_linkedin_profile(url: str):
    client = ApifyClient(os.environ.get("TOKEN_APIFY"))

    run_input = {
        "profileUrls": [url],
        "minDelay": 15,
        "maxDelay": 60,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyCountry": "US"
        },
        "findContacts": False
    }

    run = client.actor("curious_coder/linkedin-profile-scraper").call(run_input=run_input)
    
    dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    if dataset_items:
        return dataset_items[0]
    else:
        return None
