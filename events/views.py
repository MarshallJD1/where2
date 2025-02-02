import requests
from django.conf import settings
from django.shortcuts import render
from .forms import EventSearchForm
from django.templatetags.static import static

def search_events(request):
    events = []
    error_message = None  
     ## This is the list of events that will be displayed on the page
    if request.method == 'GET':
        form = EventSearchForm(request.GET)
        ## This is the form that will be displayed on the page
        if form.is_valid():
            city = form.cleaned_data['city']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            radius = form.cleaned_data['radius']

            url = "https://app.ticketmaster.com/discovery/v2/events.json"
            ## This is the URL that we will use to fetch the events
            params = { ## These are the parameters that we will pass to the API
                'apikey': settings.TICKETMASTER_API_KEY,  
                'city': city,  
                'radius': radius,
                'unit': 'miles',
                'startDateTime': f"{start_date}T00:00:00Z",
                'endDateTime': f"{end_date}T23:59:59Z",
                'size': 20,  
                'countryCode': 'GB'  # Restricting search to UK
            }

            response = requests.get(url, params=params)

            ## This is the response that we get from the API
            if response.status_code == 200:
                data = response.json()
                if '_embedded' in data and 'events' in data['_embedded']:
                    for event in data['_embedded']['events']:
                        # Try to pick a suitable image from the available ones
                        image_url = None
                        if 'images' in event and event['images']:
                            image_url = get_uniform_image(event['images'])
                        
                        # If no suitable image was found, use the default image
                        if not image_url:
                            image_url = static("images/logo.png")

                        event_info = {
                            'name': event.get('name', 'No Title'),
                            'date': event['dates']['start'].get('localDate', 'Unknown Date'),
                            'venue': event['_embedded']['venues'][0].get('name', 'Unknown Venue') if '_embedded' in event and 'venues' in event['_embedded'] else 'Unknown Venue',
                            'url': event.get('url', '#'),
                            'image': image_url,
                            'description': event.get('description', 'No description available')
                        }
                        events.append(event_info) 
                else: ## If no events are found
                    error_message = "No events found. Try increasing the radius or selecting another city."
            else: ## If there is an error in fetching the events
                error_message = f"Error fetching events. Status code: {response.status_code}"

        else: ## If the form is invalid
            error_message = "Invalid form submission. Please check your inputs."

    else: ## If the request method is not GET
        form = EventSearchForm()

    return render(request, 'events/search_events.html', {'form': form, 'events': events, 'error_message': error_message})



def get_uniform_image(images, desired_width=300, desired_height=200):
    """
    Returns an image URL that is at least as large as the desired dimensions.
    If no image meets the requirement, returns None.
    """
    for img in images: # Iterate over available images
        width = int(img.get('width', 0)) # Get the width of the image
        height = int(img.get('height', 0)) # Get the height of the image
        # Check if the image is big enough
        if width >= desired_width and height >= desired_height: 
            return img.get('url') # Return the URL of the image
    # Fallback: return None if no suitable image is found
    return None