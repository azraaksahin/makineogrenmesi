from scraper.github_scraper import scrape_github
from scraper.utils import is_real_cv
from scraper.downloader import download_file
from scraper.pdf_to_text import pdf_to_text
import time

queries = [
    "resume experience education",
    "software engineer resume",
    "data scientist resume",
]

all_links = []
for q in queries:
    print(f"\nAranıyor: {q}")
    links = scrape_github(q, max_results=300)
    all_links.extend(links)
    print(f"Bu sorguda {len(links)} link bulundu")
    time.sleep(10)  # sorgular arası 10 saniye bekle

all_links = list(set(all_links))
print(f"\nToplam benzersiz PDF: {len(all_links)}")

for link in all_links:
    path = download_file(link)
    if path:
        text = pdf_to_text(path)
        if is_real_cv(text):
            print(f" Gerçek CV: {path} | {len(text)} karakter")
        else:
            print(f"Sahte, atlandı: {path}")

print("\nDONE")