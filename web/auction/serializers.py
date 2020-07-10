from rest_framework import serializers
from .models import Lot, Bid


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ['id', 'pet', 'price', 'owner', 'status']
        read_only_fields = ['owner', 'status']

    def validate_pet(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError('Wrong Pet ID')
        return value


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'lot', 'amount', 'author', 'status']
        read_only_fields = ['author', 'lot', 'status']


class BidStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'status']

    def validate_status(self, value):
        if value != Bid.accepted:
            raise serializers.ValidationError('Incorrect status')
        return value
