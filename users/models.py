from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    user_info = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    language = models.CharField(verbose_name='язык', max_length=128, blank=True)
    user_page_url = models.CharField(verbose_name='url', max_length=128, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

