from rest_framework import serializers
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json
from datasets.models import Dataset
from ml_models.models import Ml_model

class DatasetSerializer(serializers.ModelSerializer):
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

class DatasetDownloadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dataset
        fields = [
           'file'
        ]

class Ml_modelSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField('_get_access')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def _get_access(self, ml_model):
        if Ml_model.objects.filter(pk=ml_model.id, purchased__id__exact=self.user.id):
            return True
        return False

    class Meta:
        model = Ml_model
        fields = [
            'id',
            'name',
            'model_name',
            'username',
            'description',
            'version',
            'eval_metrics',
            'columns',
            'access'
        ]

class Ml_modelDownloadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ml_model
        fields = [
           'file'
        ]

class Ml_modelDownloadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ml_model
        fields = [
           'file'
        ]