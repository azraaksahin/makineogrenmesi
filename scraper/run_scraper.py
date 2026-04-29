from google_scraper import scrape_google
from downloader import download_file
from pdf_to_text import pdf_to_text

links = scrape_google()

for link in links:
    raw_link = link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    path = download_file(raw_link)

    if path:
        text = pdf_to_text(path)
        print(text[:200])