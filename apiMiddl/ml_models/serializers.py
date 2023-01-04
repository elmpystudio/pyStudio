from rest_framework import serializers
from .models import Ml_model

class ml_modelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Ml_model
        fields = "__all__"

    def create(self, data):
        data['user_id'] = self.user.id
        return Ml_model.objects.create(**data)