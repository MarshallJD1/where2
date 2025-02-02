from django.urls import path
from . import views

app_name = 'vacations'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_vacation, name='create_vacation'),
    path('add-event/', views.add_event_to_vacation, name='add_event_to_vacation'),
]
