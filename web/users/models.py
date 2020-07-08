from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionUser(AbstractUser):
    balance = models.DecimalField(max_digits=9,
                                  decimal_places=2,
                                  verbose_name='balance',
                                  default=0)
