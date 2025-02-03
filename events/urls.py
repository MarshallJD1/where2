from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_events, name='search_events'),
    path('save/', views.save_event, name='save_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('dashboard/', views.dashboard, name='dashboard'),
]