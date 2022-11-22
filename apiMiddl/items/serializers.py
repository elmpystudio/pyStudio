from rest_framework import serializers
from .models import *
from utils.minio import minio
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json


class VisualAnalyticsCreate(serializers.Serializer):
    dataset = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all(), write_only=True)
    tableau_workbook_id = serializers.CharField(read_only=True)
    name = serializers.CharField(write_only=True)


class CreateDatasetSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=100)
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all())

    def create(self, data):
        user = self.context['request'].user
        d = Dataset.objects.create(**data)
        path = "/tmp/tessest"
        d.download(path)

        profile = generate_science_data_html(path)
        d.set_science_data_html(profile)

        profile = generate_science_data_json(path)
        d.set_science_data_json(profile)
        d.save()
        user.private.add(d.id)
        return d


class DatasetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        exclude = ["id", "file"]
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False}
        }


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    owner = serializers.CurrentUserDefault()

    def create(self, data):
        f = data['file']
        user = self.context['request'].user
        file_object = File.objects.create(filename=f.name, owner=user)
        file_object.save_to_minio("datasets", f, f.size)

        return file_object


class ItemDashboardSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    uuid = serializers.CharField(max_length=100)
    fileName = serializers.CharField(max_length=100)
    format = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=10)
    last_updated = serializers.DateTimeField()
