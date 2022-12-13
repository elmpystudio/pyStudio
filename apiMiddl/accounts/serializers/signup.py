from rest_framework import serializers
from .users import UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

User = get_user_model()

class OutputLoginSerializer(serializers.Serializer):  # noqa: E501 pylint: disable=abstract-method
    result = serializers.BooleanField()
    error = serializers.CharField()

class InputLoginSerializer(serializers.Serializer):  # noqa: E501 pylint: disable=abstract-method
    username = serializers.CharField()
    password = serializers.CharField()

    def get_authenticated_user(self):
        from django.contrib.auth import authenticate
        data = self.validated_data
        u = authenticate(username=data['username'], password=data['password'])
        if u == None:
            u = authenticate(username=data['username'], password=data['password'])

        return u


class InputRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=15,
        min_length=4,
        required=True
    )
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    about = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(**self.cleaned_data)
        return user

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'about': self.validated_data.get('about', ''),
            'avatar': self.validated_data.get('avatar', ''),
            'jhub_token': get_random_string(length=60),
            # 'is_staff': True,
            # 'is_superuser': True
        }

