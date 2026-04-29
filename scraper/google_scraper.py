from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_google():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    query = 'site:github.com "resume" "pdf"'

    driver.get("https://www.google.com")
    time.sleep(5)

    search = driver.find_element(By.NAME, "q")
    search.send_keys(query)
    search.send_keys(Keys.RETURN)

    time.sleep(5)

    links = set()

    for _ in range(5):  # sayfa sayısı
        results = driver.find_elements(By.CSS_SELECTOR, "a")

        for r in results:
            href = r.get_attribute("href")

            if href and "github.com" in href and ".pdf" in href.lower():
                links.add(href)

        try:
            next_btn = driver.find_element(By.ID, "pnnext")
            next_btn.click()
            time.sleep(3)
        except:
            break

    driver.quit()
    return list(links)