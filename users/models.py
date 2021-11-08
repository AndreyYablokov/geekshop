from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    age = models.PositiveIntegerField(default=40)
    activation_key = models.CharField(max_length=128, blank=True)

    def safe_delete(self):
        self.is_active = False
        self.save()

    def is_activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=48)
