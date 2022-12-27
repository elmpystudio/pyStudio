from rest_framework import serializers
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json
from datasets.models import Dataset

class MarketplaceSerializer(serializers.ModelSerializer):

    access = serializers.SerializerMethodField('_get_access')


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user



    def _get_access(self, dataset):
        if Dataset.objects.filter(pk=dataset.id, purchased__id__exact=self.user.id):
            return True
        return False

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
            'access'
        ]


class MarketplaceDownloadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dataset
        fields = [
           'file'
        ]