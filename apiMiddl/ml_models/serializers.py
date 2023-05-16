from rest_framework import serializers
from .models import Ml_model

class ml_modelSerializer(serializers.ModelSerializer):
    purchased = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Ml_model
        fields = '__all__'

    def create(self, validated_data):
        user = self.user
        ml_model = Ml_model.objects.create(user=user, **validated_data)
        ml_model.purchased.add(user)
        return ml_model