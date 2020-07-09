from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

UserModel = get_user_model()


class CreateAuctionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AuctionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'username', 'balance']
        read_only_fields = ['username', 'balance']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['balance']
        extra_kwargs = {'balance': {'write_only': True}}


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
