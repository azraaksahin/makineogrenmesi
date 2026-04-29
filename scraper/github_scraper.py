import requests
import time
import os 
from dotenv import load_dotenv
load_dotenv()

def scrape_github(query="resume pdf", max_results=50):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + os.getenv("GITHUB_TOKEN")
    }
    links = []
    page = 1
    while len(links) < max_results:
        url = f"https://api.github.com/search/code?q=resume+experience+education+extension:pdf&per_page=30&page={page}"
        print(f"Status kontrol ediliyor...")
        r = requests.get(url, headers=headers)
        print(f"Status: {r.status_code}")
        if r.status_code != 200:
            print(r.text[:300])
            break
        items = r.json().get("items", [])
        if not items:
            break
        for item in items:
            html_url = item.get("html_url", "")
            raw_url = html_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            links.append(raw_url)
        page += 1
        time.sleep(1)
    return links