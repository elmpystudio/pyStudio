from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse, Http404
import random
import string
from datasets.models import Dataset
from ml_models.models import Ml_model
from .serializers import DatasetSerializer, Ml_modelSerializer, DatasetDownloadSerializer
    
class DatasetList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        datasets = Dataset.objects.filter(user_id=request.user.id)
        serializer = DatasetSerializer(datasets, user=request.user, many=True)
        return Response(serializer.data)

class Ml_modelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        ml_models = Ml_model.objects.filter(user_id=request.user.id)
        serializer = Ml_modelSerializer(ml_models, user=request.user, many=True)
        return Response(serializer.data)

class DatasetDownload(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Dataset.objects.filter(pk=pk, purchased__id__exact=self.request.user.id)
            if len(data) > 0:
                return data[0]
            raise Dataset.DoesNotExist
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        file_name = dataset.name + ".csv"
        dataset.download('media/tmp_datasets/' + file_name)
        dataset.file = 'tmp_datasets/' + file_name
        serializer = DatasetDownloadSerializer(dataset)
        return Response(serializer.data)
