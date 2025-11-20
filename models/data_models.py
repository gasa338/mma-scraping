from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Location:
    """Model podataka za lokaciju"""
    country: Optional[str] = None
    city: Optional[str] = None
    venue: Optional[str] = None


@dataclass
class EventData:
    """Model podataka za celokupan događaj"""
    text: str
    link: str
    time: str
    location: Location
    event: Dict[str, Any]
    
    def to_dict(self):
        """Konvertuje u dictionary za JSON serijalizaciju"""
        return {
            'text': self.text,
            'link': self.link,
            'time': self.time,
            'location': {
                'country': self.location.country,
                'city': self.location.city,
                'venue': self.location.venue
            },
            'event': self.event
        }