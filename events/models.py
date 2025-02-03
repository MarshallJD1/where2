from django.db import models
from django.contrib.auth.models import User

class SavedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=100)  # Ticketmaster event ID
    name = models.CharField(max_length=255)
    date = models.DateField()  # or DateTimeField if you want time as well
    venue = models.CharField(max_length=255)
    url = models.URLField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.event_id}) - {self.user.username}"
