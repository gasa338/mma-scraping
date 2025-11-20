from selenium.webdriver.chrome.options import Options


class BrowserConfig:
    """Konfiguracija browser opcija"""
    
    @staticmethod
    def get_chrome_options(headless=False):
        """Vraća konfigurisane Chrome opcije"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        
        return chrome_options