from scraper.github_scraper import scrape_github
from scraper.utils import filter_pdf_links
from scraper.downloader import download_file

links = scrape_github("resume pdf")

pdfs = filter_pdf_links(links)

for link in pdfs:
    download_file(link)

print("DONE")