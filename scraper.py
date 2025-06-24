from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_cookies_from_env():
    """Get cookies from environment variables"""
    cookies = []
    cookie_mappings = {
        "li_at": os.getenv("LI_AT_COOKIE"),
        "JSESSIONID": os.getenv("JSESSIONID_COOKIE"),
        "bcookie": os.getenv("BCOOKIE_COOKIE"),
        "bscookie": os.getenv("BSCOOKIE_COOKIE"),
        "lidc": os.getenv("LIDC_COOKIE")
    }
    for name, value in cookie_mappings.items():
        if value:
            cookies.append({"name": name, "value": value})
    
    return cookies

def scrape_linkedin_profile(url: str):
    client = ApifyClient(os.environ.get("TOKEN_APIFY"))

    run_input = {
    "urls": [url],
    "cookie": get_cookies_from_env(),
    "minDelay": 15,
    "maxDelay": 60,
    "proxy": {
        "useApifyProxy": True,
    },
    "findContacts": False
    }

    try:
        run = client.actor("curious_coder/linkedin-profile-scraper").call(run_input=run_input)
        
        dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if dataset_items:
            return dataset_items[0]
        else:
            return None
    except Exception as e:
        print(f"Error scraping LinkedIn profile: {e}")
        return None