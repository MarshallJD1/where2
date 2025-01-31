import requests
from django.conf import settings
from django.shortcuts import render
from .forms import EventSearchForm

def search_events(request):
    events = None
    if request.method == 'GET' and 'location' in request.GET and 'start_date' in request.GET and 'end_date' in request.GET:
        location = request.GET['location']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        # Ticketmaster Discovery API URL
        url = f"https://app.ticketmaster.com/discovery/v2/events.json"
        
        # Parameters for the API request
        params = {
            'apikey': settings.TICKETMASTER_API_KEY,  # API key from Heroku config
            'city': location,
            'startDateTime': start_date + 'T00:00:00Z',  # Use the start date with midnight
            'endDateTime': end_date + 'T23:59:59Z',  # Use the end date with just before midnight
        }

        # Make the request to the Ticketmaster API
        response = requests.get(url, params=params)
        if response.status_code == 200:
            events = response.json()['_embedded']['events']
        else:
            events = []

    form = EventSearchForm()
    return render(request, 'search_events.html', {'form': form, 'events': events})
