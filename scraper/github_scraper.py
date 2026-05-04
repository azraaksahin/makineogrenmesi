import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_github(query, max_results=200):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + os.getenv("GITHUB_TOKEN")
    }

    links = []
    page = 1

    while len(links) < max_results:
        url = f"https://api.github.com/search/code?q={query}+extension:pdf&per_page=30&page={page}"
        print(f"Sayfa {page} | Toplam: {len(links)}")

        try:
            r = requests.get(url, headers=headers, timeout=30)
        except Exception:
            print("Bağlantı hatası, tekrar deneniyor...")
            time.sleep(10)
            continue

        if r.status_code == 403:
            print("Rate limit, bekleniyor...")
            time.sleep(30)
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

            if "/blob/" not in html_url:
                continue

            raw_url = html_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

            links.append(raw_url)

        page += 1
        time.sleep(2)

    return links