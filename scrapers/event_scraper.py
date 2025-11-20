from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from scrapers.functions import get_promotions, get_geography_data, get_event_data_requests
from models.data_models import EventData, Location


class EventScraper:
    def __init__(self, driver):
        self.driver = driver
    
    def process_events(self, events):
        """Procesira listu elemenata događaja i vraća podatke"""
        results = []
        
        for element in events:
            event_data = self._process_single_event(element)
            if event_data:
                results.append(event_data)
        
        return results
    
    def _process_single_event(self, element):
        """Procesira jedan događaj i vraća podatke"""
        try:
            promotion_div = element.find_element(By.CLASS_NAME, "promotion")
            geography_div = element.find_element(By.CLASS_NAME, "geography")
            
            location_data = get_geography_data(geography_div)
            if location_data is None:
                return None
            
            promotion_data = get_promotions(promotion_div)
            event_details = get_event_data_requests(promotion_data['link'])
            
            return self._create_event_data(promotion_data, location_data, event_details)
            
        except Exception as e:
            print(f"Greška pri procesiranju događaja: {e}")
            return None
    
    def _create_event_data(self, promotion_data, location_data, event_details):
        """Kreira EventData objekat iz sirovih podataka"""
        location = Location(
            country=location_data.get('country'),
            city=location_data.get('city'),
            venue=location_data.get('venue')
        )
        
        return EventData(
            text=promotion_data['text'],
            link=promotion_data['link'],
            time=promotion_data['time'],
            location=location,
            event=event_details
        ).to_dict()