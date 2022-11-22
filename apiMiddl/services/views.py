from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Service
from .serializers import ServiceSerializer
import requests
from django.conf import settings
import json

@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))   
def service_list(request):
    if request.method == 'GET':
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))   
def run(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)        
        url = settings.ML_ROOT_URL+"run/"+request_data['username']+"_"+request_data["model_name"]
        response = requests.post(url, json.dumps(request_data['columns']))
        response_status = status.HTTP_200_OK
        if response.status_code != 200:
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response.text, status=response_status)

@api_view(['POST'])
@permission_classes((AllowAny,))   
def uploadcsv(request):
    if request.method == 'POST':
        file = request.FILES['file']
        url = settings.ML_ROOT_URL+"uploader"
        response = requests.post(url, files={'file': file})
        response_status = status.HTTP_200_OK
        if response.status_code != 200:
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response.text, status=response_status)