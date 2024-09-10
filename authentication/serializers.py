from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that email already exists.'
            )
        ]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
