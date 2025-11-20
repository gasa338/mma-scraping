import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from config import BrowserConfig
from scrapers.event_scraper import EventScraper
from utils.helpers import save_to_json, close_popup_ads
from models.data_models import EventData


class FightCenterScraper:
    def __init__(self):
        self.driver = self._setup_driver()
        self.scraper = EventScraper(self.driver)

    def _setup_driver(self):
        """Postavlja Chrome driver sa konfigurisanim opcijama"""
        chrome_options = BrowserConfig.get_chrome_options(headless=True)
        return webdriver.Chrome(options=chrome_options)

    def _setup_filters(self):
        """Postavlja filtere na stranici"""
        wait = WebDriverWait(self.driver, 5)
        form = wait.until(EC.presence_of_element_located((By.ID, 'fightCenterRefine')))

        filter_configs = [
            ('group', 'regional'),
            ('schedule', 'results'),
            ('search_refine_sport', 'mma')
        ]

        for filter_id, filter_value in filter_configs:
            select = Select(self.driver.find_element(By.ID, filter_id))
            select.select_by_value(filter_value)

        time.sleep(5)  # Čekanje učitavanja rezultata

    def _load_more_events(self, max_pages=6):
        """Klikna na 'Load More' dugme za učitavanje dodatnih događaja"""
        for page_num in range(max_pages):
            try:
                close_popup_ads(self.driver)

                load_more_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'loadMoreButton'))
                )

                self._click_load_more(load_more_btn)
                time.sleep(4)
                close_popup_ads(self.driver)

                print(f"Učitana {page_num + 1}. dodatna stranica")

            except TimeoutException:
                print(f"Load More dugme nije pronađeno nakon {page_num + 1}. pokušaja")
                break
            except Exception as e:
                print(f"Greška pri učitavanju {page_num + 1}. stranice: {e}")
                close_popup_ads(self.driver)
                continue

    def _click_load_more(self, button):
        """Pokušava kliknuti na Load More dugme na različite načine"""
        try:
            button.click()
        except ElementClickInterceptedException:
            print("Regularni klik blokiran - koristim JavaScript klik")
            self.driver.execute_script("arguments[0].click();", button)

    def scrape_events(self):
        """Glavna funkcija za skrapovanje svih događaja"""
        try:
            self.driver.get('https://www.tapology.com/fightcenter')

            self._setup_filters()
            self._load_more_events()

            events = self.driver.find_elements(By.CSS_SELECTOR, "[data-controller='bout-toggler']")
            results = self.scraper.process_events(events)

            save_to_json(results)
            return results

        finally:
            self.driver.quit()


if __name__ == "__main__":
    scraper = FightCenterScraper()
    results = scraper.scrape_events()