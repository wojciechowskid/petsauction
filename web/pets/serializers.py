from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'pet_type', 'name', 'breed', 'owner']
        read_only_fields = ['owner']
