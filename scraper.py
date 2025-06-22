from apify_client import ApifyClient
import os

def scrape_linkedin_profile(url: str):
    client = ApifyClient(os.environ.get("TOKEN_APIFY"))

    run_input = {
        "urls": [url],  
        "cookie": [
            {"name": "li_at", "value": "AQEDAT_oPWECobv9AAABltVftpMAAAGXu_g5PU0Aq35x4j4qntisplf4p68Qn_1vHzONf_8Gr48iwuPz21_3V5BBVJlaIaMFdlPj5H7bkhWs3xD3l4wVReOpmnWRCA6jHZSVbqkrCDhr7aj6IyOd_x6-"},
            {"name": "JSESSIONID", "value": "ajax:2226503378999304052"},
            {"name": "bcookie", "value": "v=2&d8191c3b-646e-4b39-8755-7a2618b66678"},
            {"name": "bscookie", "value": "v=1&20250303163900965906ca-de2f-48c9-8e83-1264586cabdaAQGIlmSD1E1h26oc7mE3Q8v4yi-RZMr5"},
            {"name": "lidc", "value": "b=VB73:s=V:r=V:a=V:p=V:g=3851:u=340:x=1:i=1750602933:t=1750679761:v=2:sig=AQGhc5Rf_Z9TmigU1ovCC-9iEl2y8I8w"}
        ],
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