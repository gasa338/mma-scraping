from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from mainAPI import FightCenterScraper


app = FastAPI(title="Fight Events Scraper API")

class ScrapingResponse(BaseModel):
    events: List[Dict[str, Any]]
    total_events: int
    status: str


@app.get("/scrape-events", response_model=ScrapingResponse)
async def scrape_events():
    """API endpoint za skrapovanje fight eventova"""
    try:
        scraper = FightCenterScraper()
        results = scraper.scrape_events()
        
        return ScrapingResponse(
            events=results,
            total_events=len(results),
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška pri skrapovanju: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}