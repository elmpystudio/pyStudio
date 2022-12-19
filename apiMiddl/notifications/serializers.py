from rest_framework import serializers
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json
from .models import Notification
from datasets.models import Dataset


class NotificationSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Notification
        fields = '__all__'

    def create(self, data):
        data['from_user'] = self.user

        # GET the user of the dataset | ml_model: (to_user)
        if data['dataset']:
            data['to_user'] = data['dataset'].user

        return Notification.objects.create(**data)
