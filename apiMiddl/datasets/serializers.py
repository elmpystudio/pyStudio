from rest_framework import serializers
from utils.PandaWrapper import generate_science_data_html, generate_science_data_json
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
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
            'purchased'
        ]

    def create(self, data):
        file = data['file']
        data['user_id'] = self.user.id
        data['filename'] = file.name
        del data['file']
        del data['purchased']
        dataset = Dataset.objects.create(**data)
        dataset.upload(file)
        tmp_path = "/tmp/tessest"
        dataset.download(tmp_path)
        dataset.set_science_data_html(generate_science_data_html(tmp_path))
        dataset.set_science_data_json(generate_science_data_json(tmp_path))
        return dataset
