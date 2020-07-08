from django.db import models
from django.conf import settings

"""
Although one can implement separate models for Hedgehogs and Cats and use
abstract base class inheritance or generic foreign key with content types,
the task in question is quite simple and Hedgehogs/Cats have the same fields
and behaviour. That's why using inheritance/generic foreign key is overkill
here.
Taking that into account a simple Pet model implemented which has just
pet_type field pointing to the type of the animal.
"""


class Pet(models.Model):
    hedgehog = 'HG'
    cat = 'CT'
    pet_types = [
        (hedgehog, 'Hedgehog'),
        (cat, 'Cat'),
    ]
    pet_type = models.CharField(max_length=2, choices=pet_types)

    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
