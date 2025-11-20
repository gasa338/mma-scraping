import json
from datetime import datetime
from pprint import pprint

from selenium.webdriver.remote.webdriver import WebDriver


def save_to_json(data, filename=None):
    """Čuva podatke u JSON fajl"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'fight_events_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Podaci sačuvani u {filename}")


# Ova funkcija ostaje ista kao u tvom originalnom kodu
def close_popup_ads(driver: WebDriver):
    """Zatvara popup reklame ako postoje"""
    # Tvoj postojeći kod za close_popup_ads
    pass