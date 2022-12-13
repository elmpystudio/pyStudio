from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.http import HttpResponse, Http404
import json
from .models import Dataset, PublicDataset
from .serializers import DatasetSerializer, PublicDatasetSerializer


class DatasetList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        datasets = Dataset.objects.filter(user_id=request.user.id)
        serializer = DatasetSerializer(datasets, user=None, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DatasetSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatasetDetail(APIView):
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
        serializer = DatasetSerializer(dataset, user=None)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DatasetSerializer(dataset, data=request.data, user=None)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dataset = self.get_object(pk)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DatasetSampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Dataset.objects.filter(user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Dataset.DoesNotExist
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dataset = self.get_object(pk)
        sample_path = "/tmp/sample"
        dataset.download(sample_path)
        sample = [open(sample_path, 'r').readline() for x in range(0, 11)]
        return HttpResponse(JSONRenderer().render({"sample": sample}))


class DatasetRaportHtmlView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Dataset.objects.filter(user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Dataset.DoesNotExist
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dataset = self.get_object(pk)
        return HttpResponse(JSONRenderer().render({"raport": dataset.get_science_data_html()}))

class DatasetRaportJsonView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Dataset.objects.filter(user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Dataset.DoesNotExist
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dataset = self.get_object(pk)
        return HttpResponse(JSONRenderer().render({"raport": json.loads(dataset.get_science_data_json())}))


class PublicDatasetList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dataset_ids = []
        for dataset in PublicDataset.objects.all():
            dataset_ids.append(dataset.id)

        datasets = Dataset.objects.filter(pk__in=dataset_ids)
        serializer = DatasetSerializer(datasets, user=None, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PublicDatasetSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
