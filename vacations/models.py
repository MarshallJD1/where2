from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # or use get_user_model() if needed

class Vacation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

class VacationEvent(models.Model):
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE, related_name='events')
    # Storing minimal event data; adjust as needed:
    event_id = models.CharField(max_length=100)  # You can store the Ticketmaster event id if available
    name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    event_url = models.URLField(max_length=500, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
