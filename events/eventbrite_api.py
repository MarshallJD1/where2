import requests
import os

EVENTBRITE_API_KEY = os.getenv('EVENTBRITE_API_KEY')

def get_events(location, start_date, end_date):
    """Fetch events from Eventbrite based on location and date range."""
    url = "https://www.eventbriteapi.com/v3/events/search/"
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}"
    }
    params = {
        "location.address": location,
        "location.within": "10km",  # Adjust search radius if needed
        "start_date.range_start": start_date,
        "start_date.range_end": end_date
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # Returns event data
    else:
        return {"error": "Failed to fetch events", "status": response.status_code}