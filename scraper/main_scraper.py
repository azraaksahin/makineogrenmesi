from scraper.github_scraper import scrape_github
from scraper.utils import filter_pdf_links
from scraper.downloader import download_file
from scraper.pdf_to_text import pdf_to_text

links = scrape_github("resume pdf", max_results=50)
pdfs = filter_pdf_links(links)

for link in pdfs:
    path = download_file(link)
    if path:
        text = pdf_to_text(path)
        print(f"İndirildi: {path} | {len(text)} karakter")

print(f"DONE — {len(pdfs)} PDF indirildi")