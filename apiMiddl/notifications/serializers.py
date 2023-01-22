from rest_framework import serializers
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json
from .models import Notification
from datasets.models import Dataset

class NotificationSerializerGet(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField('_get_from_user')
    to_user = serializers.SerializerMethodField('_get_to_user')
    dataset = serializers.SerializerMethodField('_get_dataset')
    ml_model = serializers.SerializerMethodField('_get_ml_model')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def _get_from_user(self, notification):
        return {
            "id": notification.from_user.id,
            "username": notification.from_user.username,
        }

    def _get_to_user(self, notification):
        return {
            "id": notification.from_user.id,
            "username": notification.from_user.username,
        }

    def _get_dataset(self, notification):
        if notification.dataset:
            return {
                "name": notification.dataset.name,
            }
        return

    def _get_ml_model(self, notification):
        if notification.ml_model:
            return {
                "name": notification.ml_model.name,
            }
        return

    class Meta:
        model = Notification
        fields = [
            'id',
            'message',
            'from_user',
            'to_user',
            'dataset',
            'ml_model'
        ]


class NotificationSerializerPost(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Notification
        fields = '__all__'

    def create(self, data):
        data['from_user'] = self.user
        # GET the user (OWNER) of the dataset | ml_model: (to_user)
        if 'dataset' in data:
            data['to_user'] = data['dataset'].user
        elif 'ml_model' in data:
            data['to_user'] = data['ml_model'].user
        return Notification.objects.create(**data)
