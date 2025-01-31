from django.urls import path
from .views import search_events

urlpatterns = [
    path('search/', search_events, name='search_events'),
]