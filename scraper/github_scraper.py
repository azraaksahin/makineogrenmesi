from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_github(query="resume pdf"):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-data-dir=C:\\temp\\chrome_selenium")
   # options.add_argument("user-data-dir=C:\\Users\\irem\\AppData\\Local\\Google\\Chrome\\User Data")
    #options.add_argument("profile-directory=Default")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://github.com/search?q={query}&type=repositories"
    driver.get(url)

    time.sleep(3)

    links = set()

    for _ in range(5):
        elements = driver.find_elements(By.CSS_SELECTOR, "a")

        for e in elements:
            href = e.get_attribute("href")
            if href and ".pdf" in href.lower():
                links.add(href)

        try:
            driver.find_element(By.CLASS_NAME, "next_page").click()
            time.sleep(3)
        except:
            break

    driver.quit()
    return list(links)