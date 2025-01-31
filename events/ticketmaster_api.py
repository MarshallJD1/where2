import requests
import os

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

def get_ticketmaster_events(location, start_date=None, end_date=None):
    """Fetch events from Ticketmaster API."""
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": location,
        "radius": 10,  # Search within 10 miles
        "unit": "miles",
        "size": 20  # Number of results to return
    }

    # Add date filters if provided
    if start_date and end_date:
        params["startDateTime"] = f"{start_date}T00:00:00Z"
        params["endDateTime"] = f"{end_date}T23:59:59Z"

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("_embedded", {}).get("events", [])  # Extract events
    else:
        return {"error": "Failed to fetch events", "status": response.status_code, "details": response.json()}
