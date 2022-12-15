from rest_framework import serializers
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json
from datasets.models import Dataset

class MarketplaceSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'description',
            'filename',
            'create_at',
            'uuid',
            'file',
            'user',
            'is_public',
            'purchased'
        ]

class MarketplaceDownloadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dataset
        fields = [
           'file'
        ]