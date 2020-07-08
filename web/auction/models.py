from django.db import models


class Lot(models.Model):
    pet = models.ForeignKey(
        'pets.Pet',
        on_delete = models.CASCADE
    )
    owner = models.ForeignKey(
        'users.AuctionUser',
        on_delete = models.CASCADE
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )


class Bid(models.Model):
    author = models.ForeignKey(
        'users.AuctionUser',
        on_delete = models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )

