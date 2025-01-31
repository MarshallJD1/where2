from django.shortcuts import render
from .ticketmaster_api import get_ticketmaster_events

# Create your views here.


def search_events(request):
    events = None
    form = EventSearchForm(request.GET)
    
    if form.is_valid():
        # Get user input (location, start date, and end date) from the form
        location = form.cleaned_data['location']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        # Construct the API URL with location, start date, and end date parameters
        api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={settings.TICKETMASTER_API_KEY}&city={location}&startDateTime={start_date}T00:00:00Z&endDateTime={end_date}T23:59:59Z'
        
        # Fetch data from the Ticketmaster API
        response = requests.get(api_url)
        data = response.json()

        # Extract event details (this depends on the API response structure)
        if '_embedded' in data:
            events = data['_embedded']['events']

    # Render the results in a template with the form
    return render(request, 'events/search_events.html', {'form': form, 'events': events})