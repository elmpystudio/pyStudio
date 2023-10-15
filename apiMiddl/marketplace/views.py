from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse, Http404
import random
import string
from datasets.models import Dataset
from ml_models.models import Ml_model
from users.models import User
from .serializers import DatasetSerializer, Ml_modelSerializer, DatasetDownloadSerializer, Ml_modelDownloadSerializer
    
class DatasetList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, user=request.user, many=True)
        return Response(serializer.data)

class Ml_modelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        ml_models = Ml_model.objects.all()
        serializer = Ml_modelSerializer(ml_models, user=request.user, many=True)
        return Response(serializer.data)

class DatasetDownload(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            # Owner
            data = Dataset.objects.filter(pk=pk, user=self.request.user)
            if not data:
                # Others
                data = Dataset.objects.filter(pk=pk, purchased__id__exact=self.request.user.id)
            if data:
                return data[0]
            raise Dataset.DoesNotExist
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        file_name = dataset.name + ".csv"
        dataset.download('media/tmp/' + file_name)
        dataset.file = 'tmp/' + file_name
        serializer = DatasetDownloadSerializer(dataset)
        return Response(serializer.data)

class Ml_modelDownload(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, request):
        try:
            # Owner
            data = Ml_model.objects.filter(pk=pk, user=self.request.user)
            if not data:
                # Others
                data = Ml_model.objects.filter(pk=pk, user=self.request.user)
            if data:
                return data[0]
            raise Ml_model.DoesNotExist
        except Ml_model.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ml_model = self.get_object(pk, request)
        file_name = ml_model.name + ".csv"
        ml_model.download('media/tmp/' + file_name)
        ml_model.file = 'tmp/' + file_name
        serializer = Ml_modelDownloadSerializer(ml_model)
        return Response(serializer.data)

class DatasetAdd(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        dataset = Dataset.objects.get(pk=pk, user=request.user)
        askUser = request.data['user_id']

        # Check if user exist
        if User.objects.filter(pk=askUser):
            dataset.purchased.add(askUser)

        return Response({"status": "Success", "message": "user added successfully"}, status=status.HTTP_200_OK)    



class Ml_modelAdd(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        ml_model = Ml_model.objects.get(pk=pk, user=request.user)
        askUser = request.data['user_id']

        # Check if user exist
        if User.objects.filter(pk=askUser):
            ml_model.purchased.add(askUser)

        return Response({"status": "Success", "message": "user added successfully"}, status=status.HTTP_200_OK) 

    

