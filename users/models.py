from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserLogin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username