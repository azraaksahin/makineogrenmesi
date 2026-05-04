from scraper.github_scraper import scrape_github
from scraper.utils import is_real_cv
from scraper.downloader import download_file
from scraper.pdf_to_text import pdf_to_text
import time

queries = [
    '"resume" "education" "experience"',
    '"software engineer" "resume"',
    '"data scientist" "resume"',
    '"curriculum vitae" "university"'
]

all_links = []
good_cvs = []

for q in queries:
    print(f"\nAranıyor: {q}")
    links = scrape_github(q, max_results=200)
    all_links.extend(links)
    print(f"Bu sorguda {len(links)} link bulundu")
    time.sleep(5)

all_links = list(set(all_links))
print(f"\nToplam benzersiz PDF: {len(all_links)}")

for link in all_links:
    path = download_file(link)

    if not path:
        continue

    text = pdf_to_text(path)

    if is_real_cv(text):
        print(f"CV bulundu: {path}")
        good_cvs.append(path)

print("\nSEÇİLEN CV'LER:\n")

for cv in good_cvs[:10]:
    print(cv)

print(f"\nToplam kaliteli CV: {len(good_cvs)}")
print("DONE")