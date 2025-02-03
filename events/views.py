import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventSearchForm, SavedEventForm
from django.contrib.auth.decorators import login_required


def get_uniform_image(images):
    """
    Return the URL of an image that meets our criteria.
    In this example, we're looking for an image with a width of at least 640 pixels.
    You can adjust the criteria as needed.
    """
    for image in images:
        # Suppose the Ticketmaster API returns image details as a dict with 'width' and 'url'
        # Adjust the keys depending on the API's response structure.
        width = image.get('width', 0)
        if width >= 640:  # Change this value as per your requirement.
            return image.get('url')
    # If no image meets the criteria, return None.
    return None




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
                'city': city,
                'radius': radius,
                'unit': 'miles',
                'startDateTime': f"{start_date}T00:00:00Z",
                'endDateTime': f"{end_date}T23:59:59Z",
                'size': 20,
                'countryCode': 'GB'
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if '_embedded' in data and 'events' in data['_embedded']:
                    for event in data['_embedded']['events']:
                        # Get a suitable image using our helper function
                        image_url = get_uniform_image(event.get('images', []))
                        if not image_url:
                            # Fallback to a stock image if no appropriate image was found.
                            image_url = static("images/logo.png")

                        event_info = {
                            'id': event.get('id'),
                            'name': event.get('name', 'No Title'),
                            'date': event['dates']['start'].get('localDate', 'Unknown Date'),
                            'venue': (event['_embedded']['venues'][0].get('name', 'Unknown Venue')
                                      if '_embedded' in event and 'venues' in event['_embedded'] else 'Unknown Venue'),
                            'url': event.get('url', '#'),
                            'image': image_url,
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


## 2. Create a view to save events

@login_required
def save_event(request):
    if request.method == "POST":
        form = SavedEventForm(request.POST)
        if form.is_valid():
            saved_event = form.save(commit=False)
            saved_event.user = request.user
            saved_event.save()
            return redirect('dashboard')  
        else:
            # Handle errors or re-render the page with form errors
            return render(request, 'events/save_event.html', {'form': form})
    else:
        # For a GET request, you might want to display a blank form if needed
        form = SavedEventForm()
    return render(request, 'events/save_event.html', {'form': form})


## 3. Create a view to edit events
@login_required
def edit_event(request, event_id):
    # Ensure the event exists and belongs to the current user
    event = get_object_or_404(SavedEvent, id=event_id, user=request.user)
    
    if request.method == "POST":
        form = SavedEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or any page where you list events
    else:
        form = SavedEventForm(instance=event)
        
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


## 4. Create a view to delete events
@login_required
def delete_event(request, event_id):
    # Ensure the event exists and belongs to the current user
    event = get_object_or_404(SavedEvent, id=event_id, user=request.user)
    
    if request.method == "POST":
        event.delete()
        return redirect('dashboard')
        
    return render(request, 'events/delete_event.html', {'event': event})


@login_required
def dashboard(request):
    # Retrieve saved events for the current user, ordered by the creation date (newest first)
    saved_events = SavedEvent.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'events/dashboard.html', {'saved_events': saved_events})