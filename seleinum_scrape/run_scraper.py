from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from link_scraper import get_all_sample_links, get_links_from_page
from resume_scraper import scrape_resume_text
from filters import is_software_link, is_software_cv
from saver import save_text, save_to_csv


MAX_CV = 40


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.set_page_load_timeout(25)

    return driver


def restart_driver(driver):
    try:
        driver.quit()
    except:
        pass

    time.sleep(2)

    return create_driver()


def main():
    driver = create_driver()

    all_resume_links = set()

    try:
        print("Ana sayfadaki linkler çekiliyor...")
        first_links = get_all_sample_links(driver)

        print(f"Ana sayfadan {len(first_links)} link bulundu.")

        for link in first_links:
            try:
                links = get_links_from_page(driver, link)
                all_resume_links.update(links)
                time.sleep(1)

            except Exception as e:
                print("Kategori linki geçildi:", e)
                continue

        print(f"\nToplam {len(all_resume_links)} CV linki bulundu.")

        software_links = []

        for link in all_resume_links:
            if is_software_link(link):
                software_links.append(link)

        print(f"URL filtresinden geçen yazılım CV sayısı: {len(software_links)}")

        saved_rows = []
        saved_count = 0

        for link in software_links:
            if saved_count >= MAX_CV:
                break

            print(f"\nCV çekiliyor: {link}")

            try:
                text = scrape_resume_text(driver, link)
                time.sleep(2)

                if text and is_software_cv(text):
                    saved_count += 1

                    save_text(text, saved_count)
                    saved_rows.append([saved_count, link, text])

                    print(f"Kaydedildi: resume_{saved_count}.txt")

                else:
                    print("Yazılım CV değil veya metin yetersiz, geçildi.")

            except Exception as e:
                print("Hata oldu, driver yeniden başlatılıyor:", e)
                driver = restart_driver(driver)
                continue

        csv_path = save_to_csv(saved_rows)

        print("\nScraping tamamlandı.")
        print(f"Toplam kaydedilen yazılım CV sayısı: {saved_count}")
        print(f"TXT klasörü: data/selenium_resumes")
        print(f"CSV dosyası: {csv_path}")

    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    main()