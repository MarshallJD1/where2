import requests
from django.conf import settings
from django.shortcuts import render
from .forms import EventSearchForm

def search_events(request):
    events = []
    error_message = None  

    if request.method == 'GET':
        form = EventSearchForm(request.GET)

        if form.is_valid():
            city = form.cleaned_data['city']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            radius = form.cleaned_data['radius']

            url = "https://app.ticketmaster.com/discovery/v2/events.json"

            params = {
                'apikey': settings.TICKETMASTER_API_KEY,  
                'city': city,  # Now searching by city instead of postal code
                'radius': radius,
                'unit': 'miles',
                'startDateTime': f"{start_date}T00:00:00Z",
                'endDateTime': f"{end_date}T23:59:59Z",
                'size': 20,  
                'countryCode': 'GB'  # Restricting search to UK
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
                            'url': event.get('url', '#'),
                            'image': event['images'][0]['url'] if 'images' in event and event['images'] else None,
                            'description': event.get('description', 'No description available')
                        }
                        events.append(event_info)
                else:
                    error_message = "No events found. Try increasing the radius or selecting another city."
            else:
                error_message = f"Error fetching events. Status code: {response.status_code}"

        else:
            error_message = "Invalid form submission. Please check your inputs."

    else:
        form = EventSearchForm()

    return render(request, 'events/search_events.html', {'form': form, 'events': events, 'error_message': error_message})
