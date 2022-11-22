from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from accounts.models import Project, CustomUser
from accounts.serializers.signup import UserSerializer
# from utils.TableauWrapper import TableauWrapper
from .users import UserSerializer

User = get_user_model()

class ProjectUserReadSerializer(serializers.ModelSerializer):
    pass

class ProjectReadSerializer(serializers.ModelSerializer):
    collaborators = UserSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Project
        fields = "__all__"

class ProjectWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        exclude = ["owner", "collaborators", "items"]

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(owner=user, **validated_data)
        project.collaborators.add(user)
        return project
