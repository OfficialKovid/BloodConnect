from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_primary = models.CharField(max_length=15)
    phone_secondary = models.CharField(max_length=15, blank=True, null=True)
    blood_type = models.CharField(max_length=5)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
