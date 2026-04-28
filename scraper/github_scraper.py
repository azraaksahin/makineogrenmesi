# scraper/github_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_github(query="resume pdf"):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://github.com/search?q=" + query + "&type=code")
    time.sleep(3)

    links = set()

    for _ in range(5):
        elements = driver.find_elements(By.CSS_SELECTOR, "a")

        for e in elements:
            href = e.get_attribute("href")
            if href and "github.com" in href:
                links.add(href)

        try:
            driver.find_element(By.CLASS_NAME, "next_page").click()
            time.sleep(3)
        except:
            break

    driver.quit()
    return list(links)