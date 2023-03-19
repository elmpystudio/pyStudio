from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     # add custom claims to the token

    #     token['username'] = user.username
    #     token['email'] = user.email

    #     return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     # add custom user data to the response
    #     data['user'] = {
    #         'id': self.user.id,
    #         'name': self.username,
    #         'email': self.user.email
    #     }
    #     return data
    pass