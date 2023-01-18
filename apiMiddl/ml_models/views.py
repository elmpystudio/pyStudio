from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from django.http import HttpResponse, Http404
import requests
import json
from django.conf import settings
from .models import Ml_model
from .serializers import ml_modelSerializer

class Ml_modelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        ml_models = Ml_model.objects.filter(user_id=request.user.id)
        serializer = ml_modelSerializer(ml_models, user=None, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ml_modelSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Ml_modelsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Ml_model.objects.filter(user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Ml_model.DoesNotExist
        except Ml_model.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     ml_model = self.get_object(pk)
    #     serializer = ml_modelSerializer(ml_model, user=None)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     ml_model = self.get_object(pk)
    #     serializer = ml_modelSerializer(ml_model, data=request.data, user=None)
    #     if (serializer.is_valid()):
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ml_model = self.get_object(pk)
        ml_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def uploadcsv(request):
    file = request.FILES['file']
    url = settings.ML_ROOT_URL + "uploader"
    response = requests.post(url, files={'file': file})
    return Response(response.text, status=response.status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def run(request):
    request_data = json.loads(request.body)
    url = settings.ML_ROOT_URL + "run/" + request_data['username'] + "_" + request_data["model_name"]
    response = requests.post(url, json.dumps(request_data['columns']))
    return Response(response.text, status=response.status_code)
    