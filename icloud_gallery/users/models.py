from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    icloud_password = models.CharField(max_length=128, blank=True, null=True)
