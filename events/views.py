import requests
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from .forms import EventSearchForm
from vacations.models import Vacation

def get_uniform_image(images, desired_width=300, desired_height=200):
    """
    Returns an image URL that is at least as large as the desired dimensions.
    If no image meets the requirement, returns None (use a fallback in the template).
    """
    for img in images:
        width = int(img.get('width', 0))
        height = int(img.get('height', 0))
        if width >= desired_width and height >= desired_height:
            return img.get('url')
    
    return None  # ✅ Let the template handle the fallback

@login_required
def search_events(request):
    events = []
    error_message = None  
    form = EventSearchForm(request.GET or None)

    # ✅ Fetch user's vacations
    user_vacations = Vacation.objects.filter(user=request.user)

    if form.is_valid():
        city = form.cleaned_data['city']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        radius = form.cleaned_data['radius']

        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            'apikey': settings.TICKETMASTER_API_KEY,
            'city': city,
            'radius': radius,
            'unit': 'miles',
            'startDateTime': f"{start_date}T00:00:00Z",
            'endDateTime': f"{end_date}T23:59:59Z",
            'size': 20,
            'countryCode': 'GB'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an error for HTTP 4XX/5XX
            data = response.json()

            if '_embedded' in data and 'events' in data['_embedded']:
                for event in data['_embedded']['events']:
                    event_info = {
                        'id': event.get('id', ''),
                        'name': event.get('name', 'No Title'),
                        'date': event['dates']['start'].get('localDate', 'Unknown Date'),
                        'venue': event['_embedded']['venues'][0].get('name', 'Unknown Venue') if '_embedded' in event and 'venues' in event['_embedded'] else 'Unknown Venue',
                        'url': event.get('url', '#'),
                        'image': get_uniform_image(event.get("images", [])),  # ✅ Use helper function
                        'description': event.get('description', 'No description available'),
                    }
                    events.append(event_info)
            else:
                error_message = "No events found. Try increasing the radius or selecting another city."

        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching events: {str(e)}"

    return render(request, 'events/search_events.html', {
        'form': form,
        'events': events,
        'error_message': error_message,
        'vacations': user_vacations,  
    })
