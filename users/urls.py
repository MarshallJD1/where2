from . import views
from django.urls import path
from .views import register_view, login_view, logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
