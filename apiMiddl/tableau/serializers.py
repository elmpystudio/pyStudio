from rest_framework import serializers
from items.models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
# from utils.TableauWrapper import TableauWrapper

class CreateTableauWorkbook(serializers.Serializer):
    name = serializers.CharField()
    dataset = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all())

    def create(self, valid_data):
        print(valid_data)

class TableauWorkbook(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.CharField()

class ListTableauWorkbook(serializers.Serializer):
    result = serializers.BooleanField()
    workbooks = serializers.ListField(
                child = TableauWorkbook()
    )
        
class ListTableauKey(serializers.Serializer):
    key = serializers.CharField(read_only=True)
    ip = serializers.CharField(write_only=True)

