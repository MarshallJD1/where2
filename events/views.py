import requests
from django.conf import settings
from django.shortcuts import render
from .forms import EventSearchForm

def search_events(request):
    events = []
    
    if request.method == 'GET' and 'location' in request.GET and 'start_date' in request.GET and 'end_date' in request.GET:
        location = request.GET['location']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            'apikey': settings.TICKETMASTER_API_KEY,  
            'city': location,
            'startDateTime': start_date + 'T00:00:00Z',  
            'endDateTime': end_date + 'T23:59:59Z',
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if '_embedded' in data and 'events' in data['_embedded']:
                for event in data['_embedded']['events']:
                    event_info = {
                        'name': event.get('name', 'No Title'),
                        'date': event['dates']['start'].get('localDate', 'Unknown Date'),
                        'venue': event['_embedded']['venues'][0].get('name', 'Unknown Venue') if '_embedded' in event and 'venues' in event['_embedded'] else 'Unknown Venue',
                        'url': event.get('url', '#')
                    }
                    events.append(event_info)

    form = EventSearchForm()
    return render(request, 'events/search_events.html', {'form': form, 'events': events})
