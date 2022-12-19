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


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)

    except Service.DoesNotExist: 

        return Response({'message': 'The service does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        service.delete()
        return Response({'message': 'Service was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes((AllowAny,))
def run(request):
    request_data = json.loads(request.body)
    url = settings.ML_ROOT_URL + "run/" + request_data['username'] + "_" + request_data["model_name"]
    response = requests.post(url, json.dumps(request_data['columns']))
    return Response(response.text, status=response.status_code)


@api_view(['POST'])
@permission_classes((AllowAny,))
def uploadcsv(request):
    file = request.FILES['file']
    url = settings.ML_ROOT_URL + "uploader"
    response = requests.post(url, files={'file': file})
    return Response(response.text, status=response.status_code)
