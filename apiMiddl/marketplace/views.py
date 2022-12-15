from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse, Http404
import random
import string
from datasets.models import Dataset
from .serializers import MarketplaceSerializer, MarketplaceDownloadSerializer
    
class MarketplaceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        datasets = Dataset.objects.filter(user_id=request.user.id)
        serializer = MarketplaceSerializer(datasets, user=None, many=True)
        return Response(serializer.data)

class MarketplaceDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Dataset.objects.filter(user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Dataset.DoesNotExist
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = MarketplaceSerializer(dataset, user=None)
        return Response(serializer.data)

class MarketplaceDownload(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Dataset.objects.filter(pk=pk, is_public=True)
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
        serializer = MarketplaceDownloadSerializer(dataset)
        return Response(serializer.data)


