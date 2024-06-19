from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add your custom fields here
    n_id = models.IntegerField(blank=True, null=True)
    company = models.TextField(max_length=500, blank=True)
