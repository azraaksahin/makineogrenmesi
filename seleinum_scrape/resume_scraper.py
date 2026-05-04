from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from filters import extract_real_resume_part


def scrape_resume_text(driver, url):
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    selectors = [
        "div[class*='resumes-sample-content']",
        "div[class*='sample-resume-container']",
        "main"
    ]

    for selector in selectors:
        try:
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )

            text = element.text.strip()
            clean_text = extract_real_resume_part(text)

            if clean_text and len(clean_text) > 100:
                return clean_text

        except:
            continue

    return None