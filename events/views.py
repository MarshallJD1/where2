from django.shortcuts import render
from .ticketmaster_api import get_ticketmaster_events

# Create your views here.


def search_events(request):
    """View to search events."""
    location = request.GET.get("location")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    events = get_ticketmaster_events(location, start_date, end_date)

    return render(request, "templates/events/search_events.html", {"events": events})