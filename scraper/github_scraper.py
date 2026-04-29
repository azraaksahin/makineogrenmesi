import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_github(query="resume pdf", max_results=300):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + os.getenv("GITHUB_TOKEN")
    }
    links = []
    page = 1

    while len(links) < max_results:
        url = f"https://api.github.com/search/code?q={query}+extension:pdf&per_page=30&page={page}"
        print(f"Sayfa {page} | Toplam: {len(links)}")
        r = requests.get(url, headers=headers)

        if r.status_code == 403:
            reset_time = int(r.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset_time - int(time.time()), 10)
            print(f"Rate limit! {wait} saniye bekleniyor...")
            time.sleep(wait)
            continue
        if r.status_code == 422:
            print("1000 limit aşıldı.")
            break
        if r.status_code != 200:
            print(f"Hata: {r.status_code}")
            break

        items = r.json().get("items", [])
        if not items:
            break

        for item in items:
            html_url = item.get("html_url", "")
            raw_url = html_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            links.append(raw_url)

        page += 1
        time.sleep(3)  # her istek arası 3 saniye bekle

    return links