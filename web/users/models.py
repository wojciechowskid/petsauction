from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class AuctionUser(AbstractUser):
    balance = models.DecimalField(max_digits=9,
                                  decimal_places=2,
                                  verbose_name='balance',
                                  default=100) # for testing purpose


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
