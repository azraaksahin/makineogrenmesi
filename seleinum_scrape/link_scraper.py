from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import time

BASE_URL = "https://www.resume.com"


def safe_get(driver, url, wait_time=3):
    driver.get(url)
    time.sleep(wait_time)


def get_all_sample_links(driver):
    safe_get(driver, f"{BASE_URL}/sample/", 4)

    links = set()
    a_tags = driver.find_elements(By.TAG_NAME, "a")

    for a in a_tags:
        href = a.get_attribute("href")

        if href and "/sample/" in href:
            full_url = urljoin(BASE_URL, href)

            if full_url != f"{BASE_URL}/sample/":
                links.add(full_url)

    return list(links)


def get_links_from_page(driver, url):
    safe_get(driver, url, 3)

    links = set()
    a_tags = driver.find_elements(By.TAG_NAME, "a")

    for a in a_tags:
        href = a.get_attribute("href")

        if href and "/sample/" in href:
            full_url = urljoin(BASE_URL, href)

            parts = full_url.strip("/").split("/")

            if len(parts) >= 5:
                links.add(full_url)

    return links