from django.db import models
from django.conf import settings


class Lot(models.Model):
    pet = models.ForeignKey(
        'pets.Pet',
        on_delete = models.CASCADE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )
    active = 'AC'
    closed = 'CD'
    statuses = [
        (active, 'Active'),
        (closed, 'Closed'),
    ]
    status = models.CharField(max_length=2, choices=statuses, default=active)


class Bid(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    lot = models.ForeignKey(
        'auction.Lot',
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )

    new = 'NW'
    accepted = 'AC'
    statuses = [
        (new, 'New'),
        (accepted, 'Accepted'),
    ]
    status = models.CharField(max_length=2, choices=statuses, default=new)
